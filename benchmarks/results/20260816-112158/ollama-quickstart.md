## Runtime Constraints
- Do not use Node.js versions older than **v22**; the runtime expects Node 22 or newer.  
- Do not build Rust components without targeting **`wasm32-wasip1`**; the Spin build command requires this target.  
- Do not use TinyGo versions older than **0.27**; the Spin SDK requires TinyGo ≥ 0.27.  
- Do not run the Go build without setting the environment variable **`CGO_ENABLED=1`**; the Go SDK depends on CGO.  
- Do not install the Spin binary on unsupported platforms; installers are provided only for **Linux (amd64), macOS (amd64 & arm64), and Windows (amd64)**.  
- Do not exceed the default local testing port **3000** unless you explicitly change it with `--listen`.  
- Do not rely on Node.js built‑in modules (e.g., `fs`, `path`) inside the Function; the code runs as WebAssembly in a WASI environment, not a full Node runtime.  

## Supported APIs and Syntax
### JavaScript / TypeScript
```javascript
import { AutoRouter } from 'itty-router';
```
- Creates an `AutoRouter` instance for declarative routing.

```javascript
let router = AutoRouter();
```
- Instantiates the router.

```javascript
router
  .get(path: string, handler: (request: Request) => Response | string | Promise<any>);
```
- Registers a GET route; the first matching route wins.

```javascript
router
  .post(path: string, handler: (request: Request) => Response | string | Promise<any>);
```
- Registers a POST route (available via itty‑router).

```javascript
addEventListener('fetch', async (event: FetchEvent) => {
  event.respondWith(router.fetch(event.request));
});
```
- Entry point for the Edge Function; forwards the incoming request to the router.

```typescript
addEventListener('fetch', async (event: FetchEvent) => { ... });
```
- Same as above, with explicit `FetchEvent` type annotation (TS).

### Rust
```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;
```
- Imports the Spin HTTP SDK types and the `http_component` attribute.

```rust
#[http_component]
fn handle_hello_spin(req: Request) -> anyhow::Result<impl IntoResponse> { ... }
```
- Declares a Spin HTTP component; receives a `Request` and returns any type that implements `IntoResponse`.

```rust
Response::builder()
    .status(u16)
    .header(&str, &str)
    .body(&str)
    .build()
```
- Builder pattern for constructing an HTTP `Response`.

### Go (TinyGo)
```go
import (
    "fmt"
    "net/http"

    spinhttp "github.com/spinframework/spin/sdk/go/v2/http"
)
```
- Imports the Spin Go SDK.

```go
func init() {
    spinhttp.Handle(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")
        fmt.Fprintln(w, "Hello Akamai!")
    })
}
```
- Registers a handler for all incoming requests via `spinhttp.Handle`.

```go
func main() {}
```
- Required `main` function; execution is driven by the SDK, not by `main`.

## Required Patterns
### JavaScript / TypeScript Router Pattern
```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

router
  .get("/", () => new Response("hello universe"))
  .get("/hello/:name", ({ name }) => `Hello, ${name}!`);

addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

### Rust HTTP Component Pattern
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

### Go (TinyGo) Handler Pattern
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
- **Unlike** a typical Node.js server, **Akamai Functions** runs your code as **WebAssembly in a WASI sandbox**, so Node built‑ins (e.g., `fs`, `process`) are unavailable.  
- **Unlike** Express or other routers, **Akamai Functions** uses **`itty-router`’s `AutoRouter`** where **route ordering matters**; the first matching route wins and any route that does not return a value is treated as middleware.  
- **Unlike** a standard Rust binary, **Akamai Functions** requires the **`#[http_component]`** attribute and the **`wasm32-wasip1`** target; omitting either prevents deployment.  
- **Unlike** a normal Go program, **Akamai Functions** requires **`CGO_ENABLED=1`** and the **TinyGo** compiler (≥ 0.27); using the standard Go compiler or forgetting the env var will cause build failures.  
- **Unlike** local development servers that default to port 80, **`spin up`** serves on **port 3000** (or a custom port via `--listen`); forgetting to change the port can cause conflicts.  

## Version and Compatibility Notes
- **Node.js**: Recommended **v22** or newer; earlier versions are not supported in the Functions runtime.  
- **Rust**: Must compile with **`wasm32-wasip1`** target; the Spin CLI automatically adds this flag during `spin build`.  
- **TinyGo**: Minimum required version **0.27**; older releases lack the necessary WASI export support.  
- **Spin CLI**: Install via the platform‑specific `install.sh` script (Linux/macOS) or manual binary (Windows). Ensure the `aka` plugin is installed/updated (`spin plugin install aka`, `spin plugins update`, `spin plugins upgrade aka`).  
- **Akamai Functions Preview**: Access requires onboarding approval and an allow‑list; the `spin aka login` flow must be completed before any `spin aka deploy` commands succeed.  