# Source: https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-postgresql
Date: 2026-06-05T09:04:13.349326
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not make outbound network requests to hosts not listed in `allowed_outbound_hosts` (must include the full `postgres://…:5432` URL).  
- Do not omit the required application variable `pg_connection_string`; the function must abort with HTTP 500 if it is missing.  
- Do not use any database driver other than the Spin‑provided `@spinframework/spin-postgres` API (`Postgres.open`, `execute`, `query`).  
- Do not exceed the default Wasm component size limits imposed by Spin (keep the bundle under ~5 MiB; the tutorial build produces a ~22 KiB `dist.js`).  
- Do not use Node‑only globals (e.g., `process`, `require`) – only the browser‑compatible globals available in the Spin runtime (`Response`, `TextDecoder`, `addEventListener`).  
- Do not use unsupported ES modules syntax such as dynamic `import()` at runtime; all imports must be static at the top of the file.  

## Supported APIs and Syntax
- `Variables.get(variableName)` — Retrieves the value of a Spin variable (e.g., `"pg_connection_string"`).  
- `Postgres.open(connectionString)` — Opens a PostgreSQL connection; returns a connection object.  
- `connection.execute(sql, paramsArray)` — Executes a non‑query statement (INSERT/UPDATE/DELETE); returns the number of affected rows.  
- `connection.query(sql, paramsArray)` — Executes a SELECT statement; returns an object with a `rows` array.  
- `uuidv4()` — Generates a random UUID v4 (from `uuid` package).  
- `uuidValidate(uuidString)` — Returns `true` if the string is a valid UUID (from `uuid` package).  
- `AutoRouter()` — Creates an itty‑router instance for HTTP routing.  
- `router.post(path, handler)`, `router.get(path, handler)`, `router.put(path, handler)`, `router.delete(path, handler)`, `router.all(path, handler)` — Register route handlers.  
- `router.fetch(request, context)` — Dispatches a request through the router; `context` can carry extra data (e.g., `{ connectionString }`).  
- `new Response(body, init)` — Constructs an HTTP response; `init` may contain `status`, `headers`.  
- `addEventListener('fetch', listener)` — Entry point for Spin functions; `listener` receives an event with `event.request` and `event.respondWith`.  

## Required Patterns
### 1. Variable Injection & Early Failure
```js
addEventListener('fetch', async (event) => {
  const connectionString = Variables.get("pg_connection_string");
  if (!connectionString) {
    event.respondWith(new Response(
      JSON.stringify({ message: "Connection String not specified" }),
      { status: 500, headers: DEFAULT_HEADERS }
    ));
    return;
  }
  event.respondWith(router.fetch(event.request, { connectionString }));
});
```

### 2. Router Boilerplate
```js
const router = AutoRouter();

router
  .post("/products", async (request, { connectionString }) =>
    createProduct(await request.arrayBuffer(), connectionString))
  .get("/products", async (_, { connectionString }) =>
    readAllProducts(connectionString))
  .get("/products/:id", async ({ params }, { connectionString }) =>
    readProductById(params.id, connectionString))
  .put("/products/:id", async (request, { connectionString }) =>
    updateProductById(request.params.id, await request.arrayBuffer(), connectionString))
  .delete("/products/:id", async ({ params }, { connectionString }) =>
    deleteProductById(params.id, connectionString))
  .all("*", () => notFound("Endpoint not found"));
```

### 3. Helper Responses
```js
function badRequest(message) {
  return new Response(JSON.stringify({ message }), {
    status: 400,
    headers: DEFAULT_HEADERS,
  });
}
function notFound(message) {
  return new Response(JSON.stringify({ message }), {
    status: 404,
    headers: DEFAULT_HEADERS,
  });
}
```

### 4. Database Interaction Pattern
```js
function someHandler(..., connectionString) {
  const conn = Postgres.open(connectionString);
  // For SELECT:
  const result = conn.query(SQL_STATEMENT, [param1, ...]);
  // For INSERT/UPDATE/DELETE:
  const affected = conn.execute(SQL_STATEMENT, [param1, ...]);
}
```

### 5. UUID Validation (Read/Update/Delete)
```js
if (!uuidValidate(id)) {
  return badRequest("Invalid identifier received via URL");
}
```

### 6. Location Header on Create/Update
```js
let customHeaders = { "Location": `/products/${newId}` };
Object.assign(customHeaders, DEFAULT_HEADERS);
return new Response(JSON.stringify(payload), { status: 201, headers: customHeaders });
```

## Common Mistakes and Gotchas
- Unlike a regular Node.js server, Akamai Functions **require** the PostgreSQL host to be listed in `allowed_outbound_hosts`; otherwise outbound connections are blocked.  
- Unlike typical environment variable handling, Spin variables are accessed via `Variables.get` and must be prefixed with `SPIN_VARIABLE_` when set on the command line.  
- Unlike a standard Express app, the request body must be read with `await request.arrayBuffer()` and decoded manually (`new TextDecoder().decode`).  
- Unlike generic JavaScript, the Spin runtime **does not** provide `require`; all modules must be imported with ES module `import` statements.  
- Unlike a full Node.js runtime, the only way to send a response is to call `event.respondWith(...)` inside the `fetch` listener.  

## Version and Compatibility Notes
- Requires Spin CLI **public preview** (access via onboarding form).  
- Application template must be `http-js` (Spin JavaScript HTTP template).  
- Dependencies: `@spinframework/spin-postgres`, `@spinframework/spin-variables`, `uuid`, `itty-router`. Ensure they are listed in `package.json` and installed with `npm install`.  
- Build with `spin build` (uses webpack 5.97.1 and `j2w` to generate the Wasm component).  
- Deploy with `spin aka deploy --variable pg_connection_string="..."`.  
- The `allowed_outbound_hosts` entry must use the exact protocol `postgres://` and port `5432`.  