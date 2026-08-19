# Akamai Functions Reference Compilation Contract

Use this contract only with the dependency-free source workflow in
`scripts/reference_sync.py`. The legacy `ingest_v2.py` and its summarized
documents remain a separate supported workflow during the migration period.

## Inputs

- `docs/reference-manifest.json` is the authoritative source inventory.
- Compile only entries whose `active` field is `true`.
- Each entry's `filepath` points to exact upstream Markdown stored beneath
  `docs/_source/`.
- Do not use `docs/techdocs-akamai-com/` as an input to this workflow; those
  files are outputs of the legacy LLM summarizer.

Read every active source before compiling. Rebuild the complete reference
rather than incrementally patching only the apparently affected section.

## Grounding rules

- Preserve every unique hard constraint, exact method or command signature,
  required manifest capability, compatibility condition, and working code
  pattern supported by the sources.
- Never invent an API, method signature, import, error string, runtime
  consequence, version requirement, or platform limitation.
- Preserve the source's level of obligation. A recommendation, tutorial
  prerequisite, example version, or observed build version must not become a
  platform-wide requirement or `NEVER` prohibition.
- Distinguish platform restrictions from the prerequisites of a particular
  tutorial or language example.
- When sources conflict, preserve both statements, identify the conflict, and
  prefer a dedicated reference page over a tutorial only when selecting a
  canonical generated example. Do not silently reconcile incompatible claims.
- Eliminate redundant prose, but never remove a unique technical constraint or
  confirmed API entry.
- Add source attribution at the subsection level using repository-relative
  links to the exact files under `docs/_source/`. A subsection that combines
  sources must cite every source that materially supports it.

## Required output

Write the unified reference to `docs/_compiled/functions-reference.md` with
these top-level sections in this exact order:

1. `## 1. Runtime Prohibitions`
2. `## 2. Import Rules`
3. `## 3. Event Handler Reference`
4. `## 4. API Reference`
5. `## 5. Cross-Reference`
6. `## 6. Known Failure Patterns`

Runtime prohibitions must state the documented consequence when a source gives
one. When the consequence is not documented, say that explicitly rather than
inventing an error or symptom.

The Cross-Reference section must identify which APIs interact, the handler
contexts in which they are documented, and the manifest capabilities required
for their use. Known Failure Patterns must contain only source-supported wrong
and correct patterns; keep the section minimal when the sources do not provide
concrete examples.

## Completion checks

After writing the reference, run:

```bash
python3 scripts/reference_sync.py finalize
python3 scripts/reference_sync.py verify
python3 -m unittest tests.test_reference_sync -v
```

`finalize` records hashes for the active source set, this compilation contract,
and the compiled reference. `verify` is offline and must pass before the new
workflow is considered current.
