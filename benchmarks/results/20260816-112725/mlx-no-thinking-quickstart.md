## Runtime Constraints

- For JavaScript/TypeScript, use Node.js version 22 or newer.
- For Rust, the `wasm32-wasip1` target must be installed via `rustup`.
- For TinyGo, the compiler must be installed and the `CGO_ENABLED=1` environment variable must be set for builds.
- For TinyGo, the Spin SDK requires TinyGo version 0.27 or above.

## Supported APIs and Syntax

### JavaScript/TypeScript
`import { AutoRouter } from 'itty-router';` — Imports the router for handling HTTP requests.
`let router = AutoRouter();` — Initializes an AutoRouter instance.
`router.get(path, handler)` — Defines a GET route; if the route does not return, it acts as middleware.
`addEventListener('fetch', async (event) => { ... });` — Standard entry point for handling fetch events.
`event.respondWith(router.fetch(event.request))` — Passes the incoming request to the router and responds with the result.

### Rust
`use spin_sdk::http::{IntoResponse, Request, Response};` — Imports necessary types for handling HTTP components.
`#[http_component]` — Attribute to mark a function as a Spin HTTP component.
`fn handle_hello_spin(req: Request) -> anyhow::Result<impl IntoResponse>` — Function signature for an HTTP component.
`Response::builder().status(code).header(key, value).body(body).build()` — Builder pattern to construct an HTTP response.

### Go (TinyGo)
`spinhttp.Handle(func(w http.ResponseWriter, r *http.Request) { ... })` — Registers the HTTP handler within the Spin runtime.

## Required Patterns

### JavaScript/TypeScript (AutoRouter Pattern)
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

## Common Mistakes and Gotaks

- Unlike standard Node.js environments where you might use `http.createServer`, Akamai Functions (via Spin) use the `addEventListener('fetch', ...)` pattern for JavaScript/TypeScript.
- Unlike standard Go builds, TinyGo requires `CGO_ENABLED=1` to be set for the Spin SDK to function correctly.
- Unlike standard routing libraries, in `itty-router`'s `AutoRouter`, route ordering matters: the first matching route is used, and routes without a return value act as middleware.