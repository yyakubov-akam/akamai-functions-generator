# Source: https://techdocs.akamai.com/akamai-functions/docs/integrate-with-property-manager
Date: 2026-06-05T08:59:36.859628
Model: gpt-oss:120b-cloud
## Supported APIs and Syntax

- `import { AutoRouter } from 'itty-router'` — imports the automatic router constructor from the **itty‑router** library.  
- `AutoRouter()` — creates a new router instance that automatically matches request methods and paths.  
- `router.get(path, handler)` — registers a handler for HTTP **GET** requests matching *path*.  
  - **Signature:** `router.get(path: string, handler: (request: Request) => Response | Promise<Response>)`  
- `new Response(body, init?)` — constructs a standard Fetch API `Response` object.  
  - **Signature:** `new Response(body?: BodyInit | null, init?: ResponseInit)`  
- `addEventListener('fetch', async (event) => { … })` — registers a listener for the **fetch** event in the Akamai Functions runtime.  
- `event.respondWith(promiseOrResponse)` — tells the runtime to use the supplied `Response` (or a promise that resolves to one) for the incoming request.  

## Required Patterns

### Minimal Spin application for Akamai Functions

```javascript
import { AutoRouter } from 'itty-router';

const router = AutoRouter();

// Route for the root path of the Spin app
router.get("/", () => new Response("Hello, Akamai Functions"));

// Entry point required by the Functions runtime
addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

*All Spin applications deployed to Akamai Functions must follow the pattern above:*

1. **Import** `AutoRouter` (or another compatible router) from `itty-router`.  
2. **Create** a router instance (`AutoRouter()` or `Router()`).  
3. **Register** route handlers (`router.get`, `router.post`, etc.).  
4. **Expose** a `fetch` event listener that calls `event.respondWith` with the router’s `fetch` result.  

---