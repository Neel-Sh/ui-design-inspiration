# Updating the collection

Keep the skill focused on decisions supported by the collection. New references should add a useful pattern or refine an existing one, rather than accumulating generic design advice.

## Add a reference

1. Put incoming material in the ignored `inbox/` folder. Inspect it before copying it into the public skill. Remove account details, private messages, secrets, personal file paths, and other content not intended for publication. Retain visible creator credits.
2. Record a canonical source URL and the original creator when known. Do not equate a curator with a creator. Do not represent an unknown license as permission for production reuse.
3. For an image, use a descriptive filename under `ui-design-inspiration/references/images/`. Remove EXIF, XMP/text, and capture-time chunks from the public PNG while preserving the pixels and color profile. Keep private originals outside the tracked skill.
4. Add an S ID to `references/source-index.md`, including what is visible, what is useful to borrow, and what needs adaptation. Open the image to verify the analysis. Add its ID, relative path, dimensions, SHA-256, review status, and source information to `references/source-manifest.json`.
5. For a link, add the canonical HTTPS URL to `references/links.txt` and an L entry to `references/motion-and-links.md`. Remove sharing parameters. Record what you actually inspected and any limitations. Do not infer motion from a still.
6. Update the routing table, design directions, counts, and third-party notices when the collection changes. Keep the entrypoint concise. New preferences should not silently override a project's explicit requirements.

Run the checks and rebuild the archive:

```sh
python3 scripts/skill.py check
python3 -m unittest discover -s tests -v
python3 scripts/skill.py package
```

The manifest's SHA-256 is the hash of the sanitized, bundled file. For example, use `shasum -a 256 path/to/image.png` on macOS. Every image must appear in the manifest and source index. Unknown source URLs should be JSON `null`, with an honest `source_status`.

## Refresh local installations

```sh
python3 scripts/skill.py install --target both --replace
```

The installer keeps previous copies under each tool's `skill-backups/` directory and reports their paths. Inspect those copies before manually removing them. Re-upload the generated ZIP separately for Claude chat/Cowork.

## Before a public push

- Inspect the staged file list and diff. Use deliberate paths when staging; the ignored inbox is not a publication source.
- Keep local notes, environment files, credentials, ZIPs, caches, and unsanitized originals out of Git history.
- Verify source/rights notes and screenshot content as well as automated checks. Do not claim the artwork as your own.
- Use a public-safe Git author email. Avoid private addresses in issues and release notes.
- Run the checks once more after changes. Publish a versioned release only from the tested commit and attach the generated archive plus its checksum.

Generated ZIPs belong in release assets, not commits. The package has a fixed internal timestamp and stable file ordering, so builds from the same files with the same Python/zlib toolchain are reproducible.
