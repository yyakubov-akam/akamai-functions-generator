## Runtime Constraints

- Must compile applications to WebAssembly.
- Rust target must be `wasm32-wasip1`.
- Go/TinyGo target must be `wasi`.
- Node.js version must be 22 or newer.
- TinyGo version must be 0.27 or above.
- Go SDK requires `CGO_ENABLED=1` environment variable.

## Supported APIs and Syntax

### JavaScript / TypeScript
`addEventListener('fetch', ...)` — Entry point for the application; receives a FetchEvent.
`AutoRouter` — Router implementation from `itty-router` for handling HTTP routes.
`Response` — Standard Web API class for constructing HTTP responses.

### Rust
`spin_sdk::http` — Module containing HTTP types.
`http_component` — Macro to define an HTTP component handler.
`handle_hello_spin(req: Request)` — Handler function signature; returns `anyhow::Result<impl IntoResponse>`.
`Response::builder()` — Builder method to construct HTTP responses.

### Go
`spinhttp.Handle(func(...))` — Function to register an HTTP handler inside the `init()` function.

## Required Patterns

### JavaScript / TypeScript Entry Point
```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

router
    .get("/", () => new Response("hello universe"))
    .get('/hello/:name', ({ name }) => `Hello, ${name}!`);

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

### Rust HTTP Component
```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;

#[http_component]
fn handle_hello_spin(req: Request) -> anyhow::Result<impl IntoResponse> {
    Ok(Response::builder()
        .status(200)
        .header("content-type", "text/plain")
        .body("Hello, Akamai")
        .build())
}
```

### Go HTTP Handler
```go
import spinhttp "github.com/spinframework/spin/sdk/go/v2/http"

func init() {
	spinhttp.Handle(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/plain")
		fmt.Fprintln(w, "Hello Akamai!")
	})
}
```

## Common Mistakes and Gotchas

- **Go CGO:** Unlike standard Go development, the Go SDK for Akamai Functions is built using CGO, so `CGO_ENABLED=1` must be set in the environment.
- **Go Compiler:** Unlike standard Go development, the standard Go compiler does not support WASI exports; you must use TinyGo.
- **Rust Target:** Unlike standard Rust development, you must explicitly add the `wasm32-wasip1` target to compile for Akamai Functions.
- **TinyGo Version:** Unlike standard Go development, you must use TinyGo 0.27 or above; the Spin SDK requires this version.

## Version and Compatibility Notes

- **Spin:** Windows binary release v3.6.2 is supported.
- **Node.js:** Version 22 (or newer) is required/recommended for JavaScript and TypeScript tooling.
- **TinyGo:** Version 0.27 or above is required.
- **Go SDK:** Version v0.10.0 is referenced in build outputs.