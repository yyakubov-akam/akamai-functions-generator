# Source: https://techdocs.akamai.com/akamai-functions/docs/integrate-with-property-manager
Date: 2026-07-22T11:11:58.482580
Model: gpt-oss:120b-cloud
## Supported APIs and Syntax
- `import { AutoRouter } from 'itty-router'` — imports the automatic router constructor.  
- `let router = AutoRouter();` — creates a router that automatically matches HTTP methods.  
- `router.get(path, handler)` — registers a GET handler for the given `path`. Returns a `Response` object.  
- `new Response(body)` — constructs an HTTP response with the supplied `body` string.  
- `addEventListener('fetch', async (event) => { … })` — registers the entry‑point for every incoming request.  
- `event.respondWith(promise)` — tells the runtime to use the supplied `Promise<Response>` as the HTTP response.  
- `router.fetch(request)` — processes an incoming `Request` through the router and returns a `Promise<Response>`.

## Required Patterns
**Basic Spin‑on‑Akamai‑Functions handler**

```javascript
import { AutoRouter } from 'itty-router';

const router = AutoRouter();

// Example route – adjust as needed
router.get("/", () => new Response("Hello, Akamai Functions"));

addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

**Deploy workflow (CLI commands, not runtime code)**  

```bash
# Create project
spin new -E akamai-functions -t http-js -a hello-akamai-functions
cd hello-akamai-functions

# Build to WebAssembly
spin build

# Deploy (must be logged in)
spin aka login
spin aka deploy
```

**Extract origin hostname from deploy output**  

- Remove the leading `https://` and any trailing `/` from the URL printed by `spin aka deploy`.  
- Use the resulting hostname as **Origin Server Hostname** in the Property configuration.

## Common Mistakes and Gotchas
- **Path forwarding** – Unlike a plain Cloudflare Workers or Node.js server where the request path is received unchanged, Akamai Functions receives the path *after* Property‑level modifications. If the Property does **not** include a “Modify Outgoing Request Path” behavior that strips the routing prefix (e.g., `/hello/ → /`), the router will see `/hello/…` and the `router.get("/")` handler will not match.  
- **Host header** – The Property must set **Forward Host Header** to **Origin Hostname**; otherwise the upstream Spin app may reject the request because the Host header does not match its expected origin.  
- **Wildcard origin URL** – The URL shown by `spin aka deploy` is a wildcard (`…aka.akamai.tech (wildcard)`). Do **not** include the `https://` scheme or trailing slash when entering the hostname into the Property.  

## Version and Compatibility Notes
- Access to Akamai Functions requires enrollment in the **public preview** (complete the onboarding form).  
- The Spin template used must be the `http-js` template with the `-E akamai-functions` extension flag.  
- All CLI commands (`spin build`, `spin aka deploy`, `spin aka login`) assume the latest Spin version that supports the Akamai Functions extension. No additional feature flags are needed.  