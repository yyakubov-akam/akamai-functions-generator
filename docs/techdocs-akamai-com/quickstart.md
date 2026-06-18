# Source: https://techdocs.akamai.com/akamai-functions/docs/quickstart
Date: 2026-06-05T08:55:26.801346
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use Node.js versions older than 22; the runtime expects Node.js 22 or newer.  
- The Spin installer and `aka` plugin are only supported on Linux amd64.  
- The `spin up` local server defaults to port 3000; if that port is in use you must specify a different port with `--listen`.  

## Supported APIs and Syntax
- `AutoRouter()` — creates an itty‑router instance that supports declarative route registration.  
- `router.get(path, handler)` — registers a GET route; `handler` receives request parameters and must return a `Response` or string.  
- `router.fetch(request)` — processes an incoming `Request` through the router and returns a `Response`.  
- `addEventListener('fetch', async (event) => { … })` — registers a fetch event listener; `event.respondWith()` must be called with a `Response`.  
- `new Response(body, init?)` — constructs an HTTP response; `body` can be a string, `Uint8Array`, etc.; `init` may contain status, headers, etc.  
- `spin new -t http-js --accept-defaults <app-name>` — creates a new JavaScript Spin application from the `http-js` template.  
- `npm install` — installs Node.js dependencies defined in `package.json`.  
- `spin build` — compiles the Spin application to a WebAssembly component (`.wasm`).  
- `spin up [--listen <host:port>]` — runs the application locally, exposing an HTTP server (default `0.0.0.0:3000`).  
- `spin aka login` — initiates the Akamai Functions authentication flow.  
- `spin aka deploy` — deploys the current Spin application to Akamai Functions; prompts for an app name and confirmation.  
- `spin plugin install aka` — installs the `aka` plugin for interacting with Akamai Functions.  
- `spin plugins update` / `spin plugins upgrade aka` — updates all Spin plugins and upgrades the `aka` plugin to the latest version.  

## Required Patterns
**Pattern: Basic HTTP Router with AutoRouter**
```js
import { AutoRouter } from 'itty-router';
const router = AutoRouter();

router
  .get("/", () => new Response("hello universe"))
  .get("/hello/:name", ({ name }) => `Hello, ${name}!`);

addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

**Pattern: Local Development Server**
```bash
# Build the component
spin build

# Run locally (default port 3000)
spin up

# Or specify a custom port
spin up --listen 127.0.0.1:3001
```

**Pattern: Deploy to Akamai Functions**
```bash
# Authenticate (once per session)
spin aka login   # follow the printed link and complete auth

# Deploy the current workspace
spin aka deploy   # will prompt for app name and confirmation
```

## Common Mistakes and Gotchas
- Unlike generic Express‑style routers, **Akamai Functions** route ordering matters – the first matching route is used; later routes are ignored.  
- Unlike a typical fetch handler, **any route that does not return a value is treated as middleware** and will continue to the next matching route.  
- Unlike a generic HTTP server, **unmatched routes automatically return a 404** response; you must explicitly add a catch‑all route if you want custom handling.  
- Unlike standard Node.js scripts, **the `spin up` command binds to `0.0.0.0:3000` by default**, which may conflict with other services; always specify `--listen` when the default port is occupied.  

## Version and Compatibility Notes
- Node.js **v22** (or newer) is the recommended runtime version for building JavaScript Spin apps.  
- The `aka` plugin requires the **public preview** of Akamai Functions; access must be granted via the onboarding form.  
- The Spin installer script (`fwf_install.sh`) and the `aka` plugin are currently **Linux amd64‑only**.  
- The `http-js` template generates code that depends on the **itty‑router** library; ensure it is listed in `package.json`.  
- The `spin aka deploy` command reads the `spin.toml` file in the current directory to determine deployment configuration.  
