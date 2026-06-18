# Akamai Functions — Unified Coding Reference

> Master reference for generating Akamai Functions code (Spin applications compiled to WebAssembly).
> Compiled from `/docs/techdocs-akamai-com/`. Scan top-to-bottom to answer:
> *"what can I use, what are the exact signatures, what must I never do."*

Akamai Functions runs **Spin applications compiled to WebAssembly** with SDK support for **Rust, Go, JavaScript, and Python**. The platform is currently **limited-availability (public preview)**.

---

## 1. Runtime Prohibitions

Every constraint below is a hard rule. Violations produce the listed runtime consequence.

### 1.1 Execution / sandbox

- **NEVER use Node.js standard APIs** such as `fs`, `net`, `child_process`, `process`, or `require`. → They are not available in the WebAssembly sandbox; calls fail at runtime / module-load (`ReferenceError` or "not supported"). All I/O must go through streams or network calls.
- **NEVER use dynamic `import()` at runtime.** → Only static ES module `import` statements at the top of the file are supported; dynamic imports fail to resolve.
- **NEVER read configuration from `process.env`.** → `process` is undefined. Use `Variables.get(name)` (Spin variables) instead.
- **NEVER write logs to a file.** → Only output written to `stdout` / `stderr` is captured by `spin aka logs`. File logs are silently dropped.
- **NEVER rely on runtime configuration changes.** → Runtime configuration is not supported; values are fixed at deploy time.

### 1.2 Triggers / interfaces

- **NEVER define custom triggers.** → Not supported. Only the built-in HTTP trigger is available.
- **NEVER use the Redis trigger.** → Not supported on Akamai Functions.
- **NEVER use SQLite storage.** → Not supported.
- **NEVER use `wasi-blobstore`.** → Not supported.
- **NEVER use `wasi-messaging`.** → Not supported.
- **NEVER use the `wasi:keyvalue/atomic` interface.** → Not supported; only `wasi:keyvalue/store` and `wasi:keyvalue/batch` are available.
- **Cron-job scheduling is Tech Preview / UNSTABLE.** → Do not use in production; commands may change without notice.

### 1.3 Inter-service / outbound networking

- **NEVER use `localhost` or short service names to call another Spin application.** → Resolution fails. Always use the full public URL, e.g. `https://<app-id>.fwf.app`.
- **NEVER make outbound calls to hosts not listed in `allowed_outbound_hosts` (in `spin.toml`).** → The runtime blocks the request and the SDK call fails. Each external host (S3 endpoint, Postgres host, etc.) must be explicitly allowed.
- The `allowed_outbound_hosts` entries must use exact protocol + port (e.g. `postgres://...:5432`, `https://...`). Wildcard pattern requires a trailing dot (`'https://.'`).

### 1.4 Quotas and limits (silent or hard failures)

| Limit | Value | Consequence if exceeded |
|---|---|---|
| RAM per execution | **128 MiB** | Execution aborted / OOM |
| App bundle size | **50 MiB** | Deploy rejected |
| Request handler duration | **30 seconds** | Execution terminated |
| Request or response size | **10 MiB** | Truncated / rejected |
| KV total storage per app (all stores) | **2 GB** | Write rejected |
| KV read RPS per app | **1,000 RPS** | Throttled |
| KV write RPS per app | **50 RPS** | Throttled |
| KV value size | **1 MB** (also documented as 1 MiB) | Write rejected |
| KV key size | **8 KB** | Write rejected |

### 1.5 Key-value store specifics

- **NEVER share a KV store between apps.** → Stores are scoped to a single Spin application.
- **NEVER specify a `key_value_stores` label other than `"default"` in the manifest.** → Any other label is rejected at deploy.
- **NEVER call Akamai Functions KV via EdgeKV APIs.** → They are separate systems and not compatible.

### 1.6 Application variables

- **NEVER omit a required variable declared in `[variables]`.** → Missing / empty values must cause a `500` response (the function code is responsible for this guard).
- Variables marked `secret = true` are stored encrypted and must be referenced by the exact declared name.
- When set on the command line locally, variables must be prefixed with `SPIN_VARIABLE_` (e.g. `SPIN_VARIABLE_PG_CONNECTION_STRING`).

### 1.7 Modules / third-party packages

Only the following NPM packages are guaranteed available in JS/TS apps:

- `itty-router`
- `@spinframework/spin-variables`
- `@spinframework/spin-postgres`
- `@spinframework/spin-kv`
- `@aws-sdk/client-s3`

Importing any other third-party module may fail at build or runtime.

### 1.8 CLI constraints (`spin aka`)

- **NEVER set `--expiration-days` greater than `90`** on `auth token create`. → CLI rejects the value.
- **NEVER pass both `--account-id` and `--account-name`** simultaneously. → They are mutually exclusive; CLI ignores both and falls back to current context.
- **NEVER request `--usage-since` outside `5m`–`7d`** (inclusive). → Rejected.
- **NEVER omit `--schedule`** when creating a cron job. → Required.
- **NEVER omit `<NAME>`** for `cron delete`. → Required positional argument.

### 1.9 Project scaffolding (JS/TS apps)

- **NEVER hand-write `spin.toml`, `package.json`, `build.mjs`, or the build script for a JS/TS app.** → Always scaffold via `spin new -t http-js --accept-defaults <app-name>`. The template generates an **esbuild** step (`build.mjs`) that bundles `src/index.js` + everything under `node_modules` into a single ESM bundle at `build/bundle.js`, and then invokes the **`j2w`** componentizer to produce `dist/<app-name>.wasm`. Without that bundling step, the componentizer cannot resolve packages like `itty-router` and may not parse ES `import` syntax at all.
- **NEVER set `scripts.build` in `package.json` to invoke a JS→Wasm converter (`spin js2wasm`, `j2w`, etc.) directly on `src/index.js`.** → The legacy `spin js2wasm` plugin in particular traps during Wizer pre-initialization with `Uncaught SyntaxError: expecting '('` at the first `import` keyword and produces `Error: Couldn't create wasm from input`.
- After scaffolding, modify only: `src/index.js` (your code), `spin.toml`'s `[variables]` / `key_value_stores` / `allowed_outbound_hosts` entries on the component, and `package.json` `dependencies`. Do not touch `build.mjs`, `scripts.build`, or `[component.<name>.build]`.

---

## 2. Import Rules

All imports must be **static**, at the top of the file, using ES module syntax. Dynamic `import()` and CommonJS `require()` are not supported.

### 2.1 Routing

```js
import { AutoRouter } from 'itty-router';
```

### 2.2 Spin variables (application config / secrets)

```js
import { Variables } from '@spinframework/spin-variables';
```

> Some sample code uses `Variables` as a global without explicit import. Prefer the explicit static import.

### 2.3 PostgreSQL

```js
import { Postgres } from '@spinframework/spin-postgres';
```

### 2.4 Key-value store

```js
import { openDefault } from '@spinframework/spin-kv';
// or, for a non-default label (only `"default"` is currently provisioned):
import { Kv } from '@spinframework/spin-kv';
```

### 2.5 S3-compatible object store (e.g. Linode Object Storage)

```ts
import { S3Client, GetObjectCommand, ListObjectsV2Command } from '@aws-sdk/client-s3';
```

### 2.6 INCORRECT patterns (do not use)

```js
// ❌ CommonJS — `require` is undefined in the Spin runtime
const router = require('itty-router');

// ❌ Node built-ins — unavailable in the WASM sandbox
import fs from 'fs';
import http from 'http';
import crypto from 'crypto';

// ❌ Runtime dynamic import — not supported
const mod = await import('./helper.js');

// ❌ Reading config via process.env — `process` is undefined
const conn = process.env.PG_CONNECTION_STRING;
```

### 2.7 Build-time bundling is required

ES `import` statements only work because the scaffolded `build.mjs` (esbuild, see §1.9) inlines all imported modules into a single bundle at `build/bundle.js` prior to `j2w`. If that bundling step is skipped, every `import` line becomes a runtime parse error in the JS→Wasm converter. This is a property of the build pipeline, not the runtime — it is the reason §1.9 forbids hand-rolling the build script.

### 2.8 Handler-scoped vs module-scoped

- `openDefault()` / `Kv.open(label)` / `Postgres.open(connectionString)` / `new S3Client(...)` **must be called inside a request handler** (not at module top level). They depend on per-request capabilities.
- `AutoRouter()`, `new TextDecoder()`, `new TextEncoder()`, and constant headers may be declared at module scope.

---

## 3. Event Handler Reference

Akamai Functions exposes exactly **one** entry point: the HTTP `fetch` event. There are no per-phase handlers (`onClientRequest`, `onOriginRequest`, etc.).

### 3.1 The `fetch` handler

```js
addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

**Available on `event`:**

| Member | Type | Notes |
|---|---|---|
| `event.request` | `Request` (Fetch API) | Incoming HTTP request |
| `event.respondWith(response)` | `(Response | Promise<Response>) => void` | **Must be called** to produce a response |

**Permitted operations inside the handler:**

- Read Spin variables via `Variables.get(name)`.
- Open KV stores via `openDefault()` / `Kv.open(label)`.
- Open a Postgres connection via `Postgres.open(connectionString)`.
- Construct an S3 client via `new S3Client({ region, endpoint, credentials })`.
- Make outbound `fetch()` calls to hosts in `allowed_outbound_hosts`.
- Construct and return `Response` objects (including streamed bodies via `ReadableStream` / `TransformStream`).
- Pass per-request context to the router as the second argument to `router.fetch(request, context)`.

**Forbidden in the handler context:**

- Any Node built-in (`fs`, `net`, `http`, `crypto`, `path`, `buffer`, `child_process`).
- Filesystem access of any kind.
- `process.env`, `process.exit`, or any `process` member.
- Dynamic `import()` or `require()`.
- Outbound calls to hosts not in `allowed_outbound_hosts`.
- Calls to `localhost` or short Spin app names.

### 3.2 Early-failure variable validation pattern

Required when the function depends on Spin variables — abort with HTTP 500 before invoking the router:

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

### 3.3 Cron-triggered functions (Tech Preview)

A cron job invokes an existing HTTP route at the scheduled time. The handler is still the standard `fetch` listener; the cron schedule and target path are configured outside the code via `spin aka app cron create`.

---

## 4. API Reference

### 4.1 Router — `itty-router`

```ts
AutoRouter()
  : Router

router.get(path: string, handler: (request, context?) => Response | Promise<Response>): Router
router.post(path: string, handler: (request, context?) => Response | Promise<Response>): Router
router.put(path: string, handler: (request, context?) => Response | Promise<Response>): Router
router.delete(path: string, handler: (request, context?) => Response | Promise<Response>): Router
router.all(path: string, handler: (request, context?) => Response | Promise<Response>): Router

router.fetch(request: Request, context?: object): Promise<Response>
```

Behavior:

- The **first matching route wins**; later routes for the same method+path are not invoked.
- A handler that **returns no value is treated as middleware** and execution continues to the next matching route.
- Unmatched requests **automatically return 404** unless a catch-all (`router.all("*", ...)`) is registered.
- The second argument to `router.fetch(request, context)` is forwarded as the second argument to every route handler — use this to inject per-request config (DB connection string, S3 config, etc.).

### 4.2 Standard fetch globals

```ts
new Response(body?: BodyInit | null, init?: ResponseInit): Response
new Request(input, init?): Request
addEventListener('fetch', (event: FetchEvent) => void): void
event.respondWith(response: Response | Promise<Response>): void
fetch(input: RequestInfo, init?: RequestInit): Promise<Response>  // outbound; allowed_outbound_hosts required

new TextDecoder([label?, options?])
textDecoder.decode(buffer: ArrayBuffer | TypedArray, options?: { stream?: boolean }): string

new TextEncoder()
textEncoder.encode(input: string): Uint8Array

new TransformStream({ transform(chunk, controller) { ... } })
readableStream.pipeThrough(transform: TransformStream): ReadableStream
```

### 4.3 Spin Variables — `@spinframework/spin-variables`

```ts
Variables.get(name: string): string
```

- Returns the value of a variable declared under `[variables]` in `spin.toml`.
- Returns falsy (empty string) when the variable is missing/empty — the handler is responsible for guarding (typically responding `500`).
- Variables marked `secret = true` are decrypted on access.

### 4.4 Key-Value Store — `@spinframework/spin-kv`

```ts
openDefault(): Store                  // opens the store labeled "default"
Kv.open(label: string): Store         // only "default" is currently provisioned

store.exists(key: string): boolean
store.getJson(key: string): any       // deserializes JSON value
store.setJson(key: string, payload: any): void   // serializes JSON-serializable value
```

Underlying interfaces: `wasi:keyvalue/store` and `wasi:keyvalue/batch`. `wasi:keyvalue/atomic` is **not** supported.

Consistency: all standard operations exhibit **read-your-writes** behavior within a single request.

### 4.5 PostgreSQL — `@spinframework/spin-postgres`

```ts
Postgres.open(connectionString: string): Connection

connection.execute(sql: string, params: any[]): number
  // For INSERT / UPDATE / DELETE. Returns the number of affected rows.

connection.query(sql: string, params: any[]): { rows: any[] }
  // For SELECT. Returns an object with a `rows` array.
```

- The host (and port `5432`) must appear in `allowed_outbound_hosts` as `postgres://<host>:5432`.
- Open the connection inside the handler; pass the connection string via the router context.

### 4.6 S3-compatible object store — `@aws-sdk/client-s3`

```ts
new S3Client(config: {
  region: string;
  endpoint: string;
  credentials: {
    accessKeyId: string;
    secretAccessKey: string;
  };
}): S3Client

new ListObjectsV2Command(input: { Bucket: string }): Command
new GetObjectCommand(input: { Bucket: string; Key: string }): Command

s3.send(command): Promise<{
  Contents?: Array<{ Key?: string; ... }>;   // for ListObjectsV2Command
  Body?: ReadableStream;                      // for GetObjectCommand
  // ...
}>
```

The `Body` returned by `GetObjectCommand` is a `ReadableStream` and can be:
- returned directly: `new Response(Body as ReadableStream, { status: 200 })`
- piped through a `TransformStream` for streaming transformation.

### 4.7 `json()` helper (from `itty-router`)

```ts
json(data: any): Response  // returns a Response with JSON-encoded body and content-type
```

### 4.8 CLI — `spin aka` (Spin >= v3.0.0, plugin v0.7.0)

Equivalent JS object form is shown for reference; in practice these are shell commands.

```
spin aka login                       # Log into Akamai Functions (session ~30 days idle)
spin aka info                        # Print user and workspace information
spin aka deploy [-f <PATH>] [--variable KEY=VALUE|@FILE.json|@FILE.toml]...
                                     # Deploy current app (alias of `app deploy`).
                                     # `-f, --from` defaults to ./spin.toml.
spin aka logs [--app-name <NAME>] [--verbose] [--since <DURATION>] [--max-lines <N>]
                                     # Default --since is 7 days. Default --max-lines is 10.
spin aka app delete [--no-confirm]
spin aka app link
spin aka app unlink
spin aka app list
spin aka app status
spin aka app history
spin aka app cron create --schedule "<CRON>" [--name <NAME>] [--path-and-query <PATH>]
                                     # UNSTABLE / Tech Preview. --schedule REQUIRED.
spin aka app cron delete <NAME> [--no-confirm]
spin aka app cron list
spin aka auth login
spin aka auth token create --name <NAME> [--description <TEXT>] [--expiration-days <DAYS>] [--short]
                                     # --name REQUIRED. --expiration-days default 30, max 90.
spin aka auth token delete <NAME> [--no-confirm]
spin aka auth token list
spin aka auth token regenerate <NAME>
```

Duration syntax (`--since`, `--usage-since`): `s` (seconds), `m`, `h`, `d`. ISO-8601 timestamps also accepted. `--usage-since` is bounded to `5m`–`7d`.

`--account-id` and `--account-name` are mutually exclusive.

---

## 5. Cross-Reference

### 5.1 Object × event-handler availability

Akamai Functions has a **single event handler** (`fetch`). The "available" matrix is therefore trivial — every supported object is callable from inside the `fetch` listener, and **nowhere else**.

| Object / API | `fetch` handler | Module top level |
|---|---|---|
| `addEventListener('fetch', ...)` | — | ✅ (required) |
| `AutoRouter()` | ✅ | ✅ (preferred) |
| `router.fetch(req, ctx)` | ✅ | ❌ |
| `Variables.get(name)` | ✅ | ⚠️ Avoid — call inside handler |
| `openDefault()` / `Kv.open(label)` | ✅ | ❌ (needs request capabilities) |
| `Postgres.open(connStr)` | ✅ | ❌ |
| `new S3Client(...)` | ✅ | ❌ |
| `s3.send(cmd)` | ✅ | ❌ |
| `fetch(url, init)` (outbound) | ✅ | ❌ |
| `new Response(...)` | ✅ | ✅ (for constants) |
| `new TextEncoder/Decoder()` | ✅ | ✅ |
| `new TransformStream(...)` | ✅ | ✅ |

### 5.2 Object × object interaction

```
addEventListener('fetch') ──► event.respondWith( Response | router.fetch(event.request, ctx) )

router (AutoRouter)
  ├── .get/.post/.put/.delete/.all( path, handler )
  └── handler(request, ctx)
        ├── Variables.get(name)             → string                     (Spin variables)
        ├── openDefault()                   → Store                      (KV)
        │     └── store.exists / getJson / setJson
        ├── Postgres.open(connectionString) → Connection                 (PostgreSQL)
        │     └── conn.query / conn.execute
        ├── new S3Client({ region, endpoint, credentials })              (S3-compatible)
        │     └── s3.send( new ListObjectsV2Command | new GetObjectCommand )
        │             └── result.Body (ReadableStream)
        │                   └── .pipeThrough( new TransformStream({transform}) )
        │                          └── new Response(transformed, init)
        └── fetch(url, init)                → Response                   (outbound HTTP)
```

### 5.3 Required `spin.toml` capability declarations by API

| API used | Required in `spin.toml` |
|---|---|
| `Variables.get(name)` | `[variables]` entry for `name`; pass via `--variable name=value` at deploy |
| `openDefault()` | `key_value_stores = ["default"]` on the component |
| `Postgres.open(...)` | `allowed_outbound_hosts = ["postgres://<host>:5432"]` |
| `new S3Client({ endpoint, ... })` then `s3.send(...)` | `allowed_outbound_hosts` includes the S3 endpoint (e.g. `"https://.<region>.linodeobjects.com"` or `"https://."`) |
| outbound `fetch(url, ...)` | `allowed_outbound_hosts` includes the target host (and inter-Function calls must use full `https://<app-id>.fwf.app`) |

### 5.4 Module → API → consequence-on-misuse

| Module | Provides | Forgetting required setup causes |
|---|---|---|
| `itty-router` | `AutoRouter`, `json` | Without `event.respondWith(router.fetch(...))` no requests are answered |
| `@spinframework/spin-variables` | `Variables.get` | Without `[variables]` entry, returns empty → handler must respond 500 |
| `@spinframework/spin-kv` | `openDefault`, `Kv.open` | Without `key_value_stores = ["default"]`, store operations fail |
| `@spinframework/spin-postgres` | `Postgres.open`, `query`, `execute` | Without `allowed_outbound_hosts`, connection blocked |
| `@aws-sdk/client-s3` | `S3Client`, `GetObjectCommand`, `ListObjectsV2Command` | Without `allowed_outbound_hosts`, `s3.send` fails |

---

## 6. Known Failure Patterns

### 6.1 Using `require()` or Node built-ins

```js
// ❌ WRONG — `require` is undefined; `fs` does not exist
const fs = require('fs');
const data = fs.readFileSync('./config.json');

// ✅ CORRECT — static ES import; never touch the filesystem
import { Variables } from '@spinframework/spin-variables';
const data = Variables.get('config_json');
```
**Symptom:** Runtime `ReferenceError: require is not defined` or module load failure (`fs` not available in the Spin runtime).

---

### 6.2 Reading config from `process.env`

```js
// ❌ WRONG — `process` is undefined in the WASM sandbox
const conn = process.env.PG_CONNECTION_STRING;

// ✅ CORRECT — Spin variables
const conn = Variables.get('pg_connection_string');
if (!conn) {
  return new Response(JSON.stringify({ message: "Connection String not specified" }),
    { status: 500, headers: { "content-type": "application/json" } });
}
```
**Symptom:** `TypeError: Cannot read properties of undefined (reading 'env')`.

---

### 6.3 Calling another Spin app via localhost

```js
// ❌ WRONG — localhost / short names do not resolve between Spin apps
const res = await fetch('http://my-other-app/api');

// ✅ CORRECT — full public URL
const res = await fetch('https://<app-id>.fwf.app/api');
```
**Symptom:** outbound request fails with name-resolution / not-allowed error.

---

### 6.4 Outbound host not in `allowed_outbound_hosts`

```toml
# ❌ WRONG — S3 endpoint missing
[component.my-app]
allowed_outbound_hosts = []

# ✅ CORRECT — explicit allowlist
[component.my-app]
allowed_outbound_hosts = ["https://us-east-1.linodeobjects.com"]
```
**Symptom:** `s3.send(...)` / `fetch(...)` rejects with permission/blocked error inside the function.

---

### 6.5 Bypassing the router

```js
// ❌ WRONG — calling handlers directly bypasses parameter parsing
addEventListener('fetch', async (event) => {
  event.respondWith(listFiles(config));  // no params, no method dispatch
});

// ✅ CORRECT — go through router.fetch with per-request context
addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request, { config }));
});
```
**Symptom:** route params (`:name`) are `undefined`; method dispatch is broken; unmatched paths do not return 404.

---

### 6.6 Reading request body incorrectly

```js
// ❌ WRONG — `request.body` is a stream, not parsed JSON
const payload = request.body;

// ✅ CORRECT — read ArrayBuffer, decode, then parse
const decoder = new TextDecoder();
const bytes = await request.arrayBuffer();
const payload = JSON.parse(decoder.decode(bytes));
```
**Symptom:** `payload` is a `ReadableStream` instance; property access yields `undefined`.

---

### 6.7 Returning `undefined` from a route handler

```js
// ❌ WRONG — handler returns nothing; itty-router treats this as middleware
router.get("/health", () => { console.log("ok"); });

// ✅ CORRECT — always return a Response
router.get("/health", () => new Response("ok", { status: 200 }));
```
**Symptom:** request continues to the next matching route or falls through to the auto-404.

---

### 6.8 Wrong KV manifest label

```toml
# ❌ WRONG — only "default" is accepted today
[component.my-app]
key_value_stores = ["my-store"]

# ✅ CORRECT
[component.my-app]
key_value_stores = ["default"]
```
**Symptom:** deploy is rejected.

---

### 6.9 Using `wasi:keyvalue/atomic`

```js
// ❌ WRONG — atomic interface is not supported
import { increment } from 'wasi:keyvalue/atomic';

// ✅ CORRECT — use the store interface
import { openDefault } from '@spinframework/spin-kv';
const store = openDefault();
const current = store.exists('counter') ? store.getJson('counter') : 0;
store.setJson('counter', current + 1);
```
**Symptom:** module-load failure / "not supported".

---

### 6.10 Writing logs to a file

```js
// ❌ WRONG — no filesystem; logs are lost
import fs from 'fs';
fs.appendFileSync('/tmp/log.txt', 'hello');

// ✅ CORRECT — log to stdout/stderr; captured by `spin aka logs`
console.log('hello');
console.error('oops');
```
**Symptom:** function fails to load (`fs` unavailable) or — if guarded — log lines never appear in `spin aka logs`.

---

### 6.11 Opening clients at module top level

```js
// ❌ WRONG — request-scoped capabilities may not be ready at module init
import { openDefault } from '@spinframework/spin-kv';
const store = openDefault();                  // top-level

// ✅ CORRECT — open inside the handler
function handleGetValue(key) {
  const store = openDefault();
  if (!store.exists(key)) return new Response(null, { status: 404 });
  return new Response(JSON.stringify(store.getJson(key)),
    { status: 200, headers: { "content-type": "application/json" } });
}
```
**Symptom:** initialization error or "not supported" at cold start.

---

### 6.12 Exceeding KV value or key size

```js
// ❌ WRONG — value > 1 MB or key > 8 KB
store.setJson('huge', new Array(10_000_000).fill('x'));

// ✅ CORRECT — chunk large payloads or store in object storage
```
**Symptom:** write rejected by KV.

---

### 6.13 Bundle / response size

- Bundle > **50 MiB** → deploy rejected.
- Response body > **10 MiB** → response truncated/rejected. Stream large bodies via `ReadableStream` to stay within per-request limits where possible.

---

### 6.14 CLI: `--expiration-days` > 90

```bash
# ❌ WRONG
spin aka auth token create --name ci --expiration-days 365

# ✅ CORRECT — max 90
spin aka auth token create --name ci --expiration-days 90
```
**Symptom:** CLI rejects the command.

---

### 6.15 CLI: both `--account-id` and `--account-name`

```bash
# ❌ WRONG — mutually exclusive
spin aka app list --account-id abc --account-name "My Account"

# ✅ CORRECT — pick one
spin aka app list --account-name "My Account"
```
**Symptom:** both flags are ignored; command falls back to current context (silent surprise).

---

### 6.16 Hand-rolled `package.json` instead of `spin new` scaffolding

```json
// ❌ WRONG — runs a JS→Wasm converter directly on ES-module source; no bundler
{ "scripts": { "build": "spin js2wasm -o target/app.wasm src/index.js" } }

// ✅ CORRECT — verbatim from `spin new -t http-js --accept-defaults <name>`
//   (esbuild bundles via build.mjs, then j2w componentizes the bundle)
{ "scripts": {
  "build": "node build.mjs && mkdirp dist && j2w -i build/bundle.js --initLocation http://<app-name>.localhost -o dist/<app-name>.wasm"
} }
```

The corresponding `[component.<name>.build]` in the scaffolded `spin.toml` is:

```toml
[component.<name>.build]
command = ["npm install", "npm run build"]
watch = ["src/**/*.js"]
```

**Symptom (verbatim) when the hand-rolled `spin js2wasm` path is used:**

```
thread '<unnamed>' panicked at 'called `Result::unwrap()` on an `Err` value:
  Uncaught SyntaxError: expecting '('
    at script.js:1
', crates/spin-js-engine/src/lib.rs:1306:15
Error: the `wizer.initialize` function trapped
Error: Couldn't create wasm from input
```

**Why it fails:** the `js2wasm` plugin embeds a QuickJS engine that parses input as a *classic script*, not an ES module, and has no module resolver for `node_modules`. The first `import` keyword in `src/index.js` triggers `SyntaxError: expecting '('` (QuickJS expected the dynamic-import expression `import(...)`). The scaffolded template avoids this by bundling with esbuild first and then componentizing the single-file bundle with `j2w`.

**Fix:** delete the hand-rolled `package.json` / `spin.toml` / build script, run `spin new -t http-js --accept-defaults <app-name>` in a clean directory, then copy your `src/index.js` over the scaffolded one and re-add only the `dependencies` / `[variables]` / `key_value_stores` / `allowed_outbound_hosts` entries your code requires.

---
