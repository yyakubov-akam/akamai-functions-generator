## Runtime Constraints

- Do not use Node.js specific modules (e.g., `fs`, `path`, `http`) unless explicitly documented as supported.
- Do not use browser-specific APIs (e.g., `window`, `document`, `localStorage`).
- Code must be compatible with WebAssembly execution environment.
- Application start-up time and execution must be fast; avoid blocking operations.

## Supported APIs and Syntax

`spin aka deploy` — Deploys the current Spin application to Akamai Functions using the `spin aka` plugin.
`spin aka` — The CLI plugin used for deployment and management of Akamai Functions applications.
`spin` — The open source framework for building and running event-driven applications.

## Required Patterns

### Deployment Command
```bash
spin aka deploy
```

### Application Structure
```javascript
// Example Akamai Functions application structure
// Ensure exports are correctly formatted for the runtime
export default {
  async handler(request) {
    // Handle the request
    return new Response("Hello, Akamai Functions!");
  }
};
```

## Common Mistakes and Gotchas

- Unlike standard Node.js, Akamai Functions does not support the `fs` module for file system operations.
- Unlike standard Node.js, Akamai Functions does not support the `http` module for creating HTTP servers.
- Unlike standard browser environments, Akamai Functions does not provide access to `window` or `document` objects.
- Ensure all dependencies are compatible with WebAssembly and the Akamai Functions runtime.

## Version and Compatibility Notes

- Akamai Functions is currently in limited availability (public preview).
- Access must be requested via the [Onboarding form](https://fibsu0jcu2g.typeform.com/fwf-preview?typeform-source=developer.fermyon.com).
- The platform uses Spin framework version compatible with WebAssembly-based execution.
- Global geo replication is enabled by default.