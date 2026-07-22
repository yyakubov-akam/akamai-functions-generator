# Source: https://techdocs.akamai.com/akamai-functions/docs/quickstart
Date: 2026-07-22T11:11:40.308532
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not run code directly on Node.js; Akamai Functions only executes compiled WebAssembly modules.  
- Do not use the default local server port 3000 if it is already in use; specify a different address with `--listen`.  
- Do not attempt to deploy without first authenticating via `spin aka login`.  
- Do not use an outdated `aka` plugin; always run `spin plugins update` and `spin plugins upgrade aka` before building or deploying.  
- Do not deploy to a non‑existent app without linking; use `spin aka app link` to associate the workspace with an existing app.  

## Supported APIs and Syntax
- `spin.build()` — compiles the Spin application to WebAssembly.  
- `spin.up()` — starts a local HTTP server (default `0.0.0.0:3000`) and invokes the Spin app for each request.  
- `spin.up(--listen address:port)` — starts the local server on the specified address and port.  
- `spin.aka.login()` — initiates the device‑code OAuth flow for Akamai Functions; prints a URL for the user to open.  
- `spin.aka.deploy()` — deploys the compiled WebAssembly app to Akamai Functions; prompts for an app name and confirmation.  
- `spin.aka.app.link()` — links the current workspace to an existing Akamai Functions app.  

## Required Patterns
**Pattern 1 – Build → Test → Deploy**

```bash
# Compile to WebAssembly
spin build

# Run locally (default port 3000)
spin up

# Deploy to Akamai Functions
spin aka deploy
```

**Pattern 2 – Login before any `aka` command**

```bash
spin aka login
# Follow the device‑code URL, authenticate, then return to the terminal.
```

**Pattern 3 – Override listening port if 3000 is busy**

```bash
spin up --listen 127.0.0.1:3001
```

## Common Mistakes and Gotchas
- Unlike standard Node.js, Akamai Functions cannot execute raw JavaScript; the code must be compiled to WebAssembly.  
- Unlike typical CLI servers, `spin up` always binds to `0.0.0.0:3000` by default; you must explicitly set `--listen` when that port is occupied.  
- Unlike persistent cloud services, local testing with `spin up` does not retain state between restarts; each request starts a fresh instance.  
- Unlike generic plugin managers, the `aka` plugin must be upgraded with `spin plugins update` / `spin plugins upgrade aka` to access the latest commands.  

## Version and Compatibility Notes
- Access to Akamai Functions requires enrollment in the public preview and an allow‑list status.  
- The `aka` plugin must be installed (`spin plugin install aka`) and kept up‑to‑date; older versions may lack required commands.  
- Deployment commands (`spin aka deploy`, `spin aka login`) are only available after the `aka` plugin is installed and the user is logged in.  
- Supported languages are limited to those that can compile to WebAssembly; consult the WebAssembly language support matrix for the definitive list.