# Source: https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-mysql
Date: 2026-08-16T10:55:34.098748
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not make outbound network requests to any host not listed in `allowed_outbound_hosts` (must be prefixed with `mysql://` and include the correct port).  
- Do not import or use Node.js built‑in modules that are not part of the Spin SDK (e.g., `fs`, `net`, `http`).  
- Do not exceed the default Wasm component size limit enforced by Akamai Functions (the build process will fail if the bundle is too large).  
- Do not use JavaScript language features that require a runtime not provided by the Spin WASI environment (e.g., `worker_threads`, `process.env`).  

## Supported APIs and Syntax
- `Variables.get(name:string)` — Retrieves the value of a Spin variable (e.g., the MySQL connection string).  
- `Mysql.open(connectionString:string)` — Opens a MySQL connection; returns a connection object.  
- `connection.execute(sql:string, params:any[])` — Executes a non‑query statement (INSERT, UPDATE, DELETE); returns the number of affected rows.  
- `connection.query(sql:string, params:any[])` — Executes a SELECT statement; returns an object with a `rows` array.  
- `AutoRouter()` — Constructs an itty‑router instance for HTTP routing.  
- `router.post(path:string, handler:Function)` — Registers a POST handler.  
- `router.get(path:string, handler:Function)` — Registers a GET handler.  
- `router.put(path:string, handler:Function)` — Registers a PUT handler.  
- `router.delete(path:string, handler:Function)` — Registers a DELETE handler.  
- `router.all(path:string, handler:Function)` — Catch‑all route handler.  
- `router.fetch(request:Request, context:any)` — Dispatches an incoming request through the router.  
- `new Response(body:any, init:ResponseInit)` — Creates an HTTP response.  
- `new TextDecoder()` — Decodes `ArrayBuffer` payloads to strings.  
- `uuidv4()` — Generates a UUID v4 string (from `uuid` package).  
- `uuidValidate(id:string)` — Returns `true` if the string is a valid UUID (from `uuid` package).  

## Required Patterns
### 1. Spin entry point with variable injection
```typescript
addEventListener('fetch', async (event: FetchEvent) => {
  const connectionString = Variables.get("mysql_connection_string");
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

### 2. Router definition passing the connection string
```typescript
const router = AutoRouter();

router
  .post("/products", async (req, { connectionString }) =>
    createProduct(await req.arrayBuffer(), connectionString))
  .get("/products", async (_, { connectionString }) =>
    readAllProducts(connectionString))
  .get("/products/:id", async ({ params }, { connectionString }) =>
    readProductById(params.id, connectionString))
  .put("/products/:id", async (req, { connectionString }) =>
    updateProductById(req.params.id, await req.arrayBuffer(), connectionString))
  .delete("/products/:id", async ({ params }, { connectionString }) =>
    deleteProductById(params.id, connectionString))
  .all("*", () => notFound("Endpoint not found"));
```

### 3. CRUD handler skeleton (create example)
```typescript
function createProduct(body: ArrayBuffer, connStr: string) {
  const payload = JSON.parse(decoder.decode(body));
  if (!payload || !payload.name || typeof payload.price !== "number") {
    return badRequest("Invalid payload received. Expecting {\"name\":\"...\", \"price\":9.99}");
  }

  const product = { id: uuidv4(), name: payload.name, price: payload.price };
  const conn = Mysql.open(connStr);
  conn.execute(SQL_CREATE, [product.id, product.name, product.price]);

  const headers = { "Location": `/products/${product.id}`, "content-type": "application/json" };
  return new Response(JSON.stringify(product), { status: 201, headers });
}
```

### 4. Helper responses
```typescript
function badRequest(msg: string) {
  return new Response(JSON.stringify({ message: msg }), {
    status: 400,
    headers: { "content-type": "application/json" }
  });
}
function notFound(msg: string) {
  return new Response(JSON.stringify({ message: msg }), {
    status: 404,
    headers: { "content-type": "application/json" }
  });
}
```

## Common Mistakes and Gotchas
- **Unlike standard Node.js**, Akamai Functions does **not** allow arbitrary outbound network traffic; you must list the MySQL host in `allowed_outbound_hosts` with the `mysql://` scheme and correct port.  
- **Unlike a typical Express app**, you cannot read environment variables directly; you must expose them as Spin variables and retrieve them via `Variables.get`.  
- **Unlike browser JavaScript**, the global `process` object is unavailable; use the Spin SDK and standard Web APIs only.  
- **Unlike a regular MySQL client**, the `Mysql.open` call returns a lightweight connection object that **must not** be cached across requests; open a new connection inside each handler.  
- **Unlike typical REST services**, returning a `204` response must have `null` as the body (no JSON).  

## Version and Compatibility Notes
- The tutorial targets the **public preview** of Akamai Functions; features such as `allowed_outbound_hosts` and the `@spinframework/spin-mysql` package are only available in this preview.  
- The `http-ts` (TypeScript) template is required; using a JavaScript‑only template may miss type definitions for the Spin SDK.  
- The `spin aka deploy` command requires all MySQL connection details to be passed via `--variable` flags; omitting any will cause deployment‑time validation errors.  