# Source: https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-postgresql
Date: 2026-08-17T08:45:08.362191
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Entry point must be `addEventListener('fetch', ...)` to handle incoming requests
- Outbound network requests to PostgreSQL require explicit configuration in `spin.toml` under `[component.<component_name>]`
- Outbound connectivity protocol must be `postgres://` and port must be `5432`
- Environment variables defined in `spin.toml` must be accessed via `Variables.get("key")`

## Supported APIs and Syntax

- `Variables.get(key)` — Retrieves the value of a variable defined in the application manifest
- `Postgres.open(connectionString)` — Opens a connection to a PostgreSQL database
- `connection.execute(sql, params)` — Executes an SQL statement (INSERT, UPDATE, DELETE) and returns the number of affected rows
- `connection.query(sql, params)` — Executes a SELECT query and returns a result object with a `rows` array
- `AutoRouter()` — Creates an instance of the itty-router for defining HTTP routes
- `addEventListener('fetch', handler)` — Registers the main event listener for handling HTTP requests
- `uuid.v4()` — Generates a random UUID v4 string
- `uuid.validate(id)` — Validates if a string is a valid UUID
- `new Response(body, options)` — Constructs an HTTP response object

## Required Patterns

### Router Setup Pattern
```javascript
import * as Variables from "@spinframework/spin-variables";
import * as Postgres from "@spinframework/spin-postgres";
import { AutoRouter } from "itty-router";
import { v4 as uuidv4 } from 'uuid';
import { validate as uuidValidate } from 'uuid';

const router = AutoRouter();
const decoder = new TextDecoder();
const DEFAULT_HEADERS = { "content-type": "application/json" };

// Define routes
router
    .post("/products", async (request, { connectionString }) => createProduct(await request.arrayBuffer(), connectionString))
    .get("/products", async (_, { connectionString }) => readAllProducts(connectionString))
    .get("/products/:id", async ({ params }, { connectionString }) => readProductById(params.id, connectionString))
    .put("/products/:id", async (request, { connectionString }) => updateProductById(request.params.id, await request.arrayBuffer(), connectionString))
    .delete("/products/:id", async ({ params }, { connectionString }) => deleteProductById(params.id, connectionString))
    .all("*", () => notFound("Endpoint not found"));

// Entry point
addEventListener('fetch', async (event) => {
    const connectionString = Variables.get("pg_connection_string");
    if (!connectionString) {
        return event.respondWith(new Response(JSON.stringify({ message: "Connection String not specified" }), { status: 500, headers: DEFAULT_HEADERS }));
    }
    event.respondWith(router.fetch(event.request, { connectionString }));
});
```

### Database Connection Pattern
```javascript
// Open connection
const connection = Postgres.open(connectionString);

// Execute query
const result = connection.query(SQL_READ_ALL, []);

// Iterate rows
const items = result.rows.map(row => ({
    id: row["id"],
    name: row["name"],
    price: row["price"]
}));
```

### HTTP Response Pattern
```javascript
// Success response
return new Response(JSON.stringify(data), { 
    status: 200, 
    headers: DEFAULT_HEADERS 
});

// Error response helper
function badRequest(message) {
    return new Response(JSON.stringify({ message }), { status: 400, headers: DEFAULT_HEADERS });
}
```

## Common Mistakes and Gotchas

- Unlike standard Node.js where `require('pg')` is used directly, Akamai Functions requires using `@spinframework/spin-postgres` and opening connections via `Postgres.open(connectionString)`.
- Unlike standard Node.js where environment variables are accessed via `process.env.VAR_NAME`, Akamai Functions requires using `Variables.get("VAR_NAME")`.
- Unlike standard browser fetch APIs, Akamai Functions requires explicit `allowed_outbound_hosts` configuration in `spin.toml` to allow network requests to the database.
- The `connection.execute` method returns the number of affected rows (integer), not a result object like `query`.
- The `decoder.decode(requestBody)` is required to convert the `ArrayBuffer` request body into a string for JSON parsing.

## Version and Compatibility Notes

- Requires the `@spinframework/spin-postgres` and `@spinframework/spin-variables` npm packages.
- Requires the `http-js` Spin application template.
- Configuration is managed via `spin.toml` using the `[variables]` and `[component.<name>]` sections.
- Deployment is performed using the `spin aka deploy` command.