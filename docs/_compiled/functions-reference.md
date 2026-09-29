# Akamai Functions — Unified Coding Reference

> Master reference for generating Akamai Functions code (Spin applications compiled to WebAssembly).
> Compiled from exact upstream Markdown sources in `docs/_source/techdocs-akamai-com/`.

## 1. Runtime Prohibitions

Each entry states a platform, runtime, deployment, or tooling constraint and its documented consequence. When a source does not state the exact enforcement error, the entry says so rather than inventing one. Defaults and other facts that restrict nothing are in §4.

### 1.1 Platform and runtime

**Sources:** [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md)

- Akamai Functions runs Spin applications compiled to WebAssembly. Code that is not compiled to WebAssembly cannot run on the platform.
- A language needs WASI support (at least Preview 1) or a Spin SDK to run; either one is sufficient. Rust, Go, JavaScript, and Python are highlighted as production suggestions, which is a recommendation and not an exclusive support list. Languages with neither are not documented to run.
- Deployment to Akamai Functions goes through the `spin aka` plugin; no other deployment path is documented.
- The platform is in limited availability / Public Preview. Users without preview access (sign-up and onboarding) cannot log in and deploy.
- Configuration cannot be hot-swapped at runtime. Changing application variables creates a new deployment and increments the version.
- Only the `http` trigger type is supported. A manifest that uses another or a custom trigger cannot run on Akamai Functions.
- SQLite storage is not supported on Akamai Functions. Local KV testing persists to `.spin/sqlite_key_value.db`, but that is local tooling, not a platform capability available to a deployed application.
- The Redis trigger is not supported, so a Redis-triggered component cannot be deployed. Outbound Redis is a separate, supported API.
- `wasi-blobstore` and `wasi-messaging` are not supported in Spin or Akamai Functions. Components that require either interface cannot run.
- Serverless AI is available only under Limited Access. Code cannot assume access to it.

### 1.2 Execution and storage quotas

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md)

- Memory per function execution is limited to 128 MiB. The source does not state the termination or error text when the limit is exceeded.
- Total application size is limited to 50 MiB. The source does not state the deployment error for an oversized application.
- A request handler can run for at most 30 seconds. The source does not state the termination or error text when the limit is exceeded.
- A request or response can be at most 10 MiB. The source does not state whether an oversized payload is rejected or truncated.
- Total KV storage across all store instances is limited to 2 GB. The source does not state the write error when the quota is exceeded.
- KV reads are limited to 1,000 requests per second. This is an experimentation-level limit; the source does not state the throttling response.
- KV writes are limited to 50 requests per second. This is an experimentation-level limit; the source does not state the throttling response.
- A KV value can be at most 1 MB. The source does not state the write error for an oversized value.
- A KV key can be at most 8 KB. The source does not state the write error for an oversized key.

The dedicated quotas page defines 30 seconds as the request-handler limit. The comparison page separately describes Akamai Functions execution time as “30 seconds default, extendable.” These statements conflict. Use 30 seconds as the canonical generated limit and do not assume an extension is available unless Akamai explicitly grants one.

KV query-rate limits are described as experimentation-level limits and can be increased by customer request.

### 1.3 Key-value store

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md)

- `wasi:keyvalue/atomic` is not supported. A component that imports it cannot use that capability.
- The only `key_value_stores` label Akamai Functions accepts is `"default"`. The source does not state the exact error for another label.
- A KV store is scoped to a single application. Another application cannot access the same store.
- EdgeKV is not compatible with Akamai Functions. EdgeKV APIs cannot access the Akamai Functions KV store. The use-cases page separately describes a Function pushing data into EdgeKV Admin APIs; that cross-service integration (§4.12, §4.19) does not make the two stores interchangeable.

### 1.4 Outbound networking and databases

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md)

- Every outbound target has to be listed in `allowed_outbound_hosts` in `spin.toml`. The capabilities-based security model denies requests to unlisted hosts. The comparison page's “outbound HTTP to any hostname” means Functions is not limited to Akamized hostnames as EdgeWorkers is; it does not remove the allowlist.
- `localhost` and short service names do not resolve to other applications the way Docker Compose or Kubernetes service names do. Inter-application calls use the full public URL, such as `https://<app-id>.fwf.app`.
- A MySQL entry in `allowed_outbound_hosts` needs the `mysql://` protocol. Without it, the MySQL outbound capability is not granted.
- PostgreSQL outbound connectivity is configured with `postgres://` and port `5432`. Without that entry, the PostgreSQL request lacks the outbound capability.
- The documented MySQL and PostgreSQL integrations read the connection string through `Variables.get(...)` from a component variable mapping. An unmapped variable is not available to the component.
- The documented database integrations use the Spin SDK packages `@spinframework/spin-mysql` (`Mysql.open(connectionString)`) and `@spinframework/spin-postgres` (`Postgres.open(connectionString)`). Without the package, the `open` call is not available.

### 1.5 Application variables and deployment versions

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

- `Variables.get()` can read only variables linked to the component in its manifest configuration. An unlinked variable is not accessible.
- The key in `spin.toml` and the string passed to `Variables.get()` have to match exactly. A mismatched key does not retrieve the intended value.
- In the object-store tutorial, a handler with any empty required variable returns HTTP `500` with `Application not configured correctly` instead of continuing.
- The update guide instructs users to supply required application variables again on the new `spin aka deploy`. It does not document the runtime result of omitting a previously supplied value.
- A `spin aka deploy --variable ...` override is not a live runtime change. It creates a new deployment and increments the version.
- Application variables are encrypted at rest and in transit, but the underlying cryptographic implementations have not been assessed for PCI compliance.

### 1.6 Updates, deletion, and account security

**Sources:** [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md)

- Akamai Functions does not route traffic to multiple application versions at once, so canary and blue-green routing are unavailable. In-flight requests finish on the previous version, then traffic uses the update.
- Deleting an application is permanent and cannot be undone.
- Team accounts have no role-based access control. Every member has the same permissions and can permanently delete any application in the account.

### 1.7 Cron jobs

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

- Cron jobs are Tech Preview and marked `UNSTABLE` in the CLI, so command behavior can change.
- All cron schedules are interpreted in UTC. A schedule written in local time runs at a different local time than intended.
- Within one application, each combination of schedule and path-and-query has to be unique. The source does not state the error returned for a duplicate.
- `spin aka [app] cron create` requires `--schedule <SCHEDULE>` (usage line `spin aka app cron create [OPTIONS] --schedule <SCHEDULE>`). The source does not reproduce the CLI's error for an incomplete command.
- `spin aka [app] cron delete` requires the positional `<NAME>` of the job to delete.

### 1.8 Language and toolchain constraints

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

- The object-store tutorial lists Node.js 22 or later as a prerequisite. The quickstart recommends Node.js 22 or newer and the MySQL tutorial recommends at least Node.js 21. These are tutorial prerequisites and recommendations, not platform-wide minimum versions.
- The documented Go component is built with TinyGo 0.27 or above, because the standard Go compiler cannot produce the required WASI exports.
- The documented Go SDK build requires `CGO_ENABLED=1`.
- The documented Rust component is compiled for the `wasm32-wasip1` target. Without that target installed, the Rust toolchain cannot produce the required artifact.
- An application has to be compiled to WebAssembly before deployment, with `spin build` or the `spin aka deploy --build` option for a local application.

### 1.9 CLI constraints

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

- The command reference lists `Spin compatibility: >=v4.0.0` for every `spin aka` command. It does not state what happens with older Spin versions. Two other sources give different version guidance, listed in §4.17: the quotas page says “Spin CLI v0.6.0 or newer,” and the quickstart's Windows instructions link to the Spin v3.6.2 binary release. The sources do not reconcile these.
- A personal access token's expiration can be at most 90 days (`--expiration-days`, `[max: 90]`). Once a token expires, a new token has to be created to keep using it in a CI/CD pipeline.
- A new personal access token is displayed only once. If it is not saved, a new token has to be created or the existing one regenerated.
- `spin aka app status --usage-since` accepts a window of at least 5 minutes and at most 7 days; the CLI enforces this range. No range is documented for `spin aka logs --since`, so the status range does not carry over to logs.

### 1.10 Property Manager integration

**Sources:** [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md)

- The property's Origin Hostname is the Spin application URL with `https://` and the trailing `/` removed. A value that keeps either one is not the documented hostname form.
- **Forward Host Header** has to be set to `Origin Hostname`. With another value, requests are not forwarded to the function as documented.

---

## 2. Import Rules

The source articles prescribe the following module imports. They do **not** state a general rule that all imports must be static, nor do they state that dynamic `import()` is unsupported.

### 2.1 Router and HTTP helpers

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

```javascript
import { AutoRouter } from 'itty-router';
```

When returning JSON or using custom request typing:

```typescript
import { AutoRouter, json, IRequest } from 'itty-router';
```

### 2.2 Application variables

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

```typescript
import * as Variables from "@spinframework/spin-variables";
```

Correct access:

```javascript
const connectionString = Variables.get("pg_connection_string");
```

### 2.3 Key-value store

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

Named-import pattern:

```javascript
import { openDefault } from '@spinframework/spin-kv';
```

Namespace-import pattern:

```typescript
import * as Kv from "@spinframework/spin-kv";
```

Use the matching call for the import style: `openDefault()` for the named import, or `Kv.openDefault()` for the namespace import.

### 2.4 MySQL

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md)

```typescript
import * as Mysql from "@spinframework/spin-mysql";
```

### 2.5 PostgreSQL

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

```javascript
import * as Postgres from "@spinframework/spin-postgres";
```

### 2.6 UUID

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

```javascript
import { v4 as uuidv4 } from 'uuid';
import { validate as uuidValidate } from 'uuid';
```

### 2.7 Supabase

**Sources:** [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

```typescript
import { createClient } from '@supabase/supabase-js';
```

### 2.8 S3-compatible object storage and streams

**Sources:** [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

```typescript
import { S3Client, GetObjectCommand, ListObjectsV2Command } from '@aws-sdk/client-s3';
```

`TransformStream`, `TextDecoder`, and `TextEncoder` are available globals in the runtime environment.

### 2.9 Rust

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;
```

The handler also uses `anyhow::Result`.

### 2.10 Go

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

```go
import (
    spinhttp "github.com/spinframework/spin/sdk/go/v2/http"
)
```

The handler uses the standard `http.ResponseWriter`, `http.Request`, and `fmt.Fprintln` APIs.

---

## 3. Event Handler Reference

Akamai Functions currently supports only the `http` trigger. Cron does not introduce a second language-level event handler: it invokes an HTTP path in the deployed application.

### 3.1 JavaScript/TypeScript `fetch` event

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

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
| `event.request` | Pass incoming request to `router.fetch(...)` | Entry point registered with `addEventListener('fetch', ...)` |
| `event.respondWith(responseOrPromise)` | Return HTTP result to client | Required by the documented JS/TS entry-point pattern |
| `request.headers.get(name)` | Read request and injected Spin headers | `spin-path-match-n` exists only when that wildcard is in the route |
| `request.arrayBuffer()` | Read request body | Decode with `TextDecoder` before `JSON.parse(...)` |
| `router.fetch(event.request, context)` | Dispatch and pass per-request context | Route ordering matters; first matching route wins |
| `Variables.get(key)` | Read linked application variable | Declare and link in manifest before accessing |
| `Mysql.open(...)`, `Postgres.open(...)`, `openDefault()` / `Kv.openDefault()` | Open host resources used by route | Required manifest capabilities/configuration must be present |
| `new S3Client(...)` and `s3.send(...)` | Access S3-compatible storage | Endpoint must be allowed in `allowed_outbound_hosts` |
| outbound `fetch(fullPublicUrl, init)` | Chain to another application | Use full public URL, never localhost or short names |
| `new URL(request.url)` | Parse URL and query parameters | Used by cron-invoked routes |
| `new Date().toISOString()` and `console.log(...)` | Timestamp and log an invocation | Logs go to stdout/stderr and are retrieved with `spin aka logs` |

Handler-specific forbidden operations:

- A JS/TS application must **not** omit `addEventListener('fetch', ...)` or `event.respondWith(...)`; it then lacks the documented request/response lifecycle.
- Read request bodies with the documented `req.arrayBuffer()` / `request.arrayBuffer()` pattern and decode them with `TextDecoder` before parsing JSON.
- Read component-linked application variables with `Variables.get(...)`, as shown by the exact database and object-store integrations.
- Database, S3, and outbound HTTP access must **not** target a host absent from `allowed_outbound_hosts`.

#### Variable/context validation pattern

```javascript
addEventListener('fetch', async (event) => {
    const connectionString = Variables.get("pg_connection_string");
    if (!connectionString) {
        return event.respondWith(new Response(
            JSON.stringify({ message: "Connection String not specified" }),
            { status: 500, headers: DEFAULT_HEADERS }
        ));
    }
    event.respondWith(router.fetch(event.request, { connectionString }));
});
```

### 3.2 Rust HTTP component handler

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

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

- `#[http_component]` marks the function as the HTTP component entry point.
- The handler receives `spin_sdk::http::Request` and returns `anyhow::Result<impl IntoResponse>`.
- Compile for the `wasm32-wasip1` target.

### 3.3 Go HTTP handler

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

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

- Register the handler through `spinhttp.Handle(...)` in `init()`.
- The callback uses `http.ResponseWriter` and `*http.Request`.
- Build with TinyGo 0.27 or above and `CGO_ENABLED=1`; standard Go cannot emit the required WASI exports.

### 3.4 Cron invocation of an HTTP route

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

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

The cron service invokes the configured path; the code receives the standard HTTP `fetch` event. Schedules are UTC and the schedule/path-and-query pair must be unique per application.

---

## 4. API Reference

### 4.1 HTTP trigger manifest and injected headers

**Sources:** [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md)

```toml
[[trigger.http]]
route = "/..."
component = "my-application"
```

Injected Spin headers and client headers:

| Header | Meaning |
|---|---|
| `spin-full-url` | Full request URL including host and scheme |
| `spin-path-info` | Request path relative to the component route |
| `spin-path-match-n` | Wildcard value, where `n` is the segment name (e.g. `spin-path-match-userid`) |
| `spin-matched-route` | Matched part of the trigger route |
| `spin-raw-component-route` | Component route pattern that matched |
| `true-client-ip` | IP address of the client sending the request |

Wildcard access pattern:

```javascript
// Access the 'userid' wildcard value from a route matching a wildcard segment
const userId = request.headers.get('spin-path-match-userid');
```

`spin-path-match-n` is conditional: it is present only when the route definition contains that wildcard segment.

### 4.2 JavaScript/TypeScript HTTP and routing APIs

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

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
event.respondWith(promise)
request.arrayBuffer()
request.headers.get(name)
new TextDecoder().decode(buffer)
new URL(request.url)
new Date().toISOString()
console.log(message)
```

Router behavior from the sources:

- Routes can be chained from `AutoRouter()`.
- The first matching route is used; route ordering matters.
- Any route that does not return will be treated as middleware.
- Unmatched routes return `404` unless handled by a fallback route.
- Route parameters appear as `({ name })`, `({ params })`, or `request.params`.
- The second argument to `router.fetch(request, context)` is received as the second route-handler argument, for example `{ connectionString }` or `{ config }`.
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

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

```text
Variables.get(key)
Variables.get(key: string)
Variables.get("key")
```

- Retrieves a value defined in `spin.toml` and linked to the component.
- Keys must match exactly.
- Variables must be linked through the component's `[component.<name>.variables]` section before `Variables.get(...)` can access them.
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

[component.linode-mysql.variables]
mysql_connection_string = "mysql://{{ mysql_user }}:{{ mysql_password }}@{{ mysql_host }}:{{ mysql_port }}/{{ mysql_database }}"
```

Deploy-time override:

```shell
spin aka deploy --variable compression_level=3
```

### 4.4 Key-value store — `@spinframework/spin-kv`

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

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
- `exists(key)` checks for key existence.
- `getJson(key)` retrieves and JSON-decodes a value.
- `setJson(key, value)` JSON-encodes and stores a value.
- `delete(key)` removes a key/value pair.
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
import { AutoRouter } from 'itty-router';

const router = AutoRouter();

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

Canonical operations:

```javascript
const store = openDefault();

if (!store.exists(key)) {
    return new Response(null, { status: 404 });
}

let found = store.getJson(key);
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
};

const onlyValidCacheData = (cacheItem: CacheData): any | undefined => {
  const now = new Date();
  const expiresAt = new Date(cacheItem.expiresAt);
  if (now > expiresAt) {
    return undefined;
  }
  return cacheItem.data;
};
```

#### List-cache invalidation

```typescript
import * as Kv from "@spinframework/spin-kv";

export const ALL_ARTICLES_CACHE_KEY = "all-articles";

export function storeInCache(key: string, value: any, ttl: number) {
  const store = Kv.openDefault();
  store.setJson(key, buildCacheData(value, ttl));

  if (key !== ALL_ARTICLES_CACHE_KEY && store.exists(ALL_ARTICLES_CACHE_KEY)) {
    store.delete(ALL_ARTICLES_CACHE_KEY);
  }
}

export function invalidate(key: string) {
  const store = Kv.openDefault();
  if (store.exists(key)) {
    store.delete(key);
  }
  if (key !== ALL_ARTICLES_CACHE_KEY && store.exists(ALL_ARTICLES_CACHE_KEY)) {
    store.delete(ALL_ARTICLES_CACHE_KEY);
  }
}
```

### 4.5 MySQL — `@spinframework/spin-mysql`

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md)

```text
Mysql.open(connectionString: string)
connection.execute(sql: string, params: any[])
connection.query(sql: string, params: any[])
connection.rows
```

- `Mysql.open` opens a MySQL connection.
- `connection.execute` runs INSERT/UPDATE/DELETE and returns the number of affected rows.
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

[component.linode-mysql.variables]
mysql_connection_string = "mysql://{{ mysql_user }}:{{ mysql_password }}@{{ mysql_host }}:{{ mysql_port }}/{{ mysql_database }}"
```

Full router and entry-point pattern:

```typescript
import * as Variables from "@spinframework/spin-variables";
import * as Mysql from "@spinframework/spin-mysql";
import { AutoRouter } from "itty-router";

const router = AutoRouter();
const decoder = new TextDecoder();

router
    .post("/products", async (request, { connectionString }) => createProduct(await request.arrayBuffer(), connectionString))
    .get("/products", async (_, { connectionString }) => readAllProducts(connectionString))
    .all("*", () => notFound("Endpoint not found"));

addEventListener('fetch', async (event: FetchEvent) => {
    const connectionString = Variables.get("mysql_connection_string");
    if (!connectionString) {
        return event.respondWith(new Response(JSON.stringify({ message: "Connection String not specified" }), { status: 500 }));
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

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

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
import { v4 as uuidv4, validate as uuidValidate } from 'uuid';

const router = AutoRouter();
const decoder = new TextDecoder();
const DEFAULT_HEADERS = { "content-type": "application/json" };

router
    .post("/products", async (request, { connectionString }) => createProduct(await request.arrayBuffer(), connectionString))
    .get("/products", async (_, { connectionString }) => readAllProducts(connectionString))
    .get("/products/:id", async ({ params }, { connectionString }) => readProductById(params.id, connectionString))
    .put("/products/:id", async (request, { connectionString }) => updateProductById(request.params.id, await request.arrayBuffer(), connectionString))
    .delete("/products/:id", async ({ params }, { connectionString }) => deleteProductById(params.id, connectionString))
    .all("*", () => notFound("Endpoint not found"));

addEventListener('fetch', async (event) => {
    const connectionString = Variables.get("pg_connection_string");
    if (!connectionString) {
        return event.respondWith(new Response(JSON.stringify({ message: "Connection String not specified" }), { status: 500, headers: DEFAULT_HEADERS }));
    }
    event.respondWith(router.fetch(event.request, { connectionString }));
});
```

### 4.7 Supabase client — `@supabase/supabase-js`

**Sources:** [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

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
};
```

### 4.8 S3-compatible object storage — `@aws-sdk/client-s3`

**Sources:** [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

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

const endpoint = Variables.get("endpoint");
const accessKeyId = Variables.get("access_key_id");
const secretAccessKey = Variables.get("secret_access_key");
const bucketName = Variables.get("bucket_name");
const region = Variables.get("region");

if (!endpoint || !accessKeyId || !secretAccessKey || !bucketName || !region) {
    return new Response("Application not configured correctly", { status: 500 });
}
```

Streaming response:

```typescript
import { GetObjectCommand } from '@aws-sdk/client-s3';

const { Body } = await s3.send(new GetObjectCommand(input));
return new Response(Body as ReadableStream, {
    status: 200,
});
```

Transforming a streamed body:

```typescript
const upperCaseTransform = new TransformStream({
    transform(chunk, controller) {
        const txt = dec.decode(chunk, { stream: true });
        controller.enqueue(enc.encode(txt.toUpperCase()));
    }
});

const transformed = (Body as ReadableStream).pipeThrough(upperCaseTransform);
return new Response(transformed, { status: 200 });
```

`Body` must be cast to `ReadableStream` before it is used as a `Response` body or piped through `TransformStream`.

### 4.9 UUID

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

```text
uuidv4()
uuidValidate(id: string)
```

- `uuidv4()` generates a UUID v4 string.
- `uuidValidate(id)` tests whether a string is a valid UUID.

### 4.10 Logging

**Sources:** [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md)

```text
console.log(message)
spin aka logs [OPTIONS]
spin aka app logs [OPTIONS]
```

- Akamai Functions captures everything written to stdout and stderr.
- `spin aka logs` defaults to the application linked to the workspace; use `--app-name` to target another application.
- The application-logs article documents Go's `log/slog` package for generating messages and says its example application is written in Go.

### 4.11 Rust and Go HTTP APIs

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

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

### 4.12 Other platform interfaces

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md)

- `HTTP` — supported incoming trigger.
- `Outbound HTTP` — supported to non-Akamized and third-party hostnames with capability allowlisting in `spin.toml`; “any hostname” in the comparison page does not remove the allowlist requirement.
- `Application Variables` — supported configuration API.
- `Key Value Storage` / `wasi-keyvalue` — supported through `wasi:keyvalue/store` and `wasi:keyvalue/batch` at the 2024-10-17 snapshot.
- `MySQL` and `PostgreSQL` — supported outbound database APIs.
- `Outbound Redis` — supported for customer-managed Redis; distinct from the unsupported Redis trigger. The comparison page says Akamai does not currently provide managed Redis.
- `wasi-config` — supported at the 2024-09-27 snapshot.
- `Component dependencies` — supported.
- Serverless AI — Limited Access only.
- External AI inference orchestration — the use-cases page describes AI agents that integrate with inference calls and explicitly says inference itself runs outside Functions. Do not turn that example into a claim of generally available in-runtime inference.
- EdgeKV Admin API interaction — the use-cases page says Functions can push data into EdgeKV Admin APIs. This is a cross-service integration, not access to the separate Functions KV store.

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

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md)

The command reference shows `--help` output for plugin v0.7.6 (newest), v0.7.0, and, for some commands, v0.4.0. Each command heading carries a single `Spin compatibility: >=v4.0.0` line above all of its version blocks; the page does not map individual plugin versions to Spin versions. The signatures below are from the v0.7.6 output.

Top-level commands (`spin aka --help`): `app`, `cron` (UNSTABLE), `deploy`, `logs`, `auth`, `login`, `send-feedback`, `info`, `help`. Options: `-h, --help`, `-V, --version`. In v0.7.6 `-V, --version` appears only on the top-level command; v0.7.0 subcommands also listed it.

Dedicated command-reference signatures (v0.7.6):

```text
spin aka app cron create [OPTIONS] --schedule <SCHEDULE>
spin aka app cron delete [OPTIONS] <NAME>
spin aka app cron list [OPTIONS]
spin aka app delete [OPTIONS]
spin aka app deploy [OPTIONS]
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
spin aka auth token regenerate --id <ID>
spin aka cron create [OPTIONS] --schedule <SCHEDULE>
spin aka cron delete [OPTIONS] <NAME>
spin aka cron list [OPTIONS]
spin aka deploy [OPTIONS]
spin aka info [OPTIONS]
spin aka login [OPTIONS]
spin aka logs [OPTIONS]
spin aka send-feedback
```

In v0.7.6, `spin aka app deploy` and `spin aka app logs` have the same help text and options as the top-level `deploy` and `logs` apart from the usage line, and `spin aka app cron` lists the same `list`, `create`, and `delete` subcommands as `spin aka cron`. v0.7.6 also documents `help` subcommands (`spin aka help`, `spin aka app help`, `spin aka app cron help`, `spin aka auth help`, `spin aka auth token help`, `spin aka cron help`) that print the parent command's usage.

Shared selector options (on most app-scoped commands):

- `--account-id <ACCOUNT_ID>` / `--account-name <ACCOUNT_NAME>`: account to operate in; if neither is given, the current account context is used.
- `--app-id <APP_ID>` / `--app-name <APP_NAME>`: app to operate on; if neither is given, the app is inferred from the workspace config.
- `-f, --from <PATH>`: a `spin.toml` file or a directory containing one; defaults to `./spin.toml`.
- `--format <FORMAT>`: `plain` (default) or `json` on `app list`, `app status`, `app history`, and `info`; `auth token create` also accepts `table` and `yaml` (default `plain`), and `auth token list` accepts `plain`, `table`, `json`, and `yaml` (default `table`).

Per-command options (v0.7.6):

| Command | Options and defaults |
|---|---|
| `deploy` / `app deploy` | `--build` (run `spin build` first for local apps; ignored for remote apps; env `SPIN_ALWAYS_BUILD`); `--cache-dir <CACHE_DIR>`; `--variable <KEY=VALUE \| @FILE.json \| @FILE.toml>` (repeatable; for a duplicated key the last value is used); `--app-id` (if omitted, the app is inferred from the workspace config, and if none is inferred a new app is created); `--create-name <NEW_APP_NAME>` (only when deploying to an app that does not exist yet); `--no-confirm`; `--skip-readiness-check`; account selectors; `--from` |
| `logs` / `app logs` | `-v, --verbose`; `-n, --max-lines <MAX_LINES>` (lines from the end, default `10`); `--since <SINCE>` (default `7d`); `--component-id` (default: all components); `--deployment-version` (default: latest deployment version); `--region` (default: all regions); account and app selectors; `--from` |
| `app status` | `--format`; `--usage-since <USAGE_SINCE>` (default `7d`, minimum 5 minutes, maximum 7 days); account and app selectors; `--from` |
| `app list` | `--format`; `--verbose`; account selectors |
| `app history` | Lists past events for an app. `--format`; account and app selectors; `--from` |
| `app link` | `--app-name` / `--app-id` of the app to link to (selected from an interactive prompt if omitted); account selectors; `--from` (workspace to link) |
| `app unlink` | `--from` (workspace to unlink) only. v0.7.0 also listed account selectors; v0.7.6 does not. |
| `app delete` | `--no-confirm` (skip the delete confirmation prompt); account and app selectors; `--from` |
| `login` / `auth login` | `--token <TOKEN>` (personal access token; env `SPIN_AKA_ACCESS_TOKEN`) |
| `auth token create` | `-n, --name <NAME>` (required); `-d, --description`; `-e, --expiration-days` (default `30`, max `90`); `-s, --short` (print only the token); `--format` |
| `auth token list` | `--format`; `--verbose` |
| `auth token delete` | `-i, --id <ID>` (required); `--no-confirm` |
| `auth token regenerate` | `-i, --id <ID>` (required) |
| `info` | `--format`. Prints user and workspace information. |
| `send-feedback` | No options besides `--help`. |

Time values for `--since` and `--usage-since` accept an RFC3339 timestamp, a Unix epoch timestamp in seconds, or a duration from the present: a number followed by `s`, `m`, `h`, or `d` (for example `30m`).

Additional exact command forms from lifecycle, account, and CI articles:

```text
spin aka login
spin aka login --token <TOKEN>
spin aka app delete --app-name <name>
spin aka auth token create --name <name>
spin aka auth token create --expiration-days <days>
spin aka deploy --variable <key>=<value>
gh secret set <name>
```

- `spin aka app list` prints names as plain text by default; `--verbose` includes details such as App IDs, and `--format json` emits JSON.
- `spin aka app status` uses the application linked to the workspace unless `--app-name` selects another.
- The account guide says `spin aka info` displays the account name and ID and requires plugin v0.4 or higher.

Inspection and lifecycle examples:

```shell
spin aka app list --format json
spin aka app list --verbose
spin aka app status --app-name <app_name> --format json
spin aka app delete --app-name validate-jwt-tokens
spin aka app list --account-name <team_name>
spin aka deploy --account-name <team_name>
```

The account guide contains this deletion example:

```shell
spin aka delete app --app-name <app_name> --account-name <team_name>
```

That ordering conflicts with the dedicated command reference, which defines `spin aka app delete [OPTIONS]`. Prefer the dedicated command-reference form:

```shell
spin aka app delete --app-name <app_name> --account-name <team_name>
```

### 4.14 Cron CLI

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

Canonical dedicated-command-reference forms:

```text
spin aka app cron create [OPTIONS] --schedule <SCHEDULE>
spin aka app cron delete [OPTIONS] <NAME>
spin aka app cron list [OPTIONS]
spin aka cron create [OPTIONS] --schedule <SCHEDULE>
spin aka cron delete [OPTIONS] <NAME>
spin aka cron list [OPTIONS]
```

`cron create` options (v0.7.6): `-s, --schedule <SCHEDULE>` (required; for example `"0 0 * * *"` for every day at midnight), `-p, --path-and-query <PATH_AND_QUERY>` (the request path and query the job calls, for example `"/api/cron?foo=bar"`), `--name <NAME>` (optional; an auto-generated name is used if omitted), plus the shared account, app, and `--from` selectors. `cron delete` takes the job name as a positional argument; `cron list` takes only the shared selectors.

Example assembled from the documented options:

```shell
spin aka cron create --schedule "*/5 * * * *" --path-and-query "/" --name cron-job-1
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

The positional create form conflicts with the dedicated command reference's required `--schedule` option. Preserve it as tutorial evidence, but use `spin aka cron create [OPTIONS] --schedule <SCHEDULE>` with `--path-and-query` and `--name` as the canonical syntax for generated commands.

### 4.15 Deployment, updates, and CI

**Sources:** [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md)

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

The old version gracefully completes in-flight requests, but multiple versions are not simultaneously routable. The update guide instructs users to re-specify required application variables; it does not state the exact result of omitting a previously supplied value.

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

Personal access tokens expire after 30 days by default, support a maximum of 90 days, and are displayed only once.

### 4.16 Property Manager integration

**Sources:** [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md)

The Property Manager tutorial uses the `http-js` template, entry point `src/index.js`, `AutoRouter`, and the fetch-event pattern from §3.1. These are tutorial choices, not platform-wide requirements for every Property Manager integration.

Property configuration requirements:

- Derive Origin Hostname by removing `https://` and the trailing `/` from the Spin application URL.
- Set **Forward Host Header** to **Origin Hostname**.
- Configure **Modify Outgoing Request Path** (e.g. replace `/hello/` with `/`, keep query parameters).

Deployment through `spin aka deploy` requires authentication through the documented Akamai Control Center or GitHub-credential login flow.

### 4.17 Version and compatibility ledger

**Sources:** [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

| Area | Exact source note |
|---|---|
| Platform | Limited availability / Public Preview |
| Command reference | Every command lists `Spin compatibility: >=v4.0.0`; `--help` output shown for `aka` plugin v0.7.6, v0.7.0, and, for some commands, v0.4.0. The page does not say which plugin version needs which Spin version |
| Quotas article | Says “Akamai Functions supports Spin CLI v0.6.0 or newer.” This conflicts with the command reference's `>=v4.0.0`. The sources do not explain the difference; when generating commands, follow the dedicated command reference |
| JavaScript/TypeScript quickstart | Recommends Node.js 22 or newer; documentation example uses Node.js 22.13.0 |
| Windows quickstart | Links to the Spin v3.6.2 Windows binary release. This conflicts with the command reference's `Spin compatibility: >=v4.0.0`; the macOS/Linux instructions use an install script with no pinned version |
| Rust quickstart | Requires target `wasm32-wasip1` |
| Go quickstart | TinyGo 0.27 or above, `CGO_ENABLED=1`; Go SDK v0.10.0 appears in build output |
| MySQL tutorial | Node.js 21 or higher recommended; requires Linode Managed Databases, `@spinframework/spin-mysql`, and `@spinframework/spin-variables` |
| PostgreSQL tutorial | Requires `http-js`, `@spinframework/spin-postgres`, and `@spinframework/spin-variables` |
| Supabase cache proxy | Requires `http-ts`, `itty-router`, `@spinframework/spin-variables`, `@spinframework/spin-kv`, and `@supabase/supabase-js` |
| Object-store tutorial | Node.js 22 or later; requires `@spinframework/spin-variables` and `@aws-sdk/client-s3` |
| KV tutorial | Requires `@spinframework/spin-kv` and `itty-router`; local development persists through SQLite |
| Account management | `spin aka info` requires plugin v0.4 or higher |
| Cron | Tech Preview/UNSTABLE; `http-js` tutorial template |

### 4.18 Platform and operational reference

**Sources:** [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

#### Availability, placement, and routing

- Akamai Functions is in limited availability / Public Preview and requires onboarding before a user can log in and deploy.
- The FAQ says the service is deployed in more than 20 locations worldwide. The welcome page describes a globally distributed PaaS with global geo replication by default and routing to the fastest responding region where the application is available.
- A deployed application has a stable URL across deployments. Updating an application preserves its name, URL, integrations, and links; in-flight requests complete on the prior version while new traffic moves to the updated version.

#### Accounts, ownership, visibility, and collaboration

- Sign-up creates a personal account. Applications in a personal account belong to that account, operate independently, and are visible and manageable only by that user.
- Team accounts provide collaboration. The dedicated account guide directs users to a request form and says the same form can later modify membership; the FAQ more generally directs users to support, the account guide, or an Akamai representative for shared access.
- The account guide states that there is currently no limit on the number of team accounts or users per team account.
- Team accounts have no RBAC or per-application permissions. Every member has the same permissions and can permanently delete any application in the account.
- Account-default wording differs by source: the dedicated command reference says omitted account selectors use the current account context, while the account guide says operations otherwise default to the personal account. Use an explicit `--account-name` or `--account-id` whenever the target account matters.

#### Authentication and distinct lifetimes

- Interactive login supports Akamai Control Center and GitHub identities. Accounts with the same email address are automatically cross-linked, and the user authorizes the Spin CLI after authentication.
- The FAQ says an interactive `spin aka login` session persists for 30 days without activity.
- A personal access token is a separate credential: its default expiration is 30 days and its maximum configured lifetime is 90 days. Do not transfer either token rule to the interactive-login session.
- The FAQ question mentions application persistence after logout but its answer states only the login-session duration. Application lifecycle is documented separately: an application persists until an explicit permanent deletion, while updates replace the active version as described above.

#### Configuration, storage, and observability

- Application-variable changes are deployments, not runtime hot swaps, and increment the deployment version. Variables are encrypted at rest and in transit for the application's lifetime, but the cryptographic implementation is not assessed for PCI compliance.
- The managed KV store is isolated to one application, and each component needs explicit manifest permission. It is globally replicated with a replica in the same geographic area as each compute region, and standard operations provide read-your-writes behavior within one request.
- Akamai Functions captures everything an application writes to `stdout` and `stderr`. `spin aka logs` targets the linked application by default; the command reference additionally documents filters for component, deployment version, region, and time.

### 4.19 Akamai Functions, EdgeWorkers, and workload placement

**Sources:** [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md)

The two Akamai compute products are documented as complementary execution layers:

| Area | EdgeWorkers | Akamai Functions |
|---|---|---|
| Runtime | JavaScript on V8 | WebAssembly through Spin/Wasmtime |
| Execution layer | CDN HTTP pipeline at edge locations | Akamai Cloud compute regions with automatic location-based routing |
| Trigger model | HTTP lifecycle events: `onClientRequest`, `onOriginRequest`, `onOriginResponse`, `onClientResponse`, and `responseProvider` | HTTP requests; cron schedules invoke an HTTP path rather than adding a language-level trigger |
| Execution time | Less than 10 seconds, varying by event and tier | Source conflict: 30-second quota versus “30 seconds default, extendable” in the comparison page |
| Primary placement | Routing, authentication, cache-key construction, header enforcement, request/response transformation | Business rules, APIs, microservices, orchestration, data transformation, server-side rendering, and heavier application logic |
| Data access | EdgeKV and outbound HTTP to Akamized hostnames | Functions KV, allowlisted outbound HTTP, and customer-managed MySQL, PostgreSQL, and Redis |

Use-case and operational guidance:

- Choose Functions for application-level compute such as API backends, microservices, data enrichment, server-side rendering, media processing, and stateful application APIs. These examples remain subject to the 30-second handler, memory, and payload limits in §1.2.
- Choose EdgeWorkers for CDN-pipeline work such as advanced request routing, A/B assignment, token validation, cache-key customization, security-header enforcement, and geography-based request adaptation.
- EdgeWorkers `responseProvider` can act as an origin and has somewhat higher limits than other EdgeWorkers events, but the comparison still describes it as lightweight compute constrained by the capacity of small CDN regions.
- The use-cases page describes AI-agent logic that integrates with inference calls, but says inference itself runs outside Functions. The comparison page more broadly lists AI inference as a Functions workload, while the quotas page marks Serverless AI as Limited Access. Generated applications must preserve this difference and must not assume general in-runtime inference access.
- MySQL with Linode DBaaS is described as the smoothest managed Akamai-native database path, although a multi-region MySQL cluster requires extra effort. PostgreSQL protocol support is available but is not yet compatible with Linode DBaaS; Redis protocol support requires a customer-managed or third-party Redis service.
- The comparison calls Functions execution time “30 seconds default, extendable,” but the dedicated quotas page defines a 30-second request-handler limit. Use the dedicated quota as canonical unless an explicit customer-specific increase is confirmed.
- Combined designs can use EdgeWorkers as the traffic controller and Functions as the application server. The use-cases page says EdgeWorkers can make requests to Functions and Functions can push data into EdgeKV Admin APIs. The latter does not make EdgeKV interchangeable with Functions KV.

---

## 5. Cross-Reference

### 5.1 API and event-handler availability matrix

**Sources:** [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md)

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

Only HTTP is a supported trigger. “Cron invocation” is an external scheduler calling the configured HTTP route.

### 5.2 Object/method interactions

**Sources:** [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

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

**Sources:** [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

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

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md)

| Command | Implicit context | Related command/data |
|---|---|---|
| `spin aka app deploy` / `spin aka deploy` | Current account and `./spin.toml` unless selectors override; app inferred from workspace config, and a new app is created if none is inferred | `--variable`, `--create-name`, `--no-confirm`, `--skip-readiness-check`; linked app or `--app-id` |
| `spin aka app list` | Current/personal account unless account selector is supplied | `--verbose`, `--format json` reveal IDs/details |
| `spin aka app status` | Workspace-linked app unless `--app-name` is supplied | `--usage-since` accepts supported time formats/range |
| `spin aka logs` | Workspace-linked app unless `--app-name` is supplied; latest deployment version, all components, all regions | Captured stdout/stderr; `--since` (default `7d`), `--max-lines` (default `10`), `--component-id`, `--deployment-version`, `--region` |
| `spin aka auth token create` | Current user | Save once, store as `SPIN_AKA_ACCESS_TOKEN`, rotate before expiration |
| `spin aka app delete` | Selected/current account and app | Permanent; any team member can perform it because RBAC is absent; `--no-confirm` skips the prompt |
| `spin aka app link` / `app unlink` | Workspace at `--from` | `link` prompts for the app if `--app-name`/`--app-id` is omitted; in v0.7.6 `unlink` accepts only `--from` |
| `spin aka cron create/list/delete` | Current/deployed app | Operates on HTTP paths; Tech Preview/UNSTABLE |

### 5.5 Cross-platform and data-service interactions

**Sources:** [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md)

| Interaction | Documented purpose | Capability or boundary |
|---|---|---|
| EdgeWorkers → Akamai Functions | Route selected requests from the CDN pipeline to application/business logic | The new sources state this interaction but do not define an EdgeWorkers configuration signature |
| Akamai Functions → third-party HTTP/API | API orchestration, external services, and inference calls | Target must be present in the Function component's `allowed_outbound_hosts`; inference itself is outside Functions in the AI-agent use case |
| Akamai Functions → MySQL/PostgreSQL | Customer-managed relational persistence and queries | Use the documented `mysql://` or `postgres://` outbound capability; MySQL has a Linode DBaaS path, while PostgreSQL requires other infrastructure as described in §4.19 |
| Akamai Functions → Redis | Customer-managed caching, sessions, pub/sub, and related in-memory data patterns | Outbound Redis is listed as supported, but the active sources do not provide an exact SDK binding or manifest signature; Akamai does not currently offer managed Redis |
| Akamai Functions → EdgeKV Admin APIs | Publish control-plane data for EdgeWorkers, such as revocation or health information | The use-cases page states the integration but does not give an exact binding or command; EdgeKV remains separate from Functions KV |
| Cron service → Akamai Functions HTTP route | Periodic polling, maintenance, or aggregation | Cron is Tech Preview, schedules use UTC, and the schedule/path pair must be unique |

### Source Coverage

This table accounts for every active entry in `docs/reference-manifest.json`. `Included` rows name substantive subsections that incorporate the source's unique reference facts. `Excluded` is reserved for a source that contains no source-specific Akamai Functions API, constraint, operational fact, or working code pattern.

| Active exact source | Status | Compiled coverage or exclusion reason |
|---|---|---|
| [aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md) | Included | §1.7 Cron jobs; §1.9 CLI constraints; §4.13 CLI command reference (v0.7.6 signatures and options); §4.14 Cron CLI; §4.17 compatibility ledger; §5.4 CLI context |
| [akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md) | Included | §1.2 execution-limit conflict; §1.4 outbound networking and databases; §4.12 platform interfaces; §4.19 workload placement; §5.5 cross-platform interactions |
| [application-logs.md](../_source/techdocs-akamai-com/application-logs.md) | Included | §4.10 Logging; §4.18 Platform and operational reference; §5.4 CLI context and lifecycle interactions |
| [build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md) | Included | §2.7 Supabase; §4.4 Key-value store; §4.7 Supabase client; §6.11 and §6.14 failure patterns |
| [delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md) | Included | §1.6 Updates, deletion, and account security; §4.13 CLI command reference; §4.18 Platform and operational reference |
| [deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md) | Included | §2.2 Application variables; §4.3 Application variables; §4.15 Deployment, updates, and CI; §4.18 Platform and operational reference |
| [deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md) | Included | §1.9 CLI constraints; §4.15 Deployment, updates, and CI |
| [faq.md](../_source/techdocs-akamai-com/faq.md) | Included | §4.18 Platform and operational reference |
| [http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md) | Included | §3.1 JavaScript/TypeScript fetch event; §4.1 HTTP trigger manifest and injected headers; §5.1 and §5.3 cross-reference tables |
| [integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md) | Included | §1.10 Property Manager integration; §4.16 Property Manager integration; §6.2 and §6.20 failure patterns |
| [link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md) | Included | §4.13 CLI command reference; §4.18 Platform and operational reference; §5.4 CLI context and lifecycle interactions; §6.19 failure pattern |
| [list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md) | Included | §4.13 CLI command reference; §5.4 CLI context and lifecycle interactions |
| [manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md) | Included | §1.6 Updates, deletion, and account security; §4.13 CLI command reference; §4.18 Platform and operational reference; §6.21 failure pattern |
| [query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md) | Included | §2.4 MySQL; §4.5 MySQL; §5.3 required capabilities; §6.7 failure pattern |
| [query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md) | Included | §2.5 PostgreSQL; §4.6 PostgreSQL; §5.3 required capabilities; §6.3, §6.4, and §6.7 failure patterns |
| [quickstart.md](../_source/techdocs-akamai-com/quickstart.md) | Included | §2.1, §2.9, and §2.10 import rules; §3.1–§3.3 handler reference; §4.17 compatibility ledger; §4.18 operational reference |
| [quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md) | Included | §1.1 and §1.2 runtime limits; §1.9 and §4.17 Spin version note; §4.12 Other platform interfaces; §5.3 required capabilities |
| [related-standards.md](../_source/techdocs-akamai-com/related-standards.md) | Excluded | Curated external standards and navigation links only; it defines no source-specific Akamai Functions API, constraint, operational fact, or working code pattern |
| [schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md) | Included | §1.7 Cron jobs; §3.4 Cron invocation; §4.14 Cron CLI; §6.15, §6.16, and §6.22 failure patterns |
| [stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md) | Included | §2.8 S3-compatible object storage and streams; §4.8 S3-compatible object storage; §6.12 and §6.13 failure patterns |
| [update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md) | Included | §1.5 and §1.6 deployment constraints; §4.15 Deployment, updates, and CI; §4.18 operational reference; §6.17 and §6.18 failure patterns |
| [use-cases.md](../_source/techdocs-akamai-com/use-cases.md) | Included | §1.3 KV service boundary; §4.12 platform interfaces; §4.19 workload placement; §5.5 cross-platform interactions |
| [use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md) | Included | §1.3 Key-value store; §4.4 Key-value store; §4.18 operational reference; §6.9 and §6.10 failure patterns |
| [webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md) | Included | §1.1 Platform and runtime; §1.8 Language and toolchain constraints; §4.17 compatibility ledger |
| [welcome.md](../_source/techdocs-akamai-com/welcome.md) | Included | §1.1 Platform and runtime; §4.12 Other platform interfaces; §4.18 Platform and operational reference |

---

## 6. Known Failure Patterns

Only symptoms stated or directly implied by the upstream sources are used. When an exact error string is available, it is preserved.

### 6.1 Unsupported/custom trigger

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md)

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

**Sources:** [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

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

### 6.3 Missing PostgreSQL Spin SDK import

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

```javascript
// WRONG — Postgres.open is unavailable because the documented host SDK is absent.
// const connection = Postgres.open(connectionString);

// CORRECT
import * as Postgres from "@spinframework/spin-postgres";
const connection = Postgres.open(connectionString);
```

**Symptom:** the documented `Postgres.open(...)` integration is not in scope.

### 6.4 Missing component variable mapping

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

```toml
# WRONG — declared globally but not exposed to the component.
[variables]
pg_connection_string = { required = true }

# CORRECT
[component.hello-postgresql.variables]
pg_connection_string = "{{ pg_connection_string }}"
```

```javascript
const connectionString = Variables.get("pg_connection_string");
```

**Symptom:** the component lacks the documented mapping needed by `Variables.get(...)`.

### 6.5 Request body not decoded before JSON parsing

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

```javascript
// WRONG — requestBody is an ArrayBuffer in the documented handler pattern.
const payload = JSON.parse(requestBody);

// CORRECT
const requestBody = await req.arrayBuffer();
const payload = JSON.parse(new TextDecoder().decode(requestBody));
```

**Symptom:** the documented handlers decode the `ArrayBuffer` with `TextDecoder` before calling `JSON.parse`.

### 6.6 Missing outbound host capability

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

```toml
# WRONG
[component.linode-mysql]
allowed_outbound_hosts = []

# CORRECT
[component.linode-mysql]
allowed_outbound_hosts = ["mysql://{{ mysql_host }}:{{ mysql_port }}"]
```

**Symptom:** the capabilities-based security model denies the database or HTTP request.

### 6.7 Wrong MySQL/PostgreSQL protocol declaration

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

```toml
# WRONG — missing mysql://
allowed_outbound_hosts = ["{{ mysql_host }}:{{ mysql_port }}"]

# CORRECT
allowed_outbound_hosts = ["mysql://{{ mysql_host }}:{{ mysql_port }}"]
```

For PostgreSQL, use `postgres://` and port `5432`.

**Symptom:** the corresponding outbound database capability is not granted.

### 6.8 Localhost/short-name service chaining

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

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

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

```toml
# WRONG
[component.component-name]
key_value_stores = [ "custom" ]

# CORRECT
[component.component-name]
key_value_stores = [ "default" ]
```

**Symptom:** Akamai Functions allows only the `"default"` label, which signals the platform to provision the application's store automatically. The source does not state the error produced by another label.

### 6.10 Atomic KV or EdgeKV used for the managed store

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md)

```javascript
// WRONG — wasi:keyvalue/atomic and direct EdgeKV-as-Functions-KV access are unsupported here.
// atomic.increment("count", 1)

// CORRECT
import { openDefault } from '@spinframework/spin-kv';
const store = openDefault();
store.setJson("count", payload);
```

**Symptom:** the unsupported interface or separate EdgeKV service cannot access the Akamai Functions managed KV store. A Function-to-EdgeKV Admin API integration described by the use-cases page is a separate cross-service path and does not change this store boundary.

### 6.11 Supabase `.single()` for an optional match

**Sources:** [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

```javascript
// WRONG for an optional match — this does not follow the tutorial's nullable-result pattern.
const result = await supabase.from(table).select().eq(column, value).single();

// CORRECT — returns null for no match; check it and return 404.
const result = await supabase.from(table).select().eq(column, value).maybeSingle();
```

**Symptom:** `.single()` throws when no row is found, whereas `.maybeSingle()` returns `null`.

### 6.12 Missing required configuration

**Sources:** [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

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

**Sources:** [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

```typescript
// WRONG — Body is not automatically treated as the response stream type here.
return new Response(Body, { status: 200 });

// CORRECT
return new Response(Body as ReadableStream, { status: 200 });
```

**Symptom:** `Body` is not automatically a standard stream compatible with every context; the documented Response use requires the explicit cast.

### 6.14 KV cache invalidation omitted

**Sources:** [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

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

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

```shell
# WRONG — schedule copied as local wall-clock time.
spin aka cron create --schedule "0 9 * * *" --path-and-query "/" --name local-nine

# CORRECT — convert the desired time to UTC before creating the schedule.
spin aka cron create --schedule "<UTC_CRON>" --path-and-query "/" --name utc-schedule
```

**Symptom:** the job runs according to UTC, at a different local time than intended.

### 6.16 Duplicate cron schedule and path

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

```text
WRONG: create a second job with the same schedule and path-and-query.
CORRECT: change either the schedule or the path-and-query so the pair is unique.
```

**Symptom:** the application violates the documented uniqueness requirement for cron jobs.

### 6.17 Treating a variable change as a hot swap or omitting update inputs

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md)

```shell
# WRONG — treat a variable update as an in-place runtime mutation, or omit values
# that the update guide instructs you to supply.
spin aka deploy

# CORRECT — explicitly supply the values required by the new deployment.
spin aka deploy --variable <key>=<value>
```

**Symptom:** a variable change creates a new deployment and increments the version. The update guide does not state the exact result of omitting a previously supplied value.

### 6.18 Assuming canary/blue-green version routing

**Sources:** [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md)

```text
WRONG: deploy a new version and expect both versions to receive selectable traffic.
CORRECT: treat deployment as an update; only in-flight requests finish on the previous version.
```

**Symptom:** no simultaneous-version routing is available.

### 6.19 Logs fetched from the wrong app

**Sources:** [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md)

```shell
# WRONG — when the workspace is linked to a different application.
spin aka logs

# CORRECT
spin aka logs --app-name <app_name>
```

**Symptom:** the unqualified command fetches logs for the workspace-linked application.

### 6.20 Property Manager hostname/header mismatch

**Sources:** [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md)

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

**Sources:** [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# SOURCE DISCREPANCY — shown by the account guide.
spin aka delete app --app-name <app_name> --account-name <team_name>

# CANONICAL — matches the dedicated command reference.
spin aka app delete --app-name <app_name> --account-name <team_name>
```

**Symptom:** the first spelling conflicts with the dedicated command-reference signature and may not parse as the intended command.

### 6.22 Cron syntax discrepancy

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# TUTORIAL FORM
spin aka cron create "*/5 * * * *" "/" "cron-job-1"

# CANONICAL COMMAND-REFERENCE SHAPE (v0.7.6 options)
spin aka cron create --schedule "*/5 * * * *" --path-and-query "/" --name cron-job-1
```

**Symptom:** the tutorial positional form and the command-reference option form conflict. The command reference makes `--schedule` required and exposes the path and name as `--path-and-query` and `--name`; the source does not reproduce the CLI's response to the positional form.
