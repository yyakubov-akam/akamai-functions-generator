## Runtime Constraints

- JavaScript/TypeScript: Use Node.js version 22 or newer.
- Rust: Must use the `wasm32-wasip1` target.
- TinyGo: Must use TinyGo 0.27 or above.
- TinyGo: Must set the environment variable `CGO_ENABLED=1`.

## Supported APIs and Syntax

### JavaScript / TypeScript
`AutoRouter()` — Creates an instance of an itty-router for routing.
`router.get(path, handler)` — Defines a GET route.
`addEventListener('fetch', callback)` — The standard entry point for handling fetch events.
`event.respondWith(response)` — Sends the response back to the runtime.

### Rust
`#[http_component]` — Attribute to mark a function as an HTTP component.
`Response::builder()` — Initiates a response builder.
`Response.status(code)` — Sets the HTTP status code.
`Response.header(key, value)` — Sets an HTTP header.
`Response.body(body)` — Sets the response body.
`Response.build()` — Finalizes and returns the response.

### TinyGo
`spinhttp.Handle(callback)` — Registers the HTTP handler function.

## Required Patterns

### JavaScript / TypeScript (AutoRouter)
```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

router
    .get("/", () => new Response("hello universe"))
    .get('/hello/:name', ({ name }) => `Hello, ${name}!`)

addEventListener('fetch', async (event) => {  
    event.respondWith(router.fetch(event.request));
});
```

### Rust (HTTP Component)
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

### TinyGo (Handle Pattern)
```go
package main

import (
	"fmt"
	"net/http"
	spinhttp "github.com/spinframework/spin/sdk/go/v2/http"
)

func init() {
	spinhttp.Handle(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Hello Akamai!")
	})
}

func main() {}
```

## Common Mistakes and Gotchas

- Unlike standard Node.js environments where logic typically resides in the main execution flow, Akamai Functions JavaScript/TypeScript require the `addEventListener('fetch', ...)` pattern to handle requests.
- Unlike standard Go applications where logic is typically placed in the `main()` function, Akamai Functions TinyGo applications require the handler to be registered within the `init()` function.
- Unlike standard Rust binaries, Akamai Functions require the `#[http_component]` attribute to define the entry point.

## Version and Compatibility Notes

- JavaScript/TypeScript: Node.js 22+ is recommended.
- TinyGo: Requires version 0.27 or above.
- Rust: Requires `wasm32-wasip1` target compatibility.