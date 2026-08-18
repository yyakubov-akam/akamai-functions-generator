# Source: https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-mysql
Date: 2026-08-17T09:16:18.693411
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Outbound network requests to MySQL must specify the protocol as `mysql://` in the `allowed_outbound_hosts` configuration.
- Public preview access is required to use Akamai Functions.
- Node.js version 21 or higher is recommended for TypeScript development.

## Supported APIs and Syntax

- `Mysql.open(connectionString: string)` — Opens a MySQL connection using the provided connection string.
- `connection.execute(sql: string, params: any[])` — Executes a non-query SQL statement (INSERT, UPDATE, DELETE); returns the number of affected rows.
- `connection.query(sql: string, params: any[])` — Executes a query SQL statement (SELECT); returns an object containing a `.rows` property.
- `connection.rows` — Array of rows returned by a query.
- `Variables.get(key: string)` — Retrieves a variable value defined in `spin.toml` or environment variables.
- `AutoRouter` — Router for handling HTTP requests.
- `addEventListener('fetch', ...)` — Entry point for the Wasm component.
- `uuidv4()` — Generates a v4 UUID.
- `uuidValidate(id: string)` — Validates if a string is a valid UUID.

## Required Patterns

### Configuration Pattern (spin.toml)
Define variables and explicitly allow outbound MySQL traffic.

```toml
[variables]
mysql_host = { required = true }
mysql_user = { required = true }
mysql_password = { required = true, secret = true }
mysql_port = { required = true }
mysql_database = { required = true }

[component.linode-mysql]
source = "dist/linode-mysql.wasm"
exclude_files = ["**/node_modules"]
allowed_outbound_hosts = ["mysql://{{ mysql_host }}:{{ mysql_port }}"]
```

### Router and Entry Point Pattern
Use `AutoRouter` to handle requests and pass the connection string as context. Retrieve the connection string using `Variables.get()` inside the event listener.

```typescript
import * as Variables from "@spinframework/spin-variables";
import * as Mysql from "@spinframework/spin-mysql";
import { AutoRouter } from "itty-router";

const router = AutoRouter();
const decoder = new TextDecoder();

// Define routes
router
    .post("/products", async (request, { connectionString }) => createProduct(await request.arrayBuffer(), connectionString))
    .get("/products", async (_, { connectionString }) => readAllProducts(connectionString))
    .all("*", () => notFound("Endpoint not found"));

// Entry point
addEventListener('fetch', async (event: FetchEvent) => {
    const connectionString = Variables.get("mysql_connection_string");
    if (!connectionString) {
        event.respondWith(new Response(JSON.stringify({ message: "Connection String not specified" }), { status: 500 }));
    }
    event.respondWith(router.fetch(event.request, { connectionString }));
});
```

### CRUD Handler Pattern
Open connection, execute SQL, handle result, and return HTTP response.

```typescript
function readAllProducts(connectionString: string) {
  const connection = Mysql.open(connectionString);
  let result = connection.query("SELECT Id, Name, Price from Products ORDER BY Name", []);
  
  let items = result.rows.map(row => ({
    id: row["Id"],
    name: row["Name"],
    price: +row["Price"]!.toString()
  }));

  return new Response(JSON.stringify(items), { status: 200, headers: { "content-type": "application/json" } });
}
```

## Common Mistakes and Gotchas

- Unlike standard Node.js, Akamai Functions requires the `mysql://` protocol to be explicitly included in the `allowed_outbound_hosts` array in `spin.toml`.
- Unlike standard Node.js environment variables, local development variables must be prefixed with `SPIN_VARIABLE_` (e.g., `SPIN_VARIABLE_MYSQL_HOST`).
- The `connection.execute` method returns the number of affected rows, not a result object.
- The `connection.query` method returns an object with a `.rows` property containing the result array.
- The `Variables.get` function must be called inside the `addEventListener` scope to access runtime variables.

## Version and Compatibility Notes

- Public preview status.
- Requires Linode Managed Databases for the MySQL backend.
- Requires the `@spinframework/spin-mysql` and `@spinframework/spin-variables` packages.