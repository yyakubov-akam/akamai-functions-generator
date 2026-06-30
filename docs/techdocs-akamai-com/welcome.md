# Source: https://techdocs.akamai.com/akamai-functions/docs/welcome
Date: 2026-06-30T09:37:45.678483
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use native binaries or OS‑level system calls; Akamai Functions runs code in a WebAssembly sandbox.
- Do not rely on a persistent local filesystem; the runtime provides no durable storage.
- Do not exceed the implicit WebAssembly module size limits enforced by the platform (the exact limit is not documented, so keep modules as small as possible).

## Supported APIs and Syntax
- `spin aka deploy` — Deploys a compiled Spin (WebAssembly) application to Akamai Functions.  
  *Usage:* `spin aka deploy [options]`  
- `spin build` — Compiles source code (Rust, Go, JavaScript/TypeScript, Python) to a WebAssembly module ready for deployment.  
  *Usage:* `spin build [options]`

## Required Patterns
**Pattern: Local build → Deploy**

```bash
# 1. Build the Spin application locally (produces a .wasm module)
spin build

# 2. Deploy the built artifact to Akamai Functions
spin aka deploy
```

**Pattern: JavaScript/TypeScript entry point**

```javascript
// src/main.ts (or .js)
// Export a handler that conforms to the Spin HTTP interface
export async function handle(request) {
  // Your logic here
  return new Response("Hello from Akamai Functions!");
}
```

## Common Mistakes and Gotchas
- Unlike a typical Node.js environment, Akamai Functions **does not provide** access to Node’s built‑in modules (e.g., `fs`, `net`, `child_process`) because the code runs inside a WebAssembly sandbox.
- Unlike a traditional server, there is **no persistent local storage**; any state must be stored in external services (e.g., Akamai’s managed databases or external APIs).

## Version and Compatibility Notes
- Akamai Functions is currently in **public preview**; features and limits may change without notice.  
- The platform supports **Rust, Go, JavaScript/TypeScript, and Python** SDKs that compile to WebAssembly; other languages are not supported at this time.