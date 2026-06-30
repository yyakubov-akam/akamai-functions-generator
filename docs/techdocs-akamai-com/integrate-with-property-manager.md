# Source: https://techdocs.akamai.com/akamai-functions/docs/integrate-with-property-manager
Date: 2026-06-30T09:38:23.786190
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not exceed the WebAssembly module size limit imposed by Akamai Functions (the platform will reject modules larger than the allowed size; exact limit is defined by the service and must be checked in the console).  
- Do not use Node‑specific built‑ins (e.g., `fs`, `net`, `process`) – the runtime is a lightweight V8 environment compiled to WebAssembly.  
- Do not rely on dynamic `import()` at runtime; all imports must be resolved at build time by the `spin build` step.  
- Do not exceed the per‑request CPU‑time quota (the platform enforces a hard timeout; long‑running loops will be terminated).  
- Do not reference external URLs directly from the function code; all outbound traffic must be routed through the configured Property origin.  

## Supported APIs and Syntax
```
import { AutoRouter } from 'itty-router';
```
- **AutoRouter()** – creates an itty‑router instance that can be used to register HTTP handlers.

```
router.get(path: string, handler: (request: Request) => Response | Promise<Response>)
```
- Registers a GET route; `handler` receives a `Request` and returns a `Response` (or a promise of one).

```
router.fetch(request: Request): Response | Promise<Response>
```
- Returns the router’s response for the supplied `Request`. Used inside the fetch event listener.

```
addEventListener('fetch', async (event: FetchEvent) => { … })
```
- Registers the entry point for every incoming HTTP request. `event` is a `FetchEvent`.

```
event.respondWith(response: Response | Promise<Response>)
```
- Sends the supplied response back to the client.

```
new Response(body?: BodyInit, init?: ResponseInit)
```
- Constructs an HTTP response. `body` can be a string, Blob, etc.; `init` may contain status, headers, etc.

## Required Patterns
**Pattern: Minimal Spin‑Functions entry point**

```js
import { AutoRouter } from 'itty-router';

const router = AutoRouter();

// Example route – respond to GET /
router.get("/", () => new Response("Hello, Akamai Functions"));

addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

**Pattern: Deploying a Spin app for Akamai Functions**

```bash
# Create a new Spin project using the Akamai Functions template
spin new -E akamai-functions -t http-js -a hello-akamai-functions
cd hello-akamai-functions

# Replace src/index.js with the Minimal entry point (see above)

# Build to WebAssembly
spin build

# Authenticate (once per session)
spin aka login

# Deploy
spin aka deploy
```

**Pattern: Configuring the Property origin**

1. Obtain the origin hostname from the deploy output (strip `https://` and any trailing `/`).  
2. In the Property rule, set **Origin Server Hostname** to that hostname.  
3. Set **Forward Host Header** to **Origin Hostname**.  

**Pattern: Stripping the routing prefix before forwarding to the function**

```text
Modify Outgoing Request Path behavior:
  Action: Replace Part of the incoming path
  Find what: /hello/
  Replace with: /
  Occurrences: First occurrence only
  Keep the query parameters: Yes
```

## Common Mistakes and Gotchas
- **Unlike a typical Node.js server, Akamai Functions runs in a WebAssembly‑based V8 sandbox** – any use of Node core modules (`fs`, `path`, etc.) will throw “module not found”.  
- **Unlike a regular HTTP server, the request path is not automatically rewritten** – if you route `/hello/*` to the function, you must add a **Modify Outgoing Request Path** behavior to strip the `/hello/` prefix; otherwise the function receives `/hello/…` and will not match the defined route (`/`).  
- **Unlike a standard URL, the Origin Server Hostname field expects only the hostname** – do not include the `https://` scheme or a trailing slash; the platform will reject the configuration.  
- **Unlike a typical fetch handler, you must call `event.respondWith` exactly once** – returning a response directly from the listener without `respondWith` will result in a 500 error.  
- **Unlike a local development server, the function code must be compiled with `spin build` before deployment** – attempting to deploy raw JavaScript files will fail with a “invalid module” error.  

## Version and Compatibility Notes
- The Akamai Functions edge runtime is currently in **public preview**; you must complete the onboarding form and be granted preview access before you can use `spin aka` commands.  
- The `http-js` template targets the **Akamai Functions edge runtime version bundled with the current Spin CLI**; upgrading the Spin CLI may change the underlying runtime version.  
- The `AutoRouter` API is provided by the **itty‑router** library bundled with the template; it is fully supported in the preview runtime but may be subject to change in future releases.  
- Property rule changes (origin hostname, path rewrite) only take effect after the new property version is **activated** (preferably in the Staging environment).  