## Runtime Constraints

- For JavaScript/TypeScript, use Node.js version 22 or newer.
- For Rust, the `wasm32-wasip1` target must be installed.
- For TinyGo, the compiler must be installed and the Spin SDK requires TinyGo 0.27 or above.
- For TinyGo builds, the environment variable `CGO_ENABLED=1` must be set.

## Supported APIs and Syntax

### JavaScript / TypeScript
`import { AutoRouter } from 'itty-router';` — Imports the router for handling HTTP requests.
`let router = AutoRouter();` — Initializes an AutoRouter instance.
`router.get(path, handler)` — Defines a GET route.
`router.post(path, handler)` — Defines a POST route.
`addEventListener('fetch', async (event) => { ... })` — The standard entry point for handling fetch events in the runtime.
`event.respondWith(response)` — Used within a fetch event listener to send a response back to the client.

### Rust
`use spin_sdk::http::{IntoResponse, Request, Response};` — Imports necessary types for HTTP component handling.
`#[http_component]` — Attribute used to mark a function as a Spin HTTP component.
`fn handle_name(req: Request) -> anyhow::Result<impl IntoResponse)` — Signature for a standard Spin HTTP component handler.

### Go (TinyGo)
`spinhttp.Handle(func(w http.ResponseWriter, r *http.Request) { ... })` — Registers the HTTP handler function within the Spin runtime.

## Required Patterns

### JavaScript/TypeScript (AutoRouter Pattern)
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

### Rust (HTTP Component Pattern)
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

### Go (TinyGo Pattern)
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

- Unlike standard Node.js environments where you might use `http.createServer`, Akamai Functions (via Spin) use the `addEventListener('fetch', ...)` pattern for JavaScript/TypeScript.
- Unlike standard Node.js, route ordering in `AutoRouter` matters: the first route that matches will be used.
- Unlike standard Node.js, any route that does not return will be treated as a middleware.
- Unlike standard Node.js, any unmatched route will return a 404.
- Unlike standard Go, TinyGo must be used instead of the standard Go compiler to support WASI exports.