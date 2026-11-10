# Akamai Functions — Unified Coding Reference

> Master reference for generating Akamai Functions code (Spin applications compiled to WebAssembly).
> Compiled from the exact upstream Markdown sources listed in `docs/reference-manifest.json` and stored in `docs/_source/techdocs-akamai-com/`.

Conventions used throughout this reference:

- Every statement is documented Akamai Functions behavior unless it is labeled **Inference** or **General knowledge**. Labeled statements are supplementary guidance, not platform documentation.
- When sources disagree, both statements are kept and the disagreement is identified. A dedicated reference page, such as the `aka` command reference or the quotas page, is preferred over a tutorial only when choosing the canonical form for generated code. §5.6 indexes the conflicts and defective samples identified during compilation.
- Tutorial prerequisites, example versions, and recommendations are reported as such. They are not platform-wide requirements.
- Code blocks reproduce source code; only whitespace and Markdown escape artifacts (such as `\<` in placeholders) are normalized. Code marked as an illustration is not from a source. When a source sample is defective, the defect is called out beside it, and any corrected form is labeled as corrected.

## 1. Runtime Prohibitions

Each entry states a platform, runtime, deployment, or tooling constraint and its documented consequence. When a source does not document the error or symptom, the entry says so rather than inventing one. Defaults and other facts that restrict nothing are in §4.

### 1.1 Platform, runtime, and triggers

**Sources:** [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md)

- Akamai Functions runs Spin applications on a WebAssembly-based runtime. The language SDKs compile to WebAssembly, and `spin build` compiles an application to WebAssembly. The sources document no other execution format.
- `http` is the only supported trigger type ("Akamai Functions currently supports the `http` trigger type"). The Redis trigger and custom triggers are listed as not supported. The sources do not state the deployment or runtime error for a manifest that uses them.
- Spin runtime configuration is "not supported at this time." The source does not state what happens if an application supplies one.
- SQLite storage is not supported. Local key-value testing stores data in a SQLite file under `.spin/` (§4.4); that is local tooling, not a platform SQLite API. The source does not state the error for using the SQLite API on the platform.
- `wasi-blobstore` and `wasi-messaging` are "Not supported in Spin, Not supported in Akamai Functions." The consequence for a component that requires them is not stated.
- Serverless AI is available only through Limited Access, which is requested through a form. Code cannot assume Serverless AI access. The behavior without access is not stated.
- The language-matrix page states that Akamai Functions requires WASI support (at least Preview 1), and also that anything with WASI or Spin SDK support runs on it. The two statements differ for languages that have a Spin SDK but no WASI support (§4.12).
- Access is gated: Akamai Functions is in limited availability (public preview). The quickstart says logging in requires access to the public preview and lists receiving allow-listing status as a prerequisite. The error shown to a user without access is not stated.
- Deployment is documented only through the `spin aka` plugin (`spin aka deploy`). No other deployment path is documented.

### 1.2 Execution and storage quotas

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md)

The quotas page lists both the app limits and the Functions KV limits in "Default limit" columns. For the app limits (memory, app size, handler duration, and request/response size), it adds that limits are subject to change as part of the public preview and tells customers interested in higher limits to contact their Akamai representative. KV rate increases are covered separately by the KV page.

- Memory allocated per function execution is limited to 128 MiB. The source does not state the termination behavior or error text when the limit is exceeded.
- App size is limited to 50 MiB. The source does not state the deployment error for a larger application.
- Request-handler duration is limited to 30 seconds. The source does not state the termination behavior or error text when the limit is exceeded.
- Request and response size is limited to 10 MiB. The source does not state whether a larger payload is rejected or truncated.
- KV storage is limited to 2 GB "across all store instances." The source does not state the write error when this quota is exceeded.
- KV reads are limited to 1,000 requests per second per app, and KV writes to 50 requests per second per app. The KV page explains that query rates are limited "to enable experimenting with this feature" and can be increased for production needs at customer request. The throttling response is not stated.
- A KV value can be at most 1 MB and a KV key at most 8 KB. The source does not state the error for a larger value or key.

The comparison page describes Akamai Functions execution time as "30 seconds default, extendable." This is consistent with the quotas page, which lists 30 seconds as a default limit and points customers interested in higher limits to their Akamai representative. Neither page promises an increase. **Inference:** generated code should assume 30 seconds unless a higher limit has been confirmed.

### 1.3 Key-value store

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md)

- `wasi:keyvalue/atomic` is not supported "because it requires a consistency guarantee not provided by our global store." Only `wasi:keyvalue/store` and `wasi:keyvalue/batch` (2024-10-17 snapshot) are supported. The consequence for a component that imports the atomic interface is not stated.
- The only label Akamai Functions allows in `key_value_stores` is `"default"`. It signals the platform to provision the application's store automatically. A code comment in the KV tutorial mentions `Kv.open("mylabel")` for a different label, but the platform does not allow other labels. The error for another label is not stated.
- A component can use the store only when the manifest explicitly grants it permission through `key_value_stores`, under Spin's capabilities-based security model. The source does not state the runtime error for a component without the grant.
- Key-value stores are "currently scoped to applications and cannot be shared between applications."
- The Functions KV store "is different and separate from EdgeKV." The same page says "Edge is not currently compatible with Akamai Functions." (**Inference:** "Edge" there refers to EdgeKV.) The comparison page describes Functions KV as "similar in concept to EdgeKV but with access from the compute layer." The use-cases page describes Functions pushing data into the EdgeKV admin APIs (§4.22). The sources do not reconcile these pages (§5.6). **Inference:** an admin-API call is an integration with another service and does not make the two stores interchangeable.

### 1.4 Outbound networking and databases

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md)

- Outbound requests have to be granted per component in `allowed_outbound_hosts`. The Supabase tutorial says that under Spin's capabilities-based security model "we must explicitly grant the application access to variables and outbound requests." The database tutorials add the endpoint "so that the Wasm component is allowed to send network requests to it." The exact error for an ungranted host is not stated. The comparison page's "outbound HTTP to any hostname" means Functions is not limited to Akamized hostnames as EdgeWorkers is. It does not remove the allowlist.
- An application cannot reach another Spin application through `localhost` or short service names, as it could with Docker Compose or Kubernetes. It has to call the other application's full public URL, for example `https://<app-id>.fwf.app`. The resolution error is not stated.
- A MySQL entry in `allowed_outbound_hosts` has to use the `mysql://` protocol and explicitly include the port configured on the MySQL server (the tutorial's example port is `22691`). The tutorial says this is required for outbound connectivity but does not state the error when either part is missing.
- A PostgreSQL entry has to use the `postgres://` protocol and explicitly include the port. The tutorial uses the PostgreSQL default port, `5432`. The error when either part is missing is not stated.
- A Linode Managed MySQL cluster accepts only inbound connections that it explicitly allows, by IPv4 or IPv6 address. The tutorial allows `0.0.0.0/0` (any host) "for the sake of this tutorial and during public preview of Akamai Functions." The sources do not publish Akamai Functions egress IP ranges.
- PostgreSQL protocol support is not yet compatible with Linode DBaaS. Use self-managed or third-party PostgreSQL. Akamai does not currently offer a managed Redis service, so outbound Redis requires a self-managed or third-party Redis instance. The sources do not describe what happens if a Linode DBaaS PostgreSQL database is used.

### 1.5 Application variables and deployment versions

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

- A component can read only the application variables granted to it in its `[component.<name>.variables]` table, under the capabilities-based security model. The sources do not state what `Variables.get(...)` returns for a variable that has not been granted. The documented samples treat a falsy result as missing configuration (§3.2).
- During local runs, environment variables prefixed with `SPIN_VARIABLE_` "will be accessible by your applications, if a corresponding variable is defined as part of the application manifest."
- The object-store tutorial notes that variables marked `required = true` have to be supplied before the application runs. The source does not state the error when a required variable is missing.
- A variable value supplied with `spin aka deploy --variable` is not a live runtime change. It is "propagated as a new deployment," and the version increments.
- The update guide instructs users to specify the application's variables again when they upgrade with `spin aka deploy`. It does not state the result of omitting a previously supplied value.
- Application variables are encrypted at rest and in transit for the lifetime of the application, but "the underlying cryptographic implementations have not been assessed for PCI compliance." Do not present application variables as PCI-assessed secret storage.

### 1.6 Updates, deletion, and account security

**Sources:** [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

- Akamai Functions has no built-in support for running multiple versions simultaneously, for example canary or blue-green deployments. During an update, in-flight requests are gracefully completed by the previous version while all new traffic is routed to the updated version.
- Deleting an application is permanent and cannot be undone. `spin aka app delete` asks for confirmation unless `--no-confirm` is passed.
- Akamai Functions does not support role-based access control (RBAC) or per-application permissions. Every team-account member has the same permissions and can permanently delete any application in the account.
- An application persists until it is explicitly deleted with `spin aka app delete`. Unlinking a workspace does not delete the application.

### 1.7 Cron jobs

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

- Cron-job support is in Tech Preview, and the CLI labels the command group `UNSTABLE`. The sources give no compatibility guarantee for it.
- A cron job can be associated only with an application that is already deployed to Akamai Functions. The source does not state the error for an application that is not deployed.
- A schedule that names a time of day has to be written in UTC. The tutorial warns that local times may need converting "to ensure correct execution."
- Within one application, each combination of schedule and path-and-query has to be unique. The error for a duplicate is not stated.
- In the command reference, `cron create` requires `--schedule <SCHEDULE>`, and `cron delete` requires the job's positional `<NAME>`. The cron tutorial shows a positional form of `create` that conflicts with this (§4.17, §6.21). The CLI's response to an incomplete command is not reproduced.

### 1.8 Language and toolchain constraints

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

- Rust components need the `wasm32-wasip1` target (`rustup target add wasm32-wasip1`). The GitHub Actions guide says some applications "need additional build tools installed before it will compile," and that a Rust project "will need the `wasm32-wasip1` Rust compiler target available." It adds the target in CI before `spin build`.
- Go components are built with TinyGo, because "the standard Go compiler does not yet support WASI exports." The quickstart lists these checks for a failed build: the Spin SDK needs TinyGo 0.27 or above, and `CGO_ENABLED=1` has to be set because the Go SDK is built using CGO.
- Node.js versions are tutorial guidance, not platform minimums. The quickstart recommends Node.js 22 or newer, the object-store tutorial lists Node.js 22 or later as a prerequisite, and the MySQL tutorial recommends at least Node.js 21.
- An application is deployed as compiled WebAssembly. Build it with `spin build` before deploying, or pass `spin aka deploy --build`, which runs `spin build` first for local apps and is ignored for remote apps.

### 1.9 CLI and authentication constraints

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md)

- The command reference lists `Spin compatibility: >=v4.0.0` for every `spin aka` command and does not state what happens with an older Spin. Two other sources give different version guidance: the quotas page says "Akamai Functions supports Spin CLI v0.6.0 or newer," and the quickstart's Windows instructions link to the Spin v3.6.2 binary release. The sources do not reconcile these (§4.20).
- A personal access token (PAT) expires after 30 days by default. In plugin v0.7.0 and v0.7.6 (the versions whose help shows it), `--expiration-days` has a maximum of 90 (`[max: 90]`); the CLI's response to a larger value is not stated. Once a token expires, a new token has to be created to keep deploying from CI/CD. `spin aka auth token regenerate --id <ID>` ("Regenerate a personal access token") also exists, but the sources do not say whether it works on an expired token or what expiration the regenerated token receives.
- A new PAT is displayed only once ("This is your only chance to see it"). It has to be saved immediately.
- `spin aka app status --usage-since` enforces a window of at least 5 minutes and at most 7 days. The CLI's response to an out-of-range value is not stated. No range is documented for `spin aka logs --since`, so the status range does not carry over to logs.
- `--create-name` is valid only when deploying to an app that does not exist yet. The CLI's response otherwise is not stated.
- The account guide says `spin aka info` displays the account name and ID with plugin version v0.4 or higher.

### 1.10 Property Manager integration

**Sources:** [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md)

These are the settings the tutorial instructs ("ensure to update these fields"). They are tutorial-documented settings for this integration, not platform-wide restrictions.

- The Origin Server behavior's hostname is the application's origin: its URL with the `https://` prefix and the trailing `/` removed. The source gives no reason or consequence for another form.
- **Forward Host Header** is set to **Origin Hostname**. The source gives no reason or consequence for another value.
- The tutorial adds a **Modify Outgoing Request Path** behavior so that the property does not send the routing criteria (`/hello/`) as a path to the application.
- A new rule takes effect only after the new property version is activated ("At this point, the new rule isn't active, yet!"). The tutorial highly recommends activating and testing in the Staging environment before production. This is a recommendation, not a platform requirement.

---

## 2. Import Rules

The sources prescribe the following imports. They do not state a general rule that imports must be static, and they do not state that dynamic `import()` is unsupported. Install the matching package before importing it (§2.11).

### 2.1 Router and HTTP helpers

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

Router only (templates, KV, cron, and Property Manager samples; the Property Manager sample's `Fimport` typo is corrected, §5.6):

```javascript
import { AutoRouter } from 'itty-router';
```

Router plus the `json` response helper (object-store and Supabase `src/index.ts`):

```typescript
import { AutoRouter, json } from 'itty-router';
```

Request type for middleware (Supabase `src/middlewares.ts`):

```typescript
import { IRequest } from "itty-router";
```

`itty-router` is a dependency of the `http-js` and `http-ts` templates. The PostgreSQL tutorial notes that it "is specified as dependency of the app."

### 2.2 Application variables

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

```typescript
import * as Variables from "@spinframework/spin-variables";
```

Read a variable with `Variables.get("<name>")`, for example `Variables.get("pg_connection_string")` (§4.3).

The webhook revision of the Supabase middleware imports `Variables` from `@spinframework/spin-kv` instead. That is a defect in the sample; every other variables sample, including the same tutorial's first middleware, imports from `@spinframework/spin-variables` (§5.6, §6.25).

### 2.3 Key-value store

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

Named import (KV tutorial):

```javascript
import { openDefault } from '@spinframework/spin-kv';
```

Namespace import (Supabase cache module):

```typescript
import * as Kv from "@spinframework/spin-kv";
```

Call `openDefault()` with the named import or `Kv.openDefault()` with the namespace import.

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

Local modules in the tutorial:

```typescript
import { Config, withConfig } from './middlewares';
import {
	ALL_ARTICLES_CACHE_KEY,
	buildKey,
	invalidate,
	readFromCache,
	storeInCache
} from './cache';
```

`src/inform.ts` imports `{ ALL_ARTICLES_CACHE_KEY, buildKey, invalidate }` from `"./cache"`. The tutorial then imports the webhook processor with `import  processDatabaseUpdate  from './inform';`, which is a default import, but `src/inform.ts` declares a named export (`export function processDatabaseUpdate`). See §5.6.

### 2.8 S3-compatible object storage and stream globals

**Sources:** [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

```typescript
import { S3Client, GetObjectCommand, ListObjectsV2Command } from '@aws-sdk/client-s3';
```

The tutorial uses `TextDecoder`, `TextEncoder`, `TransformStream`, and `ReadableStream` without importing them.

### 2.9 Rust

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;
```

The handler also refers to `anyhow::Result` by its full path.

### 2.10 Go

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

```go
import (
	"fmt"
	"net/http"

	spinhttp "github.com/spinframework/spin/sdk/go/v2/http"
)
```

The quickstart's TinyGo build output shows the SDK module `github.com/spinframework/spin/sdk/go v0.10.0` being downloaded (see §5.6 for the `/v2` import-path mismatch).

### 2.11 Package installation by integration

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

| Integration | Template used by the tutorial | Exact install command(s) after `spin new` |
|---|---|---|
| Starter app (quickstart), cron | `http-js` or `http-ts` | `npm install` |
| Key-value store | `http-js` | `npm install @spinframework/spin-kv` (installs the template defaults plus the KV SDK) |
| MySQL | `http-ts` (the prose says `http-js`; §5.6) | `npm install @spinframework/spin-mysql @spinframework/spin-variables`, then `npm install uuid --save` |
| PostgreSQL | `http-js` | `npm install`, then `npm install  @spinframework/spin-postgres @spinframework/spin-variables uuid` |
| Supabase cache proxy | `http-ts` | `npm install @spinframework/spin-variables @spinframework/spin-kv @supabase/supabase-js --save` |
| Linode Object Storage | `http-ts` | `npm install @spinframework/spin-variables @aws-sdk/client-s3` |
| Rust | `http-rust` | No npm packages. Install the `wasm32-wasip1` target (§1.8). |
| Go | `http-go` | No npm packages. Install TinyGo (§1.8). |

---

## 3. Event Handler Reference

Akamai Functions supports only the `http` trigger. Cron does not add a second language-level event handler: the platform's cron service invokes an HTTP path of the deployed application (§3.5).

### 3.1 JavaScript/TypeScript `fetch` event

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md)

The `http-js` template generates `src/index.js`:

```javascript
// For AutoRouter documentation refer to <https://itty.dev/itty-router/routers/autorouter>
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

// Route ordering matters, the first route that matches will be used
// Any route that does not return will be treated as a middleware
// Any unmatched route will return a 404
router
    .get("/", () => new Response("hello universe"))
    .get('/hello/:name', ({ name }) => `Hello, ${name}!`)

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

The `http-ts` template generates `src/index.ts` with the same routes. Its entry point is typed and preceded by `//@ts-ignore`:

```typescript
//@ts-ignore
addEventListener('fetch', async (event: FetchEvent) => {
    event.respondWith(router.fetch(event.request));
});
```

Objects and operations used by the documented handlers:

| Object/member | Documented use | Constraint or note |
|---|---|---|
| `addEventListener('fetch', handler)` | Registers the entry point | Present in every documented JS/TS sample |
| `event.request` | Incoming request passed to `router.fetch(...)` | — |
| `event.respondWith(responseOrPromise)` | Returns the response | The documented flow passes the router result here. For the defective double call in the database samples, see §3.2. |
| `router.fetch(event.request)` / `router.fetch(event.request, context)` | Dispatches to the first matching route | Properties of `context` arrive as the route handler's second argument (§3.2) |
| Route handler return value | A `Response`, `json(...)`, or a string (the template's `/hello/:name` route returns a template string) | A route that does not return acts as middleware; an unmatched route returns `404` |
| `request.params.<name>` or destructured `({ name })` / `({ params })` | Reads route parameters | Forms are listed in §4.2 |
| `request.arrayBuffer()` + `TextDecoder` | Reads the request body | The samples decode with `TextDecoder` before `JSON.parse` |
| `request.headers.get(name)` | Reads request headers (the Supabase webhook reads `x-webhook-token`) | The Spin-injected headers in §4.1 are request headers too. **Inference:** read them the same way; no JS sample does, and only the Rust sample reads one (`spin-full-url`). |
| `new URL(request.url)` | Parses the URL and query | Used in the cron sample |
| `Variables.get(name)` | Reads a granted application variable | The variable must be granted to the component (§1.5) |
| `openDefault()` / `Kv.openDefault()` | Opens the `default` KV store | Requires `key_value_stores = ["default"]` |
| `Mysql.open(...)` / `Postgres.open(...)` | Opens a database connection | Requires `mysql://` or `postgres://` in `allowed_outbound_hosts` |
| `createClient(url, key)` / `new S3Client(...)` | Third-party clients | The endpoint must be in `allowed_outbound_hosts` |
| Outbound `fetch(url, init)` | Calls another application or HTTP API | Use a full public URL, never `localhost` or a short name |
| `console.log(...)` | Writes logs | stdout and stderr are captured and retrieved with `spin aka logs` |

Practices shown by the JS/TS samples:

- Register the handler with `addEventListener('fetch', ...)` and return the result through `event.respondWith(...)`. The sources document no other JS/TS entry point.
- The samples read request bodies with `await request.arrayBuffer()` and decode them with `TextDecoder` before `JSON.parse(...)`. The sources show no other body reader.
- Do not target a host absent from `allowed_outbound_hosts` from a database client, S3 client, Supabase client, or outbound `fetch` (§1.4).

### 3.2 Per-request context and configuration checks

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

The samples read configuration in one of three ways and pass it to route handlers.

**Pattern A — read in the fetch listener and pass as router context (PostgreSQL; MySQL is identical except for `"mysql_connection_string"` and a `//@ts-ignore` / `FetchEvent` signature):**

```javascript
// Spin application entry point
addEventListener('fetch', async (event) => {
    // if the connection string is not set, return early with a HTTP 500
    const connectionString = Variables.get("pg_connection_string");
    if (!connectionString) {
        event.respondWith(new Response(
          JSON.stringify({ message: "Connection String not specified" }),
            { status: 500, headers: DEFAULT_HEADERS }
          ));
    }

    // Let the HTTP router handle incoming requests
    // pass the connection string as extra
    event.respondWith(router.fetch(event.request, { connectionString }));
});
```

Route handlers receive the context as their second argument, for example `.get("/products", async (_, { connectionString }) => readAllProducts(connectionString))`.

The comment says "return early," but the code has no `return`. When the variable is missing, `event.respondWith(...)` is called a second time. The sources do not document the runtime result. **Inference (general Fetch-event knowledge):** a fetch event accepts one `respondWith` call, so generated code should return after the first. Corrected form, which is not from a source:

```javascript
    if (!connectionString) {
        return event.respondWith(new Response(
            JSON.stringify({ message: "Connection String not specified" }),
            { status: 500, headers: DEFAULT_HEADERS }
        ));
    }
```

**Pattern B — validate several variables and pass a config object (object-store tutorial):**

```typescript
//@ts-ignore
addEventListener('fetch', async (event: FetchEvent) => {

    // load application variables
    const endpoint = Variables.get("endpoint");
    const accessKeyId = Variables.get("access_key_id");
    const secretAccessKey = Variables.get("secret_access_key");
    const bucketName = Variables.get("bucket_name");
    const region = Variables.get("region");

    // if any variable is not specified or empty, terminate and send a HTTP 500
    if (!endpoint || !accessKeyId || !secretAccessKey || !bucketName || !region) {
        return new Response("Application not configured correctly", { status: 500 });
    }

    // Pass the Configuration to the Router
    event.respondWith(router.fetch(event.request, {
        config: {
            endpoint,
            accessKeyId,
            secretAccessKey,
            bucketName,
            region
        } as Config
    }));
});
```

Handlers destructure the context, for example `.get("/files", async (_, {config}) => await listFiles(config))`. The intended result for missing configuration is HTTP `500` with the body `Application not configured correctly`. However, the sample returns the `Response` from the listener without calling `event.respondWith(...)`, unlike every other documented response path. The sources do not document what the runtime does with a value returned from the listener. **Inference:** wrap the response in `event.respondWith(...)`, as in Pattern A's corrected form.

**Pattern C — router middleware sets `request.config` (Supabase tutorial):**

```typescript
router
  // run the withConfig middleware for every incoming request
  .all('*', withConfig)
```

`withConfig` reads variables and throws `new Error("Required Configuration data not set")` when required values are missing. Otherwise it sets `request.config`, and handlers read `req.config` or destructure `({ id, config })`. The sources do not document the HTTP response produced when the middleware throws. The full middleware is in §4.7.

### 3.3 Rust HTTP component handler

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

The `http-rust` template generates `src/lib.rs`:

```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;

/// A simple Spin HTTP component.
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
- The handler receives `spin_sdk::http::Request` and returns `anyhow::Result<impl IntoResponse>`. `req.header(name)` reads a header, such as the injected `spin-full-url`.
- `spin build` runs `cargo build --target wasm32-wasip1 --release`.

### 3.4 Go HTTP handler

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

The `http-go` template generates `main.go`:

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

- Register the handler with `spinhttp.Handle(...)` inside `init()`, and keep an empty `main()`.
- The callback uses the standard `http.ResponseWriter` and `*http.Request` types.
- `spin build` runs `tinygo build -target=wasi -gc=leaking -no-debug -o main.wasm main.go`, which requires TinyGo 0.27 or above and `CGO_ENABLED=1` (§1.8).

### 3.5 Cron invocation of an HTTP route

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

`spin aka cron` "allows applications to receive scheduled HTTP triggers without relying on external services." The tutorial's handler is an ordinary HTTP route (`src/index.js` from the `http-js` template):

```javascript
// For AutoRouter documentation refer to https://itty.dev/itty-router/routers/autorouter
import { AutoRouter } from 'itty-router';

// Initialize the router
let router = AutoRouter();

// Define a route that responds to GET requests
router.get("/", (request) => {
    // Parse the request URL to access query parameters
    const url = new URL(request.url);

    // Capture the current timestamp
    const now = new Date().toISOString();

    // Log every time the route is triggered, including the message (if any)
    console.log(`Cron job triggered at ${now}"`);

    // Return a generic success response
    return new Response("Cron job executed", {
        status: 200,
    });
});

// Attach the router to the fetch event
addEventListener('fetch', (event) => {
    event.respondWith(router.fetch(event.request));
});
```

- The cron job calls the configured path and query on the deployed application, and the code receives the standard HTTP `fetch` event.
- The sources do not state which HTTP method the cron service uses. The tutorial registers its handler with `router.get` and schedules the path `/`.
- Schedules use UTC, and each schedule/path-and-query pair has to be unique within the application (§1.7). Verify invocations with `spin aka logs`.

---

## 4. API Reference

### 4.1 HTTP trigger manifest and injected headers

**Sources:** [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

```toml
[[trigger.http]]
route = "/..."                # the route that the trigger matches
component = "my-application"  # the name of the component to handle this route
```

`spin up` and `spin aka deploy` print this route as `(wildcard)` under "Available Routes" or "App Routes."

In addition to any headers passed by the client, several Spin-related headers are included in the request passed to the component:

| Header | Meaning |
|---|---|
| `spin-full-url` | The full URL of the request, including host and scheme |
| `spin-path-info` | The request path relative to the component route |
| `spin-path-match-n` | (Conditionally included) Where `n` is the pattern for a single-segment wildcard value; for example, `spin-path-match-userid` holds the value for a route that includes `userid` |
| `spin-matched-route` | The part of the trigger route that was matched, including the wildcard indicator if present |
| `spin-raw-component-route` | The component route pattern matched, including the wildcard indicator if present |

The triggered component can also use the `true-client-ip` header, which "returns the IP of the client sending the request," for example `151.49.93.60`.

Illustration (not from a source) of reading a wildcard header with the documented `request.headers.get` API:

```javascript
const userId = request.headers.get('spin-path-match-userid');
```

### 4.2 JavaScript/TypeScript HTTP and routing APIs

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

```text
AutoRouter()
router.get(path, handler)
router.post(path, handler)
router.put(path, handler)
router.delete(path, handler)
router.all(path, handlerOrMiddleware)
router.fetch(request)
router.fetch(request, context)
json(data)
json(data, { status, headers })
new Response(body)
new Response(body, { status, headers })
new Response(null, { status })
addEventListener('fetch', handler)
event.respondWith(responseOrPromise)
request.arrayBuffer()
request.headers.get(name)
request.params.<name>
new TextDecoder().decode(buffer)
new TextEncoder().encode(text)
new URL(request.url)
new Date().toISOString()
console.log(message)
```

Router behavior, quoted from the template comments:

- "Route ordering matters, the first route that matches will be used."
- "Any route that does not return will be treated as a middleware." The Supabase tutorial uses `.all('*', withConfig)` as middleware that sets `request.config`.
- "Any unmatched route will return a 404." The database samples add an explicit fallback: `.all("*", () => notFound("Endpoint not found"))`.

Route parameters appear in these documented forms:

| Form | Source sample |
|---|---|
| `({ name }) => ...` | Quickstart `/hello/:name` |
| `({key}) => handleGetValue(key)` | KV `/get/:key` |
| `req.params.key` / `request.params.id` | KV `/set/:key`; database `PUT /products/:id` |
| `({ params }, ctx) => ... params.id` | Database `GET` and `DELETE /products/:id` |
| `({ id, config }) => ...` / `req.params.id` | Supabase `/articles/:id` (with middleware-provided `config`) |
| `async ({ name }, {config}) => ...` | Object store `/files/:name` |

The second argument to `router.fetch(request, context)` becomes the route handler's second argument, for example `{ connectionString }` or `{ config }` (§3.2).

Response helpers and constants used by both database tutorials (TypeScript version):

```typescript
const DEFAULT_HEADERS = {
  "content-type": "application/json"
};

// helper function to quickly respond with an HTTP 400
function badRequest(message: string) {
    return new Response(JSON.stringify({ message }), { status: 400, headers: DEFAULT_HEADERS });
}

// helper function to quickly respond with a 404
function notFound(message: string) {
    return new Response(JSON.stringify({ message }), { status: 404, headers: DEFAULT_HEADERS });
}
```

The CRUD route layout shared by the database tutorials:

```javascript
router
    // C(reate) -> Add a new product
    .post("/products", async (request, { connectionString }) => createProduct(await request.arrayBuffer(), connectionString))
    // R(ead) -> Read all products
    .get("/products", async (_, { connectionString }) => readAllProducts(connectionString))
    // R(ead) -> Read a single product using its identifier
    .get("/products/:id", async ({ params }, { connectionString }) => readProductById(params.id, connectionString))
    // U(pdate) -> Update a product using its identifier
    .put("/products/:id", async (request, { connectionString }) => updateProductById(request.params.id, await request.arrayBuffer(), connectionString))
    // D(elete) -> Delete a product using its identifier
    .delete("/products/:id", async ({ params }, { connectionString }) => deleteProductById(params.id, connectionString))
    .all("*", () => notFound("Endpoint not found"));
```

Status codes used by the samples:

| Status | Use in samples |
|---|---|
| `200` | Successful read, update, KV set, cron, and webhook processing |
| `201` | Created, with a `Location` header (`/products/<id>`) in the database samples |
| `204` | Successful delete (`new Response(null, { status: 204 })`) |
| `400` | Invalid payload or identifier (`badRequest(...)`, `"Bad Request"`) |
| `401` | Missing or invalid `x-webhook-token` (Supabase webhook) |
| `404` | Missing key or record, or an unmatched route |
| `500` | Missing configuration (`Connection String not specified`, `Application not configured correctly`) or a backend error |

### 4.3 Application variables — `@spinframework/spin-variables`

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md)

```text
Variables.get(name)
```

- `Variables.get(name)` returns the value of an application variable granted to the component. The samples treat a falsy result as missing configuration.
- Variable values "can be updated without modifying the application," which supports rotating secrets and updating API endpoints. Because variables are encrypted by default, they can also hold secrets. They are encrypted at rest and in transit for the application's lifetime, with the PCI caveat in §1.5.

Declare variables in the application manifest, then grant them to a component:

```toml
[variables]
compression_level = { default = "1" }
```

```toml
[variables]
pg_connection_string = { required = true}

[component.hello-postgresql.variables]
pg_connection_string = "{{ pg_connection_string }}"
```

A component variable can be composed from several application variables (MySQL tutorial):

```toml
[component.linode-mysql.variables]
mysql_connection_string = "mysql://{{ mysql_user}}:{{ mysql_password }}@{{ mysql_host }}:{{ mysql_port }}/{{ mysql_database }}"
```

Variable attributes in the sources are `default = "..."`, `required = true`, and `secret = true`. The Supabase tutorial instead marks `supabase_key` with `sensitive = true` (§5.6). The object-store and Supabase snippets show component variable values as empty strings (`""`, or `"https://"` for `endpoint`), even though the Supabase prose says the grants use "the interpolation syntax." Use the interpolation form shown above (§5.6).

Supplying values:

| Context | Documented mechanism |
|---|---|
| Local `spin up` | Environment variables named `SPIN_VARIABLE_<NAME>` in uppercase, for example `SPIN_VARIABLE_MYSQL_HOST` or `SPIN_VARIABLE_PG_CONNECTION_STRING`. They "will be accessible by your applications, if a corresponding variable is defined as part of the application manifest." |
| Deployment | `spin aka deploy --variable key=value`. The option is repeatable, also accepts `@file.json` or `@file.toml`, and uses the last value when the same key is given more than once. |
| CI | `spin aka deploy --variable compression_level=${{ secrets.COMPRESSION_LEVEL }}` in a GitHub Actions step |

```shell
spin aka deploy --variable compression_level=3
```

Deploy-time output shows that a variable change is a new deployment:

```text
Deploying updated version of app my-app in account your-account (version 1 → 2)
OK to continue? yes
Waiting for app to be ready... ready

App Routes:
- my-app: https://ec8a19d8-6d10-4056-bb69-cc864306b489.fwf.app (wildcard)
```

### 4.4 Key-value store — `@spinframework/spin-kv`

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

```text
openDefault()
Kv.openDefault()
store.exists(key)
store.getJson(key)
store.setJson(key, value)
store.delete(key)
```

- `openDefault()` and `Kv.openDefault()` open the store labeled `"default"`, the only label the platform allows. `Kv.open("mylabel")` appears only in a tutorial code comment and cannot be used with a non-default label on Akamai Functions (§1.3).
- `exists(key)` checks whether a key exists, `getJson(key)` loads JSON data stored at a key, `setJson(key, value)` stores JSON data at a key, and `delete(key)` removes a key.
- The platform provisions and manages the store ("no-ops"). Data persists across application restarts and updates. The store is low-latency, persisted, and globally replicated, with a replica in the same geographic area as each compute region. All standard key-value operations have read-your-writes behavior within a request.
- At the WASI level, `wasi:keyvalue/store` and `wasi:keyvalue/batch` (2024-10-17 snapshot) are supported and `wasi:keyvalue/atomic` is not. The sources do not say how the Spin KV SDK maps onto these interfaces. Quotas are in §1.2.
- The sources document no native key expiration. The Supabase tutorial implements a time to live (TTL) by storing an `expiresAt` timestamp next to the data.
- The KV tutorial points to the Spin key value store API guide (`https://spinframework.dev/kv-store-api-guide`) for the SDK and for granting store permissions to components.

Manifest grant:

```toml
[component.hello-key-value-store]
key_value_stores = [ "default" ]
```

Locally, `spin up` stores KV data in `.spin/sqlite_key_value.db` ("Storing default key-value data to ".spin/sqlite_key_value.db"."). The file persists across invocations and updates.

KV tutorial (`src/index.js`, `http-js`):

```javascript
import { openDefault } from '@spinframework/spin-kv';
import { AutoRouter } from 'itty-router'

const router = AutoRouter();
const decoder = new TextDecoder();

// register the GET endpoint
// pass the response object (res) and the route parameter :key to the handleGetValue function
router.get("/get/:key", ({key}) => handleGetValue(key));

// register the POST endpoint
// pass the response object (res), the router parameter :key and the request body to the handleSetValue function
router.post("/set/:key", async (req) => handleSetValue(req.params.key, await req.arrayBuffer()));

// handle incoming requests using the HTTP router
addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

```javascript
function handleGetValue(key) {
    // open the Key Value store with label "default"
    const store = openDefault();

    // check if key exists, if not return early with an HTTP 404
    if (!store.exists(key)) {
        return new Response(null, { status: 404 });
    }

    // load JSON data at key from key value store
    let found = store.getJson(key);

    // Return an HTTP 200 with corresponding HTTP header and payload
    // if something was found at position key in the key value store
    return new Response(
      JSON.stringify(found),
      { status: 200, headers: { "content-type": "application/json" } }
      );
}
```

```javascript
function handleSetValue(key, requestBody) {
    // parse the request body using JSON.parse
    let payload = JSON.parse(decoder.decode(requestBody));

    // check if the payload has expected properties
    // otherwise return HTTP 400
    if (!payload || !payload.firstName || !payload.lastName) {
        return new Response("Invalid payload received.\nExpecting {\"firstName\": \"some\", \"lastName\": \"some\"}", { status: 400 });
    }

    // open the Key Value store with label "default"
    // if you specified a different label use the Kv.open("mylabel") function instead
    const store = openDefault();

    // store data in the Key Value store at key
    store.setJson(key, payload);

    // return an HTTP 200
    return new Response(null, { status: 200 });
}
```

Supabase cache module (`src/cache.ts`). It is reproduced from the source except where marked: the source's `invalidate` omits the opening brace of its second `if` (§5.6).

```typescript
import * as Kv from "@spinframework/spin-kv";

// CacheData is a wrapper for data stored in the key value store
// it defines when data will expire
interface CacheData {
  expiresAt: string,
  data: any
}

// Key for caching the list of all articles
export const ALL_ARTICLES_CACHE_KEY = "all-articles";

// function to compute the cache key for a particular article using its identifier
export function buildKey(id: string): string {
  return `article-${id}`;
}

// read a value from the cache
// returns either the cached value or undefined if key is unknown, or data is expired
export function readFromCache(key: string): any | undefined {
  console.log(`Reading from Cache with key: ${key}`);
  const store = Kv.openDefault();
  // return early with `undefined` if key is not known
  if (!store.exists(key)) {
    return undefined;
  }
  // load CacheData from the key value store
  const cacheData = store.getJson(key);
  // return either cached data or undefined if data is expired
  return onlyValidCacheData(cacheData);
};

// store value for ttl in the cache at key
export function storeInCache(key: string, value: any, ttl: number) {
  console.log(`Storing data in Cache at ${key}`);
  const store = Kv.openDefault();
  // create a CacheData instance and store it at position key
  store.setJson(key, buildCacheData(value, ttl));
  // because we modified the underlying data storage, we must check
  // if the list of all articles is in cache, if so, remove it
  if (key !== ALL_ARTICLES_CACHE_KEY && store.exists(ALL_ARTICLES_CACHE_KEY)) {
    console.log(`Invalidating data from Cache at ${ALL_ARTICLES_CACHE_KEY}`);
    store.delete(ALL_ARTICLES_CACHE_KEY);
  }
}

// remove item at position key from the cache
export function invalidate(key: string) {
  console.log(`Invalidating data from Cache at ${key}`);
  const store = Kv.openDefault();
  // if key exists, remove the cached data
  if (store.exists(key)) {
    store.delete(key);
  }
  // if a particular article was updated / removed from the cache
  // we must check and remove the list of all articles as well
  if (key !== ALL_ARTICLES_CACHE_KEY && store.exists(ALL_ARTICLES_CACHE_KEY)) { // corrected: "{" is missing in the source
    console.log(`Invalidating data from Cache at ${ALL_ARTICLES_CACHE_KEY}`);
    store.delete(ALL_ARTICLES_CACHE_KEY);
  }
}

// creates a new instance of CacheData
// ttl defines when data will expire
const buildCacheData = (data: any, ttl: number): CacheData => {
  return {
    expiresAt: new Date(Date.now() + ttl * 60 * 1000).toISOString(),
    data: data
  } as CacheData;
}

// If cacheItem is expired, this function will return `undefined`
// otherwise, the containing data will be returned to the callee
const onlyValidCacheData = (cacheItem: CacheData): any | undefined => {
  const now = new Date();
  const expiresAt = new Date(cacheItem.expiresAt);
  if (now > expiresAt) {
    return undefined;
  }
  return cacheItem.data;
}
```

The tutorial's cache requirements are to cache individual articles by ID, cache the full list under a fixed key (`all-articles`), give all cached data an expiration timestamp derived from `cache_ttl`, and invalidate the cache whenever data is added, updated, or removed.

### 4.5 MySQL — `@spinframework/spin-mysql`

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md)

```text
Mysql.open(connectionString)
connection.execute(sql, params)   -> return value not documented (see below)
connection.query(sql, params)     -> result with .rows
```

- `Mysql.open` opens a MySQL connection using a `mysql://user:password@host:port/database` connection string.
- `connection.execute` runs `INSERT`, `UPDATE`, and `DELETE`. The source does not document its return value. The samples store it as `updatedRows` or `deletedRows` and compare it with `0` to return "not found." **General knowledge (not in the sources):** the current `@spinframework/spin-mysql` SDK (spin-js-sdk repository) declares `execute` to return `void`, so those comparisons never match and the samples' update and delete `404` branches would not run. **Inference:** detect a missing row another way, for example with a `SELECT` before the update or delete.
- `connection.query` runs `SELECT`. `result.rows` is an array, and each row is indexed by column name as declared, for example `row["Id"]` and `row["Name"]`. The sample converts the price with `+row["Price"]!.toString()`.
- Parameters use `?` placeholders.

```typescript
// define application constants
const SQL_CREATE = "INSERT INTO Products (Id, Name, Price) VALUES (?, ?, ?)";
const SQL_READ_ALL = "SELECT Id, Name, Price from Products ORDER BY Name";
const SQL_READ_BY_ID = "SELECT Id, Name, Price from Products WHERE Id = ?";
const SQL_UPDATE_BY_ID = "UPDATE Products SET Name = ?, Price = ? WHERE Id = ?";
const SQL_DELETE_BY_ID = "DELETE FROM Products WHERE Id = ?";
```

Manifest (`linode-mysql` component built from the `http-ts` template):

```toml
[variables]
mysql_host = { required = true }
mysql_user = { required = true }
mysql_password = { required = true, secret = true }
mysql_port = { required = true }
mysql_database = { required = true }

[component.linode-mysql.variables]
mysql_connection_string = "mysql://{{ mysql_user}}:{{ mysql_password }}@{{ mysql_host }}:{{ mysql_port }}/{{ mysql_database }}"
```

```toml
[component.linode-mysql]
source = "dist/linode-mysql.wasm"
exclude_files = ["**/node_modules"]
allowed_outbound_hosts = ["mysql://{{ mysql_host }}:{{ mysql_port }}"]
```

The entry point reads `mysql_connection_string` and passes it as router context (§3.2, Pattern A).

```typescript
function readAllProducts(connectionString: string) {
  // open MySQL connection
  const connection = Mysql.open(connectionString);

  // load all products from the database
  let result = connection.query(SQL_READ_ALL, []);
  // iterate over each row received
  let items = result.rows.map(row => {
    // and construct a TypeScript object containing the data of a particular product
    return {
      id: row["Id"],
      name: row["Name"],
      price: +row["Price"]!.toString()
    };
  });

  // Create an HTTP response with status code 200
  return new Response(JSON.stringify(items), { status: 200, headers: DEFAULT_HEADERS });
}
```

```typescript
function createProduct(requestBody: ArrayBuffer, connectionString: string) {

  // validate the request payload
  let payload = JSON.parse(decoder.decode(requestBody));

  // if payload does not match the expectations, return early by sending an HTTP 400
  if (!payload || !payload.name || typeof payload.price != "number") {
    return badRequest("Invalid payload received. Expecting {\"name\":\"some name\", \"price\": 9.99}");
  }

  // construct a new Product using user provided data and
  // by rolling a new UUID
  const newProduct = {
    id: uuidv4(),
    name: payload.name,
    price: payload.price
  };

  // Open the MySQL connection
  const connection = Mysql.open(connectionString);

  // Persist the new product in database
  connection.execute(SQL_CREATE, [newProduct.id, newProduct.name, newProduct.price]);

  // Create an HTTP 201 (Created) response
  let customHeaders = {
    "Location": `/products/${newProduct.id}`
  };
  Object.assign(customHeaders, DEFAULT_HEADERS);

  return new Response(JSON.stringify(newProduct), { status: 201, headers: customHeaders });
}
```

```typescript
function deleteProductById(id: string, connectionString: string) {
  // validate UUID
  if (!uuidValidate(id)) {
    return badRequest("Invalid identifier received via URL");
  }

  // open MySQL connection
  const connection = Mysql.open(connectionString);
  const deletedRows = connection.execute(SQL_DELETE_BY_ID, [id]);

  // if delete did not affect any rows, return a not found
  if (deletedRows == 0) {
    return notFound("Product not found");
  }

  // construct a HTTP 204 response
  return new Response(null, { status: 204 });
}
```

The remaining handlers follow the same pattern:

- `readProductById` validates the ID with `uuidValidate` (`400 "Invalid identifier received via URL"`), runs `connection.query(SQL_READ_BY_ID, [id])`, returns `404 "Product not found"` when `result.rows.length == 0`, and otherwise returns `200` built from `result.rows[0]`.
- `updateProductById` validates the ID and the payload, then runs `connection.execute(SQL_UPDATE_BY_ID, [product.name, product.price, product.id])`. Its `404` branch compares the `execute` result with `0` (see the caveat above). Otherwise it returns `200` with `Location: /items/${id}`, which differs from the create handler's `/products/...` path (§5.6).

Database setup and access (tutorial): the database is a Linode Managed Databases MySQL cluster. The schema is created with `USE defaultdb;` and `CREATE TABLE IF NOT EXISTS Products (Id varchar(36) PRIMARY KEY, Name TEXT NOT NULL, Price DOUBLE PRECISION);`. Inbound access must be allowed on the cluster (§1.4).

Local run and deployment (deployment line continuations added; the source omits them, §5.6):

```shell
export SPIN_VARIABLE_MYSQL_HOST=<YOUR_MYSQL_HOST_HERE>
export SPIN_VARIABLE_MYSQL_PORT=<YOUR_MYSQL_PORT_HERE>
export SPIN_VARIABLE_MYSQL_USER=<YOUR_MYSQL_USER_HERE>
export SPIN_VARIABLE_MYSQL_PASSWORD=<YOUR_MYSQL_PASSWORD_HERE>
export SPIN_VARIABLE_MYSQL_DATABASE=<YOUR_MYSQL_DATABASE_HERE>

spin up
```

```shell
spin aka deploy \
  --variable mysql_host="<YOUR_MYSQL_HOST_HERE>" \
  --variable mysql_port="<YOUR_MYSQL_PORT_HERE>" \
  --variable mysql_user="<YOUR_MYSQL_USER_HERE>" \
  --variable mysql_password="<YOUR_MYSQL_PASSWORD_HERE>" \
  --variable mysql_database="<YOUR_MYSQL_DATABASE_HERE>"
```

### 4.6 PostgreSQL — `@spinframework/spin-postgres`

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

```text
Postgres.open(connectionString)
connection.execute(sql, params)   -> treated by the samples as the affected-row count
connection.query(sql, params)     -> result with .rows
```

- `Postgres.open` opens a PostgreSQL connection using the connection string from `pg_connection_string`. The tutorial uses a NEON-hosted database and copies the connection string from NEON's project dashboard.
- `connection.execute` runs `INSERT`, `UPDATE`, and `DELETE`. The source does not document its return value, but the samples compare it with `0` ("if update did not affect any rows, return a not found"). **General knowledge (not in the sources):** the current `@spinframework/spin-postgres` SDK declares `execute` to return the number of affected rows as a `bigint`, and `0n == 0` is `true` in JavaScript, so these checks work.
- `connection.query` runs `SELECT` and returns `.rows`. Rows are indexed by lowercase column names (`row["id"]`, `row["name"]`, `row["price"]`) even though the table declares `Id`, `Name`, and `Price`.
- Parameters use numbered placeholders: `$1`, `$2`, and so on.

```javascript
// define application constants
const SQL_CREATE = "INSERT INTO Products (Id, Name, Price) VALUES ($1, $2, $3)";
const SQL_READ_ALL = "SELECT Id, Name, Price from Products ORDER BY Name";
const SQL_READ_BY_ID = "SELECT Id, Name, Price from Products WHERE Id = $1";
const SQL_UPDATE_BY_ID = "UPDATE Products SET Name = $1, Price = $2 WHERE Id = $3";
const SQL_DELETE_BY_ID = "DELETE FROM Products WHERE Id = $1";
```

Manifest (`hello-postgresql` component built from the `http-js` template):

```toml
[variables]
pg_connection_string = { required = true}

[component.hello-postgresql.variables]
pg_connection_string = "{{ pg_connection_string }}"
```

```toml
[component.hello-postgresql]
source = "target/hello-postgresql.wasm"
allowed_outbound_hosts = [
    "postgres://ep-bread-garden-11223344.eu-central-1.aws.neon.tech:5432",
]
```

The tutorial says that "for outbound connectivity you need to specify the protocol as `postgres://` and explicitly add the PostgreSQL default port (`5432`)." The entry point is §3.2 Pattern A.

```javascript
function readAllProducts(connectionString) {
    // open PostgreSQL connection
    const connection = Postgres.open(connectionString);

    // load all products from the database
    let result = connection.query(SQL_READ_ALL, []);
    // iterate over each row received
    let items = result.rows.map(row => {
        // and construct a JavaScript object containing the data of a particular product
        return {
            id: row["id"],
            name: row["name"],
            price: row["price"]
        };
    });

    // Create an HTTP response with status code 200
    return new Response(JSON.stringify(items), { status: 200, headers: DEFAULT_HEADERS });
}
```

The create, read-by-ID, update, and delete handlers follow the MySQL handlers in §4.5, using `Postgres.open(...)`, the `$n` constants, and lowercase row keys. They return the same status codes and messages. Two other differences: the PostgreSQL handlers are untyped JavaScript, and read-by-ID returns `price: result.rows[0]["price"]` without MySQL's `+...!.toString()` conversion.

Local run and deployment (deployment line continuation added):

```shell
SPIN_VARIABLE_PG_CONNECTION_STRING="<YOUR_CONNECTION_STRING>" spin up
```

```shell
spin aka deploy \
  --variable pg_connection_string="YOUR_POSTGRESQL_CONNECTION_STRING_HERE"
```

### 4.7 Supabase client — `@supabase/supabase-js`

**Sources:** [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

Client call chains used in the tutorial (arguments abbreviated):

```text
createClient(url, key)
supabase.from('articles').select().order('created_at', { ascending: false })
supabase.from('articles').select().eq('id', id).maybeSingle()
supabase.from('articles').insert({ title, content }).select().single()
supabase.from('articles').update({ title, content, published }).eq('id', id).select().maybeSingle()
supabase.from('articles').delete().eq('id', id)
```

- Query results are destructured as `{ data, error }`. Errors are logged with `error.message`, `error.details`, and `error.stack`.
- The tutorial uses `.maybeSingle()` where "there might be no match at all," and returns `404` when `data` is falsy. It uses `.single()` after `insert(...).select()`. The sources do not describe `.single()` behavior when no row matches.
- The delete handler checks `response.error`, then `response.count == 0` for "not found." **General knowledge (not in the sources):** supabase-js (postgrest-js) fills `count` only when the query requests a count, for example `.delete({ count: 'exact' })`. Otherwise `count` is `null`, so this check never matches and the `404` branch would not run.
- Supabase calls go to the project URL, which has to be granted in `allowed_outbound_hosts`.

Manifest snippets as shown in the source. The component snippet's empty values are discussed in §4.3 and §5.6.

```toml
[variables]
supabase_url = { required = true }
supabase_key = { required = true, sensitive = true }
cache_ttl = { default = "5" }
```

```toml
# Excerpt from the application configuration file (TOML)
# This section defines a component named "supabase-proxy" and links it to application variables.

[component.supabase-proxy]
# Explicitly allow outbound requests to the Supabase URL
allowed_outbound_hosts = ["<your-supabase-url-here>"]

# Link environment variables to the component
[component.supabase-proxy.variables]
supabase_url = ""
supabase_key = ""
cache_ttl = ""
```

```toml
[component.supabase-proxy]
key_value_stores = ["default"]
```

`cache_ttl` is the cache time to live in minutes.

First version of the configuration middleware (`src/middlewares.ts`):

```typescript
import * as Variables from "@spinframework/spin-variables"
import { IRequest } from "itty-router";

/**
 * Application Configuration
 */
export interface Config {
  url: string,
  key: string,
  cacheTtl: number,
}

/**
  * Middleware to load application configuration
  * An instance of {@link Config} is set on the request
  *
  * @param request The {@link IRequest} automatically passed by itty-router
  * @throws An error if required configuration data is falsy
  */
export function withConfig(request: IRequest) {
  const url = Variables.get('supabase_url');
  const key = Variables.get('supabase_key');
  const ttl = (Variables.get('cache_ttl') ?? "5");
  if (!url || !key) {
    throw new Error("Required Configuration data not set");
  }

  // set the config on the actual request
  request.config = {
    url,
    key,
    cacheTtl: ttl
  } as Config;
}
```

This first version assigns the string `ttl` to the numeric `cacheTtl`. The webhook revision converts it with unary `+`.

Webhook revision of the middleware, reproduced from the source except for the marked import:

```typescript
import * as Variables from "@spinframework/spin-variables"; // corrected: the source imports from "@spinframework/spin-kv"
import { IRequest } from "itty-router";

export interface Config {
  url: string,
  key: string,
  cacheTtl: number,
  webhookToken: string,
}

export function withConfig(request: IRequest) {
  const url = Variables.get('supabase_url');
  const key = Variables.get('supabase_key');
  const ttl = +(Variables.get('cache_ttl') ?? "5");
  const webhookToken = Variables.get('supabase_webhook_token');

  if (!url || !key || !webhookToken) {
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

Router (`src/index.ts`):

```typescript
import { AutoRouter, json } from 'itty-router';
import { Config, withConfig } from './middlewares';

let router = AutoRouter();

router
  // run the withConfig middleware for every incoming request
  .all('*', withConfig)
  // Create new article
  .post('/articles', async (req) => createArticle(await req.arrayBuffer(), req.config as Config))
  // Read all articles
  .get('/articles', ({ config }) => readArticles(config))
  // Read article by id
  .get('/articles/:id', ({ id, config }) => readArticleById(id, config))
  // Update article by id
  .put('/articles/:id', async (req) => updateArticleById(req.params.id, await req.arrayBuffer(), req.config as Config))
  // Delete article by id
  .delete('/articles/:id', ({ id, config }) => deleteArticleById(id, config));

//@ts-ignore
addEventListener('fetch', async (event: FetchEvent) => {
  event.respondWith(router.fetch(event.request));
});
```

Read one row, where a match is optional:

```typescript
const readArticleById = async (id: string, config: Config): Promise<Response> => {
  // create a Supabase client
  const supabase = createClient(config.url, config.key);
  // load a single article using it's identifier
  // use the maybeSingle function, indicating that there might be no match at all
  const { data, error } = await supabase.from('articles')
    .select()
    .eq('id', id)
    .maybeSingle();

  // Return early with an HTTP 500, if something went wrong
  if (error) {
    console.log(`Error while reading single article: ${error.message} ${error.details} ${error.stack}`);
    return new Response(error.message, { status: 500 });
  }
  // Return early with an HTTP 404, if no article was found
  if (!data) {
    return new Response("Not Found", { status: 404 });
  }

  // Create an HTTP 200 result and sent the article as JSON
  return json(data, { status: 200 });
}
```

Insert a row:

```typescript
const createArticle = async (requestBody: ArrayBuffer, config: Config): Promise<Response> => {
  let payload;
  try {
    // create a new TextDecoder
    const decoder = new TextDecoder();
    // try to parse the request payload
    payload = JSON.parse(decoder.decode(requestBody));
  } catch (error) {
    // return early with an HTTP 400, in case malformatted data is provided
    return new Response("Bad Request", { status: 400 });
  }

  // if the provided payload does not specify title or content, return with an HTTP 400
  if (!payload.title || !payload.content) {
    return new Response("Bad Request", { status: 400 });
  }

  const supabase = createClient(config.url, config.key);

  // insert the article into the database
  const { data, error } = await supabase
    .from('articles')
    .insert({ title: payload.title, content: payload.content })
    .select()
    .single();
  // return early with HTTP 500, in case of any error
  if (error) {
    console.log(`Error while storing article in database: ${error.message} ${error.details} ${error.stack}`);
    return new Response('Internal Server Error', { status: 500 });
  }

  // return the new article with an HTTP 201
  return json(data, { status: 201 });
}
```

Other handlers:

- `readArticles` uses `.select().order('created_at', { ascending: false })` and returns `500` with `error.message` on error, or `json(data, { status: 200 })`.
- `updateArticleById` returns `400 "Bad Request"` for an invalid body, `500 'Internal Server Error'` on error, `404 'Not Found'` when `data` is falsy, and otherwise `200`.
- `deleteArticleById` returns `500` on `response.error`, `404` when `response.count == 0` (see the `count` caveat above), and otherwise `204`.

Cache integration: a cache hit is returned with the response header `x-served-via-cache: true`. The prose calls this header `x-served-by-cache`, but the code and sample output use `x-served-via-cache` (§5.6).

```typescript
const readArticles = async (config: Config): Promise<Response> => {
  const cached = readFromCache(ALL_ARTICLES_CACHE_KEY);
  if (cached) {
    return json(cached, { status: 200, headers: { 'x-served-via-cache': 'true' } });
  }

  // existing code from readArticles ...

  storeInCache(ALL_ARTICLES_CACHE_KEY, data, config.cacheTtl);
  return json(data, { status: 200 });
}
```

The other handlers integrate the cache the same way:

- `readArticleById` reads and stores `buildKey(id)`.
- `createArticle` calls `storeInCache(buildKey(data.id), data, config.cacheTtl)`.
- `updateArticleById` calls `storeInCache(buildKey(id), data, config.cacheTtl)`.
- `deleteArticleById` calls `invalidate(buildKey(id))`.

`storeInCache` and `invalidate` also drop the `all-articles` list (§4.4).

Webhook-driven cache invalidation:

```toml
[variables]
# ...
supabase_webhook_token = { required = true, secret = true }

# ...

[component.supabase-proxy.variables]
# ...
supabase_webhook_token = ""
```

The webhook handler is reproduced from the source except for the marked import:

```typescript
import { processDatabaseUpdate } from './inform'; // corrected: the source uses a default import of a named export

// ..

router // ...
  .post("/inform", async (req) => onDatabaseUpdate(req.headers, await req.arrayBuffer(), req.config as Config));

const onDatabaseUpdate = (headers: Headers, requestBody: ArrayBuffer, config: Config): Response => {
  const token = headers.get("x-webhook-token");
  if (!token || token !== config.webhookToken) {
    console.log("Webhook invoked without or with invalid token")
    return new Response(null, { status: 401 });
  }
  return processDatabaseUpdate(requestBody)
};
```

```typescript
import { ALL_ARTICLES_CACHE_KEY, buildKey, invalidate } from "./cache"

interface InformPayload {
  type: string
  table: string
  record: ArticleLike | null,
  schema: string
  old_record: ArticleLike | null
}

interface ArticleLike {
  id: string
}

export function processDatabaseUpdate(requestBody: ArrayBuffer): Response {
  let payload;

  try {
    const decoder = new TextDecoder();
    payload = JSON.parse(decoder.decode(requestBody)) as InformPayload;
  }
  catch (error) {
    return new Response('Bad Requst', { status: 400 });
  }
  switch (payload.type.toLowerCase()) {
    case "insert":
      invalidate(ALL_ARTICLES_CACHE_KEY);
      return new Response(null, { status: 200 });
    case "update":
      invalidate(buildKey(payload.record!.id));
      return new Response(null, { status: 200 });
    case "delete":
      invalidate(buildKey(payload.old_record!.id));
      return new Response(null, { status: 200 });
    default:
      return new Response('Bad Request', { status: 400 });
  }
}
```

In the Supabase portal, open **Integrations** → **Postgres Modules** → **Database Webhooks**. "Database Webhooks must be enabled once per project" (**Enable Webhooks**). Then create the hook on the **Webhooks** tab with **Create a new hook**, using these values:

| Property | Value |
|---|---|
| Name | Call Spin App on Akamai Functions |
| Conditions to fire webhook | Table `articles`; events Insert, Update, Delete |
| Webhook configuration | HTTP Request |
| HTTP Request Method | `POST` |
| HTTP Request URL | `<YOUR_APP_URL>/inform` (the app URL printed by `spin aka deploy`) |
| HTTP Headers | `content-type: application/json` and `x-webhook-token: <some_value>`, a random value such as a new UUID |

Tutorial choices that are not platform requirements: the Supabase free tier, a table with Row Level Security disabled "to keep things as simple," and the `articles` schema. The first deployment passes `supabase_url` and `supabase_key` with `--variable`. After adding the webhook code, rebuild with `spin build` and redeploy with the token variable added. The sample output shows this redeploy as `version 1 → 2`:

```shell
spin aka deploy --variable supabase_url="<YOUR_SUPABASE_URL>" \
    --variable supabase_key="<YOUR_SUPABASE_KEY>" \
    --variable supabase_webhook_token="<YOUR_TOKEN>"
```

The tutorial links its complete source at `https://github.com/fermyon/fwf-examples/tree/main/tutorials/supabase-proxy-tutorial`.

### 4.8 S3-compatible object storage — `@aws-sdk/client-s3`

**Sources:** [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

```text
new S3Client({ region, endpoint, credentials: { accessKeyId, secretAccessKey } })
s3.send(new ListObjectsV2Command({ Bucket }))        -> { Contents }
s3.send(new GetObjectCommand({ Bucket, Key }))       -> { Body }
(Body as ReadableStream).pipeThrough(transformStream)
new TransformStream({ transform(chunk, controller) { ... } })
```

Linode Object Storage is S3-compatible, and the tutorial accesses it with `@aws-sdk/client-s3` from a TypeScript (`http-ts`) application. It uses an existing bucket. To use your own instance, "permissions for deploying a new Object Storage bucket to Linode are required." The tutorial routes do not agree with each other:

| Purpose | Prose list and curl tests | Route registered in the code |
|---|---|---|
| List files | `GET /files` | `/files` |
| Stream a file | `GET /file/:name` | `/files/:name` |
| Stream an uppercase transform | `GET /transformed-file/:name` | `/transformed-files/:name` |

With the code as written, the documented `/file/...` and `/transformed-file/...` requests match no registered route. An unmatched route returns `404` (§3.1, §6.24).

Module header and routes (`src/index.ts`):

```typescript
import { AutoRouter, json } from 'itty-router';
import { S3Client, GetObjectCommand, ListObjectsV2Command } from '@aws-sdk/client-s3';
import * as Variables from '@spinframework/spin-variables';

const dec = new TextDecoder();
const enc = new TextEncoder();

let router = AutoRouter();

// a custom config interface holding all configuration data
interface Config {
    region: string,
    endpoint: string,
    accessKeyId: string,
    secretAccessKey: string,
    bucketName: string
}

router
    .get("/files", async (_, {config}) => await listFiles(config))
    .get('/files/:name', async ({ name }, {config}) => await streamFile(name, config))
    .get("/transformed-files/:name", async ({ name }, {config}) => await streamAndTransformFile(name, config));
```

Manifest snippets as shown in the source:

```toml
[variables]
region = { required = true }
endpoint = { required = true }
bucket_name = { required = true }
access_key_id = { required = true }
secret_access_key = { required = true, secret = true}
```

```toml
[component.linode-streaming-app.variables]
region = ""
endpoint = "https://"
bucket_name = ""
access_key_id = ""
secret_access_key = ""
```

```toml
[component.linode-streaming-app]
# ...
allowed_outbound_hosts = ['https://.']
```

**Inference:** these component values appear to have lost their `{{ ... }}` interpolation expressions in rendering, and the intended values cannot be recovered with certainty. The remnants are consistent with `endpoint = "https://{{ endpoint }}"` and `allowed_outbound_hosts = ['https://{{ bucket_name }}.{{ endpoint }}']`, because the tutorial supplies the endpoint without a scheme (`se-sto-1.linodeobjects.com`). **General knowledge (not in the sources):** by default, the AWS SDK v3 S3 client addresses a bucket with virtual-hosted-style URLs (`https://<bucket>.<endpoint>`) unless `forcePathStyle: true` is set. Grant each variable with the interpolation form in §4.3, and make `allowed_outbound_hosts` match the host the client actually calls.

The entry point validates all five variables and passes a `Config` object as router context (§3.2, Pattern B).

```typescript
const listFiles = async (config: Config): Promise<Response> => {
    // construct a new S3 client using configuration data
    const s3 = new S3Client({
        region: config.region,
        endpoint: config.endpoint,
        credentials: {
            accessKeyId: config.accessKeyId,
            secretAccessKey: config.secretAccessKey,
        }
    });
    try {
        const input = { Bucket: config.bucketName };
        // load metadata of all files in our S3 bucket
        const { Contents } = await s3.send(new ListObjectsV2Command(input));
        // grab all files names, fallback to an empty array
        const files = Contents?.map((file) => file.Key) || [];
        // return list of files as JSON
        return json({ files });
    } catch (error) {
        console.log(error);
        return new Response(JSON.stringify(error), { status: 500 })
    }
}
```

```typescript
const streamFile = async (name: string, config: Config): Promise<Response> => {
    const s3 = new S3Client({
        region: config.region,
        endpoint: config.endpoint,
        credentials: {
            accessKeyId: config.accessKeyId,
            secretAccessKey: config.secretAccessKey,
        }
    });

    try {
        // construct command input for receiving the desired file
        const input = { Bucket: config.bucketName, Key: name };
        // request the desired file
        const { Body } = await s3.send(new GetObjectCommand(input));
        // pipe the file contents to the response
        return new Response(Body as ReadableStream, {
            status: 200,
        });

    } catch (error: any) {
        return new Response(`error : ${error.message}`, { status: 500 });
    }
}
```

```typescript
const streamAndTransformFile = async (name: string, config: Config): Promise<Response> => {
    // define the transform operation
    const upperCaseTransform = new TransformStream({
        transform(chunk, controller) {
            // decode the byte array using TextDecoder
            const txt = dec.decode(chunk, { stream: true });
            // apply transformation and encode the transformed chunk again
            controller.enqueue(enc.encode(txt.toUpperCase()));
        }
    });

    const s3 = new S3Client({
        region: config.region,
        endpoint: config.endpoint,
        credentials: {
            accessKeyId: config.accessKeyId,
            secretAccessKey: config.secretAccessKey,
        }
    });

    try {
        const input = { Bucket: config.bucketName, Key: name };
        const { Body } = await s3.send(new GetObjectCommand(input));
        // pipe the file contents through the custom transformation
        const transformed = (Body as ReadableStream).pipeThrough(upperCaseTransform);
        // pipe the transformed stream to the response
        return new Response(transformed, {
            status: 200,
        });
    } catch (error: any) {
        return new Response(`error : ${error.message}`, { status: 500 });
    }
}
```

`Body` is cast to `ReadableStream` before it is used as a `Response` body or piped through a `TransformStream`; the sources do not state what happens without the cast. The list route returns JSON such as `{"files":["large.txt","small.txt","tiny.txt"]}`.

Local run and deployment. The tutorial uses a pre-existing demo bucket and publishes a read-only access key for it. The access key ID, secret access key, and bucket name are replaced here with placeholders, and line continuations are added to the deploy command.

```shell
spin build

export SPIN_VARIABLE_REGION=se
export SPIN_VARIABLE_ENDPOINT=se-sto-1.linodeobjects.com
export SPIN_VARIABLE_ACCESS_KEY_ID=<ACCESS_KEY_ID>
export SPIN_VARIABLE_SECRET_ACCESS_KEY=<SECRET_ACCESS_KEY>
export SPIN_VARIABLE_BUCKET_NAME=<BUCKET_NAME>

spin up
```

```shell
spin aka deploy --variable region=se \
  --variable endpoint=se-sto-1.linodeobjects.com \
  --variable access_key_id=<ACCESS_KEY_ID> \
  --variable secret_access_key=<SECRET_ACCESS_KEY> \
  --variable bucket_name=<BUCKET_NAME>
```

### 4.9 UUID

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

```text
uuidv4()
uuidValidate(id)
```

- `uuidv4()` generates a new product ID (a UUID v4 string) in the create handlers.
- `uuidValidate(id)` validates a route parameter. An invalid ID returns `400 "Invalid identifier received via URL"`.

### 4.10 Logging

**Sources:** [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

```text
console.log(message)
spin aka logs [OPTIONS]
spin aka app logs [OPTIONS]
```

- "Everything your Spin application writes to `stdout` and `stderr` is captured by Akamai Functions and made accessible via the `spin aka logs` command," which prints the messages to `stdout`.
- By default, `spin aka logs` returns logs for the application linked to the workspace. Use `--app-name` for a one-time selection, or link the workspace (§4.15).
- The logging page's example messages come from a Go application that uses the `log/slog` package. The JS/TS samples log with `console.log`.
- The page says that enabling verbose Spin error messages requires the `--verbose` flag, without naming the command. `spin aka logs` documents `-v, --verbose` ("Verbose output").
- Filters (plugin v0.7.0 and v0.7.6): `-n, --max-lines` (default `10`), `--since` (default `7d`), `--component-id`, `--deployment-version` (default: latest), and `--region` (default: all regions). Options are in §4.15.
- Locally, `spin up` logs component stdio to `.spin/logs/`. The logging page refers local logging questions to the Spin observability guide at `https://spinframework.dev/observing-apps#application-logs`.
- The page is titled "Application logs and usage" but documents only logs. Usage (invocation counts) is reported by `spin aka app status` (§4.15).

Log line format:

```text
2025-01-16 13:31:46 [hello-akamai-functions]  2025/01/16 13:31:36 INFO GET https://11077e3b-d632-4df3-921f-f7ebefb9aaca.fwf.app/hello: Handled by handle_hello func
2025-02-13 14:50:54 [supabase-proxy]  Storing data in Cache at all-articles
```

### 4.11 Rust and Go HTTP APIs

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md)

Rust:

```text
spin_sdk::http::Request
spin_sdk::http::Response            (Response::builder().status(..).header(..).body(..).build())
spin_sdk::http::IntoResponse
spin_sdk::http_component            (#[http_component] attribute)
req.header(name)
anyhow::Result<impl IntoResponse>
```

Go (TinyGo):

```text
spinhttp.Handle(func(w http.ResponseWriter, r *http.Request))
w.Header().Set(name, value)
fmt.Fprintln(w, ...)
```

The sources document no Rust or Go bindings for variables, KV, databases, or outbound HTTP. The CI guide links the Spin language guides for Rust, Go, JavaScript/TypeScript, and Python components.

### 4.12 WebAssembly language support

**Sources:** [docs/_source/techdocs-akamai-com/webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md)

The language-matrix page states the support rule in two ways:

1. "Spin, SpinKube, and Akamai Functions require WASI support. Any language supported for WASI should be supported on the Akamai Functions."
2. "Anything with WASI or Spin SDK support runs on Spin, and Akamai Functions."

These differ for languages that have a Spin SDK but no WASI support: TypeScript and Prolog (WASI ✗, Spin SDK ✓). TypeScript is fully documented through the `http-ts` template, which is consistent with the second statement. No Akamai page documents Prolog.

Support categories: **Core** means a WebAssembly 1.0 implementation exists, **Browser** means at least one browser implementation, **WASI** means support for at least WASI Preview 1, and **Spin SDK** means a Spin SDK is available. For production-grade WebAssembly, the page suggests Rust, JavaScript/TypeScript, Python, and Go. This is a recommendation, not an exclusive list. The welcome page lists SDK support for Rust, Go, JavaScript, and Python. The quickstart has samples for JavaScript, TypeScript, Rust, and TinyGo.

| Matrix status | Languages |
|---|---|
| Spin SDK ✓ | JavaScript, TypeScript, Python, Rust, Go, C# and .NET, Prolog |
| WASI ✓, Spin SDK in progress | Java, Swift, Scala (JVM), Kotlin (JVM), Clojure |
| WASI ✓, no Spin SDK | PHP, C++, Ruby, C, Kotlin (Wasm), Haskell, Zig, AssemblyScript, Grain, Motoko |
| WASI in progress, no Spin SDK | Dart (`ip`), COBOL, Erlang (BEAM), Lisp |
| Neither WASI nor Spin SDK | R, Objective-C, Scala (native), PowerShell, Lua, Perl |
| Not applicable | CSS, Shell |

### 4.13 Spin feature support and other platform interfaces

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md)

| Spin feature or interface | Akamai Functions support |
|---|---|
| HTTP trigger | Supported |
| Redis trigger | Not supported |
| Outbound HTTP | Supported |
| Application variables | Supported |
| Key-value storage | Supported |
| SQLite storage | Not supported |
| Serverless AI | Limited Access |
| Service chaining | Supported |
| MySQL | Supported |
| PostgreSQL | Supported |
| Outbound Redis | Supported |
| `wasi-blobstore` | Not supported in Spin, not supported in Akamai Functions |
| `wasi-config` | Supported (2024-09-27 snapshot) |
| `wasi-keyvalue` | `wasi:keyvalue/store` and `wasi:keyvalue/batch` supported (2024-10-17 snapshot) |
| `wasi-messaging` | Not supported in Spin, not supported in Akamai Functions |
| Component dependencies | Supported |
| Custom triggers | Not supported |
| Runtime configuration | Not supported at this time |
| Cron jobs | Tech Preview |

Notes:

- Service chaining is listed as supported. The same page says applications cannot reach each other through `localhost` or short service names and must use the full public URL. **General knowledge:** in Spin, "local service chaining" refers to calls between components of the same application. The sources show no service-chaining code sample. Illustration (not from a source) of calling another application with its documented URL form:

```javascript
const response = await fetch('https://<app-id>.fwf.app', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data: 'payload' })
});
```

- Outbound Redis is supported for customer-managed Redis and is distinct from the unsupported Redis trigger. The sources give no SDK binding or manifest example for it.
- AI: the comparison page lists AI inference among Functions workloads. The use-cases page says an AI agent built on Functions "integrates with AI inference calls (inference itself runs outside of functions)." The quotas page marks Serverless AI as Limited Access. Do not assume generally available in-runtime inference.
- The welcome page says any Akamai CDN, Security, or Cloud service can be used with a Functions application, for example API Acceleration, App & API Protector, or Akamai's managed databases. Other pages qualify this: PostgreSQL support is not yet compatible with Linode DBaaS, and the KV page says "Edge is not currently compatible with Akamai Functions" (§5.6).
- The use-cases page describes Functions pushing data into the EdgeKV admin APIs (§4.22). This cross-service integration does not give access to the Functions KV store.

### 4.14 Project setup, local development, and builds

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md)

Install Spin. Spin is both a CLI and a runtime.

| Platform | Documented steps |
|---|---|
| Linux (amd64), macOS (amd64, arm64) | `curl -fsSL https://developer.fermyon.com/downloads/fwf_install.sh \| bash`, then `sudo mv ./spin /usr/local/bin/spin` |
| Windows (amd64) | Download the Windows binary release from GitHub (the quickstart links Spin v3.6.2), unzip it, put `spin.exe` on the system path, and install the language templates or plugins |
| GitHub Actions (§4.18) | `curl -fsSL https://wasm-functions.fermyon.app/downloads/install.sh \| bash`, then `mv spin /usr/local/bin/spin` |

Check the installed version with `spin --version`. Install the `aka` plugin with `spin plugin install aka`, and upgrade an existing installation with:

```shell
spin plugins update
spin plugins upgrade aka
```

Language tooling (quickstart): JavaScript and TypeScript apps need Node.js installed, and version 22 or newer is recommended. Rust apps need the Rust toolchain plus the `wasm32-wasip1` target. Go apps need the TinyGo compiler; see the TinyGo installation guide.

Create an application from an Akamai Functions template. The command below generalizes the quickstart's concrete commands. **Inference:** several tutorials use `-a` where the quickstart uses `--accept-defaults`, so `-a` appears to be its short form.

```shell
spin new -E akamai-functions -t <template> --accept-defaults <app-name>
```

| Template | Language | Generated source | `spin build` runs |
|---|---|---|---|
| `http-js` | JavaScript | `src/index.js` | `npm run build` (webpack and `j2w`, producing `target/<app>.wasm`) |
| `http-ts` | TypeScript | `src/index.ts` | `npm run build`. The MySQL tutorial's build also runs `npm install` first and writes `dist/linode-mysql.wasm`. |
| `http-rust` | Rust | `src/lib.rs` | `cargo build --target wasm32-wasip1 --release` |
| `http-go` | Go (TinyGo) | `main.go` | `tinygo build -target=wasi -gc=leaking -no-debug -o main.wasm main.go` |

The build command is stored in the manifest, for example:

```toml
[component.hello-spin.build]
command = "tinygo build -target=wasi -gc=leaking -no-debug -o main.wasm main.go"
```

The MySQL component also sets `exclude_files = ["**/node_modules"]` and `source = "dist/linode-mysql.wasm"`. The PostgreSQL component uses `source = "target/hello-postgresql.wasm"`. More samples are available on the Spin Hub (`https://spinframework.dev/hub`) and in the Akamai Functions samples repository (`https://github.com/akamai-developers/akamai-functions-samples`).

Local testing:

- `spin up` starts a local HTTP server on port `3000` by default. It instantiates and invokes the application for every request and logs component stdio to `.spin/logs/`.
- If port `3000` is in use, pass `--listen`, for example `spin up --listen 127.0.0.1:3001`.
- `spin up --build` (KV tutorial) and `spin build --up` (cron tutorial) both build the application and run it in one step.
- Test with `curl -i http://localhost:3000/`, and stop the server with `CTRL+C`.
- Supply variables through `SPIN_VARIABLE_<NAME>` environment variables (§4.3). Local KV data is stored in `.spin/sqlite_key_value.db` (§4.4).

### 4.15 CLI command reference (plugin v0.7.6)

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md)

The command reference shows `--help` output for plugin v0.7.6 (the newest), v0.7.0, and, for some commands, v0.4.0. Each command heading has a single `Spin compatibility: >=v4.0.0` line above all of its version blocks, and the page does not map plugin versions to Spin versions. The signatures below are from v0.7.6. Older versions are compared in §4.16.

Top-level commands (`spin aka --help`):

| Command | Description |
|---|---|
| `app` | Manage apps deployed to Akamai Functions |
| `cron` | UNSTABLE: Manage cron jobs for an app |
| `deploy` | Deploy an app to Akamai Functions |
| `logs` | Fetch the logs for an app |
| `auth` | Manage user authentication |
| `login` | Log into Akamai Functions |
| `send-feedback` | Send us your feedback! |
| `info` | Print out user and workspace information |
| `help` | Print this message or the help of the given subcommand(s) |

`spin aka app` subcommands are `list`, `delete`, `status`, `deploy`, `logs`, `cron`, `link` ("Link your local workspace to an existing Akamai Functions app"), `unlink`, `history` ("Lists past events for an app"), and `help`. `spin aka auth` has `login`, `token`, and `help`. `spin aka auth token` has `create`, `list`, `delete`, `regenerate`, and `help`. No version of the command reference lists a top-level `spin aka link`; linking is `spin aka app link` (§6.22).

Signatures (v0.7.6):

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

Apart from the usage line, `spin aka app deploy` and `spin aka app logs` have the same help text and options as the top-level `deploy` and `logs`. `spin aka app cron` has the same `list`, `create`, and `delete` subcommands as `spin aka cron`. The `help` subcommands (`spin aka help`, `spin aka app help`, `spin aka app cron help`, `spin aka auth help`, `spin aka auth token help`, `spin aka cron help`) print the parent command's usage. In v0.7.6, `-V, --version` appears only on the top-level command.

Shared selector options on most app-scoped commands:

- `--account-id <ACCOUNT_ID>` / `--account-name <ACCOUNT_NAME>` select the account. If neither is given, the current account context is used. See §5.6 for the account guide's different wording.
- `--app-id <APP_ID>` / `--app-name <APP_NAME>` select the app. If neither is given, the app is inferred from the workspace config.
- `-f, --from <PATH>` takes a `spin.toml` file or a directory containing one, and defaults to `./spin.toml`.
- `--format <FORMAT>` accepts `plain` (default) or `json` on `app list`, `app status`, `app history`, and `info`. `auth token create` accepts `plain`, `table`, `json`, and `yaml`, defaulting to `plain`. `auth token list` accepts the same four, defaulting to `table`.

Per-command options (v0.7.6):

| Command | Options and defaults |
|---|---|
| `deploy` / `app deploy` | `--build` (run `spin build` first for local apps; ignored for remote apps; env `SPIN_ALWAYS_BUILD`); `--cache-dir <CACHE_DIR>` (cache for downloaded components and assets); `--variable <KEY=VALUE \| @FILE.json \| @FILE.toml>` (repeatable; for a duplicated key the last value is used); `--app-id` (if omitted, the app is inferred from the workspace config, and if none is inferred a new app is created); `--create-name <NEW_APP_NAME>` (only when deploying to an app that does not exist yet); `--no-confirm` (skip the deploy confirmation prompt); `--skip-readiness-check` (skip the readiness check after deployment); account selectors; `--from`. There is no `--app-name` option in any version shown. |
| `logs` / `app logs` | `-v, --verbose`; `-n, --max-lines <MAX_LINES>` (lines from the end, default `10`); `--since <SINCE>` (default `7d`); `--component-id` (default: all components); `--deployment-version` (default: latest deployment version); `--region` (default: all regions); account and app selectors; `--from` |
| `app status` | `--format`; `--usage-since <USAGE_SINCE>` (default `7d`; a minimum of 5 minutes and a maximum of 7 days is enforced); account and app selectors; `--from` |
| `app list` | `--format`; `--verbose` ("Show more detailed information"); account selectors |
| `app history` | `--format`; account and app selectors; `--from` |
| `app link` | `--app-name` / `--app-id` of the app to link to (chosen from an interactive prompt if omitted); account selectors; `-f, --from` (the workspace to link) |
| `app unlink` | `-f, --from` (the workspace to unlink) only |
| `app delete` | `--no-confirm` (skip the delete confirmation prompt); account and app selectors; `--from` |
| `cron create` / `app cron create` | `-s, --schedule` (required); `-p, --path-and-query`; `--name`; account and app selectors; `--from` (§4.17) |
| `cron delete` / `app cron delete` | Positional `<NAME>`; account and app selectors; `--from` |
| `cron list` / `app cron list` | Account and app selectors; `--from` |
| `login` / `auth login` | `--token <TOKEN>` (a personal access token; env `SPIN_AKA_ACCESS_TOKEN`) |
| `auth token create` | `-n, --name <NAME>` (required); `-d, --description`; `-e, --expiration-days` (default `30`, max `90`); `-s, --short` (show only the token); `--format` |
| `auth token list` | `--format`; `--verbose` |
| `auth token delete` | `-i, --id <ID>` (required); `--no-confirm` |
| `auth token regenerate` | `-i, --id <ID>` (required) |
| `info` | `--format`. Prints user and workspace information. |
| `send-feedback` | No options besides `--help` |

Time values for `--since` and `--usage-since` can be an RFC3339 timestamp, a Unix epoch timestamp in seconds, or a duration from the present: a number followed by `s`, `m`, `h`, or `d` (for example `30m`).

Workspace and inspection commands from the lifecycle guides:

- A workspace is the local directory containing the application code and `spin.toml`. Any child directory where the manifest is located also belongs to the workspace.
- The first `spin aka deploy` links the workspace to the new application automatically. After that, `spin aka deploy` targets the linked application, and `spin aka logs` and other app-scoped commands target it without `--app-name`. `deploy` itself has no `--app-name` option in any version shown, although the link guide implies otherwise (§5.6, §6.26).
- Link manually with `spin aka app link` (interactive prompt) or `spin aka app link --app-name <app-name>`. Linking helps when the workspace was not linked automatically, for example after cloning a repository, switching machines, or joining a team.
- Unlink with `spin aka app unlink`. This does not delete the application.
- `spin aka info` shows the account(s) and whether the workspace is linked:

```text
Auth Info
  Accounts: your-account
Workspace Info
  Root dir: /Users/user/src/hello-spin
  Linked app: hello-spin
```

- With plugin v0.4 or higher, `spin aka info` lists each account name with its ID (`# returns account_name (id: account_id)`), including team accounts the user belongs to. These are the values for `--account-name` and `--account-id`:

```text
Auth Info
  Accounts:
    - my_username (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
    - dev_team_1 (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
    - dev_team_2 (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
```

- `spin aka app list` prints app names as plain text. `--format json` prints a JSON array of names, and `--verbose` prints `name (app-id)`.
- `spin aka app status` reports the linked app, or the app given by `--app-name`. Its plain output contains `Name`, `ID`, `URL` (the public origin), `Created at`, and `Invocations` (for example `229 in the past 7 days`). The JSON output has these keys:

```json
{
  "id": "ec8a19d8-6d10-4056-bb69-cc864306b489",
  "name": "hello-akamai-functions",
  "urls": [
    "https://ec8a19d8-6d10-4056-bb69-cc864306b489.fwf.app"
  ],
  "created_at": "2025-05-23 16:11:49 UTC",
  "invocations": "229 in the past 7 days"
}
```

- `spin aka app delete --app-name <name>` asks `Are you sure you want to delete the app '<name>' (<id>)?` and prints `Deleted app successfully.`

Lifecycle and account examples:

```shell
spin aka app list --format json
spin aka app list --verbose
spin aka app status --app-name hello-akamai-functions --format json
spin aka app delete --app-name validate-jwt-tokens
spin aka app list --account-name dev_team_1
spin aka deploy --account-name dev_team_1
spin aka logs --app-name hello-akamai-functions
```

The account guide's deletion example, `spin aka delete app --app-name graphql --account-name dev_team_1`, conflicts with the dedicated `spin aka app delete [OPTIONS]` signature. Use `spin aka app delete --app-name <app_name> --account-name <team_name>` (§6.20).

### 4.16 CLI differences in older plugin versions

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md)

The command reference shows v0.7.0 help for every command except the six `help` subcommands, which show only v0.7.6. It shows v0.4.0 help for 22 commands: the top-level command, `app`, `app history` (whose output identifies itself as `spin-aka-app-history 0.4.1 (486ad84 2025-07-04)`), `app link`, `app list`, `app status`, `app unlink`, `auth`, `auth token` and its `create`, `delete`, `list`, and `regenerate` subcommands, `cron` and its `create`, `delete`, and `list` subcommands, `deploy`, `info`, `login`, `logs`, and `send-feedback`.

| Area | v0.7.6 | v0.7.0 (`887b0b3 2026-03-20`) | v0.4.x (`d0e9cc8 2025-05-22`; `app history` shows 0.4.1) |
|---|---|---|---|
| Help style | `Usage:` / `Commands:` | `USAGE:` / `SUBCOMMANDS:` with a version banner | Same as v0.7.0 |
| `-V, --version` | Top-level command only | Every subcommand | Every subcommand |
| Account selectors | `--account-id`, `--account-name` | Same | `--account-id` only ("Defaults to the current account context.") |
| `app unlink` | `-f, --from` only | Account selectors and `-f, --from` | `--account-id` and `-f, --from` |
| `deploy` | Includes `--skip-readiness-check` | Includes it | Not present |
| `logs` line count | `-n, --max-lines <MAX_LINES>` (default 10) | Same | `--tail <tail>` (default 10) |
| `logs` filters | `--component-id`, `--deployment-version`, `--region` | Same | Not present; `--since <since>` is the only filter |
| `info` | `--format plain\|json` | Same | No options (`spin aka info`) |
| `auth token create --expiration-days` | `[max: 90] [default: 30]` | Same | `[default: 30]`, with no maximum shown |

The cron, auth, and app subcommand sets are the same in the versions shown. The account guide separately notes that showing account names and IDs with `spin aka info` needs plugin v0.4 or higher.

### 4.17 Cron CLI

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

Canonical forms from the command reference:

```text
spin aka cron create [OPTIONS] --schedule <SCHEDULE>
spin aka cron delete [OPTIONS] <NAME>
spin aka cron list [OPTIONS]
spin aka app cron create [OPTIONS] --schedule <SCHEDULE>
spin aka app cron delete [OPTIONS] <NAME>
spin aka app cron list [OPTIONS]
```

`cron create` options:

- `-s, --schedule <SCHEDULE>` is required. Example: `"0 0 * * *"` for every day at midnight.
- `-p, --path-and-query <PATH_AND_QUERY>` is the path and query of the request made to the app. Example: `"/api/cron?foo=bar"`.
- `--name <NAME>` is optional. If omitted, the job gets an auto-generated name.
- The shared account, app, and `--from` selectors also apply.

The job is associated with the deployed application in the current working directory, or with the app given by `--app-name` or `--app-id`.

Schedule syntax is standard crontab. The tutorial adds:

- Each field can have multiple digits, and intervals are allowed in any position. The tutorial's example is `* */12 * * *` "to run every 12 hours."
- Comma-separated lists and ranges are allowed.
- Times of day are UTC.

**General knowledge:** in standard five-field crontab syntax, `* */12 * * *` matches every minute of hours 0 and 12, while `0 */12 * * *` runs once every 12 hours. The source does not discuss this.

Example assembled from the documented options:

```shell
spin aka cron create --schedule "*/5 * * * *" --path-and-query "/" --name cron-job-1
```

The tutorial gives positional forms instead:

```shell
spin aka cron create "*/5 * * * *" "/" "cron-job-1"
spin aka cron list
spin aka cron delete cron-job-1
```

The positional `create` form conflicts with the command reference, which requires `--schedule`. Keep it as tutorial evidence, but generate commands with `--schedule`, `--path-and-query`, and `--name` (§6.21). The tutorial's prose for this step also mentions a `/*` path with a `msg=fwf` query parameter, which its command does not use.

Documented outputs:

```text
Created cron which will next run at 2025-04-02 04:00:00 UTC
```

```text
+----------------+--------------+-------------------------+
| Name           | Schedule     | Next Run                |
+=========================================================+
| cron-job-1     |  */5 * * * * | 2025-04-02 04:00:00 UTC |
+----------------+--------------+-------------------------+
```

Deleting prints `Deleted cron job 'cron-job-1' with schedule '*/5 * * * *'`. The source's rendering of the schedule (`'_/5 _ \* \* \*'`) is garbled by Markdown escaping. The tutorial suggests cron jobs for data backups, periodic API polling, log rotation, scheduled notifications, querying stale records, syncing data, and cleaning up expired sessions.

### 4.18 Deployment, updates, and CI

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

First deployment: `spin aka deploy` reads `spin.toml` in the current directory, asks for a name for the new application, asks for confirmation, links the workspace, and waits for readiness:

```text
Name of new app: hello-spin
Creating new app hello-spin in account your-account
Note: If you would instead like to deploy to an existing app, cancel this deploy and link this workspace to the app with `spin aka app link`
OK to continue? yes
Workspace linked to app hello-spin
Waiting for app to be ready... ready

App Routes:
- hello-spin: https://ec8a19d8-6d10-4056-bb69-cc864306b489.fwf.app (wildcard)
```

A later deployment of a linked workspace prints `Deploying updated version of app <app> in account <account> (version 1 → 2)`. `--no-confirm` skips the deploy confirmation prompt, and `--skip-readiness-check` skips the readiness check after deployment (§4.15). **Inference:** `--create-name` (for a new app) or `--app-id` (for an existing app) avoids the new-app name prompt. No option is documented for the version-upgrade prompt that the update guide mentions.

Updating an application:

- Redeploy after changing code and, optionally, the version. The application keeps its name and URL, and existing integrations and links keep working.
- The version can be changed manually in `spin.toml` (`version = "0.1.0"` → `version = "0.1.1"`), or the "major version default upgrade prompted during the deployment process" can be accepted. The version bump is optional.
- Run `spin aka deploy`, and specify the application's variables again with `spin aka deploy --variable <key>=<value>`.
- To update an application in a team account, pass `--account-name` or `--account-id` on the deploy.
- In-flight requests are gracefully completed by the previous version while all new traffic goes to the updated version. There is no built-in support for running multiple versions simultaneously (§1.6).

GitHub Actions deployment:

1. Create a PAT for non-browser contexts such as CI/CD. Run `spin aka login`, then `spin aka auth token create --name mytoken`. The output is:

```text
A personal access token has been created! The token will expire 30 days from now.
Here is your access token: pat_**************************
```

2. Save the token immediately; it is shown only once. Store it as the repository secret `SPIN_AKA_ACCESS_TOKEN` through **Settings → Secrets and Variables → Actions → New repository secret**, or with `gh secret set SPIN_AKA_ACCESS_TOKEN` (which prompts for the value) or `gh secret set SPIN_AKA_ACCESS_TOKEN < access_token.txt`. Any secret name works if the workflow references the same name.
3. Create `.github/workflows/deploy.yml`:

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

The workflow runs `spin aka deploy` without `--no-confirm`, `--app-id`, or `--create-name`. The sources do not explain how the confirmation prompt and app selection behave in CI. **Inference:** pass `--app-id` and `--no-confirm` for non-interactive deployments of an existing app. The workflow also never runs `spin plugin install aka`, although the quickstart installs the plugin to interact with Akamai Functions, and the sources do not say whether the CI install script includes it. **Inference:** add `spin plugin install aka` if `spin aka` is unavailable in CI.

Add build tools before `spin build` when needed, for example the Rust target. This excerpt is from the source and omits the `mv spin /usr/local/bin/spin` line shown in the full workflow:

```yaml
- name: Install Spin
  run: curl -fsSL https://wasm-functions.fermyon.app/downloads/install.sh | bash

- name: Add build dependencies
  run: rustup target add wasm32-wasip1

- name: Build
  run: spin build
```

Pass variables from repository secrets. The source's `run:` line is over-indented; it is normalized here:

```yaml
- name: Deploy to Akamai Functions
  run: spin aka deploy --variable compression_level=${{ secrets.COMPRESSION_LEVEL }}
```

Token rotation: tokens expire after 30 days by default. Before the old token expires, create a new one, optionally with a longer expiration of up to 90 days, and update the repository secret:

```shell
spin aka auth token create --name mynewtoken --expiration-days 90
```

```text
A personal access token has been created! The token will expire 90 days from now.
Here is your access token: pat_**************************
```

### 4.19 Property Manager integration

**Sources:** [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md)

The tutorial routes a path on an existing Akamai property, such as `https://www.mydomain.com/hello`, to a Functions application. Its prerequisites are a property created and configured in Akamai Control Center, public-preview access, Spin, and the `aka` plugin.

1. Create and deploy the application. The tutorial uses `spin new -E akamai-functions -t http-js -a hello-akamai-functions` and `src/index.js`:

```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

router.get("/", () => new Response("Hello, Akamai Functions"));

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

The source's first line reads `Fimport { AutoRouter } from 'itty-router';`, a typo that is fixed above (§5.6). Build and deploy with `spin build` and `spin aka deploy`. Deployment requires authentication with `spin aka login`, using Akamai Control Center or GitHub credentials. Copy the app URL from the deploy output, or get it later with `spin aka app status`.

2. In Control Center, open the latest property version and select **Edit New Version**. Add a rule with **+ Rule** → **Blank Rule Template**. Add a match with **+ Match**: `Path` `matches one of` `/hello/*`.
3. Add the **Origin Server** behavior (**+ Behavior** → **Standard Property Behavior**):

| Field | Value |
|---|---|
| Origin Server Hostname | The application's origin: its URL without the `https://` prefix and the trailing `/` |
| Forward Host Header | Origin Hostname |

4. Add **Modify Outgoing Request Path** so that the routing criteria (`/hello/`) are not sent to the application:

| Field | Value |
|---|---|
| Action | Replace Part of the incoming path |
| Find what | `/hello/` |
| Replace with | `/` |
| Occurrences | First occurrence only |
| Keep the query parameters | Yes |

5. Save and activate the new property version. The rule is not active until activation. Activating in Staging first is highly recommended.
6. Test with `curl https://<your-property-domain>/hello/`. It should print `Hello, Akamai Functions`, the same response as the application's root route.

The `http-js` template, the root-route response, and the `/hello/` path are tutorial choices, not requirements for every Property Manager integration.

### 4.20 Version and compatibility ledger

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

| Area | Exact source note |
|---|---|
| Platform | "Limited availability" and "public preview" |
| Command reference | Every command lists `Spin compatibility: >=v4.0.0`. `--help` output is shown for `aka` plugin v0.7.6, v0.7.0, and, for some commands, v0.4.0/0.4.1. The page does not say which plugin version needs which Spin version. |
| Quotas page | "Akamai Functions supports Spin CLI v0.6.0 or newer." This conflicts with the command reference's `>=v4.0.0`, and the sources do not explain the difference. Follow the dedicated command reference when generating commands. |
| Windows quickstart | Links to the Spin v3.6.2 Windows binary release. This conflicts with `Spin compatibility: >=v4.0.0`. The macOS and Linux steps use an install script without a pinned version. |
| JavaScript/TypeScript quickstart | Recommends Node.js 22 or newer. The example output is `v22.13.0`. |
| Rust quickstart | Target `wasm32-wasip1` |
| Go quickstart | TinyGo 0.27 or above and `CGO_ENABLED=1`. The build output shows `github.com/spinframework/spin/sdk/go v0.10.0` (see §5.6). |
| MySQL tutorial | Recommends Node.js 21 or higher. Uses Linode Managed Databases, `@spinframework/spin-mysql`, `@spinframework/spin-variables`, and `uuid`. The command uses `http-ts`, but the prose says `http-js`. |
| PostgreSQL tutorial | `http-js` template, NEON, `@spinframework/spin-postgres`, `@spinframework/spin-variables`, and `uuid` |
| Supabase cache proxy | `http-ts` template, `itty-router`, `@spinframework/spin-variables`, `@spinframework/spin-kv`, and `@supabase/supabase-js` |
| Object-store tutorial | Prerequisite Node.js 22 or later. `http-ts` template, `@spinframework/spin-variables`, and `@aws-sdk/client-s3`. |
| KV tutorial | `http-js` template, `@spinframework/spin-kv`, and `itty-router`. Local data persists in SQLite. |
| WASI snapshots | `wasi-config` 2024-09-27; `wasi-keyvalue` 2024-10-17 |
| Account management | `spin aka info` account display requires plugin v0.4 or higher |
| Cron | Tech Preview, `UNSTABLE` in the CLI. The tutorial uses the `http-js` template. |

### 4.21 Platform and operational reference

**Sources:** [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md)

#### Availability, placement, and routing

- Akamai Functions is in limited availability (public preview). The FAQ says it is "deployed throughout the world in more than 20 locations."
- The welcome page describes a globally distributed PaaS hosted on Akamai Cloud, with "global geo replication by default." Client requests are forwarded "to the fastest responding region where your application is available." The comparison page says execution is routed automatically by the user's location.
- There is no infrastructure to provision, patch, or maintain.

#### Access and onboarding

- Logging in and deploying require public-preview access, requested through the onboarding form (`https://fibsu0jcu2g.typeform.com/fwf-preview`). "The Akamai Functions team will review your request and follow up shortly," so access is not immediate. The quickstart's login prerequisites are installing the `aka` plugin, receiving allow-listing status, and receiving preview access.
- Serverless AI access is requested through a Limited Access form (`https://fibsu0jcu2g.typeform.com/to/dOFZ338a?typeform-source=developer.fermyon.com`). Team accounts are requested through their own form (`https://fibsu0jcu2g.typeform.com/to/coitknMl?typeform-source=developer.fermyon.com`). For higher quota limits, the quotas page tells customers to contact their Akamai representative.
- For help, the FAQ directs users to their Akamai representative. The CLI also provides `spin aka send-feedback`.

#### Accounts, ownership, visibility, and collaboration

- The account guide says signing up assigns a personal account automatically, and that all actions run in that account's context unless a team account is used. The FAQ says each user's account is "created using the `spin aka login` command" and is "the primary entity for resource management."
- The personal account name matches the sign-up username.
- Applications in a personal account belong to that account and operate independently. Only that user can view and interact with them. Applications include metadata, dependencies, and deployment configurations.
- Team accounts provide collaboration. A team account is requested with a team name and the complete list of member usernames; the same form, with **Modify existing account** selected on question two, adds or removes members. After the confirmation email, members see the team in `spin aka info` while logged in with a profile that was added. The FAQ more generally says to "reach out to support" for shared access.
- There is currently no limit on the number of team accounts or on users per team account.
- Team accounts have no RBAC or per-application permissions (§1.6).
- The command reference says omitted account selectors default to "the current account context." The account guide says that otherwise "the default will be your personal account." Pass `--account-name` or `--account-id` whenever the target account matters.

#### Authentication and distinct lifetimes

- Interactive login supports two identity providers, Akamai Control Center and GitHub. "If you have an Akamai Control Center account, you can log in using your user ID and password. Otherwise, you need to use GitHub" (an individual GitHub account). Accounts with the same email address are cross-linked automatically. `spin aka login` prints a device-login URL (for example `https://login.infra.fermyon.tech/realms/neutrino/device?user_code=...`). The user authenticates there and then authorizes the `spin` CLI.
- The FAQ says: "Your login session started by `spin aka login` persists for 30 days without activity." The sources do not say how this applies to logins with `--token`.
- A personal access token is a separate credential, intended for contexts without a browser such as CI/CD. It expires after 30 days by default and after at most 90 days (§1.9). `spin aka login --token` or the `SPIN_AKA_ACCESS_TOKEN` environment variable supplies it. Do not apply the token rules to the interactive-login session, or the reverse.
- The FAQ question also asks whether applications persist after logout, but its answer covers only the session duration. Application lifecycle is documented separately: an application persists until it is explicitly deleted with `spin aka app delete`.

#### Application identity and URLs

- A deployed application has "a stable URL that persists across deployments." Updates preserve its name and URL.
- Example application URLs in the sources use three host patterns: `https://<uuid>.fwf.app` (quickstart, variables, list and inspect, logs), `https://<uuid>.aka.fermyon.tech` (KV, cron, MySQL, PostgreSQL, Supabase), and `https://<uuid>.aka.akamai.tech` (Property Manager, object storage). The quotas page's inter-application example is `https://<app-id>.fwf.app`. Get the real URL from the `spin aka deploy` output or `spin aka app status`. Do not construct it.
- The application ID is a UUID, shown by `spin aka app list --verbose` and `spin aka app status`.
- In the sample output, responses from deployed applications carry platform headers such as `Server: envoy`, `x-envoy-upstream-service-time`, `Akamai-GRN`, and `Set-Cookie: akaalb_...`. These are observed sample output, not documented behavior.

#### Configuration, storage, networking, and observability

- Changing an application variable is a deployment, not a runtime hot swap, and it increments the version. Variables are encrypted at rest and in transit for the application's lifetime, but the cryptographic implementation has not been assessed for PCI compliance.
- The managed KV store is isolated to one application and needs explicit permission for each component. It is globally replicated, with a replica in the same geographic area as each compute region, and standard operations have read-your-writes behavior within a request.
- A database server may need to allow inbound connections from Functions. The MySQL tutorial allows `0.0.0.0/0` during the public preview, and the sources publish no egress IP ranges (§1.4).
- Akamai Functions captures everything an application writes to stdout and stderr. `spin aka logs` targets the linked application by default and can filter by component, deployment version, region, and time. `spin aka app status` reports invocation counts over a `--usage-since` window.

### 4.22 Akamai Functions, EdgeWorkers, and workload placement

**Sources:** [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

The sources present the two products as complementary layers. Traffic-flow logic belongs in EdgeWorkers, and logic about "what happens to the data" belongs in Functions.

| Area | EdgeWorkers | Akamai Functions |
|---|---|---|
| Runtime | JavaScript (V8) | WebAssembly (Spin, which uses Wasmtime) |
| Execution layer | CDN / HTTP pipeline at Akamai's edge locations | Akamai Cloud regions, with automatic location-based routing |
| Primary use | Traffic orchestration and request/response manipulation | Application logic, APIs, microservices, and AI inference |
| Execution time | Less than 10 seconds, varying by event and tier | 30 seconds default, extendable (§1.2) |
| Trigger model | HTTP lifecycle events: `onClientRequest`, `onOriginRequest`, `onOriginResponse`, `onClientResponse`, and `responseProvider` | HTTP requests. Cron invokes an HTTP path and does not add a trigger type. |
| Infrastructure | Fully managed | Fully managed |
| Data access | Outbound HTTP to Akamized hostnames; EdgeKV | Outbound HTTP to any (allowlisted) hostname; Functions KV; customer-managed MySQL, PostgreSQL, and Redis |

Functions features from the comparison page: fully managed; a Wasm runtime that is language-agnostic with fast cold starts and strong sandboxing; auto-routing to the nearest region; longer execution than CDN-layer compute; and the Spin framework.

Data-store guidance from the comparison page:

- MySQL is compatible with Linode DBaaS MySQL. The page calls it "the smoothest path today" for a fully managed Akamai-native persistence layer in a single region; a multi-region MySQL cluster needs extra effort.
- PostgreSQL is not yet compatible with Linode DBaaS, so use self-managed or third-party PostgreSQL.
- Redis has to be brought by the customer. Akamai does not currently offer managed Redis.
- The page says "the platform roadmap indicates managed options are coming" for PostgreSQL and Redis. Do not treat this as current availability.
- Outbound HTTP to any hostname avoids "needing to create a CDN property to act as proxy."

Documented Functions use cases:

- Edge API endpoints and microservices served from the nearest region.
- Real-time data transformation and enrichment.
- Server-side rendering with lightweight frameworks such as Preact.
- WebAssembly-based image and media processing.
- Stateful CRUD APIs against self-managed PostgreSQL.
- Session validation against a customer-managed Redis cluster co-located with the nearest region, with total latency under 50 ms in the example.
- AI agents that call external inference. Inference itself runs outside Functions.

Documented EdgeWorkers use cases: advanced request routing, A/B testing and feature flagging, authentication and token validation (with EdgeKV blocklists), cache-key customization, security-header enforcement, and geography-based content adaptation. EdgeWorkers `responseProvider` can act as an origin and has somewhat higher limits than other events. It still provides lightweight compute limited by small CDN regions.

Combined designs treat EdgeWorkers as the traffic controller and Functions as the application server. "EdgeWorkers can make requests to Akamai Functions, or Akamai Functions can push data into the EdgeKV admin APIs." Documented examples:

- Personalized content assembly: EdgeWorkers serves cached variants and routes cache misses and fully personalized pages to a Function, in a pattern "similar to Edge Side Includes."
- Multi-region failover: a Function periodically polls origin health and writes status to a store such as EdgeKV, and EdgeWorkers reads it to make routing decisions.
- Token revocation: a Function keeps the revocation list in MySQL as the source of truth, reconciles it to EdgeKV, and exposes the control plane both as an OpenAPI-described API and as an MCP server for AI agents.

The sources define no EdgeWorkers configuration or EdgeKV admin-API binding for these integrations. Functions KV and EdgeKV remain separate stores (§1.3).

---

## 5. Cross-Reference

### 5.1 API and event-handler availability matrix

**Sources:** [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md)

| Object/API | JS/TS `fetch` handler | Rust `#[http_component]` | Go `spinhttp.Handle` | Cron invocation |
|---|---|---|---|---|
| Incoming HTTP request | `event.request` | `spin_sdk::http::Request` | `*http.Request` | The same HTTP handler at the configured path |
| Outgoing HTTP response | `Response` through `event.respondWith` | `Response` / `IntoResponse` | `http.ResponseWriter` | The same HTTP response contract |
| Injected Spin headers | `request.headers.get(name)` (**Inference**, §3.1) | `req.header(name)` | Not shown in the sources | Available as for any HTTP request |
| `AutoRouter`, `router.*`, `router.fetch` | ✅ | Not documented | Not documented | ✅ in the JS cron tutorial |
| `Variables.get` | ✅ | No binding documented | No binding documented | ✅ if the invoked JS route uses it |
| `openDefault` / `Kv.openDefault` | ✅ | No binding documented | No binding documented | ✅ if the invoked JS route uses it |
| `Mysql.open` / `Postgres.open` | ✅ | No binding documented | No binding documented | ✅ if capability and config exist |
| `S3Client` / `s3.send` | ✅ | No binding documented | No binding documented | ✅ if capability and config exist |
| Supabase client | ✅ | No binding documented | No binding documented | ✅ if capability and config exist |
| Outbound HTTP | Global `fetch` (illustration, §4.13) | Not documented | Not documented | ✅ if capability exists |
| Logging | `console.log` | `println!` in the template (stdout is captured) | `log/slog` in the logging page's example | ✅ (`spin aka logs`) |

HTTP is the only supported trigger. A cron job is the platform's scheduler calling the configured HTTP path of the deployed application. The cron column is an **Inference** from the tutorial's statement that a cron job invokes the application's HTTP endpoint; the cron sources do not discuss headers or SDK bindings.

### 5.2 Object/method interactions

**Sources:** [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

```text
[[trigger.http]] (route "/...", component)
  -> JS addEventListener('fetch', handler)
       -> event.request
       -> Variables.get(name) -> context { connectionString } | { config }        (§3.2 Patterns A/B)
       -> router.fetch(event.request, context)
            -> .all('*', withConfig) middleware -> request.config               (§3.2 Pattern C)
            -> first matching route handler(request, context)
                 -> request.params / request.headers.get('spin-path-match-n')
                 -> request.arrayBuffer() -> TextDecoder -> JSON.parse
                 -> openDefault() / Kv.openDefault()
                      -> exists / getJson / setJson / delete
                 -> Mysql.open(connectionString)     -> query(sql, [..?..]).rows / execute(...) (return value undocumented, §4.5)
                 -> Postgres.open(connectionString)  -> query(sql, [..$n..]).rows / execute(...) (used as affected-row count, §4.6)
                 -> createClient(url, key)
                      -> from(table).select/insert/update/delete/eq/order/maybeSingle/single
                 -> new S3Client(config)
                      -> send(ListObjectsV2Command) -> Contents
                      -> send(GetObjectCommand) -> Body as ReadableStream
                           -> pipeThrough(TransformStream) -> Response
                 -> fetch('https://<app-id>.fwf.app', init)
                 -> new Response(...) / json(...) / string
            -> unmatched route -> 404
       -> event.respondWith(response or promise)
```

Other language entry points map to the same trigger:

```text
[[trigger.http]] -> Rust #[http_component] fn(Request) -> anyhow::Result<impl IntoResponse>
[[trigger.http]] -> Go init() -> spinhttp.Handle(func(http.ResponseWriter, *http.Request))
cron schedule (UTC) -> deployed HTTP path-and-query -> one of the handlers above
```

### 5.3 Required manifest/deployment capability by API

**Sources:** [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md)

| API/feature | Required configuration or deployment action | Documented result if omitted |
|---|---|---|
| HTTP handler | `[[trigger.http]]` with `route` and `component` | `http` is the only supported trigger. No error is documented. |
| `Variables.get(name)` | Declare under `[variables]`, grant under `[component.<id>.variables]` (`name = "{{ name }}"`), and supply values with `SPIN_VARIABLE_<NAME>` locally or `--variable` on deploy | Not stated for an ungranted variable. For a missing value, the database samples respond `500` (`Connection String not specified`), the object-store sample intends `500` (`Application not configured correctly`, §3.2), and the Supabase middleware throws `Required Configuration data not set`, with an undocumented HTTP result. |
| `openDefault()` / `Kv.openDefault()` | `key_value_stores = [ "default" ]` on the component | Not stated. Labels other than `"default"` are not allowed. |
| `Mysql.open(...)` | `allowed_outbound_hosts = ["mysql://{{ mysql_host }}:{{ mysql_port }}"]`, plus inbound access allowed on the MySQL cluster | Described as needed for outbound connectivity. No error is documented. |
| `Postgres.open(...)` | `allowed_outbound_hosts` entry `postgres://<host>:5432` (explicit port) | Described as needed for outbound connectivity. No error is documented. |
| Supabase client | Project URL in `allowed_outbound_hosts`. Variables `supabase_url` and `supabase_key`, plus `supabase_webhook_token` for webhooks. `key_value_stores = ["default"]` for the cache. | The middleware throws `Required Configuration data not set`. The resulting HTTP response is not documented. |
| S3 client | Object-storage HTTPS host in `allowed_outbound_hosts`. Variables `region`, `endpoint`, `bucket_name`, `access_key_id`, and `secret_access_key`. | Missing variables: intended `500` `Application not configured correctly` (§3.2) |
| Inter-application `fetch` | The other application's full public URL, granted in `allowed_outbound_hosts` like any outbound host | `localhost` and short service names cannot be used. No error is documented. |
| Cron job | A deployed HTTP application, a UTC schedule, and a unique schedule/path-and-query pair | The duplicate-job error is not stated |
| Rust build | `rustup target add wasm32-wasip1` | The CI guide says such projects "need" the target before they compile |
| Go build | TinyGo 0.27+ and `CGO_ENABLED=1` | Listed by the quickstart as checks when the build fails |

### 5.4 CLI context and lifecycle interactions

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md)

| Command | Implicit context | Related commands and data |
|---|---|---|
| `spin aka deploy` / `spin aka app deploy` | The current account context and `./spin.toml`, unless selectors override them. The app is inferred from the workspace config; if none is inferred, a new app is created and the workspace is linked. | `--variable`, `--create-name`, `--no-confirm`, `--skip-readiness-check`, `--build`, and `--app-id`. Each deploy is a new version. |
| `spin aka app link` / `app unlink` | The workspace at `--from` | `link` prompts for the app when `--app-name`/`--app-id` is omitted. In v0.7.6, `unlink` accepts only `--from`. Unlinking does not delete the app. |
| `spin aka info` | The logged-in user and the current workspace | Shows the accounts (account names and IDs on plugin v0.4+), the workspace root, and the linked app |
| `spin aka app list` | The current account context (the account guide says the personal account) unless an account selector is given | `--verbose` shows app IDs; `--format json` emits JSON |
| `spin aka app status` | The workspace-linked app unless `--app-name`/`--app-id` is given | Name, ID, URL, creation time, and invocations over `--usage-since` (5 minutes to 7 days) |
| `spin aka app history` | The workspace-linked app unless selected | Past events for the app. `--format plain\|json`. |
| `spin aka logs` / `app logs` | The workspace-linked app unless selected; latest deployment version; all components; all regions | Captured stdout and stderr. `--since` (default `7d`), `-n/--max-lines` (default `10`), `--component-id`, `--deployment-version`, and `--region`. |
| `spin aka app delete` | The selected or current account and app | Permanent. Any team member can do it because RBAC is absent. `--no-confirm` skips the prompt. |
| `spin aka cron create/list/delete` | The deployed app of the current workspace unless selected | Calls an HTTP path. Tech Preview / `UNSTABLE`. Schedules are UTC. |
| `spin aka login` / `auth login` | Interactive device login, or `--token` / `SPIN_AKA_ACCESS_TOKEN` | The FAQ says a login session started by `spin aka login` persists for 30 days without activity; its application to `--token` logins is not stated. PATs have their own expiration. |
| `spin aka auth token create/list/delete/regenerate` | The current user | Save a new token immediately, store it as a CI secret (the guide names it `SPIN_AKA_ACCESS_TOKEN`, but any name works if the workflow matches), and rotate it before expiration. `--token` also reads the `SPIN_AKA_ACCESS_TOKEN` environment variable. |

### 5.5 Cross-platform and data-service interactions

**Sources:** [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

| Interaction | Documented purpose | Capability or boundary |
|---|---|---|
| Akamai property → Akamai Functions | Route a property path to a Functions application | Origin Server set to the app's origin, Forward Host Header set to Origin Hostname, and the path rewritten (§4.19) |
| EdgeWorkers → Akamai Functions | Route selected requests from the CDN pipeline to application logic | The sources state this interaction but give no EdgeWorkers configuration signature |
| Akamai Functions → third-party HTTP APIs | API orchestration, external services, and inference calls | The target must be in the component's `allowed_outbound_hosts`. In the AI-agent use case, inference runs outside Functions. |
| Akamai Functions → MySQL/PostgreSQL | Customer-managed relational persistence | Use the `mysql://` or `postgres://` capability with an explicit port. MySQL works with Linode DBaaS; PostgreSQL does not yet (§4.22). |
| Akamai Functions → Redis | Caching, sessions, pub/sub, rate limits, leaderboards, and locks | Outbound Redis is supported, but the sources give no SDK binding or manifest example. Akamai offers no managed Redis today. |
| Akamai Functions → EdgeKV admin APIs | Publish control-plane data, such as revocation lists or origin health, for EdgeWorkers | The use-cases page states the integration but gives no binding. EdgeKV stays separate from Functions KV. |
| Akamai Functions → another Functions application | Inter-application calls | Use the full public URL, never `localhost` or a short name. This is separate from the "Service Chaining" feature row in §4.13. |
| Cron service → Akamai Functions HTTP route | Periodic polling, maintenance, synchronization, and notifications | Tech Preview, UTC schedules, and a unique schedule/path pair |
| Akamai Functions with other Akamai services | API Acceleration, App & API Protector, and managed databases | The welcome page says any Akamai CDN, Security, or Cloud service can be used with Functions applications. Other pages add exceptions: PostgreSQL is not yet compatible with Linode DBaaS, and the KV page says Edge is not currently compatible (§5.6). |

### 5.6 Source conflicts and sample defects

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md)

Cross-source conflicts:

| Topic | What the sources say | Guidance for generated output |
|---|---|---|
| Supported Spin version | Command reference: `>=v4.0.0`. Quotas page: "Spin CLI v0.6.0 or newer." Windows quickstart: links Spin v3.6.2. | Unresolved. Follow the command reference for commands, and state the version assumption in generated docs. |
| `cron create` syntax | Command reference: `create [OPTIONS] --schedule <SCHEDULE>` with `-p, --path-and-query` and `--name`. Tutorial: `spin aka cron create "*/5 * * * *" "/" "cron-job-1"`. | Use the option form (§4.17, §6.21) |
| Deleting an app | Command reference: `spin aka app delete`. Account guide: `spin aka delete app ...`. | Use `spin aka app delete` (§6.20) |
| Linking a workspace | Command reference: `spin aka app link` and no top-level `link` in any version. Link guide and logging page: `spin aka link`. | Use `spin aka app link` (§6.22) |
| Manifest path option | Command reference: `-f, --from <PATH>`. Variables guide: "`spin aka deploy` can point to a `spin.toml` file by using the `--file` option." | Use `-f` / `--from` (§6.23) |
| Deploy target selection | Link guide: once linked, `spin aka deploy` targets the application "without needing to pass `--app-name` each time." Command reference: `deploy` has `--app-id` and `--create-name` but no `--app-name` in any version shown. | Use a linked workspace or `--app-id` (§6.26) |
| Default account | Command reference: "the current account context." Account guide: "the default will be your personal account." | Pass `--account-name` or `--account-id` explicitly |
| Account creation | Account guide: a personal account is assigned automatically at sign-up. FAQ: the account is "created using the `spin aka login` command." | Treat both as documented. Sign-up and preview access precede login. |
| Shared access | Account guide: request a team account with a form. FAQ: "reach out to support" for shared access to applications. | Point users to the team-account request |
| Spin install script | Quickstart: `https://developer.fermyon.com/downloads/fwf_install.sh`. CI guide: `https://wasm-functions.fermyon.app/downloads/install.sh`. | Both are documented; use the one matching the context (§4.14) |
| Language support rule | "Require WASI support" versus "anything with WASI or Spin SDK support runs" | TypeScript (SDK without WASI) is documented as working. Prolog (also SDK without WASI) is not documented by any Akamai page (§4.12). |
| Example app URLs | `*.fwf.app`, `*.aka.fermyon.tech`, and `*.aka.akamai.tech` | Use the URL printed by `spin aka deploy` or `spin aka app status` |
| AI inference placement | Comparison page: AI inference "belongs in Akamai Functions," including "AI inference endpoints." Use-cases page: "(inference itself runs outside of functions)." Quotas page: Serverless AI is Limited Access. | Do not assume in-runtime inference. Call external inference APIs through `allowed_outbound_hosts` (§4.13). |
| EdgeKV | KV page: "Edge is not currently compatible with Akamai Functions." Use-cases page: Functions push data into the EdgeKV admin APIs, write origin-health status to EdgeKV, and reconcile revoked tokens to EdgeKV. | **Inference:** the KV statement concerns the store, while the use cases call EdgeKV's admin APIs. The sources do not reconcile the two (§1.3). |
| Other Akamai services | Welcome page: any Akamai CDN, Security, or Cloud service can be used. Comparison page: PostgreSQL is not yet compatible with Linode DBaaS. KV page: the EdgeKV statement above. | Treat the welcome statement as general positioning, and check the specific service (§4.13) |
| KV label | "only allows the `"default"` label" versus a code comment that mentions `Kv.open("mylabel")` | Use only `"default"` (§6.9) |

Defects inside individual samples:

| Sample | Defect | Guidance |
|---|---|---|
| MySQL and PostgreSQL entry points | The missing-variable branch calls `event.respondWith(...)` without `return`, then calls `event.respondWith(router.fetch(...))` again | Return after the first call (corrected form in §3.2; **Inference**) |
| Object-store entry point | Returns `new Response(..., { status: 500 })` from the fetch listener without `event.respondWith` | Wrap the response in `event.respondWith(...)` (**Inference**, §3.2) |
| MySQL `execute` result | The samples store `connection.execute(...)` as `updatedRows` or `deletedRows` and compare it with `0`. The source does not document the return value. | **General knowledge:** the `@spinframework/spin-mysql` SDK returns `void` from `execute`, so these checks never match. Detect missing rows another way (§4.5). |
| Object-store routes | The code registers `/files/:name` and `/transformed-files/:name`, but the prose and curl tests use `/file/:name` and `/transformed-file/:name` | Keep registered routes and requests consistent (§6.24) |
| Object-store and Supabase manifests | Component variable values are rendered as `""` (and `"https://"`), `allowed_outbound_hosts = ['https://.']`, and `["<your-supabase-url-here>"]` | Use `"{{ name }}"` grants and real hosts (§4.3, §4.8) |
| Supabase variables | `supabase_key = { required = true, sensitive = true }`, while every other secret uses `secret = true` | Use `secret = true`, the attribute used everywhere else in the sources |
| Supabase webhook middleware | `import * as Variables from "@spinframework/spin-kv";` | Import from `@spinframework/spin-variables` (§6.25) |
| Supabase first middleware | `const ttl = (Variables.get('cache_ttl') ?? "5");` assigns a string to the numeric `cacheTtl` | Convert with unary `+`, as the webhook revision does |
| Supabase `src/cache.ts` | The `invalidate` function's second `if` lacks its opening `{` | Corrected in §4.4 |
| Supabase webhook import | `import processDatabaseUpdate from './inform';` default-imports a named export | Use `import { processDatabaseUpdate } from './inform';` (§4.7) |
| Supabase cache header | The prose says `x-served-by-cache`; the code and output use `x-served-via-cache` | Use the header the code sets, `x-served-via-cache` |
| Supabase delete count | `deleteArticleById` returns `404` when `response.count == 0` | **General knowledge:** supabase-js leaves `count` as `null` unless the query requests it, for example `.delete({ count: 'exact' })` (§4.7) |
| Database update handlers | Return `Location: /items/${id}`, while create returns `/products/${id}` | Prefer the resource path that matches the routes (`/products/...`) |
| MySQL tutorial | The prose says the `http-js` template; the command uses `-t http-ts` and TypeScript | Follow the command |
| PostgreSQL tutorial | Its install note names `@spinframework/spin-mysql`, and the deploy step mentions "the MySQL database" | Install `@spinframework/spin-postgres` (§2.11) |
| Multi-line commands | The MySQL, PostgreSQL, and object-store deploy commands, and the MySQL and PostgreSQL `POST` `curl` examples, are split across lines without shell line continuations. The `curl` examples also wrap the URL in `<…>`. | Use `\` continuations or one line, and pass the bare URL (§4.5, §4.6, §4.8) |
| GitHub Actions variables step | The `run:` line is over-indented relative to `- name:` | Indent `run:` at the same level as `name:` (§4.18) |
| Property Manager sample | The first line reads `Fimport { AutoRouter } from 'itty-router';` | `import { AutoRouter } from 'itty-router';` (§4.19) |
| Cron interval example | `* */12 * * *` is described as "every 12 hours" | **General knowledge:** use `0 */12 * * *` for once every 12 hours (§4.17) |
| Cron tutorial step 2 | The prose mentions a `/*` path with a `msg=fwf` query, but the command uses `/` and no query | Pass the query in `--path-and-query` when one is needed |
| Go SDK version in build output | The import path is `github.com/spinframework/spin/sdk/go/v2/http`, but the build output shows `github.com/spinframework/spin/sdk/go v0.10.0` being downloaded | **General knowledge:** a `/v2` import path belongs to a v2 module. Treat `v0.10.0` as sample output, not a version requirement (§2.10). |
| Quickstart sample response | The local test output shows `Hello, Fermyon`, which matches none of the template responses (`hello universe`, `Hello, Akamai`, `Hello Akamai!`) | Expect the response your template returns |
| Cron sample log line | The `console.log` template string ends with a stray `"`, and the sample log line's timestamp (2025-04-12) differs from its log date (2025-04-02) | Remove the stray quote, and treat the log output as illustrative |

### Source Coverage

This table accounts for every active entry in `docs/reference-manifest.json`. `Included` rows name substantive subsections that incorporate the source's unique reference facts. `Excluded` is reserved for a source that contains no source-specific Akamai Functions API, constraint, operational fact, or working code pattern.

| Active exact source | Status | Compiled coverage or exclusion reason |
|---|---|---|
| [aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md) | Included | §1.6, §1.7, §1.8, and §1.9 CLI-backed constraints; §4.3 `--variable` semantics; §4.10 log filters; §4.15 command reference (v0.7.6 signatures, options, and defaults); §4.16 v0.7.0 and v0.4.x differences; §4.17 Cron CLI; §4.18 deployment options; §4.20 compatibility ledger; §4.21 authentication and observability; §5.4 CLI context; §5.6 command-form conflicts; §6.14, §6.20, §6.21, §6.22, §6.23, and §6.26 failure patterns |
| [akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md) | Included | §1.2 execution-time wording; §1.3 Functions KV versus EdgeKV; §1.4 outbound hostnames and database services; §4.12 languages; §4.13 AI inference and other services; §4.21 routing; §4.22 workload placement and data stores; §5.5 cross-platform interactions; §5.6 AI-inference and service conflicts |
| [application-logs.md](../_source/techdocs-akamai-com/application-logs.md) | Included | §3.1 stdout/stderr capture; §4.10 Logging (the page is titled "Application logs and usage"); §4.15 log targeting; §4.21 observability; §5.1 logging matrix; §5.4 log context; §5.6 `spin aka link` conflict; §6.18 and §6.22 failure patterns |
| [build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md) | Included | §1.3, §1.4, and §1.5 capability rules; §2.1, §2.2, §2.3, §2.7, and §2.11 imports and packages; §3.1 and §3.2 handler and middleware patterns; §4.2 routing forms; §4.3 variables; §4.4 cache module; §4.7 Supabase client, webhook, and manifest; §4.10 cache logs; §4.20 ledger; §4.21 URLs; §5.1, §5.2, and §5.3 cross-reference tables; §5.6 sample defects; §6.4, §6.5, §6.6, §6.9, §6.11, §6.13, and §6.25 failure patterns |
| [delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md) | Included | §1.6 deletion and RBAC; §4.15 delete command and output; §4.21 lifecycle; §5.4 CLI context |
| [deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md) | Included | §1.5 variable deployments and PCI caveat; §4.3 Application variables; §4.18 updates; §4.21 configuration; §5.3 and §5.4 cross-reference tables; §5.6 `--file` conflict; §6.16 and §6.23 failure patterns |
| [deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md) | Included | §1.8 CI build tools; §1.9 token constraints; §4.3 CI variables; §4.11 language guides; §4.14 CI install script; §4.18 GitHub Actions workflow and token rotation; §4.21 tokens for non-browser contexts; §5.3 and §5.4 cross-reference tables; §5.6 workflow defects |
| [faq.md](../_source/techdocs-akamai-com/faq.md) | Included | §4.21 availability, accounts, login-session duration, and support; §5.6 account-wording differences |
| [http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md) | Included | §1.1 HTTP-only trigger; §3.1 handler objects; §4.1 trigger manifest and injected headers; §5.1, §5.2, and §5.3 cross-reference tables; §6.1 failure pattern |
| [integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md) | Included | §1.10 Property Manager settings; §2.1 router import; §3.1 entry point; §4.14 template usage; §4.19 integration steps; §4.21 URLs; §5.5 property routing; §5.6 `Fimport` defect; §6.2 and §6.19 failure patterns |
| [link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md) | Included | §1.6 unlink does not delete; §4.15 workspace, link, and info; §5.4 CLI context; §5.6 link and deploy-target conflicts; §6.18, §6.22, and §6.26 failure patterns |
| [list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md) | Included | §4.15 `app list` and `app status` outputs; §4.21 application identity; §5.4 CLI context |
| [manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md) | Included | §1.6 team-account RBAC; §1.9 `info` plugin version; §4.15 account examples and multi-account `info` output; §4.16 plugin v0.4 note; §4.18 team-account deploys; §4.20 ledger; §4.21 accounts and collaboration; §5.4 CLI context; §5.6 account conflicts; §6.20 failure pattern |
| [query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md) | Included | §1.4 MySQL capability and inbound access; §1.5 local variables; §1.8 Node.js guidance; §2.2, §2.4, §2.6, and §2.11 imports and packages; §3.1 and §3.2 Pattern A; §4.2 routing and helpers; §4.3 variables; §4.5 MySQL; §4.9 UUID; §4.14 build output; §4.20 ledger; §4.21 URLs and database access; §5.1, §5.2, §5.3, and §5.5 cross-reference tables; §5.6 sample defects; §6.3, §6.5, §6.6, §6.7, §6.12, and §6.25 failure patterns |
| [query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md) | Included | §1.4 PostgreSQL capability; §1.5 local variables; §2.1, §2.2, §2.5, §2.6, and §2.11 imports and packages; §3.1 and §3.2 Pattern A; §4.2 routing; §4.3 variables; §4.6 PostgreSQL; §4.9 UUID; §4.14 build output; §4.20 ledger; §4.21 URLs; §5.1, §5.2, §5.3, and §5.5 cross-reference tables; §5.6 sample defects; §6.3, §6.4, and §6.7 failure patterns |
| [quickstart.md](../_source/techdocs-akamai-com/quickstart.md) | Included | §1.1 access; §1.8 toolchains; §1.9 Windows Spin version; §2.1, §2.9, §2.10, and §2.11 imports and packages; §3.1, §3.3, and §3.4 handlers; §4.1 route output; §4.2 router behavior; §4.10 local logs; §4.11 Rust and Go APIs; §4.12 quickstart languages; §4.14 setup and local development; §4.18 first deployment; §4.20 versions; §4.21 login and onboarding; §5.1, §5.2, and §5.3 cross-reference tables; §5.6 sample defects; §6.2 and §6.24 failure patterns |
| [quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md) | Included | §1.1 unsupported features; §1.2 quotas; §1.3 WASI KV interfaces; §1.4 inter-application calls; §1.7 cron Tech Preview; §1.9 Spin version note; §4.4 KV quotas; §4.13 feature support matrix; §4.20 ledger; §4.21 limits and forms; §4.22 execution limits; §5.3 and §5.5 cross-reference tables; §5.6 conflicts; §6.1, §6.8, and §6.10 failure patterns |
| [related-standards.md](../_source/techdocs-akamai-com/related-standards.md) | Excluded | A curated list of external WebAssembly, WASI, Component Model, Wagi, and Spin Improvement Proposal links. It defines no Akamai Functions API, constraint, operational fact, or working code pattern. |
| [schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md) | Included | §1.6 application persistence; §1.7 cron constraints; §2.1 and §2.11 imports and packages; §3.1 and §3.5 cron-invoked handler; §4.2 routing; §4.10 logs; §4.14 local run; §4.17 Cron CLI, syntax, and outputs; §4.20 ledger; §4.21 lifecycle and URLs; §4.22 cron in workload placement; §5.1, §5.2, §5.3, §5.4, and §5.5 cross-reference tables; §5.6 sample defects; §6.14, §6.15, and §6.21 failure patterns |
| [stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md) | Included | §1.4 outbound grants; §1.5 required variables; §1.8 Node.js prerequisite; §2.1, §2.2, §2.8, and §2.11 imports and packages; §3.1 and §3.2 Pattern B; §4.2 routing forms; §4.3 variables; §4.8 S3-compatible object storage; §4.20 ledger; §4.21 URLs; §5.1, §5.2, and §5.3 cross-reference tables; §5.6 sample defects; §6.4, §6.6, §6.12, and §6.24 failure patterns |
| [update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md) | Included | §1.5 and §1.6 deployment constraints; §4.18 updates; §4.21 application identity; §5.4 CLI context; §6.16 and §6.17 failure patterns |
| [use-cases.md](../_source/techdocs-akamai-com/use-cases.md) | Included | §1.3 EdgeKV boundary; §4.13 AI inference; §4.22 use cases and combined designs; §5.5 cross-platform interactions; §5.6 AI-inference and EdgeKV conflicts; §6.10 failure pattern |
| [use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md) | Included | §1.1 local SQLite tooling; §1.2 KV rate rationale; §1.3 KV constraints; §2.1, §2.3, and §2.11 imports and packages; §3.1 handler objects; §4.2 routing forms; §4.4 KV API and tutorial; §4.14 local KV; §4.20 ledger; §4.21 storage and URLs; §4.22 data stores; §5.1, §5.2, §5.3, and §5.5 cross-reference tables; §5.6 conflicts; §6.3, §6.5, §6.9, and §6.10 failure patterns |
| [webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md) | Included | §1.1 language rule; §1.8 toolchain context; §4.12 WebAssembly language support; §5.6 language-rule conflict |
| [welcome.md](../_source/techdocs-akamai-com/welcome.md) | Included | §1.1 platform model; §4.12 SDK languages; §4.13 integration with other Akamai services; §4.20 availability; §4.21 routing, onboarding, and stable URLs; §5.5 other Akamai services; §5.6 "any service" conflict |

---

## 6. Known Failure Patterns

Each pattern is supported by the sources. When a source does not state the exact error, the entry says so.

### 6.1 Unsupported trigger type

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md)

```text
WRONG: a component reached through a Redis trigger or a custom trigger.
```

```toml
# CORRECT — http is the only supported trigger type.
[[trigger.http]]
route = "/..."                # the route that the trigger matches
component = "my-application"  # the name of the component to handle this route
```

**Documented consequence:** Redis and custom triggers are listed as not supported. The sources do not state the error.

### 6.2 Missing JavaScript fetch registration

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md)

```javascript
// WRONG — routes are declared, but no fetch listener hands requests to the router.
let router = AutoRouter();
router.get("/", () => new Response("Hello, Akamai Functions"));

// CORRECT — every documented JS/TS entry point registers the listener.
addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

**Documented consequence:** none stated. The sources document no other JS/TS entry point.

### 6.3 Spin SDK package not installed or imported

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md)

```shell
# WRONG — call Postgres.open(...) without installing and importing the SDK package.

# CORRECT — install the packages the tutorial installs ...
npm install  @spinframework/spin-postgres @spinframework/spin-variables uuid
```

```javascript
// ... and import the SDK before use.
import * as Postgres from "@spinframework/spin-postgres";
const connection = Postgres.open(connectionString);
```

**Documented consequence:** none stated. Every tutorial installs each Spin SDK package (§2.11) and imports it (§2) before use.

### 6.4 Missing component variable mapping

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

```toml
# WRONG — declared for the application but not granted to the component.
[variables]
pg_connection_string = { required = true}
```

```toml
# CORRECT — also grant it to the component.
[variables]
pg_connection_string = { required = true}

[component.hello-postgresql.variables]
pg_connection_string = "{{ pg_connection_string }}"
```

**Documented consequence:** under the capabilities-based security model, a component can access only the variables explicitly granted to it. The sources do not state what `Variables.get` does for an ungranted variable.

### 6.5 Request body not decoded before JSON parsing

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

```javascript
// WRONG — requestBody is the ArrayBuffer returned by request.arrayBuffer().
let payload = JSON.parse(requestBody);

// CORRECT — decode first, as every documented handler does.
const decoder = new TextDecoder();
let payload = JSON.parse(decoder.decode(requestBody));
```

**Documented consequence:** none stated. **General knowledge:** `JSON.parse` does not read an `ArrayBuffer`'s bytes as JSON text. The Supabase handlers also wrap parsing in `try`/`catch` and return `400 "Bad Request"`.

### 6.6 Missing outbound host capability

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

```toml
# WRONG — no outbound grant for the database host.
[component.linode-mysql]
source = "dist/linode-mysql.wasm"
exclude_files = ["**/node_modules"]
```

```toml
# CORRECT
[component.linode-mysql]
source = "dist/linode-mysql.wasm"
exclude_files = ["**/node_modules"]
allowed_outbound_hosts = ["mysql://{{ mysql_host }}:{{ mysql_port }}"]
```

**Documented consequence:** the grant is what allows the component to send network requests to the host. The exact error without it is not stated.

### 6.7 Wrong database protocol or missing port

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

```toml
# WRONG — no mysql:// protocol, or no explicit port.
allowed_outbound_hosts = ["{{ mysql_host }}:{{ mysql_port }}"]
```

```toml
# CORRECT — MySQL
allowed_outbound_hosts = ["mysql://{{ mysql_host }}:{{ mysql_port }}"]
```

```toml
# CORRECT — PostgreSQL (the tutorial uses the default port, 5432)
allowed_outbound_hosts = [
    "postgres://ep-bread-garden-11223344.eu-central-1.aws.neon.tech:5432",
]
```

**Documented consequence:** both tutorials say the protocol and the explicit port are needed for outbound connectivity. The error is not stated.

### 6.8 Localhost or short-name calls between applications

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

```javascript
// WRONG — localhost and short service names do not reach another Spin application.
const response = await fetch('http://localhost/service');

// CORRECT — the other application's full public URL (illustration of the documented URL form).
const response = await fetch('https://<app-id>.fwf.app', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data: 'payload' })
});
```

**Documented consequence:** calls between Spin applications have to use the full public URL. The error for `localhost` or a short name is not stated. The target must also be in `allowed_outbound_hosts` (§1.4).

### 6.9 Wrong KV label

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

```toml
# WRONG — Akamai Functions allows only the "default" label.
[component.hello-key-value-store]
key_value_stores = [ "mylabel" ]
```

```toml
# CORRECT
[component.hello-key-value-store]
key_value_stores = [ "default" ]
```

**Documented consequence:** only `"default"` is allowed, and it signals the platform to provision the store automatically. The error for another label is not stated. The tutorial comment's `Kv.open("mylabel")` therefore does not apply on Akamai Functions.

### 6.10 Atomic KV or EdgeKV used for the managed store

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md)

```text
WRONG: depend on wasi:keyvalue/atomic operations, or on EdgeKV APIs, to work with the Functions KV store.
CORRECT: use the Spin KV API on the "default" store. If you call wasi:keyvalue directly, only store and batch are supported.
```

```javascript
// Adapted from the KV tutorial (three non-adjacent lines).
import { openDefault } from '@spinframework/spin-kv';
const store = openDefault();
store.setJson(key, payload);
```

**Documented consequence:** `wasi:keyvalue/atomic` is not supported because the global store does not provide the required consistency guarantee. The Functions KV store is separate from EdgeKV. Neither error is stated. Pushing data to the EdgeKV admin APIs (use-cases page) is a separate integration.

### 6.11 Optional Supabase match without a null check

**Sources:** [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

```typescript
// WRONG — a missing article is returned as a successful read.
const { data, error } = await supabase.from('articles').select().eq('id', id).maybeSingle();
return json(data, { status: 200 });

// CORRECT — adapted from the tutorial's readArticleById (comments and logging omitted).
const { data, error } = await supabase.from('articles')
  .select()
  .eq('id', id)
  .maybeSingle();
if (error) {
  return new Response(error.message, { status: 500 });
}
if (!data) {
  return new Response("Not Found", { status: 404 });
}
return json(data, { status: 200 });
```

**Documented consequence:** the tutorial uses `.maybeSingle()` because "there might be no match at all" and returns `404` when `data` is falsy. The sources do not document `.single()` behavior for zero rows.

### 6.12 Missing required configuration

**Sources:** [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md)

```typescript
// WRONG — build the S3 client without checking the required variables.
const s3 = new S3Client({ region, endpoint, credentials: { accessKeyId, secretAccessKey } });

// CORRECT — the tutorial's check. Inside the fetch listener, return the response
// through event.respondWith(...) (§3.2; the wrapper is an inference, the source returns it directly).
if (!endpoint || !accessKeyId || !secretAccessKey || !bucketName || !region) {
    return event.respondWith(new Response("Application not configured correctly", { status: 500 }));
}
```

**Documented consequence:** the intended response for missing configuration is HTTP `500` with `Application not configured correctly`. The database samples use `500` with `{"message":"Connection String not specified"}`.

### 6.13 KV list cache not invalidated

**Sources:** [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

```typescript
// WRONG — update one article but leave the cached list in place.
store.setJson(key, buildCacheData(value, ttl));

// CORRECT — excerpt of storeInCache in §4.4 (logging omitted).
store.setJson(key, buildCacheData(value, ttl));
if (key !== ALL_ARTICLES_CACHE_KEY && store.exists(ALL_ARTICLES_CACHE_KEY)) {
  store.delete(ALL_ARTICLES_CACHE_KEY);
}
```

**Documented consequence:** none stated. The tutorial's cache design calls for invalidation "whenever data is added, updated or removed from the cache." **Inference:** without it, the cached `all-articles` list can serve old data until its `expiresAt` passes.

### 6.14 Local-time cron expression

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# WRONG — 09:00 written as local wall-clock time.
spin aka cron create --schedule "0 9 * * *" --path-and-query "/" --name local-nine

# CORRECT — convert the desired time to UTC before creating the schedule.
spin aka cron create --schedule "<UTC_CRON>" --path-and-query "/" --name utc-schedule
```

**Documented consequence:** schedules run in UTC. The tutorial warns that local times may need converting "to ensure correct execution."

### 6.15 Duplicate cron schedule and path

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

```text
WRONG: create a second job in the same application with the same schedule and path-and-query.
CORRECT: change the schedule or the path-and-query so that the pair is unique.
```

**Documented consequence:** multiple cron jobs are allowed only "as long as the combination of schedule and path and query is unique." The error for a duplicate is not stated.

### 6.16 Treating a variable change as a hot swap or omitting update inputs

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md)

```shell
# WRONG — expect the running deployment to pick up a new value, or redeploy without
# the variables the update guide says to specify.
spin aka deploy

# CORRECT — supply the values with the deployment.
spin aka deploy --variable <key>=<value>
```

**Documented consequence:** a variable change is propagated as a new deployment and the version increments. The result of omitting a previously supplied value is not stated.

### 6.17 Assuming canary or blue-green version routing

**Sources:** [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md)

```text
WRONG: deploy a new version and expect both versions to receive selectable traffic.
CORRECT: treat each deployment as a replacement; only in-flight requests finish on the previous version.
```

**Documented consequence:** there is no built-in support for running multiple versions simultaneously.

### 6.18 Logs fetched from the wrong app

**Sources:** [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md)

```shell
# WRONG — the workspace is linked to a different application.
spin aka logs

# CORRECT
spin aka logs --app-name <app_name>
```

**Documented consequence:** without `--app-name`, the command returns logs for the application linked to the workspace.

### 6.19 Property Manager hostname or header mismatch

**Sources:** [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md)

```text
WRONG:
  Origin Server Hostname = https://<uuid>.aka.akamai.tech/
  Forward Host Header    = any value other than Origin Hostname

CORRECT:
  Origin Server Hostname = <uuid>.aka.akamai.tech
  Forward Host Header    = Origin Hostname
```

**Documented consequence:** none stated. The WRONG values differ from the settings the tutorial instructs, and the source gives no reason or consequence for them.

### 6.20 Non-canonical `delete app` ordering

**Sources:** [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# SOURCE DISCREPANCY — shown by the account guide.
spin aka delete app --app-name graphql --account-name dev_team_1

# CANONICAL — matches the dedicated command reference.
spin aka app delete --app-name graphql --account-name dev_team_1
```

**Documented consequence:** the command reference has no top-level `delete` command, so the first form matches no documented signature. The CLI's response to it is not documented.

### 6.21 Cron positional syntax

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# TUTORIAL FORM
spin aka cron create "*/5 * * * *" "/" "cron-job-1"

# CANONICAL COMMAND-REFERENCE FORM (v0.7.6 options)
spin aka cron create --schedule "*/5 * * * *" --path-and-query "/" --name cron-job-1
```

**Documented consequence:** the two forms conflict. The command reference makes `--schedule` required and exposes the path and name as `--path-and-query` and `--name`. The CLI's response to the positional form is not reproduced.

### 6.22 `spin aka link` instead of `spin aka app link`

**Sources:** [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# SOURCE DISCREPANCY — shown by the link guide and the logging page.
spin aka link

# CANONICAL — the dedicated command reference.
spin aka app link
spin aka app link --app-name <app-name>
```

**Documented consequence:** no version of the command reference lists a top-level `link` command (v0.7.6 top-level commands: `app`, `cron`, `deploy`, `logs`, `auth`, `login`, `send-feedback`, `info`, `help`). The CLI's response to `spin aka link` is not documented.

### 6.23 `--file` instead of `-f, --from`

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# SOURCE DISCREPANCY — the variables guide mentions a --file option.
spin aka deploy --file <path/to/spin.toml>

# CANONICAL — the dedicated command reference.
spin aka deploy --from <path/to/spin.toml>
spin aka deploy -f <directory-containing-spin.toml>
```

**Documented consequence:** the command reference defines the manifest path option as `-f, --from <PATH>` (a `spin.toml` file or a directory containing one; default `./spin.toml`) and lists no `--file` option. The CLI's response to `--file` is not documented.

### 6.24 Requested path differs from the registered route

**Sources:** [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

```text
WRONG (as published): register /files/:name and /transformed-files/:name,
                      then request /file/tiny.txt and /transformed-file/tiny.txt.
CORRECT: use the same path scheme for the registered routes, the documentation, and the requests.
```

**Documented consequence:** "Any unmatched route will return a 404" (template comment), so the published requests do not reach the stream handlers registered by the published code.

### 6.25 Application variables imported from the KV package

**Sources:** [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md)

```typescript
// WRONG — as published in the webhook revision of src/middlewares.ts.
import * as Variables from "@spinframework/spin-kv";

// CORRECT — the variables package used by every other sample.
import * as Variables from "@spinframework/spin-variables";
```

**Documented consequence:** none stated. `Variables.get` is imported from `@spinframework/spin-variables` everywhere else in the sources, including this tutorial's first middleware.

### 6.26 `spin aka deploy --app-name`

**Sources:** [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# SOURCE DISCREPANCY — implied by the link guide ("without needing to pass --app-name each time").
spin aka deploy --app-name <app-name>

# CANONICAL — the dedicated command reference.
spin aka deploy                      # in a workspace linked with spin aka app link
spin aka deploy --app-id <APP_ID>
```

**Documented consequence:** the command reference lists no `--app-name` option for `deploy` or `app deploy` in any version shown. Deploy selects its target with `--app-id` or the workspace config, and creates a new app, which `--create-name` can name, when no app is inferred. The CLI's response to `--app-name` is not documented.
