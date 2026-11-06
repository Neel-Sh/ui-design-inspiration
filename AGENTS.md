# Repository guidance

- `ui-design-inspiration/` is the portable skill source. Repository documentation and tooling stay outside that folder, except the license and third-party notices required in distributed packages.
- Preserve the collection's source IDs and provenance. New visual claims require inspecting the relevant image or demo. Do not claim exhaustive video review or exact measurements without evidence.
- Keep screenshots as references. Do not relicense third-party artwork or invent creator attribution. Update `ui-design-inspiration/THIRD_PARTY_NOTICES.md` as needed.
- Never commit the ignored source inbox, personal usage notes, environment files, or generated ZIPs. Preserve the user's original files outside the packaged skill.
- After editing: run `python3 scripts/skill.py check`, `python3 -m unittest discover -s tests -v`, and `python3 scripts/skill.py package`.
- Keep tooling dependency-free and archive paths relative. Installations must not silently overwrite existing copies; preserve backups outside discovered skill directories.
- An update request does not authorize a public push or release unless the user asks for publication. Do not modify global tool settings or unrelated skills.
