#!/usr/bin/env python3
"""Validate, package, and install the skill using Python's standard library."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit
import uuid
import zipfile
import zlib


ROOT = Path(__file__).resolve().parents[1]
NAME = "ui-design-inspiration"
CAPTURE_CHUNKS = {b"eXIf", b"iTXt", b"tEXt", b"zTXt", b"tIME"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".py"}
SENSITIVE_PATTERNS = {
    "personal absolute path": r"/(?:Users|home)/[A-Za-z0-9_.-]+",
    "Windows user path": r"[A-Za-z]:\\Users\\[A-Za-z0-9_.-]+",
    "GitHub token": r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})",
    "API secret": r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}",
    "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_info(path):
    """Check the PNG container and return its dimensions and chunk types."""
    data = path.read_bytes()
    require(data[:8] == b"\x89PNG\r\n\x1a\n", f"Invalid PNG: {path.name}")
    pos, chunks, dimensions = 8, [], None
    while pos < len(data):
        require(pos + 12 <= len(data), f"Truncated PNG: {path.name}")
        size = struct.unpack(">I", data[pos:pos + 4])[0]
        end = pos + size + 12
        require(end <= len(data), f"Truncated PNG chunk: {path.name}")
        kind = data[pos + 4:pos + 8]
        payload = data[pos + 8:end - 4]
        crc = struct.unpack(">I", data[end - 4:end])[0]
        require(zlib.crc32(kind + payload) & 0xffffffff == crc,
                f"PNG checksum mismatch: {path.name}")
        if not chunks:
            require(kind == b"IHDR" and size == 13, f"Missing PNG header: {path.name}")
            dimensions = struct.unpack(">II", payload[:8])
        chunks.append(kind)
        pos = end
        if kind == b"IEND":
            require(size == 0 and pos == len(data), f"Trailing PNG data: {path.name}")
            break
    require(chunks and chunks[-1] == b"IEND" and b"IDAT" in chunks,
            f"Incomplete PNG: {path.name}")
    return dimensions, set(chunks)


def skill_files(source):
    files = []
    for path in sorted(source.rglob("*")):
        require(not path.is_symlink(), f"Symlinks are not portable: {path}")
        if path.is_file():
            require(path.name == "LICENSE" or path.suffix in
                    {".md", ".txt", ".json", ".yaml", ".png"},
                    f"Unexpected skill file: {path.relative_to(source)}")
            require(not any(part.startswith(".") for part in path.relative_to(source).parts),
                    f"Hidden file in skill: {path.relative_to(source)}")
            files.append(path)
    return files


def check_text(path):
    text = path.read_text(encoding="utf-8")
    for label, pattern in SENSITIVE_PATTERNS.items():
        require(not re.search(pattern, text), f"Possible {label} in {path.name}")


def check_links(path, boundary):
    text = path.read_text(encoding="utf-8")
    links = re.findall(r"\]\(([^)]+)\)", text)
    links += re.findall(r'(?:src|href)="([^"]+)"', text)
    for target in links:
        parsed = urlsplit(target)
        if parsed.scheme or not parsed.path:
            continue
        resolved = (path.parent / unquote(parsed.path)).resolve()
        require(resolved.is_relative_to(boundary.resolve()), f"Nonportable link in {path.name}")
        require(resolved.exists(), f"Broken link in {path.name}: {target}")


def check_bundle(source):
    files = skill_files(source)
    for required in ("SKILL.md", "LICENSE", "THIRD_PARTY_NOTICES.md", "agents/openai.yaml"):
        require((source / required).is_file(), f"Missing {required}")
    entry = (source / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", entry, re.S)
    require(match is not None, "SKILL.md needs YAML frontmatter")
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(": ")
        require(sep and key not in fields, "Use unique, single-line frontmatter fields")
        fields[key] = value
    require(set(fields) == {"name", "description"}, "Expected name and description frontmatter")
    require(fields["name"] == NAME, "Skill name differs from the package name")
    require(0 < len(fields["description"]) <= 200, "Keep description within 200 characters")
    require(": " not in fields["description"], "Plain YAML description cannot contain ': '")

    refs = source / "references"
    manifest = json.loads((refs / "source-manifest.json").read_text())
    entries = manifest["images"]
    require(entries, "Reference manifest is empty")
    ids, paths = set(), set()
    index = (refs / "source-index.md").read_text()
    for item in entries:
        identity, relative = item["id"], item["path"]
        require(re.fullmatch(r"S[0-9]{2,}", identity), "Invalid source ID")
        require(identity not in ids and relative not in paths, "Duplicate image ID or path")
        ids.add(identity)
        paths.add(relative)
        path = (source / relative).resolve()
        require(path.is_relative_to((refs / "images").resolve()), "Image path escapes references/images")
        require(path.is_file() and path.suffix == ".png", f"Missing image: {relative}")
        require(sha256(path) == item["sha256"], f"Update manifest hash for {identity}")
        dimensions, chunks = png_info(path)
        require(dimensions == (item["width"], item["height"]), f"Incorrect dimensions for {identity}")
        require(not chunks.intersection(CAPTURE_CHUNKS), f"Remove capture metadata from {identity}")
        require(identity in index and path.name in index, f"Missing source index entry for {identity}")
        require(item.get("source_status"), f"Record source provenance for {identity}")
        require(item.get("source_url") is None or urlsplit(item["source_url"]).scheme == "https",
                f"Use an HTTPS source URL for {identity}")
    actual = {p.relative_to(source).as_posix() for p in (refs / "images").glob("*.png")}
    require(paths == actual, "Manifest must include every reference image")

    urls = (refs / "links.txt").read_text().splitlines()
    require(urls and len(urls) == len(set(urls)), "Links must be nonempty and unique")
    notes = (refs / "motion-and-links.md").read_text()
    for url in urls:
        parts = urlsplit(url)
        require(parts.scheme == "https" and parts.netloc and not parts.query and not parts.fragment,
                "Use canonical HTTPS links without sharing parameters")
        require(url in notes, f"Missing link notes for {parts.netloc}{parts.path}")
    for path in files:
        if path.suffix in TEXT_SUFFIXES:
            check_text(path)
        if path.suffix == ".md":
            check_links(path, source)
    return files, len(entries), len(urls)


def check_repository(root):
    files, images, links = check_bundle(root / NAME)
    require((root / "LICENSE").read_bytes() == (root / NAME / "LICENSE").read_bytes(),
            "Keep repository and packaged licenses identical")
    result = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True)
    tracked = [root / p for p in result.stdout.decode().split("\0") if p] if result.returncode == 0 else []
    public = tracked or files + list(root.glob("*.md")) + list((root / "scripts").glob("*.py"))
    for path in public:
        relative = path.relative_to(root)
        require(not path.is_symlink(), f"Unexpected tracked symlink: {relative}")
        require(path.name != ".DS_Store" and not path.name.startswith(".env") and
                path.suffix not in {".zip", ".pem", ".key", ".p12", ".pfx"} and
                "inbox" not in relative.parts and "dist" not in relative.parts and
                "__pycache__" not in relative.parts and
                not path.name.startswith("Screenshot") and
                str(relative) not in {"links.txt", "USING-UI-DESIGN-SKILL.md"},
                f"Private/generated file in public inventory: {relative}")
        if path.suffix in TEXT_SUFFIXES:
            check_text(path)
        if path.suffix == ".md":
            check_links(path, root)
    print(f"Valid: {images} images, {links} links, {len(files)} portable skill files")
    return files


def package(source, destination):
    files, _, _ = check_bundle(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            info = zipfile.ZipInfo((Path(NAME) / path.relative_to(source)).as_posix(), (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(destination) as archive:
        require(archive.testzip() is None, "Archive integrity check failed")
    checksum = destination.with_suffix(destination.suffix + ".sha256")
    checksum.write_text(f"{sha256(destination)}  {destination.name}\n")
    return destination, checksum


def check_installation(source, destination, replace=False):
    require(not destination.is_symlink(), "Refusing to replace a symlink; review the installation manually")
    require(not source.resolve().is_relative_to(destination.resolve()) and
            not destination.resolve().is_relative_to(source.resolve()),
            "Source and installation must not overlap")
    require(not destination.exists() or replace, f"Already installed: {destination}; use --replace to back it up")
    require(not destination.exists() or destination.is_dir(), "Installation path is not a directory")


def install_copy(source, destination, replace=False):
    check_installation(source, destination, replace)
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{NAME}-stage-", dir=destination.parent))
    backup = None
    try:
        shutil.copytree(source, staging, dirs_exist_ok=True)
        if destination.exists():
            backups = destination.parent.parent / "skill-backups"
            backups.mkdir(parents=True, exist_ok=True)
            backup = backups / f"{NAME}-{uuid.uuid4().hex}"
            destination.rename(backup)
        try:
            staging.rename(destination)
        except OSError:
            if backup is not None:
                backup.rename(destination)
            raise
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Check the skill and public file inventory")
    commands.add_parser("package", help="Build the portable ZIP and checksum under dist/")
    install = commands.add_parser("install", help="Install a checked copy into personal skill directories")
    install.add_argument("--target", choices=["codex", "claude", "both"], required=True)
    install.add_argument("--replace", action="store_true", help="Back up and replace existing copies")
    args = parser.parse_args()
    check_repository(ROOT)
    if args.command == "package":
        for path in package(ROOT / NAME, ROOT / "dist" / f"{NAME}.zip"):
            print(path)
    elif args.command == "install":
        homes = []
        if args.target in {"codex", "both"}:
            homes.append(Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser())
        if args.target in {"claude", "both"}:
            homes.append(Path.home() / ".claude")
        destinations = [home / "skills" / NAME for home in homes]
        # Preflight both installations before changing either one.
        for destination in destinations:
            check_installation(ROOT / NAME, destination, args.replace)
        for destination in destinations:
            backup = install_copy(ROOT / NAME, destination, args.replace)
            print(f"Installed: {destination}")
            if backup is not None:
                print(f"Previous copy preserved: {backup}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit(f"Error: {error}")
