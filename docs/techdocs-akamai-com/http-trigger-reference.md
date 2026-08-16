# Source: https://techdocs.akamai.com/akamai-functions/docs/http-trigger-reference
Date: 2026-08-16T10:57:45.812625
Model: gpt-oss:120b-cloud
## Runtime Constraints
* No explicit runtime constraints are documented in the source material.  

---

## Supported APIs and Syntax
* `[[trigger.http]]` — TOML configuration block that registers an HTTP trigger for a Spin component.  
  * `route = "/..."` — The URL path pattern that the trigger matches.  
  * `component = "my-application"` — Name of the component that will handle requests matching the route.  

* `request.headers["spin-full-url"]` — Header containing the full request URL, including scheme and host.  
* `request.headers["spin-path-info"]` — Header containing the request path relative to the component’s route.  
* `request.headers["spin-path-match-n"]` — Header (conditionally included) where **n** is the name of a single‑segment wildcard in the route; its value is the matched segment.  
* `request.headers["spin-matched-route"]` — Header containing the portion of the trigger route that was matched, including any wildcard indicator.  
* `request.headers["spin-raw-component-route"]` — Header containing the raw component route pattern that was matched, including any wildcard indicator.  
* `request.headers["true-client-ip"]` — Header that returns the IP address of the original client that sent the request (e.g., `151.49.93.60`).  

---

## Required Patterns
### 1. Define an HTTP trigger in `spin.toml`
```toml
[[trigger.http]]
route = "/users/:userid"
component = "user-service"
```

### 2. Access Spin‑provided request headers in a component (Node.js example)
```js
export async function handler(request) {
  // Full URL of the incoming request
  const fullUrl = request.headers["spin-full-url"];

  // Path relative to the component route
  const pathInfo = request.headers["spin-path-info"];

  // Value of a wildcard named `userid` in the route
  const userId = request.headers["spin-path-match-userid"];

  // Matched portion of the trigger route
  const matchedRoute = request.headers["spin-matched-route"];

  // Raw component route pattern
  const rawComponentRoute = request.headers["spin-raw-component-route"];

  // Original client IP
  const clientIp = request.headers["true-client-ip"];

  // ...your logic here...
  return new Response(`User ${userId} requested ${fullUrl}`, { status: 200 });
}
```

---

## Common Mistakes and Gotchas
* Unlike standard Node.js/Express where the request URL is accessed via `req.url` or `req.originalUrl`, Akamai Functions does **not** populate those fields; you must read the full URL from the `spin-full-url` header.  
* Unlike typical frameworks that expose route parameters directly on `req.params`, Akamai Functions provides wildcard values only through headers named `spin-path-match-<name>`.  
* The `true-client-ip` header is **not** automatically added by all CDNs; it is only present when Akamai Functions injects it, so code should treat it as optional.  

---

## Version and Compatibility Notes
* No version‑specific flags, bundle requirements, or phased‑rollout limitations are mentioned in the provided excerpt.  