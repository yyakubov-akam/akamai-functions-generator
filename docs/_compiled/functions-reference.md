# Akamai Functions — Unified Coding Reference

> Master reference for generating Akamai Functions code (Spin applications compiled to WebAssembly).
> Compiled from every Markdown source in `/docs/techdocs-akamai-com/` on 2026-08-17.

## 1. Runtime Prohibitions

Every item in this section is a hard platform, runtime, deployment, or tooling constraint. When a source does not state the exact enforcement error, that is called out instead of inventing one.

### 1.1 Platform and runtime

- **Code that is not compiled to WebAssembly MUST NOT be deployed.** Akamai Functions executes Spin applications as WebAssembly; non-Wasm code cannot run on the platform.
- **Languages without WASI support MUST NOT be used.** A language must support at least WASI Preview 1; otherwise its output cannot run on Akamai Functions.
- **Languages without Spin SDK support are NOT documented as supported.** The documented supported languages are Rust, Go, JavaScript, and Python; unsupported language output has no supported runtime integration.
- **Deployment without the `spin aka` plugin is NOT supported.** The application cannot be deployed to Akamai Functions through the documented workflow.
- **General-availability access is NOT available.** The platform is in limited availability/public preview and requires sign-up/onboarding; users without preview access cannot deploy.
- **Runtime configuration changes are NOT supported.** Configuration changes cannot be hot-swapped at runtime; application-variable changes create a new deployment and increment the version.
- **Custom triggers are NOT supported.** Only the `http` trigger type is currently supported, so a manifest using another/custom trigger cannot run on Akamai Functions.
- **SQLite storage is NOT supported on Akamai Functions.** Do not confuse this with local KV testing, which uses `.spin/sqlite_key_value.db`; a deployed application cannot use SQLite storage as a platform capability.
- **The Redis trigger is NOT supported.** A Redis-triggered component cannot be deployed, although outbound Redis is listed as a supported API.
- **`wasi-blobstore` and `wasi-messaging` are NOT supported in Spin or Akamai Functions.** Components requiring either interface cannot run.
- **Serverless AI is NOT generally available.** It is available only under Limited Access; code must not assume access.

### 1.2 Execution and storage quotas

- **NEVER exceed 128 MiB of memory per function execution.** The source defines 128 MiB as the hard memory limit; it does not state the exact termination/error text.
- **NEVER exceed 50 MiB of total application size.** The application exceeds the platform size limit; the source does not state the exact deployment error.
- **NEVER let a request handler run longer than 30 seconds.** The handler exceeds the platform duration limit; the source does not state the exact termination/error text.
- **NEVER exceed 10 MiB for a request or response.** The request/response exceeds the platform size limit; the source does not state whether enforcement rejects or truncates it.
- **NEVER exceed 2 GB of total KV storage across all store instances.** The application exceeds its KV storage quota; the source does not state the exact write error.
- **NEVER exceed 1,000 KV read requests per second.** The application exceeds its experimental KV read quota; the source does not state the exact throttling response.
- **NEVER exceed 50 KV write requests per second.** The application exceeds its experimental KV write quota; the source does not state the exact throttling response.
- **NEVER store a KV value larger than 1 MB.** The value exceeds the KV value-size limit; the source does not state the exact write error.
- **NEVER use a KV key larger than 8 KB.** The key exceeds the KV key-size limit; the source does not state the exact write error.

KV query-rate limits are described as experimentation-level limits and can be increased by customer request.

### 1.3 Key-value store

- **NEVER use `wasi:keyvalue/atomic`.** The interface is not supported; a component importing it cannot use that capability.
- **NEVER configure a deployed `key_value_stores` label other than exactly `"default"`.** The Akamai Functions manifest accepts only `"default"`; any other label fails deployment/use.
- **NEVER attempt to share a KV store between applications.** Stores are scoped to a single application, so another application cannot access the same store.
- **NEVER use EdgeKV as if it were the Akamai Functions KV store.** EdgeKV is not compatible with Akamai Functions, so those APIs cannot access this store.
- **NEVER use raw file I/O for deployed KV persistence.** Raw file I/O is not supported; use `openDefault()` instead. Local KV persistence in `.spin/sqlite_key_value.db` is a local-testing implementation detail only.

### 1.4 Outbound networking and databases

- **NEVER call an outbound host that is absent from `allowed_outbound_hosts` in `spin.toml`.** The capabilities-based security model denies the outbound request.
- **NEVER use `localhost` or a short service name for inter-application communication.** These names do not resolve like Docker Compose or Kubernetes services; use the full public URL such as `https://<app-id>.fwf.app`.
- **NEVER omit the `mysql://` protocol from a MySQL entry in `allowed_outbound_hosts`.** The MySQL outbound capability is not granted.
- **NEVER configure PostgreSQL outbound connectivity without `postgres://` and port `5432`.** The PostgreSQL request lacks the required outbound capability.
- **NEVER read a PostgreSQL application variable through `process.env.VAR_NAME`.** The documented integration requires `Variables.get("VAR_NAME")`; `process.env` is not the supported configuration API.
- **NEVER use `require('pg')` for PostgreSQL.** The documented runtime integration is `@spinframework/spin-postgres` with `Postgres.open(connectionString)`; a direct Node PostgreSQL client bypasses the Spin host API.

### 1.5 Application variables and deployment versions

- **NEVER use a variable in code unless it is linked in the component's manifest configuration.** `Variables.get()` can only access variables exposed to that component.
- **NEVER mismatch a `spin.toml` variable key and the string passed to `Variables.get()`.** The lookup does not retrieve the intended value.
- **NEVER continue an object-store request when a required variable is empty.** The documented handler must return HTTP `500` with `Application not configured correctly`.
- **NEVER assume application variables survive an update without being re-specified.** The update guide says variables are not automatically retained; omit them and the new deployment lacks those values.
- **NEVER assume a variable override is a live runtime change.** `spin aka deploy --variable ...` creates a new deployment and increments the version.
- **Application variables are NOT documented as PCI-assessed cryptography.** They are encrypted at rest and in transit, but the underlying cryptographic implementations have not been assessed for PCI compliance.

### 1.6 Updates, deletion, and account security

- **NEVER rely on multiple application versions running simultaneously for canary or blue-green routing.** Akamai Functions does not support simultaneous-version routing; in-flight requests finish on the previous version, then traffic uses the update.
- **NEVER delete an application unless permanent removal is intended.** Deletion cannot be undone.
- **Role-based access control is NOT supported.** Every team-account member has the same permissions and can permanently delete any application in that account.
- **NEVER assume team-account context is selected automatically.** Actions default to the personal/current account unless `--account-name` or `--account-id` selects a team account.

### 1.7 Cron jobs

- **Cron jobs are NOT production-stable.** They are Tech Preview/UNSTABLE and command behavior can change.
- **NEVER use a non-UTC cron schedule.** All schedules are interpreted in UTC, so an unconverted local time runs at the wrong time.
- **NEVER build the documented cron application from a template other than `http-js`.** The cron tutorial requires `http-js`; another template is outside the documented workflow.
- **NEVER create two cron jobs in one application with the same combination of schedule and path-and-query.** That pair must be unique, so the duplicate cannot be created as documented.
- **NEVER omit `--schedule <SCHEDULE>` from the canonical `spin aka [app] cron create` command.** The command reference marks it required and the CLI rejects the incomplete command.
- **NEVER omit `<NAME>` from `spin aka [app] cron delete`.** The canonical command requires the positional name and cannot identify a job without it.

### 1.8 Language and toolchain constraints

- **NEVER build the documented JavaScript/TypeScript applications with Node.js older than 22.** The quickstart and object-store tutorial require Node.js 22 or later; the documented build is unsupported on an older version. The MySQL tutorial separately recommends Node.js 21 or higher.
- **NEVER build the documented Go component with the standard Go compiler.** Standard Go cannot produce the required WASI exports; use TinyGo 0.27 or above.
- **NEVER build the documented Go SDK application without `CGO_ENABLED=1`.** The Go SDK build does not satisfy the documented requirement.
- **NEVER compile the documented Rust component without the `wasm32-wasip1` target.** The Rust toolchain cannot produce the required target artifact.
- **NEVER deploy source that has not been compiled with `spin build`.** The object-store application must be compiled to WebAssembly before deployment.
- **NEVER place the documented JavaScript Property Manager integration entry point anywhere except `src/index.js`.** The `http-js` integration expects that entry point and otherwise does not build/run as documented.
- **NEVER scaffold the documented Supabase cache proxy with a template other than `http-ts`.** That tutorial requires the `http-ts` Spin template; another template is outside its documented build path.

### 1.9 CLI constraints

- **NEVER use Spin older than v3.0.0 with the command reference.** The command reference declares Spin compatibility `>=v3.0.0`; commands are not supported there on older Spin versions. The quotas summary separately says the Spin CLI must be `v0.6.0` or newer, which conflicts with the dedicated command reference; use the stricter `>=v3.0.0` requirement.
- **NEVER set personal-access-token expiration above 90 days.** The CLI rejects values above the documented maximum; the default expiration is 30 days.
- **NEVER let a CI personal access token expire unnoticed.** It expires after 30 days by default and authentication fails after expiration.
- **NEVER discard the only displayed copy of a new personal access token.** A token is shown once; failure to save it requires creating/rotating a token.
- **NEVER request status/log usage outside the documented 5-minute to 7-day range.** The CLI enforces that range and rejects an out-of-range value.
- **NEVER assume the first repeated `--variable` value wins.** The last value for a duplicated key is used, silently replacing earlier values.
- **NEVER assume `--from` has no default.** It defaults to `./spin.toml`; omitting it makes the CLI use that workspace config.

### 1.10 Property Manager integration

- **NEVER put `https://` or a trailing `/` in the Property Origin Hostname.** Derive it by removing both from the Spin application URL; otherwise the origin value is not the documented hostname form.
- **NEVER leave Forward Host Header set to an incoming/default host value.** It must be `Origin Hostname`; otherwise request forwarding to the function is incorrect.

---

## 2. Import Rules

The source articles prescribe the following module imports. They do **not** state a general rule that all imports must be static, nor do they state that dynamic `import()` is unsupported. Do not add that prohibition without a source.

### 2.1 Router and HTTP helpers

```javascript
import { AutoRouter } from 'itty-router';
```

The Supabase article also uses `IRequest` and the `json` helper:

```typescript
import { IRequest } from "itty-router";
// json(data, options) is provided by itty-router; the source summary does not show its import line.
```

The dedicated KV summary spells the package once as `itt-router`; its executable import pattern uses the canonical package name `itty-router`, shown above.

### 2.2 Application variables

```typescript
import * as Variables from "@spinframework/spin-variables";
```

Correct access:

```javascript
const connectionString = Variables.get("pg_connection_string");
```

Incorrect access for the documented database integrations:

```javascript
// WRONG — this is not the documented Spin variable API.
const connectionString = process.env.PG_CONNECTION_STRING;
```

### 2.3 Key-value store

Named-import pattern from the dedicated KV article:

```javascript
import { openDefault } from '@spinframework/spin-kv';
```

Namespace-import pattern from the Supabase cache article:

```typescript
import * as Kv from "@spinframework/spin-kv";
```

Use the matching call for the import style: `openDefault()` for the named import, or `Kv.openDefault()` for the namespace import.

### 2.4 MySQL

```typescript
import * as Mysql from "@spinframework/spin-mysql";
```

### 2.5 PostgreSQL

```javascript
import * as Postgres from "@spinframework/spin-postgres";
```

Incorrect pattern:

```javascript
// WRONG — the Akamai Functions integration does not use a direct Node pg client.
const pg = require('pg');
```

### 2.6 UUID

```javascript
import { v4 as uuidv4 } from 'uuid';
import { validate as uuidValidate } from 'uuid';
```

### 2.7 Supabase

The cache-proxy article requires the `@supabase/supabase-js` package and its `createClient(url, key)` API. Its summary does not contain an exact import statement, so no import spelling is invented here.

### 2.8 S3-compatible object storage and streams

```typescript
import { S3Client } from '@aws-sdk/client-s3';
import { GetObjectCommand } from '@aws-sdk/client-s3';
```

`ListObjectsV2Command` is also provided by `@aws-sdk/client-s3`.

The stream-transform article gives this exact import:

```typescript
import { TransformStream } from 'stream';
```

### 2.9 Rust

```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;
```

The handler also uses `anyhow::Result`.

### 2.10 Go

```go
import (
    spinhttp "github.com/spinframework/spin/sdk/go/v2/http"
)
```

The handler uses the standard `http.ResponseWriter`, `http.Request`, and `fmt.Fprintln` APIs; include their standard-library imports in complete Go source.

---

## 3. Event Handler Reference

Akamai Functions currently supports only an HTTP trigger. Cron does not introduce a second language-level event handler: it invokes an HTTP path in the deployed application.

### 3.1 JavaScript/TypeScript `fetch` event

Required entry-point shape:

```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

router.get("/", () => new Response("Hello, Akamai Functions"));

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

Available objects and operations:

| Object/member | Permitted operation | Constraint |
|---|---|---|
| `event.request` | Pass the incoming request to `router.fetch(...)` | The entry point must be registered with `addEventListener('fetch', ...)` |
| `event.respondWith(responseOrPromise)` | Return the HTTP result to the client | Required by the documented JS/TS entry-point pattern |
| `request.headers.get(name)` | Read request and injected Spin headers | `spin-path-match-n` exists only when that wildcard is present in the trigger route |
| `request.arrayBuffer()` | Read a request body | Decode with `TextDecoder` before `JSON.parse(...)` |
| `router.fetch(event.request, context)` | Dispatch and pass per-request context | Route ordering matters; the first matching route wins |
| `Variables.get(key)` | Read a linked application variable | MySQL requires this call inside the event listener; validate required values |
| `Mysql.open(...)`, `Postgres.open(...)`, `openDefault()` / `Kv.openDefault()` | Open host resources used by a route | Required manifest capabilities/configuration must be present |
| `new S3Client(...)` and `s3.send(...)` | Access S3-compatible storage | Endpoint must be allowed in `allowed_outbound_hosts` |
| outbound `fetch(fullPublicUrl, init)` | Chain to another application | Use the full public URL, never localhost/short names |
| `new URL(request.url)` | Parse URL/query parameters | Used by cron-invoked routes |
| `new Date().toISOString()` and `console.log(...)` | Timestamp and log an invocation | Logs go to stdout/stderr and are retrieved with `spin aka logs` |

Handler-specific forbidden operations:

- A JS/TS application must **not** omit `addEventListener('fetch', ...)` or `event.respondWith(...)`; it then lacks the documented request/response lifecycle.
- A body must **not** be treated as Node-style `req.body`; read `req.arrayBuffer()` and decode it.
- A runtime variable must **not** be read through `process.env`; call `Variables.get(...)`.
- Database, S3, and outbound HTTP access must **not** target a host absent from `allowed_outbound_hosts`.
- Raw file I/O must **not** be used for KV persistence.

#### Variable/context validation pattern

```javascript
addEventListener('fetch', async (event) => {
    const connectionString = Variables.get("pg_connection_string");
    if (!connectionString) {
        return event.respondWith(new Response(JSON.stringify({ message: "Connection String not specified" }), { status: 500, headers: DEFAULT_HEADERS }));
    }
    event.respondWith(router.fetch(event.request, { connectionString }));
});
```

The MySQL source shows a similar guard without `return`:

```typescript
addEventListener('fetch', async (event: FetchEvent) => {
    const connectionString = Variables.get("mysql_connection_string");
    if (!connectionString) {
        event.respondWith(new Response(JSON.stringify({ message: "Connection String not specified" }), { status: 500 }));
    }
    event.respondWith(router.fetch(event.request, { connectionString }));
});
```

Prefer the PostgreSQL form with `return`, so `respondWith` is not invoked twice after a missing configuration value.

### 3.2 Rust HTTP component handler

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

- `#[http_component]` marks the function as the HTTP component entry point.
- The handler receives `spin_sdk::http::Request` and returns `anyhow::Result<impl IntoResponse>`.
- Compile for the `wasm32-wasip1` target.

### 3.3 Go HTTP handler

```go
import (
    spinhttp "github.com/spinframework/spin/sdk/go/v2/http"
)

func init() {
    spinhttp.Handle(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "text/plain")
        fmt.Fprintln(w, "Hello Akamai!")
    })
}
```

- Register the handler through `spinhttp.Handle(...)` in `init()`.
- The callback uses `http.ResponseWriter` and `*http.Request`.
- Build with TinyGo 0.27 or above and `CGO_ENABLED=1`; standard Go cannot emit the required WASI exports.

### 3.4 Cron invocation of an HTTP route

```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

router.get("/", (request) => {
    const url = new URL(request.url);
    const now = new Date().toISOString();
    console.log(`Cron job triggered at ${now}"`);
    return new Response("Cron job executed", { status: 200 });
});

addEventListener('fetch', (event) => {
    event.respondWith(router.fetch(event.request));
});
```

The cron service invokes the configured path; the code still receives the standard HTTP `fetch` event. Schedules are UTC and the schedule/path-and-query pair must be unique per application.

---

## 4. API Reference

### 4.1 HTTP trigger manifest and injected headers

```toml
[[trigger.http]]
route = "/..."
component = "my-application"
```

The HTTP trigger adds these request headers. The sources refer to the group generally as `spin-*` headers:

| Header | Meaning |
|---|---|
| `spin-full-url` | Full request URL including host and scheme |
| `spin-path-info` | Request path relative to the component route |
| `spin-path-match-n` | Wildcard value, where `n` is the segment name, for example `spin-path-match-userid` |
| `spin-matched-route` | Matched part of the trigger route |
| `spin-raw-component-route` | Component route pattern that matched |
| `true-client-ip` | IP address of the client sending the request |

Wildcard access pattern:

```javascript
// Access the 'userid' wildcard value from a route like /user/{userid}
const userId = request.headers.get('spin-path-match-userid');
```

`spin-path-match-n` is conditional: it is present only when the route definition contains that wildcard segment.

### 4.2 JavaScript/TypeScript HTTP and routing APIs

```text
AutoRouter
router.get(path, handler)
router.post(path, handler)
router.put(path, handler)
router.delete(path, handler)
router.all(path, handler)
router.fetch(request)
router.fetch(request, context)
json(data, options)
new Response(body)
new Response(body, options)
addEventListener('fetch', handler)
addEventListener('fetch', callback)
event.respondWith(promise)
request.arrayBuffer()
request.headers.get(name)
new TextDecoder().decode(buffer)
decoder.decode(requestBody)
new URL(request.url)
new Date().toISOString()
console.log(message)
```

Router behavior from the sources:

- Routes can be chained from `AutoRouter()`.
- The first matching route is used; route ordering matters.
- Unmatched routes return `404` unless an explicit catch-all handles them.
- Route variables appear in source examples as `({ name })`, `({ params })`, and `request.params`.
- The second argument to `router.fetch(request, context)` is received as the second route-handler argument, for example `{ connectionString }`.
- `json(data, options)` creates a JSON response object.

Exact route patterns:

```javascript
router
    .post("/products", async (request, { connectionString }) => createProduct(await request.arrayBuffer(), connectionString))
    .get("/products", async (_, { connectionString }) => readAllProducts(connectionString))
    .get("/products/:id", async ({ params }, { connectionString }) => readProductById(params.id, connectionString))
    .put("/products/:id", async (request, { connectionString }) => updateProductById(request.params.id, await request.arrayBuffer(), connectionString))
    .delete("/products/:id", async ({ params }, { connectionString }) => deleteProductById(params.id, connectionString))
    .all("*", () => notFound("Endpoint not found"));
```

### 4.3 Application variables — `@spinframework/spin-variables`

```text
Variables.get(key)
Variables.get(key: string)
Variables.get("key")
```

- Retrieves a value defined in `spin.toml`/the application manifest and exposed to the component.
- Keys must match exactly.
- Variables must be linked through the component's `[component.name.variables]` section (generically, `[component.<name>]`) before `Variables.get(...)` can access them.
- The MySQL and PostgreSQL integrations retrieve the connection string inside the fetch listener.
- Local-development variable names must be prefixed with `SPIN_VARIABLE_`, for example `SPIN_VARIABLE_MYSQL_HOST`.
- Variables are encrypted at rest and in transit by default, but the cryptographic implementations have not been assessed for PCI compliance.

Manifest patterns:

```toml
[variables]
compression_level = { default = "1" }
```

```toml
[variables]
mysql_host = { required = true }
mysql_user = { required = true }
mysql_password = { required = true, secret = true }
mysql_port = { required = true }
mysql_database = { required = true }
```

Deploy-time override:

```shell
spin aka deploy --variable compression_level=3
```

### 4.4 Key-value store — `@spinframework/spin-kv`

```text
openDefault()
Kv.openDefault()
store.exists(key)
store.getJson(key)
store.setJson(key, payload)
store.setJson(key, value)
store.delete(key)
```

- `openDefault()` / `Kv.openDefault()` opens the only platform-provisioned store.
- `exists` checks for a key.
- `getJson` retrieves and JSON-decodes a value.
- `setJson` JSON-encodes and stores a value.
- `delete` removes a key/value pair.
- The global store provides read-your-writes behavior within a request.
- Underlying supported interfaces are `wasi:keyvalue/store` and `wasi:keyvalue/batch` at the 2024-10-17 snapshot; `wasi:keyvalue/atomic` is not supported.

Manifest capability:

```toml
[component.component-name]
key_value_stores = [ "default" ]
```

Import and router setup pattern:

```javascript
import { openDefault } from '@spinframework/spin-kv';
import { AutoRouter } from 'itty-router'

const router = AutoRouter();

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

Canonical operations:

```javascript
// Open store
const store = openDefault();

// Check existence
if (!store.exists(key)) {
    return new Response(null, { status: 404 });
}

// Get JSON
let found = store.getJson(key);

// Set JSON
store.setJson(key, payload);
```

#### TTL cache wrapper

```typescript
interface CacheData {
  expiresAt: string;
  data: any;
}

const buildCacheData = (data: any, ttl: number): CacheData => {
  return {
    expiresAt: new Date(Date.now() + ttl * 60 * 1000).toISOString(),
    data: data
  } as CacheData;
}

// Check if cache data is expired
const onlyValidCacheData = (cacheItem: CacheData): any | undefined => {
  const now = new Date();
  const expiresAt = new Date(cacheItem.expiresAt);
  if (now > expiresAt) {
    return undefined;
  }
  return cacheItem.data;
}
```

#### List-cache invalidation

```typescript
import * as Kv from "@spinframework/spin-kv";

export const ALL_ARTICLES_CACHE_KEY = "all-articles";

export function storeInCache(key: string, value: any, ttl: number) {
  const store = Kv.openDefault();
  store.setJson(key, buildCacheData(value, ttl));

  // Invalidate the global list if a specific item was cached
  if (key !== ALL_ARTICLES_CACHE_KEY && store.exists(ALL_ARTICLES_CACHE_KEY)) {
    store.delete(ALL_ARTICLES_CACHE_KEY);
  }
}
```

### 4.5 MySQL — `@spinframework/spin-mysql`

```text
Mysql.open(connectionString: string)
connection.execute(sql: string, params: any[])
connection.query(sql: string, params: any[])
connection.rows
```

- `Mysql.open` opens a MySQL connection.
- `connection.execute` runs INSERT/UPDATE/DELETE and returns the number of affected rows, not a result object.
- `connection.query` runs SELECT and returns an object whose `.rows` property is the result array.
- `allowed_outbound_hosts` must use `mysql://`.

Full manifest pattern:

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

Full router and entry-point pattern:

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

### 4.6 PostgreSQL — `@spinframework/spin-postgres`

```text
Postgres.open(connectionString)
connection.execute(sql, params)
connection.query(sql, params)
```

- `Postgres.open` opens a PostgreSQL connection.
- `connection.execute` runs INSERT/UPDATE/DELETE and returns the number of affected rows.
- `connection.query` runs SELECT and returns a result object with a `rows` array.
- Outbound connectivity must be configured with `postgres://` and port `5432` under `[component.<component_name>]`.

Full router setup pattern:

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

Response helper pattern:

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

### 4.7 Supabase client — `@supabase/supabase-js`

```text
createClient(url, key)
supabase.from(table).select()
supabase.from(table).insert(data)
supabase.from(table).update(data)
supabase.from(table).delete()
supabase.from(table).eq(column, value)
supabase.from(table).maybeSingle()
```

- `createClient(url, key)` creates the client.
- `.maybeSingle()` returns `null` when no row matches; it does not throw like `.single()`.
- Supabase calls require explicit outbound-host capability in `spin.toml`.

Configuration middleware:

```typescript
import * as Variables from "@spinframework/spin-variables";
import { IRequest } from "itty-router";

export interface Config {
  url: string;
  key: string;
  cacheTtl: number;
  webhookToken?: string;
}

export function withConfig(request: IRequest) {
  const url = Variables.get('supabase_url');
  const key = Variables.get('supabase_key');
  const ttl = +(Variables.get('cache_ttl') ?? "5");
  const webhookToken = Variables.get('supabase_webhook_token');

  if (!url || !key) {
    throw new Error("Required Configuration data not set");
  }

  request.config = {
    url,
    key,
    cacheTtl: ttl,
    webhookToken
  } as Config;
}
```

Webhook validation:

```typescript
const onDatabaseUpdate = (headers: Headers, requestBody: ArrayBuffer, config: Config): Response => {
  const token = headers.get("x-webhook-token");
  if (!token || token !== config.webhookToken) {
    console.log("Webhook invoked without or with invalid token");
    return new Response(null, { status: 401 });
  }
  return processDatabaseUpdate(requestBody);
}
```

### 4.8 S3-compatible object storage — `@aws-sdk/client-s3`

```text
S3Client
GetObjectCommand
ListObjectsV2Command
Variables.get(key)
```

Client initialization:

```typescript
import { S3Client } from '@aws-sdk/client-s3';

const s3 = new S3Client({
    region: config.region,
    endpoint: config.endpoint,
    credentials: {
        accessKeyId: config.accessKeyId,
        secretAccessKey: config.secretAccessKey,
    }
});
```

Required-variable validation:

```typescript
import * as Variables from '@spinframework/spin-variables';

// load application variables
const endpoint = Variables.get("endpoint");
const accessKeyId = Variables.get("access_key_id");
const secretAccessKey = Variables.get("secret_access_key");
const bucketName = Variables.get("bucket_name");
const region = Variables.get("region");

// validate required variables
if (!endpoint || !accessKeyId || !secretAccessKey || !bucketName || !region) {
    return new Response("Application not configured correctly", { status: 500 });
}
```

Streaming response:

```typescript
import { GetObjectCommand } from '@aws-sdk/client-s3';

// ... inside request handler
const { Body } = await s3.send(new GetObjectCommand(input));
return new Response(Body as ReadableStream, {
    status: 200,
});
```

Transforming a streamed body:

```typescript
import { TransformStream } from 'stream';

const upperCaseTransform = new TransformStream({
    transform(chunk, controller) {
        const txt = dec.decode(chunk, { stream: true });
        controller.enqueue(enc.encode(txt.toUpperCase()));
    }
});

const transformed = (Body as ReadableStream).pipeThrough(upperCaseTransform);
return new Response(transformed, { status: 200 });
```

`Body` must be cast to `ReadableStream` before it is used as a `Response` body or piped through the transform.

### 4.9 UUID

```text
uuidv4()
uuidValidate(id: string)
uuid.v4()
uuid.validate(id)
```

- `uuidv4()` / `uuid.v4()` generates a UUID v4 string.
- `uuidValidate(id)` / `uuid.validate(id)` tests whether a string is a valid UUID.

### 4.10 Logging

```text
console.log(message)
spin aka logs [OPTIONS]
spin aka app logs [OPTIONS]
```

- Akamai Functions captures everything written to stdout and stderr.
- `spin aka logs` defaults to the application linked to the workspace; use `--app-name` to target another application.
- The application-logs article documents Go's `log/slog` package for generating messages and says its example/application must be written in Go with Spin framework v3.

### 4.11 Rust and Go HTTP APIs

Rust:

```text
spin_sdk::http::Request
spin_sdk::http::Response
spin_sdk::http::IntoResponse
spin_sdk::http_component
anyhow::Result
```

Go:

```text
spinhttp.Handle(handler)
http.ResponseWriter
http.Request
```

See the exact entry-point patterns in §3.2 and §3.3. The quickstart's JavaScript/TypeScript pattern is:

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

### 4.12 Other platform interfaces

- `HTTP` — supported incoming trigger.
- `Outbound HTTP` — supported with capability allowlisting.
- `Application Variables` — supported configuration API.
- `Key Value Storage` / `wasi-keyvalue` — supported through `wasi:keyvalue/store` and `wasi:keyvalue/batch` at the 2024-10-17 snapshot.
- `MySQL` and `PostgreSQL` — supported outbound database APIs.
- `Outbound Redis` — supported; this is distinct from the unsupported Redis trigger. No method signatures are provided by the new source summaries.
- `wasi-config` — supported at the 2024-09-27 snapshot. No language binding signature is provided by the new source summaries.
- `Component dependencies` — supported. No API signature is provided by the new source summaries.
- Serverless AI — Limited Access only. No API signature is provided by the new source summaries.

Service-chaining pattern:

```javascript
// Service Chaining Pattern
// Unlike local environments, use the full public URL for inter-app communication
const response = await fetch('https://<app-id>.fwf.app', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data: 'payload' })
});
```

### 4.13 CLI command reference

Dedicated command-reference signatures:

```text
spin aka app deploy [OPTIONS]
spin aka app cron create [OPTIONS] --schedule <SCHEDULE>
spin aka app cron delete [OPTIONS] <NAME>
spin aka app cron list [OPTIONS]
spin aka app delete [OPTIONS]
spin aka app history [OPTIONS]
spin aka app link [OPTIONS]
spin aka app list [OPTIONS]
spin aka app logs [OPTIONS]
spin aka app status [OPTIONS]
spin aka app unlink [OPTIONS]
spin aka auth login [OPTIONS]
spin aka auth token create [OPTIONS] --name <NAME>
spin aka auth token delete [OPTIONS] --id <ID>
spin aka auth token list [OPTIONS]
spin aka auth token regenerate [OPTIONS] --id <ID>
spin aka cron create [OPTIONS] --schedule <SCHEDULE>
spin aka cron delete [OPTIONS] <NAME>
spin aka cron list [OPTIONS]
spin aka deploy [OPTIONS]
spin aka info [OPTIONS]
spin aka logs [OPTIONS]
spin aka send-feedback
```

Additional exact command forms from the lifecycle, account, and CI articles:

```text
spin aka login
spin aka login --token <TOKEN>
spin aka app delete --app-name <name>
spin aka auth token create --name <name>
spin aka auth token create --expiration-days <days>
spin aka deploy --variable <key>=<value>
gh secret set <name>
```

Argument patterns:

```bash
spin aka app deploy --variable key=value --variable @config.json
spin aka app deploy --account-id <ACCOUNT_ID>
spin aka app deploy --account-name <ACCOUNT_NAME>
spin aka app deploy
spin aka app logs --since 7d
spin aka app status --usage-since 30m
```

- Account selection: use either `--account-id` or `--account-name`; otherwise the current account context is used.
- App selection: use either `--app-id` or `--app-name`; otherwise infer the app from workspace config (`./spin.toml`).
- Time values accept RFC3339 timestamps, Unix epoch timestamps, or durations such as `30m` and `7d`.
- Repeated `--variable` flags are accepted; the last occurrence of a duplicated key wins.
- `--from` defaults to `./spin.toml`.
- `spin aka app list` prints names as plain text by default; `--verbose` includes details such as App IDs, and `--format json` emits JSON.
- `spin aka app status` uses the application linked to the workspace unless `--app-name` selects another.
- `spin aka info` displays account name and ID and requires plugin v0.4 or higher.

Inspection and lifecycle examples:

```shell
spin aka app list --format json
spin aka app list --verbose
spin aka app status --app-name <app_name> --format json
spin aka app delete --app-name validate-jwt-tokens
spin aka app list --account-name <team_name>
spin aka deploy --account-name <team_name>
```

The account guide contains this exact deletion example:

```shell
spin aka delete app --app-name <app_name> --account-name <team_name>
```

That ordering conflicts with the dedicated command reference, which defines `spin aka app delete [OPTIONS]`. Prefer the dedicated command-reference form:

```shell
spin aka app delete --app-name <app_name> --account-name <team_name>
```

### 4.14 Cron CLI

Canonical dedicated-command-reference forms:

```text
spin aka app cron create [OPTIONS] --schedule <SCHEDULE>
spin aka app cron delete [OPTIONS] <NAME>
spin aka app cron list [OPTIONS]
spin aka cron create [OPTIONS] --schedule <SCHEDULE>
spin aka cron delete [OPTIONS] <NAME>
spin aka cron list [OPTIONS]
```

The cron tutorial separately gives positional forms:

```text
spin aka cron create "<schedule>" "<path>" "<name>"
spin aka cron list
spin aka cron delete "<name>"
```

Exact tutorial example:

```shell
spin aka cron create "*/5 * * * *" "/" "cron-job-1"
```

The positional create form conflicts with the dedicated command reference's required `--schedule` option. Preserve it as tutorial evidence, but use `spin aka cron create [OPTIONS] --schedule <SCHEDULE>` as the canonical syntax for generated commands.

### 4.15 Deployment, updates, and CI

Create a documented cron/JS application:

```text
spin new -E akamai-functions -t http-js --accept-defaults <app-name>
```

Update an application:

```toml
version = "0.1.1"
```

```shell
spin aka deploy
spin aka deploy --variable <key>=<value>
```

The old version gracefully completes in-flight requests, but multiple versions are not simultaneously routable. Re-specify application variables on upgrade because the update guide says they are not retained automatically.

GitHub Actions deployment pattern:

```yaml
name: Deploy to Akamai Functions

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Clone repository
      uses: actions/checkout@v4

    - name: Install Spin
      run: |
        curl -fsSL https://wasm-functions.fermyon.app/downloads/install.sh | bash
        mv spin /usr/local/bin/spin

    - name: Build
      run: spin build

    - name: Login to Akamai Functions
      run: spin aka login --token ${{ secrets.SPIN_AKA_ACCESS_TOKEN }}

    - name: Deploy to Akamai Functions
      run: spin aka deploy
```

Token rotation:

```shell
# 1. Create a new token
spin aka auth token create --name mynewtoken --expiration-days 90

# 2. Copy the token output immediately
# 3. Update the GitHub repository secret
gh secret set SPIN_AKA_ACCESS_TOKEN
```

Personal access tokens expire after 30 days by default, support a maximum of 90 days, and are displayed only once. The install workflow puts `spin` in `/usr/local/bin/spin`; `actions/checkout@v4` is the documented checkout action.

### 4.16 Property Manager integration

The JavaScript application must use the `http-js` template, entry point `src/index.js`, `AutoRouter`, and the fetch-event pattern from §3.1.

Property configuration requirements:

- Derive Origin Hostname by removing `https://` and the trailing `/` from the Spin application URL.
- Set **Forward Host Header** to **Origin Hostname**.

Deployment through `spin aka deploy` requires authentication through the documented Akamai Control Center or GitHub-credential login flow.

### 4.17 Version and compatibility ledger

| Area | Exact source note |
|---|---|
| Platform | Limited availability/Public Preview; the welcome page was updated 2026-03-31 |
| Command reference | Spin compatibility `>=v3.0.0`; plugin versions documented: v0.4.0 and v0.7.0; evolution dates 2025-05-22 through 2026-03-20 |
| Quotas article | Separately says Spin CLI v0.6.0 or newer; use the stricter dedicated command-reference requirement when generating commands |
| Application variables | Requires Spin v3; source last updated 2026-08-05 |
| Application logs | Go application with Spin framework v3 |
| JavaScript/TypeScript quickstart | Node.js 22 or newer; documentation example uses Node.js 22.13.0 |
| Windows quickstart | Supported Spin binary release is 3.6.2 |
| Rust quickstart | Requires target `wasm32-wasip1` |
| Go quickstart | TinyGo 0.27 or above, `CGO_ENABLED=1`; Go SDK v0.10.0 appears in build output |
| MySQL tutorial | Node.js 21 or higher recommended; requires Linode Managed Databases, `@spinframework/spin-mysql`, and `@spinframework/spin-variables` |
| PostgreSQL tutorial | Requires `http-js`, `@spinframework/spin-postgres`, and `@spinframework/spin-variables` |
| Supabase cache proxy | Requires `http-ts`, `itty-router`, `@spinframework/spin-variables`, `@spinframework/spin-kv`, and `@supabase/supabase-js` |
| Object-store tutorial | Node.js 22 or later; requires `@spinframework/spin-variables` and `@aws-sdk/client-s3` |
| KV tutorial | Requires `@spinframework/spin-kv` and `itty-router`; local development persists through SQLite |
| Account management | `spin aka info` requires plugin v0.4 or higher |
| Cron | Tech Preview/UNSTABLE; `http-js` tutorial template |

---

## 5. Cross-Reference

### 5.1 API and event-handler availability matrix

| Object/API | JS/TS `fetch` | Rust `#[http_component]` | Go `spinhttp.Handle` | Cron invocation |
|---|---:|---:|---:|---:|
| Incoming HTTP request | `event.request` | `spin_sdk::http::Request` | `*http.Request` | Same HTTP handler at configured path |
| Outgoing HTTP response | `Response` + `event.respondWith` | `Response` / `IntoResponse` | `http.ResponseWriter` | Same HTTP response contract |
| `AutoRouter`, `router.*`, `router.fetch` | ✅ | Not documented | Not documented | ✅ in the JS cron tutorial |
| `Variables.get` | ✅ | No binding documented | No binding documented | ✅ if the invoked JS route uses it |
| `openDefault` / `Kv.openDefault` | ✅ | No binding documented | No binding documented | ✅ if the invoked JS route uses it |
| `Mysql.open` | ✅ | No binding documented | No binding documented | ✅ if capability/config exists |
| `Postgres.open` | ✅ | No binding documented | No binding documented | ✅ if capability/config exists |
| `S3Client` / `s3.send` | ✅ | No binding documented | No binding documented | ✅ if capability/config exists |
| Supabase client | ✅ | No binding documented | No binding documented | ✅ if capability/config exists |
| Outbound `fetch` | ✅ | SDK form not documented | SDK form not documented | ✅ if capability/config exists |
| `console.log` | ✅ | Logging API not documented | Use `log/slog` per logging article | ✅ |

Only HTTP is a supported trigger. “Cron invocation” is not a fourth language handler; it is an external scheduler calling the configured HTTP route.

### 5.2 Object/method interactions

```text
[[trigger.http]]
  -> JS addEventListener('fetch')
       -> event.request
       -> router.fetch(request, context)
            -> route handler(request, context)
                 -> request.headers.get('spin-path-match-n')
                 -> request.arrayBuffer() -> TextDecoder -> JSON.parse
                 -> Variables.get(key)
                 -> openDefault()/Kv.openDefault()
                      -> exists/getJson/setJson/delete
                 -> Mysql.open(connectionString)
                      -> query(...).rows / execute(...) -> affected-row count
                 -> Postgres.open(connectionString)
                      -> query(...).rows / execute(...) -> affected-row count
                 -> createClient(url, key)
                      -> from(table).select/insert/update/delete/eq/maybeSingle
                 -> new S3Client(config)
                      -> send(GetObjectCommand) -> Body as ReadableStream
                           -> pipeThrough(TransformStream) -> Response
                      -> send(ListObjectsV2Command)
                 -> fetch('https://<app-id>.fwf.app', init)
                 -> Response/json(...)
       -> event.respondWith(response or promise)
```

Other language entry points map to the same HTTP trigger:

```text
[[trigger.http]] -> Rust #[http_component] fn(Request) -> Result<impl IntoResponse>
[[trigger.http]] -> Go init() -> spinhttp.Handle(func(ResponseWriter, *Request))
cron schedule    -> deployed HTTP path -> one of the handlers above
```

### 5.3 Required manifest/deployment capability by API

| API/feature | Required configuration or deployment action | Failure if omitted |
|---|---|---|
| HTTP handler | Root `[[trigger.http]]` with `route` and `component` | No documented supported trigger reaches the component |
| `Variables.get(key)` | Declare/link the variable to the component; pass update values with `--variable` | Lookup is missing/empty; required object-store config returns HTTP 500 |
| `openDefault()` / `Kv.openDefault()` | `key_value_stores = [ "default" ]` | Store is unavailable; custom labels are unsupported |
| `Mysql.open(...)` | `allowed_outbound_hosts = ["mysql://{{ mysql_host }}:{{ mysql_port }}"]` | MySQL outbound capability is denied |
| `Postgres.open(...)` | `allowed_outbound_hosts` using `postgres://` and port `5432` | PostgreSQL outbound capability is denied |
| Supabase client | Supabase host in `allowed_outbound_hosts`; `supabase_url` and `supabase_key` variables | Client cannot reach the host or config middleware throws `Required Configuration data not set` |
| S3 client | S3 endpoint in `allowed_outbound_hosts`; endpoint/credentials/bucket/region variables | Request is denied or handler returns HTTP 500 for missing config |
| Inter-app outbound `fetch` | Target in `allowed_outbound_hosts`; full `https://<app-id>.fwf.app` URL | Capability denial or hostname-resolution failure |
| Cron | Deployed HTTP app, UTC schedule, unique schedule/path pair | Job cannot be created/invoked as documented |

### 5.4 CLI context and lifecycle interactions

| Command | Implicit context | Related command/data |
|---|---|---|
| `spin aka app deploy` / `spin aka deploy` | Current account and `./spin.toml` unless selectors override | `--variable`; linked app or app selector |
| `spin aka app list` | Current/personal account unless account selector is supplied | `--verbose`, `--format json` reveal IDs/details |
| `spin aka app status` | Workspace-linked app unless `--app-name` is supplied | `--usage-since` accepts supported time formats/range |
| `spin aka logs` | Workspace-linked app unless `--app-name` is supplied | Captured stdout/stderr; `--since` time selector |
| `spin aka auth token create` | Current user | Save once, store as `SPIN_AKA_ACCESS_TOKEN`, rotate before expiration |
| `spin aka app delete` | Selected/current account and app | Permanent; any team member can perform it because RBAC is absent |
| `spin aka cron create/list/delete` | Current/deployed app | Operates on HTTP paths; Tech Preview/UNSTABLE |

---

## 6. Known Failure Patterns

Only symptoms stated or directly implied by the new source summaries are used. When an exact error string is available, it is preserved.

### 6.1 Unsupported/custom trigger

```toml
# WRONG — custom trigger types are not supported.
[[trigger.custom]]
component = "my-application"

# CORRECT — HTTP is the only supported trigger.
[[trigger.http]]
route = "/..."
component = "my-application"
```

**Symptom:** the custom trigger is not supported by Akamai Functions and cannot invoke the component.

### 6.2 Missing JavaScript fetch wrapper

```javascript
// WRONG — route declaration alone is not the documented runtime entry point.
const router = AutoRouter();
router.get("/", () => new Response("Hello"));

// CORRECT
addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

**Symptom:** the application does not participate in the required fetch-event request lifecycle and does not return the router result through `respondWith`.

### 6.3 Node-style PostgreSQL client

```javascript
// WRONG
const pg = require('pg');

// CORRECT
import * as Postgres from "@spinframework/spin-postgres";
const connection = Postgres.open(connectionString);
```

**Symptom:** the code does not use the required Akamai Functions PostgreSQL host integration.

### 6.4 Node-style environment variables

```javascript
// WRONG
const connectionString = process.env.PG_CONNECTION_STRING;

// CORRECT
const connectionString = Variables.get("pg_connection_string");
```

**Symptom:** the function does not retrieve the manifest-defined application variable through the supported API.

### 6.5 Node-style request body access

```javascript
// WRONG — Akamai Functions does not provide parsed Node-style req.body.
const payload = req.body;

// CORRECT
const requestBody = await req.arrayBuffer();
const payload = JSON.parse(new TextDecoder().decode(requestBody));
```

**Symptom:** `req.body` is not the decoded payload; the source requires `ArrayBuffer` access followed by `TextDecoder`.

### 6.6 Missing outbound host capability

```toml
# WRONG
[component.linode-mysql]
allowed_outbound_hosts = []

# CORRECT
[component.linode-mysql]
allowed_outbound_hosts = ["mysql://{{ mysql_host }}:{{ mysql_port }}"]
```

**Symptom:** the capabilities-based security model denies the database request.

### 6.7 Wrong MySQL/PostgreSQL protocol declaration

```toml
# WRONG — missing mysql://
allowed_outbound_hosts = ["{{ mysql_host }}:{{ mysql_port }}"]

# CORRECT
allowed_outbound_hosts = ["mysql://{{ mysql_host }}:{{ mysql_port }}"]
```

For PostgreSQL, use `postgres://` and port `5432`.

**Symptom:** the corresponding outbound database capability is not granted.

### 6.8 Localhost/short-name service chaining

```javascript
// WRONG
const response = await fetch('http://localhost/service');

// CORRECT
const response = await fetch('https://<app-id>.fwf.app', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data: 'payload' })
});
```

**Symptom:** unlike Docker Compose/Kubernetes service names, localhost or short names do not address another Akamai Functions application.

### 6.9 Wrong KV label

```toml
# WRONG
[component.component-name]
key_value_stores = [ "custom" ]

# CORRECT
[component.component-name]
key_value_stores = [ "default" ]
```

**Symptom:** Akamai Functions accepts only the `"default"` label, so the custom-label deployment/use fails.

### 6.10 Atomic KV, EdgeKV, or raw file I/O

```javascript
// WRONG — wasi:keyvalue/atomic, EdgeKV, and raw file I/O are unsupported here.
// atomic.increment("count", 1)

// CORRECT
import { openDefault } from '@spinframework/spin-kv';
const store = openDefault();
store.setJson("count", payload);
```

**Symptom:** the unsupported interface/storage mechanism cannot access the Akamai Functions KV store.

### 6.11 Supabase `.single()` for an optional match

```javascript
// WRONG — throws when no row exists.
const result = await supabase.from(table).select().eq(column, value).single();

// CORRECT — returns null for no match; check it and return 404.
const result = await supabase.from(table).select().eq(column, value).maybeSingle();
```

**Symptom:** `.single()` throws when no row is found, whereas `.maybeSingle()` returns `null`.

### 6.12 Missing required configuration

```typescript
// WRONG — continue with empty S3 configuration.
const s3 = new S3Client({ region, endpoint, credentials: { accessKeyId, secretAccessKey } });

// CORRECT
if (!endpoint || !accessKeyId || !secretAccessKey || !bucketName || !region) {
    return new Response("Application not configured correctly", { status: 500 });
}
```

**Symptom:** the documented response is HTTP `500` with `Application not configured correctly`.

### 6.13 S3 body used without `ReadableStream` cast

```typescript
// WRONG — Body is not automatically treated as the response stream type here.
return new Response(Body, { status: 200 });

// CORRECT
return new Response(Body as ReadableStream, { status: 200 });
```

**Symptom:** `Body` is not automatically a standard stream compatible with every context; the documented Response use requires the explicit cast.

### 6.14 KV cache invalidation omitted

```typescript
// WRONG — update an individual item but leave the all-items cache stale.
store.setJson(key, buildCacheData(value, ttl));

// CORRECT
store.setJson(key, buildCacheData(value, ttl));
if (key !== ALL_ARTICLES_CACHE_KEY && store.exists(ALL_ARTICLES_CACHE_KEY)) {
  store.delete(ALL_ARTICLES_CACHE_KEY);
}
```

**Symptom:** the global list cache can continue serving stale data after an individual item changes.

### 6.15 Local-time cron expression

```shell
# WRONG — schedule copied as local wall-clock time.
spin aka cron create "0 9 * * *" "/" "local-nine"

# CORRECT — convert the desired time to UTC before creating the schedule.
spin aka cron create "<UTC_CRON>" "/" "utc-schedule"
```

**Symptom:** the job runs according to UTC, at a different local time than intended.

### 6.16 Duplicate cron schedule and path

```text
WRONG: create a second job with the same schedule and path-and-query.
CORRECT: change either the schedule or the path-and-query so the pair is unique.
```

**Symptom:** the application violates the documented uniqueness requirement for cron jobs.

### 6.17 Assuming hot-swapped variables or retained update values

```shell
# WRONG — deploy an update while assuming old values remain/live-update in place.
spin aka deploy

# CORRECT — explicitly supply the values required by the new deployment.
spin aka deploy --variable <key>=<value>
```

**Symptom:** the variable change creates a new version, and variables omitted during an upgrade are not automatically retained according to the update guide.

### 6.18 Assuming canary/blue-green version routing

```text
WRONG: deploy a new version and expect both versions to receive selectable traffic.
CORRECT: treat deployment as an update; only in-flight requests finish on the previous version.
```

**Symptom:** no simultaneous-version routing is available.

### 6.19 Logs fetched from the wrong app

```shell
# WRONG — when the workspace is linked to a different application.
spin aka logs

# CORRECT
spin aka logs --app-name <app_name>
```

**Symptom:** the unqualified command fetches logs for the workspace-linked application.

### 6.20 Property Manager hostname/header mismatch

```text
WRONG:
  Origin Hostname = https://example.fwf.app/
  Forward Host Header = incoming/default host

CORRECT:
  Origin Hostname = example.fwf.app
  Forward Host Header = Origin Hostname
```

**Symptom:** request forwarding is not configured in the form required by the Property Manager integration.

### 6.21 Non-canonical CLI command ordering

```shell
# SOURCE DISCREPANCY — shown by the account guide.
spin aka delete app --app-name <app_name> --account-name <team_name>

# CANONICAL — matches the dedicated command reference.
spin aka app delete --app-name <app_name> --account-name <team_name>
```

**Symptom:** the first spelling conflicts with the dedicated command-reference signature and may not parse as the intended command.

### 6.22 Cron syntax discrepancy

```shell
# TUTORIAL FORM
spin aka cron create "*/5 * * * *" "/" "cron-job-1"

# CANONICAL COMMAND-REFERENCE SHAPE
spin aka cron create [OPTIONS] --schedule <SCHEDULE>
```

**Symptom:** the tutorial positional form and command-reference option form conflict. Generated commands should follow the dedicated command reference and supply required options for path/name as exposed by the installed plugin version.
