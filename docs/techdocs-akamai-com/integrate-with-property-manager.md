# Source: https://techdocs.akamai.com/akamai-functions/docs/integrate-with-property-manager
Date: 2026-08-17T08:34:22.888201
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- The application entry point must be located at `src/index.js`.
- The application must be built using the `http-js` template.
- The `addEventListener('fetch', ...)` pattern is required for the runtime entry point.

## Supported APIs and Syntax

- `AutoRouter` — A router class from the `itty-router` module for handling HTTP requests.
- `router.get(path, handler)` — Defines a route handler for GET requests.
- `new Response(body)` — Constructs a new HTTP Response object.
- `addEventListener('fetch', handler)` — Registers an event listener for the 'fetch' event.
- `event.respondWith(promise)` — Sends the response back to the client within the fetch event handler.

## Required Patterns

### Fetch Event Handler Pattern
The application must wrap the router logic within an `addEventListener` for the 'fetch' event and use `respondWith` to return the result.

```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

router.get("/", () => new Response("Hello, Akamai Functions"));

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

## Common Mistakes and Gotchas

- Unlike standard Node.js routing, Akamai Functions (via this template) requires the `addEventListener('fetch', ...)` wrapper to handle the request lifecycle.
- When configuring the Akamai Property "Forward Host Header", it must be set to "Origin Hostname" to ensure correct request forwarding.
- The Origin Hostname for the Property configuration is derived by removing the `https://` prefix and the trailing slash (`/`) from the Spin application URL.

## Version and Compatibility Notes

- Access is restricted to the "public preview" (requires onboarding form completion).
- The `spin aka` plugin for Spin is required for deployment commands (`spin aka deploy`, `spin aka login`).
- The `spin aka deploy` command requires authentication via Akamai Control Center or GitHub credentials.