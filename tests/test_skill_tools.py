"""Check data integrity, archive boundaries, and non-destructive installation."""

import importlib.util
import json
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import zlib


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("skill_tools", ROOT / "scripts" / "skill.py")
tools = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tools)


class SkillToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def bundle_copy(self):
        source = self.base / "source"
        shutil.copytree(ROOT / tools.NAME, source)
        return source

    def test_packages_are_reproducible_and_self_contained(self):
        source = ROOT / tools.NAME
        first, checksum = tools.package(source, self.base / "first.zip")
        second, _ = tools.package(source, self.base / "second.zip")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertTrue(checksum.read_text().startswith(tools.sha256(first)))
        with zipfile.ZipFile(first) as archive:
            self.assertIn(f"{tools.NAME}/LICENSE", archive.namelist())
            self.assertIn(f"{tools.NAME}/THIRD_PARTY_NOTICES.md", archive.namelist())
            self.assertTrue(all(n.startswith(tools.NAME + "/") for n in archive.namelist()))
            archive.extractall(self.base / "extracted")
        tools.check_bundle(self.base / "extracted" / tools.NAME)

    def test_changed_image_is_rejected(self):
        source = self.bundle_copy()
        image = next((source / "references" / "images").glob("*.png"))
        image.write_bytes(image.read_bytes() + b"unreviewed data")
        with self.assertRaisesRegex(ValueError, "manifest hash"):
            tools.check_bundle(source)

    def test_broken_reference_is_rejected(self):
        source = self.bundle_copy()
        with (source / "SKILL.md").open("a") as entry:
            entry.write("\n[Missing](references/missing.md)\n")
        with self.assertRaisesRegex(ValueError, "Broken link"):
            tools.check_bundle(source)

    def test_capture_metadata_is_rejected_even_with_updated_hash(self):
        source = self.bundle_copy()
        manifest_path = source / "references" / "source-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        item = manifest["images"][0]
        image = source / item["path"]
        payload = b"Comment\0capture metadata"
        chunk = struct.pack(">I", len(payload)) + b"tEXt" + payload
        chunk += struct.pack(">I", zlib.crc32(b"tEXt" + payload) & 0xffffffff)
        data = image.read_bytes()
        image.write_bytes(data[:33] + chunk + data[33:])
        item["sha256"] = tools.sha256(image)
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "capture metadata"):
            tools.check_bundle(source)

    def test_sharing_parameters_are_rejected(self):
        source = self.bundle_copy()
        links = source / "references" / "links.txt"
        lines = links.read_text().splitlines()
        lines[0] += "?share=tracking"
        links.write_text("\n".join(lines) + "\n")
        with self.assertRaisesRegex(ValueError, "canonical HTTPS"):
            tools.check_bundle(source)

    def test_unexpected_private_file_is_not_packaged(self):
        source = self.bundle_copy()
        (source / ".env").write_text("private configuration\n")
        with self.assertRaises(ValueError):
            tools.package(source, self.base / "unsafe.zip")
        self.assertFalse((self.base / "unsafe.zip").exists())

    def test_install_requires_explicit_replacement_and_preserves_backup(self):
        source = self.base / "source"
        source.mkdir()
        (source / "SKILL.md").write_text("new\n")
        target = self.base / "tool" / "skills" / tools.NAME
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("previous local customization\n")
        with self.assertRaisesRegex(ValueError, "Already installed"):
            tools.install_copy(source, target)
        self.assertEqual((target / "SKILL.md").read_text(), "previous local customization\n")
        backup = tools.install_copy(source, target, replace=True)
        self.assertEqual((target / "SKILL.md").read_text(), "new\n")
        self.assertEqual((backup / "SKILL.md").read_text(), "previous local customization\n")
        self.assertFalse(backup.is_relative_to(target.parent))

    def test_failed_install_restores_existing_copy(self):
        source = self.base / "source"
        source.mkdir()
        (source / "SKILL.md").write_text("new\n")
        target = self.base / "tool" / "skills" / tools.NAME
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("old\n")
        original_rename = Path.rename

        def fail_stage(path, destination):
            if path.name.startswith(f".{tools.NAME}-stage-"):
                raise OSError("simulated installation failure")
            return original_rename(path, destination)

        with patch.object(Path, "rename", fail_stage):
            with self.assertRaises(OSError):
                tools.install_copy(source, target, replace=True)
        self.assertEqual((target / "SKILL.md").read_text(), "old\n")
        self.assertEqual(list(target.parent.glob(".*-stage-*")), [])

    def test_symlink_installation_is_not_followed(self):
        source = self.base / "source"
        source.mkdir()
        actual = self.base / "actual"
        actual.mkdir()
        target = self.base / "linked"
        target.symlink_to(actual, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            tools.install_copy(source, target, replace=True)
        self.assertTrue(target.is_symlink())


if __name__ == "__main__":
    unittest.main()
