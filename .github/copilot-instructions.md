<!--
Canonical source: AGENTS.md. Edit AGENTS.md, then run:
python scripts/sync_agent_instructions.py
-->

# Akamai Functions Code Generation Rules

## Learn Before Coding

Before writing any code, read `docs/_compiled/functions-reference.md`.

## Reference Maintenance

The checked-in reference is a curated generated artifact and may have been
prepared by any compilation workflow. When updating it in a public clone, use
the portable exact-source process below.

When asked to check or update the Akamai Functions reference, use the
dependency-free workflow in `scripts/reference_sync.py`:

1. Run `python3 scripts/reference_sync.py check`.
2. If `check` reports any updates, including validator refreshes where the
   content is unchanged, run `python3 scripts/reference_sync.py sync`.
3. Run `python3 scripts/reference_sync.py verify`, even when no upstream
   changes were reported.
4. Only if `verify` reports missing metadata or a stale reference, recompile the
   complete reference from every active exact source by following
   `REFERENCE_COMPILATION.md`. A validator-only refresh does not require
   recompilation. After recompiling, run
   `python3 scripts/reference_sync.py finalize`.
5. Run `python3 scripts/reference_sync.py verify` again and require it to pass.

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

## Document the Function for Users

Every generated function must include a function-specific `README.md`. Replace
any generic README inherited from a Spin template; leaving scaffold
documentation unchanged is not a complete handoff.

Write the README for a human who needs to understand, configure, run, and call
the function. Keep it concise, but include the following when applicable:

- A plain-language summary of what the function does and its intended use.
- Supported routes and methods, including relevant query parameters, headers,
  request bodies, response bodies, HTTP status codes, and error behavior.
- Required configuration, variables, secrets, capabilities, and allowed
  outbound hosts.
- Exact commands for installing dependencies, building, and running locally.
- Copy-pasteable request examples, such as `curl` commands, for the main usage
  and important failure cases.
- Manual deployment instructions and any relevant operational, security, or
  platform limitations.

Omit irrelevant sections rather than adding boilerplate. Before handoff, check
the README against the generated source and `spin.toml` so that its commands,
configuration, and behavior are accurate.

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
