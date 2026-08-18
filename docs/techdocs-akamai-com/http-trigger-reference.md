# Source: https://techdocs.akamai.com/akamai-functions/docs/http-trigger-reference
Date: 2026-08-17T09:29:05.102479
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Akamai Functions currently supports only the `http` trigger type for Spin applications.

## Supported APIs and Syntax

- `[[trigger.http]]` — Defines the HTTP trigger configuration block.
- `route` — The route pattern the trigger matches.
- `component` — The name of the component to handle the route.
- `spin-full-url` — The full URL of the request including host and scheme.
- `spin-path-info` — The request path relative to the component route.
- `spin-path-match-n` — The wildcard segment value (where n is the segment name, e.g., `spin-path-match-userid`).
- `spin-matched-route` — The matched part of the trigger route.
- `spin-raw-component-route` — The component route pattern matched.
- `true-client-ip` — The IP address of the client sending the request.

## Required Patterns

### HTTP Trigger Configuration
Use TOML syntax to define the trigger configuration at the root of the configuration file.

```toml
[[trigger.http]]
route = "/..."
component = "my-application"
```

### Accessing Wildcard Parameters
Access wildcard values from the request headers using the `spin-path-match-n` header name.

```javascript
// Access the 'userid' wildcard value from a route like /user/{userid}
const userId = request.headers.get('spin-path-match-userid');
```

## Common Mistakes and Gotchas

- Unlike standard Node.js environments, Akamai Functions injects specific Spin-related headers (`spin-*`) and the `true-client-ip` header into the request object.
- The `spin-path-match-n` headers are conditionally included; they are only present if the route definition contains the corresponding wildcard segment.

## Version and Compatibility Notes

- Akamai Functions is built on Spin applications.
- The `http` trigger type is the currently supported trigger type.