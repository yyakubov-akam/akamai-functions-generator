## Runtime Constraints

- Must use WebAssembly (WASM) as the runtime target.
- Must have access to the public preview of Akamai Functions (requires onboarding form completion).
- Node.js version must be 22 (or newer).
- Rust target must be `wasm32-wasip1`.
- Go/TinyGo target must be `wasi`.
- TinyGo version must be 0.27 or above.
- TinyGo build requires `CGO_ENABLED=1` environment variable.
- Identity providers supported: Akamai Control Center or GitHub.
- Access requires allow-listing status for Akamai Functions.

## Supported APIs and Syntax

- `addEventListener('fetch', ...)` — Entry point for JavaScript/TypeScript handlers.
- `spin_sdk::http::Request` — HTTP request structure for Rust.
- `spin_sdk::http::Response` — HTTP response structure for Rust.
- `spin_sdk::http::IntoResponse` — Trait for converting Rust types to HTTP responses.
- `spin_sdk::http_component` — Macro for defining HTTP components in Rust.
- `AutoRouter` — Router from 'itty-router' for handling HTTP routes in JS/TS.
- `spinhttp.Handle(func(...))` — Function for registering HTTP handlers in Go.
- `spin new -E akamai-functions -t <template> --accept-defaults <name>` — Command to create a new application.
- `spin build` — Command to compile the application to WebAssembly.
- `spin up` — Command to start a local HTTP server for testing.
- `spin aka login` — Command to authenticate with Akamai Functions.
- `spin aka deploy` — Command to deploy the application to Akamai Functions.

## Required Patterns

### JavaScript / TypeScript Entry Point
```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

// Route ordering matters, the first route that matches will be used
// Any route that does not return will be treated as a middleware
// Any unmatched route will return a 404
router
    .get("/", () => new Response("hello universe"))
    .get('/hello/:name', ({ name }) => `Hello, ${name}!`)

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
    println!("Handling request to {:?}", req.header("spin-full-url"));
    Ok(Response::builder()
        .status(200)
        .header("content-type", "text/plain")
        .body("Hello, Akamai")
        .build())
}
```

### Go HTTP Handler
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

- Unlike standard Go, Akamai Functions requires the TinyGo compiler because the standard Go compiler does not yet support WASI exports.
- Unlike standard Go builds, Akamai Functions builds require the `CGO_ENABLED=1` environment variable to be set.
- Unlike standard Node.js development, Akamai Functions requires Node.js version 22 (or newer).
- In `AutoRouter`, unlike standard middleware stacks where order might be less critical, route ordering matters strictly; the first route that matches will be used.
- Unlike standard web frameworks where unmatched routes might throw errors, unmatched routes in `AutoRouter` will return a 404.

## Version and Compatibility Notes

- Node.js version 22 (or newer) is recommended.
- TinyGo version 0.27 or above is required for the Spin SDK.
- Rust target architecture must be `wasm32-wasip1`.
- Go target architecture must be `wasi`.
- Access is currently limited to the public preview and requires completion of an onboarding form.
- The `aka` plugin for Spin must be installed to interact with the Akamai Functions platform.