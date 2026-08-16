# Source: https://techdocs.akamai.com/akamai-functions/docs/webassembly-language-support-matrix
Date: 2026-08-16T09:26:26.693176
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use a language that lacks **WASI** support; only languages marked ✓ (or “In progress” if you verify full Preview 1 compliance) for the **WASI** column can run on Akamai Functions.  
- Do not rely on **Spin SDK**‑only features; while the Spin SDK implies WASI compatibility, Akamai Functions require the underlying WASI runtime, not Spin‑specific extensions.  
- Do not target a WebAssembly version newer than **WebAssembly 1.0**; only the core implementation (✓ in the **Core** column) is guaranteed to be supported.  
- Do not assume browser‑only WebAssembly modules will execute; modules must be compiled for the **WASI Preview 1** ABI.  

## Common Mistakes and Gotchas
- **Unlike** typical browser‑oriented WebAssembly where any language with a browser build can run, **Akamai Functions** **require** the module to be compiled for **WASI Preview 1**.  
- **Unlike** generic Spin deployments that may accept Spin‑specific SDK libraries, **Akamai Functions** **do not** provide the Spin SDK at runtime; only the standard WASI system calls are available.  
- **Unlike** the “In progress” status shown for some languages (e.g., Python Browser, TypeScript Browser), **Akamai Functions** **cannot** execute those builds until the language fully supports the required WASI preview.  

## Version and Compatibility Notes
- **WebAssembly Core**: Only the stable **WebAssembly 1.0** specification is supported.  
- **WASI**: Must conform to **WASI Preview 1** (the first stable snapshot of the WASI proposal).  
- Languages with a **✓** under the **WASI** column are confirmed compatible with Akamai Functions.  
- Languages marked **“In progress”** for WASI may become compatible in future releases but are not guaranteed in the current runtime.  
- The **Spin SDK** column indicates additional libraries for Spin; these do **not** affect Akamai Functions compatibility beyond the underlying WASI support.  