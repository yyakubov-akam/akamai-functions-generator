# Source: https://techdocs.akamai.com/akamai-functions/docs/quickstart
Date: 2026-06-30T09:38:04.922415
Model: gpt-oss:120b-cloud
## Runtime Constraints
- No explicit constraints are documented in the source material. (If future docs add limits on module size, CPU, memory, or unsupported JavaScript features, they must be added here.)

## Supported APIs and Syntax
- `import { AutoRouter } from 'itty-router'` — imports the AutoRouter class used to create a router instance.  
- `AutoRouter()` — creates a new router object.  
- `router.get(path, handler)` — registers a GET route. The first route that matches the request path is used.  
- `router.post(path, handler)` — (available via itty‑router) registers a POST route.  
- `router.put(path, handler)` — (available via itty‑router) registers a PUT route.  
- `router.delete(path, handler)` — (available via itty‑router) registers a DELETE route.  
- `router.all(path, handler)` — (available via itty‑router) registers a route for any HTTP method.  
- `router.fetch(request)` — processes an incoming `Request` object and returns a `Response`.  
- `addEventListener('fetch', async (event) => { event.respondWith(router.fetch(event.request)); })` — registers the entry point for the Edge runtime; each incoming HTTP request triggers this listener.

## Required Patterns
**Basic AutoRouter pattern**
```js
import { AutoRouter } from 'itty-router';
let router = AutoRouter();

// Define routes (order matters)
router
  .get("/", () => new Response("hello universe"))
  .get('/hello/:name', ({ name }) => `Hello, ${name}!`);

// Edge entry point
addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

**Middleware pattern (any route that does not return a Response is treated as middleware)**
```js
router
  .get('/protected/*', async ({ request }) => {
    // No explicit return → treated as middleware
    const auth = request.headers.get('Authorization');
    if (!auth) return new Response('Unauthorized', { status: 401 });
    // continue to next matching route
  })
  .get('/protected/data', () => new Response('Secret data'));
```

## Common Mistakes and Gotchas
- **Unlike typical Express.js apps, Akamai Functions route ordering matters; the first matching route is used.**  
- **Unlike standard Service Worker code, any route handler that does **not** return a `Response` (or a value that can be coerced into one) is treated as middleware, not a terminal response.**  
- **Unlike a generic Node.js HTTP server, you must use `addEventListener('fetch', …)` and call `event.respondWith(router.fetch(event.request))` to send a response.**  
- **Unlike a local development server, the compiled Spin app runs inside a WebAssembly sandbox; only the APIs listed above are guaranteed to be available at runtime.**  

## Version and Compatibility Notes
- **Node.js version:** The quickstart recommends Node.js **v22** or newer for building JavaScript Spin apps.  
- **Akamai Functions preview:** Access requires enrollment in the public preview and successful `spin aka login`.  
- **Spin plugin:** The `aka` plugin must be installed (`spin plugin install aka`) and kept up‑to‑date (`spin plugins update && spin plugins upgrade aka`).  
- **Spin CLI commands:** `spin new -E akamai-functions -t http-js …`, `spin build`, `spin up`, and `spin aka deploy` are the required workflow commands; they rely on the `spin.toml` manifest in the project root.  