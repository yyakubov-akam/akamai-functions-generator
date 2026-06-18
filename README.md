# Akamai Functions Generator

An AI-assisted workspace for generating [Akamai Functions](https://techdocs.akamai.com/akamai-functions/docs/quickstart) (Spin-based WebAssembly edge functions) from natural language descriptions.

Works out of the box with **GitHub Copilot** (via `.github/copilot-instructions.md`) and **Claude Code** (via `CLAUDE.md`). Both agents are pre-configured to read a compiled Akamai Functions API reference before writing any code, so they generate correct, production-ready functions without hallucinating unsupported APIs.

---

## How it works

1. **A curated Akamai Functions API reference** is included at `docs/_compiled/functions-reference.md`.
2. **The AI agent reads that reference** before writing any code — Copilot via `.github/copilot-instructions.md`, Claude Code via `CLAUDE.md`.
3. **You describe what you want** and the agent generates a complete, deployable Akamai Function under `functions/<function-name>/`.

---

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| [GitHub Copilot](https://github.com/features/copilot) Agent mode **or** [Claude Code](https://claude.ai/code) | latest | One of these is required for code generation |
| Spin CLI + Akamai plugin | latest | Follow the [Akamai Functions quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart) |
| [Node.js](https://nodejs.org/) | ≥ 18 | Required by the Spin JS toolchain |

> The Spin JS toolchain (`j2w`, `@spinframework/build-tools`) is installed per-function via `npm install`.

---

## Generating a function

**With GitHub Copilot:** open this workspace in VS Code and use Agent mode (`Ctrl+Shift+I` / `Cmd+Shift+I`).

**With Claude Code:** run `claude` in the project root.

Then describe what you want:

```
Create an Akamai Function that redirects users to country-specific subdomains based on their GeoIP location.
```

The agent will scaffold a complete function under `functions/<name>/` including:
- `src/index.js` — the function source
- `spin.toml` — Spin component manifest
- `package.json` + `build.mjs` — build tooling
- `README.md` — usage instructions

### Build and run 

```bash
cd functions/<function-name>
spin build
spin up
spin aka deploy
```

---

## Project structure

```
.
├── .github/
│   └── copilot-instructions.md   # Instructs Copilot to read the reference before coding
├── CLAUDE.md                       # Instructs Claude Code to read the reference before coding
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
└── functions/                      # Generated functions go here
    └── <function-name>/
        ├── src/index.js
        ├── spin.toml
        └── package.json
```

---
