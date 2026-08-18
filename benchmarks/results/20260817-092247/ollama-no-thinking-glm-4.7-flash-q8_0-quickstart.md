## Runtime Constraints

- Do not use Node.js features not supported by WebAssembly (e.g., native file system access, `fs` module).
- Maximum application size is limited by the WebAssembly component format (typically a few MBs).
- CPU and memory usage are limited by the Akamai Functions execution environment.
- Unsupported JS features: Native `require`, CommonJS modules, `Buffer` (use Web Streams API).

## Supported APIs and Syntax

`AutoRouter` — A router for handling HTTP requests and responses.
`addEventListener('fetch', handler)` — Entry point for handling incoming HTTP requests.
`router.get(path, handler)` — Define a GET route.
`router.fetch(event.request)` — Execute the router with a fetch event.
`Response` — Standard Web API class for constructing HTTP responses.
`Request` — Standard Web API class representing an HTTP request.
`spin_sdk::http::Request` — Rust SDK request type.
`spin_sdk::http::Response` — Rust SDK response type.
`spin_sdk::http::IntoResponse` — Rust trait for converting a value into an HTTP response.
`spin_sdk::http_component` — Rust macro for defining HTTP components.
`spinhttp.Handle(handler)` — TinyGo SDK function to register an HTTP handler.
`http.ResponseWriter` — Go SDK interface for writing HTTP responses.
`http.Request` — Go SDK type representing an HTTP request.

## Required Patterns

### JavaScript/TypeScript Entry Point
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

### TinyGo HTTP Handler
```go
package main

import (
    "fmt"
    "net/http"
    spinhttp "github.com/spinframework/spin/sdk/go/v2/http"
)

func init() {
    spinhttp.Handle(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")
        fmt.Fprintln(w, "Hello Akamai!")
    })
}

func main() {}
```

## Common Mistakes and Gotchas

- Unlike standard Node.js, Akamai Functions runs in a WebAssembly environment; do not rely on Node.js specific globals like `process` or `Buffer`.
- Route ordering matters: the first route that matches will be used. Unmatched routes return a 404.
- Any route that does not return a value is treated as middleware.
- In Rust, the `#[http_component]` macro is required to define an HTTP handler.
- In TinyGo, the `spinhttp.Handle` function must be called in the `init()` function to register the handler.
- In TinyGo, the `CGO_ENABLED=1` environment variable must be set because the Go SDK is built using CGO.
- In TypeScript, the `@ts-ignore` comment is required to suppress type errors for the `addEventListener` call.

## Version and Compatibility Notes

- Spin CLI version 3.6.2 or higher is required.
- Node.js version 22 (or newer) is recommended for JavaScript/TypeScript development.
- Rust target `wasm32-wasip1` must be added for Rust development.
- TinyGo version 0.27 or above is required.
- The `aka` plugin for Spin must be installed to interact with Akamai Functions.
- Access to Akamai Functions is currently limited to the public preview.