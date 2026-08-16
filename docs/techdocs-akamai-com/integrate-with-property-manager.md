# Source: https://techdocs.akamai.com/akamai-functions/docs/integrate-with-property-manager
Date: 2026-08-16T09:23:56.636485
Model: gpt-oss:120b-cloud
## Supported APIs and Syntax

- `import { AutoRouter } from 'itty-router'` — imports the `AutoRouter` class from the *itty‑router* library.  
- `AutoRouter()` — creates a new router instance.  
- `router.get(path, handler)` — registers a **GET** route; `handler` must return a `Response` object.  
- `new Response(body)` — constructs an HTTP response with the supplied body string.  
- `addEventListener('fetch', async (event) => { … })` — registers a fetch‑event listener that receives each incoming request.  
- `event.respondWith(promise)` — tells the runtime to use the resolved `Response` from the supplied promise as the HTTP reply.  
- `router.fetch(request)` — processes a `Request` through the router and returns a `Response` (or a promise of one).  

## Required Patterns

**Minimal Akamai Functions handler using itty‑router**

```javascript
import { AutoRouter } from 'itty-router';

const router = AutoRouter();

router.get("/", () => new Response("Hello, Akamai Functions"));

addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```