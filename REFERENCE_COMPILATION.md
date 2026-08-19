# Akamai Functions Reference Publication and Recompilation Contract

This contract serves two purposes:

1. It defines the portable recompilation process used by public clones with
   `scripts/reference_sync.py`.
2. It defines the publication gate for `docs/_compiled/functions-reference.md`,
   regardless of which workflow produced the candidate.

A candidate may be generated directly from exact sources, from locally
maintained summaries, or through any number of compiler, critique, and revision
passes. The generation process does not need to be public. Before publication,
the final candidate must be audited against every active exact source and meet
all grounding, structure, attribution, and coverage requirements below.

## Inputs

- `docs/reference-manifest.json` is the authoritative source inventory.
- Compile only entries whose `active` field is `true`.
- Each entry's `filepath` points to exact upstream Markdown stored beneath
  `docs/_source/`.

When a public agent recompiles the reference, read every active exact source
and do not substitute another documentation tree. Rebuild the complete
reference rather than incrementally patching only the apparently affected
section.

An alternate local workflow may use private summaries or other intermediate
artifacts to produce its candidate. Those intermediates do not replace the
final exact-source audit: every published claim, attribution, and coverage
decision must still be checked against the active exact sources above.

## Grounding rules

- Preserve every unique hard constraint, exact method or command signature,
  required manifest capability, compatibility condition, and working code
  pattern supported by the sources.
- Preserve unique operational facts that affect an agent's ability to use the
  platform: service availability or deployment footprint; account and resource
  ownership, scope, visibility, isolation, and collaboration; authentication
  behavior and session or token lifetimes; application lifecycle; and required
  onboarding, access, or escalation paths.
- Never invent an API, method signature, import, error string, runtime
  consequence, version requirement, or platform limitation.
- Preserve the source's level of obligation. A recommendation, tutorial
  prerequisite, example version, or observed build version must not become a
  platform-wide requirement or `NEVER` prohibition.
- Keep login-session duration, access-token expiration, application lifecycle,
  and other distinct operational concepts separate. Do not transfer a duration
  or rule from one concept to another.
- Distinguish platform restrictions from the prerequisites of a particular
  tutorial or language example.
- When sources conflict, preserve both statements, identify the conflict, and
  prefer a dedicated reference page over a tutorial only when selecting a
  canonical generated example. Do not silently reconcile incompatible claims.
- Eliminate redundant prose, but never remove a unique technical constraint,
  confirmed API entry, or operational fact. Do not silently omit an active
  source because its useful facts do not resemble an API reference.
- Add source attribution at the subsection level. Because the compiled file is
  located in `docs/_compiled/`, every attribution target must use the form
  `../_source/techdocs-akamai-com/<filename>.md` and must resolve from the
  compiled file. Link labels may show the full `docs/_source/...` path. A
  subsection that combines sources must cite every source that materially
  supports it.

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

Place operational facts in a clearly named subsection of API Reference (for
example, `### Platform and Operational Reference`) or Cross-Reference. In
particular, retain FAQ facts about availability, account or application
ownership and visibility, collaboration, and login-session duration when they
are present in the active sources. If a FAQ and a dedicated reference page
describe the same topic differently, report the difference under the conflict
rule above; use the dedicated page for canonical guidance without deleting the
FAQ statement.

The Cross-Reference section must identify which APIs interact, the handler
contexts in which they are documented, and the manifest capabilities required
for their use. Known Failure Patterns must contain only source-supported wrong
and correct patterns; keep the section minimal when the sources do not provide
concrete examples.

Within Cross-Reference, include a `### Source Coverage` table with one row for
every active manifest entry. Each row must link to the exact source and mark it
as either:

- `Included`, with the compiled subsection(s) containing its unique facts; or
- `Excluded`, with a concise source-specific reason showing that it contains
  only navigation, duplicated material, or other non-reference content.

Exclusion is not valid merely because a source is an FAQ, tutorial, overview,
or contains operational rather than API information. The table is an audit of
coverage, not a substitute for incorporating useful facts into the reference.

## Completion checks

After writing, critiquing, and revising the final candidate, run:

```bash
python3 scripts/reference_sync.py finalize
python3 scripts/reference_sync.py verify
python3 -m unittest tests.test_reference_sync -v
```

Run `finalize` only once all compilation and critique passes are complete. It
validates the publication structure and records hashes for the active source
set, this contract, and the compiled reference. The metadata is a freshness
record, not a declaration of which compiler, model, prompt, or number of passes
produced the artifact.

`verify` is offline and must pass before the compiled reference is published
or considered current. It detects later changes to the exact sources, this
contract, or the finalized artifact; it cannot by itself prove that every
prose claim is semantically correct, which is why the exact-source audit is a
required compilation step.

Before running `finalize`, also confirm that:

- every active manifest source has exactly one Source Coverage row;
- every `Included` row points to at least one substantive compiled subsection;
- every attribution and Source Coverage link resolves relative to
  `docs/_compiled/functions-reference.md`; and
- recommendations and tutorial prerequisites have not been promoted to hard
  requirements or prohibitions.
