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

To build and test a generated function manually, change to its directory,
build it, and start the local server:

```bash
cd functions/<function-name>
spin build
spin up
```

`spin up` listens on port `3000` by default and remains running in the
foreground. Keep that terminal open and, from another terminal, test the root
endpoint:

```bash
curl -i http://localhost:3000/
```

Exercise any other routes supported by the function, then stop `spin up` with
`Ctrl+C`.

Deployment is a separate, explicit step. When you are ready to deploy, run it
manually:

```bash
spin aka deploy
```

An AI agent will run this deployment command only when you explicitly prompt
it to do so.

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

The compiled reference at `docs/_compiled/functions-reference.md` is built from individual articles scraped from Akamai techdocs. `ingest_v2.py` manages fetching, change detection, LLM summarization, and recompilation.

### Setup

```bash
pip install crawl4ai trafilatura requests ollama
```

Requires access to an [Ollama](https://ollama.com/) instance. Configure its
host, model, and generation ceiling in `config.py`, or override them with the
`OLLAMA_HOST`, `OLLAMA_MODEL`, and `OLLAMA_MAX_TOKENS` environment variables.

### Check for new and updated documentation

```bash
# Discover pages from the Akamai Functions Guides llms.txt, then check every
# indexed page using ETag/Last-Modified. New and changed pages are downloaded
# as native Markdown and summarized. Other extractors remain as fallbacks.
python ingest_v2.py --check

# Force reingestion of every page after discovery:
python ingest_v2.py --check --force
```

`--force` only modifies the `--check` workflow. Running `python ingest_v2.py
--force` by itself prints the command help and does not ingest anything. Model
changes are not part of ETag or content-hash change detection, so use
`--check --force` when every existing article must be summarized with a newly
configured model.

Existing entries without stored ETags may be reingested once to establish the
native-Markdown validator baseline.

### Discover links without checking content

```bash
# Register newly published pages without downloading or summarizing them:
python ingest_v2.py --llms

# A different llms.txt index can also be supplied explicitly, including with
# the complete check workflow:
python ingest_v2.py --check --llms https://example.com/docs/llms.txt
```

### Ingest a single URL

```bash
python ingest_v2.py https://techdocs.akamai.com/akamai-functions/docs/use-the-key-value-store
```

### Crawl an entire sitemap (fallback discovery)

```bash
python ingest_v2.py --sitemap https://techdocs.akamai.com/sitemap.xml --prefix akamai-functions
```

### Recompile the master reference

After reingesting, ask your AI agent to recompile the master reference using the prompt in `COMPILE_PROMPT.md`:

```
Recompile docs/_compiled/functions-reference.md following the instructions in COMPILE_PROMPT.md
```

---

## Project structure

```
.
├── .agents/
│   └── rules/project.md            # Antigravity imports AGENTS.md
├── .github/
│   ├── copilot-instructions.md     # Generated Copilot compatibility copy
│   └── workflows/
│       └── agent-instructions.yml  # Prevents instruction drift
├── AGENTS.md                       # Canonical instructions for every agent
├── CLAUDE.md                       # Claude Code imports AGENTS.md
├── docs/
│   ├── _compiled/
│   │   └── functions-reference.md  # ← Both agents read this (compiled reference)
│   └── techdocs-akamai-com/        # Raw Akamai techdocs articles (agent fallback)
│       ├── quickstart.md
│       ├── use-the-key-value-store.md
│       ├── stream-data-from-linode-object-store.md
│       ├── query-relational-databases-postgresql.md
│       ├── integrate-with-property-manager.md
│       ├── application-logs.md
│       ├── aka-command-reference.md
│       ├── webassembly-language-support-matrix.md
│       ├── quotas-and-limits.md
│       ├── faq.md
│       └── welcome.md
├── scripts/
│   └── sync_agent_instructions.py  # Regenerates Copilot instructions
└── functions/                      # Generated functions go here
    └── <function-name>/
        ├── src/index.js
        ├── spin.toml
        └── package.json
```

---
