<!--
Canonical source: AGENTS.md. Edit AGENTS.md, then run:
python scripts/sync_agent_instructions.py
-->

# Akamai Functions Code Generation Rules

## Learn Before Coding

Before writing any code, read `docs/_compiled/functions-reference.md`.

## Reference Maintenance

When asked to check or update the Akamai Functions reference, use the
dependency-free workflow in `scripts/reference_sync.py`:

1. Run `python3 scripts/reference_sync.py check`.
2. If changes are reported, run `python3 scripts/reference_sync.py sync`.
3. Run `python3 scripts/reference_sync.py verify`, even when no upstream
   changes were reported.
4. If verification reports missing metadata or a stale reference, recompile the
   complete reference from every active exact source by following
   `REFERENCE_COMPILATION.md`, then run
   `python3 scripts/reference_sync.py finalize`.
5. Run `python3 scripts/reference_sync.py verify` again and require it to pass.

The legacy `ingest_v2.py` Ollama workflow remains available during migration.
Do not modify or remove its summaries when using the new synchronization
workflow.

## Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them—don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## Output Structure

Write every generated function to `functions/<function_name>/`, where
`<function_name>` is a short, descriptive, lowercase-hyphenated name derived
from the task, such as `echo-request-headers` or `geo-based-redirect`.

## Build and Test Before Handoff

After writing a function, build and test it locally before considering the
task complete:

1. Change to the generated function directory: `cd functions/<function_name>`.
2. Run `spin build` and resolve any build failures.
3. Run `spin up` and keep the local HTTP server running. It listens on port
   `3000` by default and instantiates and invokes the Spin application for each
   request.
4. From another terminal or process, run
   `curl -i http://localhost:3000/` as a baseline smoke test. Exercise any
   additional routes, methods, request bodies, headers, and expected failure
   cases relevant to the generated function.
5. Verify the returned HTTP status, headers, and body against the requested
   behavior, then stop the local `spin up` server.

Do not run `spin aka deploy` as part of automatic build or test verification.
Deployment must be performed manually by the user, or by the agent only when
the user explicitly asks the agent to deploy.
