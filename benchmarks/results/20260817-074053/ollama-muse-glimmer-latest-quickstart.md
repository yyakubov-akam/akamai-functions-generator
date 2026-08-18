## Supported APIs and Syntax

`AutoRouter()` — creates an itty-router AutoRouter instance
`router.get(path, handler)` — registers a GET route on the router
`router.fetch(request)` — processes a request through the router
`Response(body)` — creates a Web Response object
`addEventListener(type, listener)` — registers a global event listener
`FetchEvent.respondWith(response)` — sets the response for a fetch event
`spin_sdk::http_component` — marks a Rust function as an HTTP component
`spin_sdk::http::Request` — incoming HTTP request type for Rust components
`spin_sdk::http::Response::builder()` — starts building an HTTP response in Rust
`ResponseBuilder.status(code)` — sets HTTP status code on builder
`ResponseBuilder.header(name, value)` — adds a header to response builder
`ResponseBuilder.body(body)` — sets response body on builder
`ResponseBuilder.build()` — finalizes and returns Response
`spinhttp.Handle(handler)` — registers Go HTTP handler for Spin

## Required Patterns

**JavaScript Fetch Handler**
```javascript
import { AutoRouter } from 'itty-router';
let router = AutoRouter();
router.get("/", () => new Response("hello universe"));
addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

**TypeScript Fetch Handler**
```typescript
import { AutoRouter } from 'itty-router';
let router = AutoRouter();
router.get("/", () => new Response("hello universe"));
addEventListener('fetch', async (event: FetchEvent) => {
    event.respondWith(router.fetch(event.request));
});
```

**Rust HTTP Component**
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

**Go HTTP Handler**
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

Unlike standard Go builds where CGO may be disabled by default, Akamai Functions Go SDK builds require `CGO_ENABLED=1` environment variable to be set.

## Version and Compatibility Notes

- Akamai Functions access requires public preview allow-listing via onboarding form
- `spin aka` plugin must be installed and upgraded: `spin plugin install aka`, `spin plugins update`, `spin plugins upgrade aka`
- Node.js version 22 or newer is recommended for JavaScript/TypeScript builds
- Rust target `wasm32-wasip1` must be added via `rustup target add wasm32-wasip1`
- TinyGo compiler version 0.27 or above is required for Go builds
- Spin application creation for Akamai Functions uses flag `-E akamai-functions` with templates `http-js`, `http-ts`, `http-rust`, `http-go`
