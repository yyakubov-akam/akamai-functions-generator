# Source: https://techdocs.akamai.com/akamai-functions/docs/welcome
Date: 2026-08-17T08:27:35.926895
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Code must be compiled to WebAssembly to run on the Akamai Functions platform.
- Deployment must be performed using the `spin aka` plugin.
- Access to the platform is restricted to the public preview; deployment is not available for general availability.

## Supported APIs and Syntax

- `spin aka deploy` — Deploys the Spin application to Akamai Functions.
- Supported languages: Rust, Go, JavaScript, and Python.

## Required Patterns

- **Deployment Command**
  ```bash
  spin aka deploy
  ```

## Common Mistakes and Gotchas

- Unlike standard Node.js or browser environments, code must be compiled to WebAssembly (Wasm) using the Spin framework before deployment.

## Version and Compatibility Notes

- Documentation updated: 2026-03-31T21:38:10.000Z
- Platform status: Limited availability (Public Preview)