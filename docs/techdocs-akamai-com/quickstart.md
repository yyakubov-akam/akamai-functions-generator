# Source: https://techdocs.akamai.com/akamai-functions/docs/quickstart
Date: 2026-08-17T08:31:08.490883
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Node.js version 22 (or newer) is required
- TinyGo version 0.27 or above is required
- Rust target `wasm32-wasip1` must be added to the Rust toolchain
- Go SDK requires the `CGO_ENABLED=1` environment variable to be set
- Standard Go compiler does not support WASI exports; TinyGo must be used

## Supported APIs and Syntax

### JavaScript / TypeScript
`AutoRouter` — A router from the `itty-router` library for handling HTTP routes
`addEventListener('fetch', callback)` — The standard Web API entry point for handling fetch events
`new Response(body)` — Constructs an HTTP response object

### Rust
`spin_sdk::http::Request` — Represents an incoming HTTP request
`spin_sdk::http::Response` — Represents an outgoing HTTP response
`spin_sdk::http::IntoResponse` — Trait for types that can be converted into a response
`spin_sdk::http_component` — Attribute macro to mark a function as an HTTP component
`anyhow::Result` — Error handling type used in component handlers

### Go
`spinhttp.Handle(handler)` — Registers a handler function for incoming HTTP requests
`http.ResponseWriter` — Interface for writing the HTTP response
`http.Request` — Represents the incoming HTTP request

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
import (
    spinhttp "github.com/spinframework/spin/sdk/go/v2/http"
)

func init() {
    spinhttp.Handle(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")
        fmt.Fprintln(w, "Hello Akamai!")
    })
}
```

## Common Mistakes and Gotchas

- Unlike standard Node.js development, Akamai Functions requires the `addEventListener('fetch')` pattern to handle incoming requests
- Route ordering matters in `AutoRouter`; the first matching route is used, and unmatched routes return a 404
- Unlike standard Go development, Akamai Functions requires the `spinhttp.Handle` function in an `init()` block to register the handler
- Unlike standard Go development, Akamai Functions requires the `CGO_ENABLED=1` environment variable to build the Go SDK

## Version and Compatibility Notes

- Spin binary version 3.6.2 is the supported release for Windows
- Node.js version 22.13.0 is the version used in the documentation examples
- The Rust target `wasm32-wasip1` is required for Rust compilation
- The Go SDK version v0.10.0 is referenced in the build output