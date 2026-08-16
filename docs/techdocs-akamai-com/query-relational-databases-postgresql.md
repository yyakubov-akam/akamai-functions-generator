# Source: https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-postgresql
Date: 2026-08-16T09:25:28.215969
Model: gpt-oss:120b-cloud
## Runtime Constraints
- **Do not omit** the `allowed_outbound_hosts` entry for the PostgreSQL endpoint in `spin.toml`; without it the Wasm component cannot make network requests.  
- **Do not use** any database driver other than `@spinframework/spin-postgres`. All other Node.js PostgreSQL libraries are unavailable in the Akamai Functions runtime.  
- **Do not exceed** the default Wasm component size limits imposed by the Spin build process (the generated `hello‑postgresql.wasm` must fit within the bundle produced by `webpack --mode=production`).  
- **Do not perform** blocking I/O; all database interactions must go through the non‑blocking Spin SDK (`Postgres.open`, `connection.execute`, `connection.query`).  
- **Do not reference** environment variables directly; only variables declared in `spin.toml` and accessed via `Variables.get` are available at runtime.  
- **Do not use** any Node.js core modules that are not part of the Spin JavaScript SDK (e.g., `fs`, `net`, `http`).  

## Supported APIs and Syntax
```
Variables.get(name)                     — Retrieves a string variable defined in spin.toml.
Postgres.open(connectionString)          — Opens a PostgreSQL connection; returns a connection object.
connection.execute(sql, params[])        — Executes a statement that does not return rows; returns number of affected rows.
connection.query(sql, params[])          — Executes a SELECT; returns an object with a .rows array.
AutoRouter()                             — Creates an itty‑router instance for HTTP routing.
router.post(path, handler)              — Registers a POST handler.
router.get(path, handler)               — Registers a GET handler.
router.put(path, handler)               — Registers a PUT handler.
router.delete(path, handler)            — Registers a DELETE handler.
router.all(path, handler)                — Registers a catch‑all handler.
router.fetch(request, context)          — Dispatches a Request through the router; `context` is passed to handlers.
new Response(body, init)                — Constructs an HTTP response.
new TextDecoder()                        — Decodes Uint8Array to string (UTF‑8).
uuidv4()                                 — Generates a RFC‑4122 v4 UUID (`import { v4 as uuidv4 } from 'uuid'`).
uuidValidate(uuid)                       — Returns true if the string is a valid UUID (`import { validate as uuidValidate } from 'uuid'`).
addEventListener('fetch', listener)     — Entry point for Akamai Functions; `listener` receives a FetchEvent.
```

## Required Patterns
### 1. Application Manifest Variables & Outbound Hosts
```toml
[variables]
pg_connection_string = { required = true }

[component.hello-postgresql]
source = "target/hello-postgresql.wasm"
allowed_outbound_hosts = [
  "postgres://<HOST>:5432"
]
```

### 2. Router & Event Listener Boilerplate
```js
import * as Variables from "@spinframework/spin-variables";
import * as Postgres from "@spinframework/spin-postgres";
import { AutoRouter } from "itty-router";
import { v4 as uuidv4 } from "uuid";
import { validate as uuidValidate } from "uuid";

const router = AutoRouter();
const decoder = new TextDecoder();
const DEFAULT_HEADERS = { "content-type": "application/json" };

function badRequest(msg) {
  return new Response(JSON.stringify({ message: msg }), {
    status: 400,
    headers: DEFAULT_HEADERS,
  });
}
function notFound(msg) {
  return new Response(JSON.stringify({ message: msg }), {
    status: 404,
    headers: DEFAULT_HEADERS,
  });
}

/* ==== CRUD route registration ==== */
router
  .post("/products", async (req, { connectionString }) =>
    createProduct(await req.arrayBuffer(), connectionString)
  )
  .get("/products", async (_, { connectionString }) =>
    readAllProducts(connectionString)
  )
  .get("/products/:id", async ({ params }, { connectionString }) =>
    readProductById(params.id, connectionString)
  )
  .put("/products/:id", async (req, { connectionString }) =>
    updateProductById(req.params.id, await req.arrayBuffer(), connectionString)
  )
  .delete("/products/:id", async ({ params }, { connectionString }) =>
    deleteProductById(params.id, connectionString)
  )
  .all("*", () => notFound("Endpoint not found"));

addEventListener("fetch", async (event) => {
  const connectionString = Variables.get("pg_connection_string");
  if (!connectionString) {
    event.respondWith(
      new Response(
        JSON.stringify({ message: "Connection String not specified" }),
        { status: 500, headers: DEFAULT_HEADERS }
      )
    );
    return;
  }
  event.respondWith(router.fetch(event.request, { connectionString }));
});
```

### 3. Create Handler Pattern
```js
function createProduct(requestBody, connectionString) {
  const payload = JSON.parse(decoder.decode(requestBody));
  if (!payload || !payload.name || typeof payload.price !== "number") {
    return badRequest(
      'Invalid payload received. Expecting {"name":"some name", "price": 9.99}'
    );
  }

  const newProduct = {
    id: uuidv4(),
    name: payload.name,
    price: payload.price,
  };

  const conn = Postgres.open(connectionString);
  conn.execute(SQL_CREATE, [newProduct.id, newProduct.name, newProduct.price]);

  const customHeaders = {
    Location: `/products/${newProduct.id}`,
    ...DEFAULT_HEADERS,
  };
  return new Response(JSON.stringify(newProduct), {
    status: 201,
    headers: customHeaders,
  });
}
```

### 4. Read‑All Handler Pattern
```js
function readAllProducts(connectionString) {
  const conn = Postgres.open(connectionString);
  const result = conn.query(SQL_READ_ALL, []);
  const items = result.rows.map((row) => ({
    id: row["id"],
    name: row["name"],
    price: row["price"],
  }));
  return new Response(JSON.stringify(items), {
    status: 200,
    headers: DEFAULT_HEADERS,
  });
}
```

### 5. Read‑By‑Id Handler Pattern (with UUID validation)
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
    headers: DEFAULT_HEADERS,
  });
}
```

### 6. Update Handler Pattern
```js
function updateProductById(id, requestBody, connectionString) {
  if (!uuidValidate(id)) return badRequest("Invalid identifier received via URL");

  const payload = JSON.parse(decoder.decode(requestBody));
  if (!payload || !payload.name || typeof payload.price !== "number") {
    return badRequest(
      'Invalid payload received. Expecting {"name":"some name", "price": 9.99}'
    );
  }

  const conn = Postgres.open(connectionString);
  const affected = conn.execute(SQL_UPDATE_BY_ID, [
    payload.name,
    payload.price,
    id,
  ]);
  if (affected === 0) return notFound("Product not found");

  const customHeaders = {
    Location: `/items/${id}`,
    ...DEFAULT_HEADERS,
  };
  return new Response(
    JSON.stringify({ id, name: payload.name, price: payload.price }),
    { status: 200, headers: customHeaders }
  );
}
```

### 7. Delete Handler Pattern
```js
function deleteProductById(id, connectionString) {
  if (!uuidValidate(id)) return badRequest("Invalid identifier received via URL");

  const conn = Postgres.open(connectionString);
  const affected = conn.execute(SQL_DELETE_BY_ID, [id]);
  if (affected === 0) return notFound("Product not found");

  return new Response(null, { status: 204 });
}
```

## Common Mistakes and Gotchas
- **Unlike** a typical Node.js environment, Akamai Functions **cannot** perform arbitrary outbound network calls; you must list the PostgreSQL host in `allowed_outbound_hosts` with the `postgres://` scheme and port `5432`.  
- **Unlike** standard server‑side JavaScript, the Spin runtime **does not** expose `process.env`; configuration must be passed via Spin variables and accessed with `Variables.get`.  
- **Unlike** many PostgreSQL client libraries, `connection.execute` **returns only the number of affected rows**, not a result set. Treat the return value as a row‑count for UPDATE/DELETE checks.  
- **Unlike** a regular Express app, the request body is accessed as an `ArrayBuffer`; you must decode it with `new TextDecoder().decode(...)` before `JSON.parse`.  
- **Unlike** typical HTTP frameworks, the router’s `fetch` method receives a **context object** (`{ connectionString }`) that you must forward to each handler; forgetting to pass it will cause `connectionString` to be `undefined`.  

## Version and Compatibility Notes
- Requires **Spin CLI** with the `akamai-functions` executor (`spin new -E akamai-functions`).  
- Uses **Spin SDK for JavaScript** packages: `@spinframework/spin-postgres`, `@spinframework/spin-variables`. Ensure the versions installed match the template (current tutorial uses the latest at time of writing).  
- The `http-js` template bundles **itty‑router**; no additional routing library is needed.  
- Deployment must be performed with `spin aka deploy` and the PostgreSQL connection string supplied via `--variable pg_connection_string="..."`.  
- The generated Wasm component must be built with `spin build` (which runs `webpack` and `j2w`). No manual changes to the build pipeline are required.  