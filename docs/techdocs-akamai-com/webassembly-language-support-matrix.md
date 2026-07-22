# Source: https://techdocs.akamai.com/akamai-functions/docs/webassembly-language-support-matrix
Date: 2026-07-22T11:14:42.226478
Model: gpt-oss:120b-cloud
## Required Patterns

**Pattern: Compile to a WASI‑compatible WebAssembly module**  
```bash
# Example using Rust (one of the recommended languages)
# 1. Install the WASI target
rustup target add wasm32-wasi

# 2. Build the project for WASI
cargo build --release --target wasm32-wasi

# 3. The resulting .wasm file can be deployed to Akamai Functions
#    (e.g., upload via the Akamai CLI or UI)
```

**Pattern: Deploy a WASI module to Akamai Functions**  
```javascript
// Using the Akamai Functions SDK (pseudo‑code – actual SDK calls may differ)
import { uploadFunction } from '@akamai/functions-sdk';

const wasmBinary = await fetch('my_module.wasm').then(r => r.arrayBuffer());

await uploadFunction({
  name: 'my-wasi-function',
  wasm: wasmBinary,
  // No additional runtime configuration needed; the platform provides WASI
});
```

**Pattern: Languages eligible for Akamai Functions**  
Only languages that list **WASI** support (or have a Spin SDK, which implies WASI) can be used:

| Language | WASI support |
|----------|--------------|
| JavaScript | ✅ |
| Python | ✅ |
| Java | ✅ |
| PHP | ✅ |
| C# / .NET | ✅ |
| C++ | ✅ |
| Ruby | ✅ |
| C | ✅ |
| Swift | ✅ |
| Scala (JVM) | ✅ |
| Go | ✅ |
| Kotlin (JVM) | ✅ |
| Rust | ✅ |
| AssemblyScript | ✅ |
| Grain | ✅ |
| Motoko | ✅ |

When selecting a language, ensure the build toolchain targets the `wasm32-wasi` (or equivalent) target.

---

## Common Mistakes and Gotchas

- **Unlike standard Node.js or browser environments, Akamai Functions only executes WebAssembly modules that have WASI support.**  
  *If you compile a module for the browser (e.g., `wasm32-unknown-unknown`) it will not run on Akamai Functions.*

- **Unlike generic WebAssembly runtimes, Akamai Functions does not provide a full POSIX environment.**  
  *Only the WASI Preview 1 APIs are available; attempts to use non‑standard syscalls will fail.*

- **Unlike typical serverless platforms, you cannot upload raw source code; you must upload a compiled `.wasm` binary that conforms to the WASI ABI.**  

- **Unlike local development, the function size is limited by the platform’s deployment quota (not specified here).**  
  *Oversized `.wasm` binaries will be rejected at upload time.*

---