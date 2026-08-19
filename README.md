# Akamai Functions Generator

An AI-assisted workspace for generating [Akamai Functions](https://techdocs.akamai.com/akamai-functions/docs/quickstart) (Spin-based WebAssembly edge functions) from natural language descriptions.

Works out of the box with **Claude Code**, **GitHub Copilot**, **Codex**, and
**Google Antigravity IDE**. All four agents receive the same project rules from
`AGENTS.md` and are instructed to read the compiled Akamai Functions API
reference before writing code.

---

## How it works

1. **A curated Akamai Functions API reference** is included at `docs/_compiled/functions-reference.md`.
2. **The AI agent reads that reference** before writing any code, using the
   shared instructions in `AGENTS.md` and small agent-specific adapters.
3. **You describe what you want** and the agent generates a complete, deployable Akamai Function under `functions/<function-name>/`.

---

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| AI coding agent | latest | Claude Code, GitHub Copilot, Codex, or Google Antigravity IDE |
| Spin CLI + Akamai plugin | latest | Follow the [Akamai Functions quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart) |
| [Node.js](https://nodejs.org/) | ≥ 18 | Required by the Spin JS toolchain |
| Python | ≥ 3.10 | Required by the reference maintenance and instruction-sync scripts |

> The Spin JS toolchain (`j2w`, `@spinframework/build-tools`) is installed per-function via `npm install`.

---

## Generating a function

**With GitHub Copilot:** open this workspace in VS Code and use Agent mode (`Ctrl+Shift+I` / `Cmd+Shift+I`).

**With Claude Code:** run `claude` in the project root.

**With Codex:** open this repository in Codex or run `codex` in the project
root.

**With Google Antigravity IDE:** open this workspace and use the Agent panel.

Then describe what you want:

```
Create an Akamai Function that redirects users to country-specific subdomains based on their GeoIP location.
```

The agent will scaffold a complete function under `functions/<name>/`
including:

- `src/index.js` — the function source
- `spin.toml` — Spin component manifest
- `package.json` + `build.mjs` — build tooling
- `README.md` — usage instructions

After generating the function, the agent will also:

1. Run `spin build` and resolve any build failures.
2. Start the local HTTP server with `spin up`.
3. Send `curl -i http://localhost:3000/` as a baseline smoke test and exercise
   any additional routes, methods, request bodies, headers, and expected
   failure cases relevant to the function.
4. Verify the returned HTTP status, headers, and body, then stop the local
   server.

The agent will **not** run `spin aka deploy` unless you explicitly ask it to
deploy. You can always perform deployment manually instead.

## Build and run

When the agent hands off a generated function, it has already run `spin build`,
started it with `spin up`, and tested its HTTP behavior. If you are satisfied
with those results, you can deploy it immediately:

```bash
cd functions/<function-name>
spin aka deploy
```

Deployment is always a separate, explicit step. The agent runs
`spin aka deploy` only when you explicitly prompt it to do so; otherwise, you
run the command manually as shown above.

Optionally, you can repeat the local test yourself before deploying. From the
generated function directory, start the already-built application:

```bash
spin up
```

`spin up` listens on port `3000` by default and remains in the foreground.
Keep that terminal open and, from another terminal, test the root endpoint:

```bash
curl -i http://localhost:3000/
```

Exercise any other routes supported by the function, then stop `spin up` with
`Ctrl+C`.

If you modify the generated source or configuration after the agent's handoff,
rebuild before testing or deploying:

```bash
spin build
```

---

## Maintaining AI-agent instructions

`AGENTS.md` is the only instruction file that should be edited by hand. Claude
Code and Antigravity import it through small native adapters. The Copilot
compatibility file is generated so GitHub interfaces that do not load
`AGENTS.md` directly still receive the same instructions.

After editing `AGENTS.md`, regenerate the Copilot file:

```bash
python scripts/sync_agent_instructions.py
```

To check for drift without changing files:

```bash
python scripts/sync_agent_instructions.py --check
```

The unit tests and `.github/workflows/agent-instructions.yml` enforce this in
pull requests.

---

## Keeping the reference up to date

`scripts/reference_sync.py` discovers pages from Akamai's `llms.txt`, downloads
the exact upstream Markdown, and stores a deterministic manifest. It uses only
Python's standard library and does not require model downloads, browser
automation, or API credentials.

The authoritative inputs are the active exact sources in
`docs/reference-manifest.json` and the compilation contract in
`REFERENCE_COMPILATION.md`. `docs/_compiled/functions-reference.md` is a
generated artifact that is rebuilt whenever either input changes.

Ask your coding agent:

```text
Check the Akamai Functions documentation for updates and regenerate the reference if needed.
```

The shared instructions in `AGENTS.md` tell supported agents to perform this
workflow:

```bash
# Network read only; does not modify the working tree.
python3 scripts/reference_sync.py check

# Store exact changed sources under docs/_source/ and update the manifest.
python3 scripts/reference_sync.py sync

# Always check local freshness, even when the upstream check found no changes.
python3 scripts/reference_sync.py verify

# If verification reports missing/stale metadata, recompile according to
# REFERENCE_COMPILATION.md, then record and verify the result:
python3 scripts/reference_sync.py finalize
python3 scripts/reference_sync.py verify
```

The first synchronization creates `docs/reference-manifest.json` and treats all
currently published pages as additions. Later runs report additions, content
changes, reactivations, and pages removed from `llms.txt`. Removed source
snapshots are retained and marked inactive rather than deleted.

`verify` is entirely offline. It checks exact-source hashes, required section
order, source coverage, local attribution links, and confirms that the active
source set, compilation contract, and compiled reference match the hashes
recorded by `finalize`. Agents run it after every upstream check, so a manual
synchronization, changed compilation contract, or edited compiled reference
cannot be mistaken for a current reference.

For CI-style detection, `check --fail-on-changes` exits with status `3` when a
sync would change the repository. Ordinary `check` always reports changes
without treating them as an execution failure.

The public repository boundary is checked with:

```bash
python3 scripts/check_public_boundary.py
```

This command and its always-running pull-request workflow prevent private local
maintenance files from being accidentally committed.

---

## Project structure

```
.
├── .agents/
│   └── rules/project.md            # Antigravity imports AGENTS.md
├── .github/
│   ├── copilot-instructions.md     # Generated Copilot compatibility copy
│   └── workflows/
│       ├── agent-instructions.yml  # Prevents instruction drift
│       ├── public-boundary.yml     # Rejects private local files
│       └── reference-sync.yml      # Verifies generated reference freshness
├── AGENTS.md                       # Canonical instructions for every agent
├── CLAUDE.md                       # Claude Code imports AGENTS.md
├── REFERENCE_COMPILATION.md        # Exact-source compilation contract
├── docs/
│   ├── _source/                    # Exact upstream Markdown
│   ├── _compiled/
│   │   ├── functions-reference.md  # ← Every agent reads this reference
│   │   └── functions-reference.meta.json # Freshness hashes
│   └── reference-manifest.json     # Exact-source inventory and hashes
├── scripts/
│   ├── check_public_boundary.py    # Prevents private-file publication
│   ├── reference_sync.py           # Dependency-free exact-source workflow
│   └── sync_agent_instructions.py  # Regenerates Copilot instructions
├── tests/                           # Public workflow and instruction tests
└── functions/                      # Generated functions go here
    └── <function-name>/
        ├── src/index.js
        ├── spin.toml
        └── package.json
```

---
