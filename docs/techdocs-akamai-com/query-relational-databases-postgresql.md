# Source: https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-postgresql
Date: 2026-07-22T11:13:21.722746
Model: gpt-oss:120b-cloud
## Runtime Constraints
- **Do not** make outbound network requests to hosts that are not listed in `allowed_outbound_hosts` in `spin.toml`.  
- **Do not** omit the `postgres://` protocol or the default PostgreSQL port (`5432`) when specifying an allowed outbound host.  
- **Do not** use any database driver other than the Spin‑provided `@spinframework/spin-postgres` API.  
- **Do not** perform asynchronous I/O with the PostgreSQL connection; `Postgres.open(...).execute(...)` and `.query(...)` are synchronous and must be used as such.  
- **Do not** rely on Node‑specific globals (e.g., `process`, `require`, `fs`, `net`). Only the Spin SDK and standard Web APIs are available.  
- **Do not** exceed the default Wasm component size limit enforced by Akamai Functions (≈10 MiB). Keep dependencies to the ones listed in the tutorial.  

---

## Supported APIs and Syntax
```
Variables.get(name)                     // Retrieve a Spin variable (string)
Postgres.open(connectionString)         // Open a PostgreSQL connection, returns a connection object
connection.execute(sql, paramsArray)    // Execute a statement, returns number of affected rows (int)
connection.query(sql, paramsArray)      // Execute a SELECT, returns { rows: Array<object> }
AutoRouter()                            // Create an itty‑router instance
router.post(path, handler)              // Register POST handler
router.get(path, handler)               // Register GET handler
router.put(path, handler)               // Register PUT handler
router.delete(path, handler)            // Register DELETE handler
router.all(path, handler)               // Register catch‑all handler
router.fetch(request, context)          // Dispatch request through router, `context` can hold extra data
addEventListener('fetch', listener)     // Spin entry point for HTTP requests
new Response(body, init)                // Create an HTTP response
JSON.stringify(value)                  // Serialize to JSON
JSON.parse(text)                        // Parse JSON
new TextDecoder()                       // Decode Uint8Array to string
uuidv4()                                // Generate a UUID v4 (from `uuid` package)
uuidValidate(uuidString)                // Validate UUID format (from `uuid` package)
```

---

## Required Patterns  

### 1. Spin manifest variables & outbound host
```toml
[variables]
pg_connection_string = { required = true }

[component.hello-postgresql]
source = "target/hello-postgresql.wasm"
allowed_outbound_hosts = [
  "postgres://<your-neon-endpoint>:5432",
]
```

### 2. Fetch entry point with variable injection
```js
addEventListener('fetch', async (event) => {
  const connectionString = Variables.get("pg_connection_string");
  if (!connectionString) {
    return event.respondWith(
      new Response(JSON.stringify({ message: "Connection String not specified" }),
      { status: 500, headers: { "content-type": "application/json" } })
    );
  }
  event.respondWith(router.fetch(event.request, { connectionString }));
});
```

### 3. Helper responses
```js
function badRequest(message) {
  return new Response(JSON.stringify({ message }), {
    status: 400,
    headers: { "content-type": "application/json" },
  });
}
function notFound(message) {
  return new Response(JSON.stringify({ message }), {
    status: 404,
    headers: { "content-type": "application/json" },
  });
}
```

### 4. Create handler (POST /products)
```js
function createProduct(requestBody, connectionString) {
  const payload = JSON.parse(decoder.decode(requestBody));
  if (!payload || !payload.name || typeof payload.price !== "number") {
    return badRequest('Invalid payload received. Expecting {"name":"some name", "price": 9.99}');
  }

  const newProduct = { id: uuidv4(), name: payload.name, price: payload.price };
  const conn = Postgres.open(connectionString);
  conn.execute(SQL_CREATE, [newProduct.id, newProduct.name, newProduct.price]);

  const headers = { "Location": `/products/${newProduct.id}`, "content-type": "application/json" };
  return new Response(JSON.stringify(newProduct), { status: 201, headers });
}
```

### 5. Read‑all handler (GET /products)
```js
function readAllProducts(connectionString) {
  const conn = Postgres.open(connectionString);
  const result = conn.query(SQL_READ_ALL, []);
  const items = result.rows.map(r => ({
    id: r["id"],
    name: r["name"],
    price: r["price"],
  }));
  return new Response(JSON.stringify(items), {
    status: 200,
    headers: { "content-type": "application/json" },
  });
}
```

### 6. Read‑by‑id handler (GET /products/:id)
```js
function readProductById(id, connectionString) {
  if (!uuidValidate(id)) return badRequest("Invalid identifier received via URL");
  const conn = Postgres.open(connectionString);
  const result = conn.query(SQL_READ_BY_ID, [id]);
  if (result.rows.length === 0) return notFound("Product not found");

  const product = {
    id: result.rows[0]["id"],
    name: result.rows[0]["name"],
    price: result.rows[0]["price"],
  };
  return new Response(JSON.stringify(product), {
    status: 200,
    headers: { "content-type": "application/json" },
  });
}
```

### 7. Update handler (PUT /products/:id)
```js
function updateProductById(id, requestBody, connectionString) {
  if (!uuidValidate(id)) return badRequest("Invalid identifier received via URL");
  const payload = JSON.parse(decoder.decode(requestBody));
  if (!payload || !payload.name || typeof payload.price !== "number") {
    return badRequest('Invalid payload received. Expecting {"name":"some name", "price": 9.99}');
  }

  const conn = Postgres.open(connectionString);
  const affected = conn.execute(SQL_UPDATE_BY_ID, [payload.name, payload.price, id]);
  if (affected === 0) return notFound("Product not found");

  const headers = { "Location": `/items/${id}`, "content-type": "application/json" };
  return new Response(JSON.stringify({ id, name: payload.name, price: payload.price }), {
    status: 200,
    headers,
  });
}
```

### 8. Delete handler (DELETE /products/:id)
```js
function deleteProductById(id, connectionString) {
  if (!uuidValidate(id)) return badRequest("Invalid identifier received via URL");
  const conn = Postgres.open(connectionString);
  const deleted = conn.execute(SQL_DELETE_BY_ID, [id]);
  if (deleted === 0) return notFound("Product not found");
  return new Response(null, { status: 204 });
}
```

### 9. Router wiring
```js
router
  .post("/products", async (req, ctx) => createProduct(await req.arrayBuffer(), ctx.connectionString))
  .get("/products", (_, ctx) => readAllProducts(ctx.connectionString))
  .get("/products/:id", ({ params }, ctx) => readProductById(params.id, ctx.connectionString))
  .put("/products/:id", async (req, ctx) => updateProductById(ctx.params.id, await req.arrayBuffer(), ctx.connectionString))
  .delete("/products/:id", ({ params }, ctx) => deleteProductById(params.id, ctx.connectionString))
  .all("*", () => notFound("Endpoint not found"));
```

---

## Common Mistakes and Gotchas
- **Unlike** standard Node.js `pg` clients, **Akamai Functions** `Postgres.open(...).execute(...)` **is synchronous** and returns the number of rows affected, not a Promise.  
- **Unlike** typical HTTP frameworks, **Akamai Functions** requires the **connection string to be passed via `router.fetch(..., { connectionString })`**; the handler does **not** have automatic access to environment variables.  
- **Unlike** generic outbound networking, **Akamai Functions** will **block any request** to a host not listed in `allowed_outbound_hosts`.  
- **Unlike** browsers, the **global `Response`** constructor must be used with explicit `content-type` headers; omitting them results in a default `text/plain` response.  
- **Unlike** many ORMs, **Spin’s PostgreSQL API** does **not** perform automatic parameter sanitization beyond positional `$1, $2…` placeholders; you must supply the exact parameter array.  
- **Unlike** typical serverless platforms, **Akamai Functions** does **not** support dynamic imports or `fs`‑based file reads; all code must be bundled into the Wasm component before deployment.  

---

## Version and Compatibility Notes
- Requires **Spin CLI** version that supports `-E akamai-functions` and the `http-js` template (Spin ≥ 1.0).  
- Must install the exact SDK packages: `@spinframework/spin-postgres`, `@spinframework/spin-variables`, and `itty-router` (any newer major version may introduce breaking API changes).  
- The `uuid` package must be version‑compatible with the ES‑module import style used (`import { v4 as uuidv4, validate as uuidValidate } from 'uuid'`).  
- The Wasm component must be built with `spin build` (Webpack 5.97.1 used in the tutorial).  
- Deployment uses `spin aka deploy` with `--variable pg_connection_string="..."`; the variable name **must** match the one declared in `spin.toml`.  