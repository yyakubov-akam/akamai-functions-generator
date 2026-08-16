# Source: https://techdocs.akamai.com/akamai-functions/docs/quickstart
Date: 2026-08-16T09:23:44.384216
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not run JavaScript code directly; it must be compiled to WebAssembly using `spin build` before deployment.  
- Do not use the `aka` plugin version older than the latest released version; always run `spin plugins update && spin plugins upgrade aka` before deploying.  
- Do not assume port 3000 is free; if it is in use, start the local server with `spin up --listen <host>:<port>`.  

## Supported APIs and Syntax
```
spin --version                     // prints the installed Spin CLI version
spin plugin install aka            // installs the Akamai Functions plugin for Spin
spin plugins update                // refreshes the list of available plugins
spin plugins upgrade aka           // upgrades the aka plugin to the latest version
spin build                         // compiles the Spin application to WebAssembly
spin up [--listen <addr:port>]     // starts a local HTTP server (default 0.0.0.0:3000) and invokes the app per request
spin aka login                    // initiates an interactive login flow for Akamai Functions
spin aka deploy                    // deploys the compiled Spin app to Akamai Functions
curl -i http://localhost:3000/    // (external tool) sends an HTTP request to the locally running app
```

## Required Patterns
### 1. Local testing pattern
```bash
# Build the app
spin build

# Run locally (optional custom port)
spin up --listen 127.0.0.1:3001   # omit --listen to use default 0.0.0.0:3000

# In a separate terminal, issue a request
curl -i http://localhost:3000/
```

### 2. Authentication & authorization pattern
```bash
# Start login flow
spin aka login

# Follow the printed URL, authenticate with Akamai Control Center or GitHub,
# then approve the CLI when prompted.
```

### 3. Deployment pattern
```bash
# Ensure you are logged in (see pattern #2)
spin aka deploy

# The CLI will:
#   1. Read spin.toml in the current directory
#   2. Prompt for a new app name (or link to an existing app)
#   3. Ask for confirmation
#   4. Deploy and output the public URL
```

## Common Mistakes and Gotchas
- **Unlike typical Node.js execution, Akamai Functions does not run raw JavaScript** – the code must be compiled to WebAssembly with `spin build` before any `spin up` or `spin aka deploy`.  
- **Unlike a generic local server, the default `spin up` port (3000) may already be occupied** – you must specify an alternate address with `--listen` to avoid a bind error.  
- **Unlike a static CLI, the `aka` plugin can become out‑of‑date** – always run the upgrade commands (`spin plugins update && spin plugins upgrade aka`) before login or deploy to avoid compatibility failures.  

## Version and Compatibility Notes
- Access to Akamai Functions requires enrollment in the public preview; the CLI will refuse login/deploy without an approved allow‑list.  
- The `aka` plugin must be the latest version released on the Spin plugin registry; older versions lack support for the current preview APIs.  
- The Quickstart documentation reflects the state of the platform as of the last update (25 days ago). Future changes may require re‑running the plugin upgrade steps.