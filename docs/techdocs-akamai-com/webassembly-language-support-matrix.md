# Source: https://techdocs.akamai.com/akamai-functions/docs/webassembly-language-support-matrix
Date: 2026-06-30T09:40:18.514347
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use languages that lack **WASI Preview 1** support; Akamai Functions only runs WebAssembly modules that implement the WASI Preview 1 API.  
- Do not rely on **Spin SDK**‑specific libraries; only the core WASI API is guaranteed to be available in Akamai Functions.  
- Do not assume browser‑only WebAssembly features (e.g., `WebGL`, `DOM` APIs) are present; Akamai Functions provides no browser environment.  

## Supported APIs and Syntax
*No explicit JavaScript/Node.js APIs are documented in the source material.*  

## Required Patterns
**Pattern: Compile to WASI Preview 1**

```bash
# Example for Rust (one of the recommended languages)
# 1. Ensure the target is wasi-preview1
rustup target add wasm32-wasi

# 2. Build the project for WASI
cargo build --release --target wasm32-wasi

# 3. The resulting .wasm file can be uploaded to Akamai Functions
#    (no additional Spin SDK libraries are required)
```

**Pattern: Deploy a WASI‑compatible WebAssembly module to Akamai Functions**

```javascript
// Minimal handler skeleton (pseudo‑code; actual deployment uses Akamai CLI)
import { handler } from 'akamai-functions';

export async function main(request) {
  // The request object is provided by Akamai Functions runtime.
  // Your WASI module can be invoked via the provided WASI host bindings.
  const result = await handler.invokeWasm('my_module.wasm', { /* wasi args */ });
  return result;
}
```

## Common Mistakes and Gotchas
- **Unlike browser‑only WebAssembly**, Akamai Functions **does not provide a DOM or browser APIs**; any code that expects `window`, `document`, or browser‑specific globals will fail.  
- **Unlike generic Spin deployments**, Akamai Functions **does not automatically include Spin SDK libraries**; only the standard WASI Preview 1 interface is available.  
- **Unlike a typical Node.js environment**, the runtime **does not expose Node built‑ins** (e.g., `fs`, `process`); all I/O must go through the WASI API.  

## Version and Compatibility Notes
- Akamai Functions requires **WASI Preview 1** compliance; languages that only list “WASI” in the matrix are assumed to meet this version.  
- Languages marked “In progress” for WASI or Spin SDK are **not yet supported** on Akamai Functions.  
- Recommended production‑grade languages (Rust, JavaScript/TypeScript, Python, Go) all have confirmed **WASI Preview 1** support.  