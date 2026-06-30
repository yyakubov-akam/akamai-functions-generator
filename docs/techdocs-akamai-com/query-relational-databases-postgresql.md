# Source: https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-postgresql
Date: 2026-06-30T09:39:39.256067
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not import or require any modules other than `@spinframework/spin-postgres`, `@spinframework/spin-variables`, `itty-router`, and `uuid` (including its `v4` and `validate` exports).  
- Do not perform asynchronous database calls; the Spin PostgreSQL API (`Postgres.open`, `connection.execute`, `connection.query`) is **synchronous**.  
- Do not omit the `allowed_outbound_hosts` entry for the PostgreSQL endpoint; it must be a string that starts with `postgres://` and includes the default port `5432`.  
- Do not read environment variables directly; use `Variables.get("<variable_name>")` for configuration values defined in `spin.toml`.  
- Do not exceed the default Wasm component size limits imposed by Akamai Functions (the tutorial’s build produces a ~22 KB JavaScript bundle; stay well under the platform’s maximum).  
- Do not use Node‑specific globals such as `process`, `require`, or `__dirname`.  

## Supported APIs and Syntax
```
Variables.get(variableName)                     // Retrieve a Spin variable value
Postgres.open(connectionString)                 // Open a synchronous PostgreSQL connection
connection.execute(sql, paramsArray)            // Execute a statement, returns number of affected rows
connection.query(sql, paramsArray)              // Execute a SELECT, returns { rows: [...] }
AutoRouter()                                    // Create an itty‑router instance
router.post(path, handler)                      // Register POST handler
router.get(path, handler)                       // Register GET handler
router.put(path, handler)                       // Register PUT handler
router.delete(path, handler)                    // Register DELETE handler
router.all(path, handler)                       // Register catch‑all handler
router.fetch(request, context)                 // Dispatch request through router
new Response(body, {status, headers})            // Create HTTP response
uuidv4()                                         // Generate a UUID v4 string
uuidValidate(uuidString)                         // Validate UUID format
new TextDecoder()                               // Decode Uint8Array to string
```

## Required Patterns
### 1. Spin Manifest Variable Wiring
```toml
[variables]
pg_connection_string = { required = true }

[component.hello-postgresql]
source = "target/hello-postgresql.wasm"
allowed_outbound_hosts = [
  "postgres://<host>:5432",
]
[component.hello-postgresql.variables]
pg_connection_string = "{{ pg_connection_string }}"
```

### 2. Event Listener Boilerplate
```js
addEventListener('fetch', async (event) => {
  const connectionString = Variables.get("pg_connection_string");
  if (!connectionString) {
    event.respondWith(new Response(
      JSON.stringify({ message: "Connection String not specified" }),
      { status: 500, headers: { "content-type": "application/json" } }
    ));
    return;
  }
  event.respondWith(router.fetch(event.request, { connectionString }));
});
```

### 3. CRUD Handler Skeletons
#### Create
```js
function createProduct(requestBody, connectionString) {
  const payload = JSON.parse(decoder.decode(requestBody));
  if (!payload || !payload.name || typeof payload.price !== "number") {
    return badRequest("Invalid payload …");
  }
  const newProduct = { id: uuidv4(), name: payload.name, price: payload.price };
  const conn = Postgres.open(connectionString);
  conn.execute(SQL_CREATE, [newProduct.id, newProduct.name, newProduct.price]);
  const headers = { Location: `/products/${newProduct.id}`, "content-type": "application/json" };
  return new Response(JSON.stringify(newProduct), { status: 201, headers });
}
```

#### Read All
```js
function readAllProducts(connectionString) {
  const conn = Postgres.open(connectionString);
  const result = conn.query(SQL_READ_ALL, []);
  const items = result.rows.map(r => ({ id: r.id, name: r.name, price: r.price }));
  return new Response(JSON.stringify(items), { status: 200, headers: DEFAULT_HEADERS });
}
```

#### Read By ID
```js
function readProductById(id, connectionString) {
  if (!uuidValidate(id)) return badRequest("Invalid identifier …");
  const conn = Postgres.open(connectionString);
  const result = conn.query(SQL_READ_BY_ID, [id]);
  if (result.rows.length === 0) return notFound("Product not found");
  const prod = { id: result.rows[0].id, name: result.rows[0].name, price: result.rows[0].price };
  return new Response(JSON.stringify(prod), { status: 200, headers: DEFAULT_HEADERS });
}
```

#### Update
```js
function updateProductById(id, requestBody, connectionString) {
  if (!uuidValidate(id)) return badRequest("Invalid identifier …");
  const payload = JSON.parse(decoder.decode(requestBody));
  if (!payload || !payload.name || typeof payload.price !== "number") {
    return badRequest("Invalid payload …");
  }
  const conn = Postgres.open(connectionString);
  const affected = conn.execute(SQL_UPDATE_BY_ID, [payload.name, payload.price, id]);
  if (affected === 0) return notFound("Product not found");
  const headers = { Location: `/items/${id}`, "content-type": "application/json" };
  return new Response(JSON.stringify({ id, name: payload.name, price: payload.price }), { status: 200, headers });
}
```

#### Delete
```js
function deleteProductById(id, connectionString) {
  if (!uuidValidate(id)) return badRequest("Invalid identifier …");
  const conn = Postgres.open(connectionString);
  const affected = conn.execute(SQL_DELETE_BY_ID, [id]);
  if (affected === 0) return notFound("Product not found");
  return new Response(null, { status: 204 });
}
```

### 4. Router Wiring
```js
router
  .post("/products", async (req, ctx) => createProduct(await req.arrayBuffer(), ctx.connectionString))
  .get("/products", (_, ctx) => readAllProducts(ctx.connectionString))
  .get("/products/:id", ({params}, ctx) => readProductById(params.id, ctx.connectionString))
  .put("/products/:id", async (req, ctx) => updateProductById(ctx.params.id, await req.arrayBuffer(), ctx.connectionString))
  .delete("/products/:id", ({params}, ctx) => deleteProductById(params.id, ctx.connectionString))
  .all("*", () => notFound("Endpoint not found"));
```

## Common Mistakes and Gotchas
- **Unlike standard Node.js**, `Postgres.open(...).execute(...)` and `.query(...)` are **synchronous**; do **not** `await` them.  
- **Unlike typical serverless environments**, you cannot read environment variables directly; you must expose them via `spin.toml` and retrieve with `Variables.get`.  
- **Unlike generic HTTP servers**, outbound network access is blocked unless the host is listed in `allowed_outbound_hosts` with the exact `postgres://` scheme and port `5432`.  
- **Unlike browsers**, the `fetch` event listener receives a `connectionString` via the router context, not via global scope.  

## Version and Compatibility Notes
- The tutorial assumes Spin CLI version that supports the `http-js` template and the `@spinframework/spin-postgres`/`spin-variables` packages (compatible with Spin 5.x and later).  
- No feature flags are required; ensure the `spin` binary and the `aka` plugin are up‑to‑date to avoid mismatched WASM/WIT versions.  