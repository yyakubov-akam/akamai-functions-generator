# Akamai Functions — Unified Coding Reference

> Master reference for generating Akamai Functions code (Spin applications compiled to WebAssembly).
> Compiled from the exact upstream Markdown sources listed in `docs/reference-manifest.json` and stored in `docs/_source/techdocs-akamai-com/`.

Conventions used throughout this reference:

- Every statement is documented Akamai Functions behavior unless it is labeled **Inference** or **General knowledge**. Labeled statements are supplementary guidance, not platform documentation.
- When sources disagree, both statements are kept and the disagreement is identified. A dedicated reference page, such as the `spin aka` command reference or the quotas page, is preferred over a tutorial only when choosing the canonical form for generated code. §5.6 indexes the conflicts and defective samples identified during compilation.
- Tutorial prerequisites, example versions, and recommendations are reported as such. They are not platform-wide requirements.
- Code blocks reproduce source code; only whitespace and Markdown escape artifacts (such as `\<` in placeholders) are normalized. Code marked as an illustration is not from a source. When a source sample is defective, the defect is called out beside it, and any corrected form is labeled as corrected.

## 1. Runtime Prohibitions

Each entry states a platform, runtime, deployment, or tooling constraint and its documented consequence. When a source does not document the error or symptom, the entry says so rather than inventing one. Defaults and other facts that restrict nothing are in §4.

### 1.1 Platform, runtime, and triggers

**Sources:** [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md), [docs/_source/techdocs-akamai-com/webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md), [docs/_source/techdocs-akamai-com/sign-up-for-akamai-functions.md](../_source/techdocs-akamai-com/sign-up-for-akamai-functions.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md)

- Akamai Functions runs Spin applications on a WebAssembly-based runtime in Akamai Cloud regions, not in the CDN delivery layer where EdgeWorkers runs. The language SDKs compile to WebAssembly, and `spin build` compiles an application to WebAssembly. The sources document no other execution format.
- `http` is the only trigger type documented for application manifests ("Akamai Functions currently supports the `http` trigger type"), and the comparison page gives the Functions trigger model as "HTTP requests." The EdgeWorkers lifecycle events (`onClientRequest`, `onOriginRequest`, `onOriginResponse`, `onClientResponse`, `responseProvider`) belong to EdgeWorkers (§4.22). The quotas page's Spin feature table lists the Redis trigger and custom triggers as not supported, and Cron as "Partial support" (Tech Preview). Its Cron row links to the `spin aka cron` tutorial, in which the platform sends scheduled HTTP requests to an application route (§1.7, §3.5); no source documents a cron trigger in `spin.toml`. The sources do not state the deployment or runtime error for a manifest that uses an unsupported trigger.
- Before a request is handled by the code, Akamai Functions strips these request headers and header prefixes: `x-request-id`, `x-forwarded-for`, `x-real-ip`, `x-forwarded-client-cert`, `akamai-*` (except `akamai-Bot` and `akamai-GRN`), `x-envoy-*`, `fermyon-*`, and `x-akamai-*`. Code therefore cannot read them, even when a client or an Akamai property sends them. For the client IP address, the HTTP trigger reference documents the `true-client-ip` header (§4.1).
- SQLite storage is not supported. Local key-value testing stores data in a SQLite file under `.spin/` (§4.4); that is local tooling, not a platform SQLite API. The source does not state the error for using the SQLite API on the platform. The quotas page adds that "Some Spin SDK triggers and APIs are not yet supported on Akamai Functions"; its feature table is in §4.13.
- AI inference: the use-cases page says that a Function used to build an AI agent "integrates with AI inference calls (inference itself runs outside of functions)." The comparison page lists "AI inference" and "AI inference endpoints" among Functions workloads (§5.6). No current source documents an inference API inside the runtime. **Inference:** generated code should call an external inference service through outbound HTTP (§1.4).
- The language-matrix page states that Akamai Functions requires WASI support (at least Preview 1), and also that anything with WASI or Spin SDK support runs on it. The two statements differ for languages that have a Spin SDK but no WASI support (§4.12).
- Access requires an Akamai Control Center (ACC) account: "To access Functions, you currently need an Akamai Control Center account." Logging in also requires Akamai Functions to be enabled on the user's ACC contract. "Only one person in your team needs to add Akamai Functions to your contract"; from then on, every ACC user coupled to that contract has access. Users authenticate with their ACC credentials, and the Functions account system uses ACC as an identity provider. The sources do not state the error that a user without access sees.
- Access starts on the sign-up page. A user without an ACC account follows the page's "Create an Akamai Functions trial account" steps: submit the form in the "Book a demo" section of the Akamai Functions homepage; after Akamai approves the demo request, an email asks the user to reset the password and activate the account, and once onboarding is complete the user activates Akamai Functions in Marketplace. A user with an active Akamai contract and ACC login activates the 30-day free trial in Marketplace directly. Users who cannot get an ACC account are directed to their Akamai account team, and access through Cloud Manager is planned for "the future" but not yet available. The sources do not say what happens to applications when the trial ends.
- The Property Manager tutorial still tells users to authenticate "using your Akamai Control Center or GitHub account credentials." The quickstart, FAQ, and account guide describe only ACC login, and no other current source mentions GitHub (§5.6).
- Deployment is documented only through the `spin aka` plugin (`spin aka deploy` or `spin aka app deploy`), including from CI. No other deployment path is documented.

### 1.2 Execution, request, and deployment quotas

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md)

The quotas page lists limits by resource tier, request, Function, account, `spin aka` plugin, logging, cron, and key-value store. This subsection covers the runtime, request, Function, and log-emission limits. Key-value limits are in §1.3, cron limits in §1.7, and plugin and log-retrieval limits in §1.9. Unless an entry says otherwise, the sources do not state the error or enforcement behavior when a limit is exceeded.

**Resource tiers.** There are currently two resource tiers: Standard, "intended for more lightweight use cases," and Extended, which "allows more computationally intensive applications."

| Limit | Standard | Extended |
|---|---|---|
| Maximum CPU time | 500 milliseconds | 1000 milliseconds |
| Maximum memory usage | 20 MiB | 128 MiB |
| Maximum wall time | 15 seconds | 30 seconds |

- "These limits can be increased to custom values" through the Akamai representative. The sources do not state what happens when a Function exceeds a tier limit.
- The quotas page does not say how a tier is assigned. The account guide's example describes a contract with Functions enabled "under the Extended plan," whose default team account is named `X-ABC-DEF-extended-default`. **Inference:** the tier follows the contract plan rather than code or `spin.toml`, so generated code should fit the Standard limits unless the plan is known.
- The comparison page gives Functions execution time as "30 seconds default, extendable." The quotas page has no single default: wall time is 15 seconds on Standard and 30 seconds on Extended, CPU time is 500 or 1000 milliseconds, and the tier limits can be raised. The 30-second figure matches only the Extended wall time (§5.6).
- Personal accounts "support lower limits and fewer requests per month"; the sources give no personal-account values. Team accounts get "the full limits and request counts specified in your contract" (§1.6).

**Request limits.** These apply "to each request handled by a Function, as well as outbound subrequests made from within a Function, for example, using the JavaScript `fetch()` API."

| Limit | Value |
|---|---|
| Request URI size | 16 KiB |
| Request body size | 10 MiB |
| Request headers count | 64 |
| Request headers size | 32 KiB |
| Response body size | 10 MiB |
| Response headers count | 64 |
| Response headers size | 32 KiB |
| Outbound subrequests | 10,000 per minute per deployed Function |

- These limits "can be increased to custom values if needed" through the Akamai representative. The sources do not state whether an oversized request or response is rejected or truncated, or what happens to subrequests over the rate.
- The body-size limits "do not apply when streaming the body through an Akamai Function"; in that case "there is no directly enforced limit besides related limits such as total memory usage."
- No requests-per-second or requests-per-minute limit is directly enforced, but "Functions has strong fairness restrictions in place which prevent a single app from taking up too many resources without manual overrides." How the restrictions affect requests is not stated. Akamai does "not recommend running your own (high scale) load tests without involvement from your Account team." Capacity checks and manual limit overrides go through the Akamai representative.

**Function quotas.**

| Quota | Value |
|---|---|
| Function bundle size | 128 MiB; "Cannot currently be increased" |
| Deployed Functions per account | 50 |
| Versions per deployed Function | 2147483647 |
| Function deploys per account per hour | 20; "Cannot currently be increased" |
| Size of a single Spin application variable | 1024 bytes |
| Size of all Spin application variables combined | 4096 bytes |

- The bundle size is "the sum of the component sizes." The quotas page suggests the Spin dashboard project (`https://github.com/radu-matei/dash`) for checking component sizes before deploying.
- The page says nothing about raising the other Function quotas. The deployment error for exceeding any of them is not stated.
- **Inference:** a variable-only redeployment creates a new version (§1.5), so it presumably counts toward the 20 deploys per hour, as does each run of a CI workflow that deploys on every push (§4.18).

**Log emission.** Akamai Functions captures what a Function writes to stdout and stderr.

- A log line can be at most 1 MiB: "Once the maximum size is reached any additional logs are silently dropped." One invocation can emit at most 10 MiB of logs in total: "Once the maximum size is reached any additional logs are dropped after a warning."
- The logs are meant for debugging. The quotas page says they "should not be used as a full, production-level observability system," and the logging page says "you should only use Akamai Functions logging for debugging at low traffic levels." Retrieval limits are in §1.9.

### 1.3 Key-value store

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md)

- The Functions key-value store is in **Limited Availability**. It "is not subject to the same expectations of scalability as the rest of the platform," and its backends "are not deployed to the same level of geographical distribution as the rest of the platform, so there can be higher latencies when using it from certain regions." The KV page also says a replica exists "in the same general geographic area of each Akamai Functions compute region" (§4.4).
- The KV page calls the default limits "intentionally low." The quotas page sets them at 1000 read requests per second per Function, 50 write requests per second per Function, a maximum value size of 1 KiB, and a maximum key size of 1 KiB. The KV page says query rates "can be increased to meet production needs per customer request"; the quotas page says an increase for "a production-level KV store" comes "at an additional cost." The sources do not state the throttling response or the error for an oversized key or value.
- **Inference:** the Supabase tutorial caches the whole article list under one key. Its sample list response is already 1,090 bytes before the cache wrapper is added, which is more than the 1 KiB value limit (§4.4, §5.6).
- Akamai Functions "currently only allows the `"default"` label," which "signals the platform to automatically provision a key value store." A code comment in the KV tutorial mentions `Kv.open("mylabel")` for a different label, but the platform does not allow other labels. The error for another label is not stated.
- A component can use the store only when the manifest grants it through the component's `key_value_stores` ("Components cannot access the store unless explicitly granted permission"). The runtime error for a component without the grant is not stated.
- Key-value stores are "currently scoped to applications and cannot be shared between applications."
- `wasi:keyvalue/store` and `wasi:keyvalue/batch` are supported. `wasi:keyvalue/atomic` "is not supported because it requires a consistency guarantee not provided by our global store." The only documented consistency guarantee is read-your-writes behavior "within a request." The consequence for a component that imports the atomic interface is not stated.
- The quotas page says the Spin WASI key-value interface "is also compatible with other KeyValue stores, such as (self-hosted) Redis or the Akamai ValKey Managed Database." The sources do not show how to connect an application's key-value API to such a store, and the platform allows only the `"default"` label.
- The Functions store "is different and separate from EdgeKV. EdgeKV is not currently compatible with Akamai Functions." The comparison page calls Functions KV "similar in concept to EdgeKV but with access from the compute layer rather than the CDN layer." The use-cases page describes Functions that "push data into the EdgeKV admin APIs," write origin-health status to "a shared data store such as EdgeKV," and reconcile revoked tokens to EdgeKV (§4.22). The sources do not reconcile these pages (§5.6). **Inference:** those use cases call EdgeKV's administrative APIs over outbound HTTP; they do not make EdgeKV available through the Functions key-value API.

### 1.4 Outbound networking and databases

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md)

- Outbound requests have to be granted per component in `allowed_outbound_hosts`. The Supabase tutorial says that under Spin's capabilities-based security model "we must explicitly grant the application access to variables and outbound requests." The database tutorials add the endpoint "so that the Wasm component is allowed to send network requests to it." The exact error for an ungranted host is not stated. The comparison page's "outbound HTTP to any hostname" means Functions is not limited to Akamized hostnames as EdgeWorkers is. It does not remove the allowlist.
- Outbound subrequests, such as JavaScript `fetch()` calls, are subject to the request limits and the rate of 10,000 subrequests per minute per deployed Function in §1.2. Connection pooling for subrequests is disabled by default, so each subrequest opens a new connection, "which can potentially impact performance." It can be enabled per Function through the Akamai representative; the feature table lists it as "Supported since Spin v3.4.0 but not enabled by default." The sources document no self-service way to enable it.
- A call from one Function to another goes through the CDN. Because Functions are deployed "in Akamai Cloud behind the `fwf.app` CDN property," a request from Function B to `https://FUNC-A.fwf.app/...` is routed through the nearest Akamai CDN edge node and back into Akamai Cloud. The documented consequence is "degraded performance": the two Functions "cannot immediately access each other's endpoints without an added round trip of latency via the CDN," even when they are likely in the same cloud cluster. Like any outbound request, the call needs its host granted and counts toward the subrequest limits.
- Local service chaining between components of the same Function (`https://COMPONENT.spin.internal/...`) avoids that round trip, because the call stays "within the same WebAssembly execution context." The quotas page calls it "a recommended best practice within Akamai Functions when using multiple components" (§4.13). **General knowledge:** Spin also requires the calling component's `allowed_outbound_hosts` to permit the `spin.internal` target; the Akamai sources show no manifest entry for it.
- A MySQL entry in `allowed_outbound_hosts` has to use the `mysql://` protocol and explicitly include the port configured on the MySQL server (the tutorial's example port is `22691`). The tutorial says this is required for outbound connectivity but does not state the error when either part is missing.
- A PostgreSQL entry has to use the `postgres://` protocol and explicitly include the port. The tutorial uses the PostgreSQL default port, `5432`. The error when either part is missing is not stated.
- A Linode Managed MySQL cluster accepts only inbound connections that it explicitly allows, by IPv4 or IPv6 address. The tutorial allows `0.0.0.0/0` (any host) "for the sake of this tutorial." The sources publish no Akamai Functions egress IP ranges. The security tutorial says that allowlisting Akamai-controlled IP ranges on an origin firewall "does not currently work well for Akamai Functions," because the platform "can use any IP address in the Cloud's considerable range"; the allowlist would have to cover all of Akamai Cloud. Sending origin traffic through an Akamai property instead, so that Site Shield or Origin IP Access Control Lists apply, "can, however, have severe latency and scalability issues when used at large scale," and the tutorial says to consult the Akamai account team first (§4.23).
- Functions uses mTLS internally, but mTLS is not currently exposed to customers for securing Function-to-origin traffic. The security tutorial's alternatives are an application-level authentication layer (for example, API access tokens distributed as encrypted Spin variables) or the `AF-Verification-Token` signing method reused between the Function and the origin (§4.23).
- PostgreSQL protocol support "is not yet compatible with Linode DBaaS"; use self-managed or third-party PostgreSQL. The sources do not describe what happens if a Linode DBaaS PostgreSQL database is used. Akamai "does not currently offer a managed Redis service," so outbound Redis needs a self-managed or third-party instance. The quotas page names the "Akamai ValKey Managed Database" as compatible with the Spin key-value interface (§1.3) but does not say whether outbound Redis can use it (§5.6). **General knowledge:** Valkey is a Redis-compatible fork of Redis.

### 1.5 Application variables and deployment versions

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md)

- A component can read only the application variables granted to it in its `[component.<name>.variables]` table, under the capabilities-based security model. The sources do not state what `Variables.get(...)` returns for a variable that has not been granted. The documented samples treat a falsy result as missing configuration (§3.2).
- A single Spin application variable can be at most 1024 bytes, and all of the application variables combined at most 4096 bytes (§1.2). The sources do not state the deployment error for larger values.
- During local runs, environment variables prefixed with `SPIN_VARIABLE_` "will be accessible by your applications, if a corresponding variable is defined as part of the application manifest."
- The object-store tutorial notes that variables marked `required = true` have to be supplied before the application runs. The source does not state the error when a required variable is missing.
- A variable value supplied with `spin aka deploy --variable` is not a live runtime change. It is "propagated as a new deployment," and the version increments. For this reason, the security tutorial rotates a shared secret by deploying the Function first, waiting until the new version is "fully deployed and actively accepting traffic," and accepting the previous secret during a grace period (§4.23).
- The update guide instructs users to specify the application's variables again when they upgrade with `spin aka deploy`. It does not state the result of omitting a previously supplied value.
- Application variables are encrypted at rest and in transit for the lifetime of the application, and a variable can be marked `secret = true`, but "the underlying cryptographic implementations have not been assessed for PCI compliance." Do not present application variables as PCI-assessed secret storage.

### 1.6 Updates, deletion, and accounts

**Sources:** [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

- Akamai Functions has no built-in support for running multiple versions simultaneously, for example canary or blue-green deployments. During an update, in-flight requests are gracefully completed by the previous version while all new traffic is routed to the updated version.
- Deleting an application is permanent and cannot be undone. `spin aka app delete` asks for confirmation unless `--no-confirm` is passed.
- Akamai Functions has its own account system, "not directly controlled by" Akamai Control Center (ACC) or Cloud Manager identity and access management. It does not support the ACC identity and access management system, any other role-based access control (RBAC) system, or per-application permissions: "all users in a team account currently have full administrative access," and every member "can create, update, permanently remove, and deploy an application." The default contract team account "includes all users of your company with an Akamai Control Center account tied to that contract." The delete guide says to use caution when sharing team-account access.
- The `spin aka` plugin cannot yet create team accounts or manage their membership; the account guide says it will "in a future update." Until then, a new team account is requested, and members are added or removed, through a form that "is currently manually processed, so allow up to 48 hours." Each user to be added has to have logged in with `spin aka login` at least once so that a personal account exists.
- Production use: by default, `spin aka deploy` deploys to the personal account (the account guide says all commands default to it; the CLI help says "the current account context," §5.6). The account guide says the personal account "should not be used for production workloads" and supports "lower limits and fewer requests per month" (§1.2). The quickstart says "For production use, you need to deploy the Function in a Team Account," for example by passing `--account-name`. The account guide and the FAQ describe team accounts as being for collaboration and production deployments. No source describes any enforcement beyond the personal account's lower limits.
- A personal access token cannot delete a deployed Function, although it can manage applications in all team accounts that its user can access (§1.9).
- An application persists until it is explicitly deleted with `spin aka app delete`. Unlinking a workspace does not delete the application.

### 1.7 Cron jobs

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

- Cron-job support is a Tech Preview. The CLI labels the command group `UNSTABLE`, and the quotas page's feature table lists cron as "Partial support." The quotas page says the cron system "is not subject to the same expectations of stability as the rest of the platform": crons "are not 100% guaranteed to run, nor are they guaranteed to run at exactly the scheduled time." **Inference:** a scheduled handler should tolerate missed and late runs.
- An account can have at most 10 configured crons "across all deployed Functions." The error for creating more is not stated.
- A cron job sends scheduled HTTP requests to a path and query of an application that is already deployed to Akamai Functions (§3.5). The source does not state the error for an application that is not deployed.
- A schedule that names a time of day has to be written in UTC. The tutorial warns that local times may need converting "to ensure correct execution."
- Within one application, each combination of schedule and path-and-query has to be unique. The error for a duplicate is not stated.
- In the command reference, `cron create` requires `--schedule <SCHEDULE>` (`-p, --path-and-query` and `--name` are optional), and `cron delete` requires the job's positional `<NAME>`. The cron tutorial shows a positional form of `create` that conflicts with this (§4.17, §6.21). The CLI's response to an incomplete command is not reproduced.

### 1.8 Language and toolchain constraints

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md)

- Rust components need the `wasm32-wasip1` target (`rustup target add wasm32-wasip1`). The GitHub Actions guide says some applications "need additional build tools installed before it will compile," and that a Rust project "will need the `wasm32-wasip1` Rust compiler target available." It adds the target in CI before `spin build`.
- Go components are built with TinyGo, because "the standard Go compiler does not yet support WASI exports." The quickstart lists these checks for a failed build: the Spin SDK needs TinyGo 0.27 or above, and `CGO_ENABLED=1` has to be set because the Go SDK is built using CGO.
- Node.js versions are tutorial guidance, not platform minimums. The quickstart recommends Node.js 22 or newer, the object-store tutorial lists Node.js 22 or later as a prerequisite, and the MySQL tutorial recommends at least Node.js 21.
- An application is deployed as compiled WebAssembly. Build it with `spin build` before deploying, or pass `spin aka deploy --build`, which runs `spin build` first for local apps and is ignored for remote apps.
- Several platform features depend on the Spin or SDK version (quotas page feature table): component dependencies are supported since Spin v4.0.0; HTTP middleware since Spin v4.1.0, "currently only out-of-the-box with Rust SDK >7.0.0"; WebAssembly garbage collection since Spin v4.2.0, enabled by default, for languages that use WasmGC such as Kotlin, Scala, or Dart. Instance reuse is supported since Spin v4.0.0 and "automatically enabled," but it "requires up-to-date Wasi-p3 compatible SDKs, such as v7.0.0 of the Rust SDK, v4.0 for the Go SDK or v5.0 of the Python SDK," and it is "not yet supported for JavaScript." The sources do not say what happens when an older Spin or SDK version is used with these features. **General knowledge:** in Spin, a WASI P3 HTTP component is subject to instance reuse, so one instance can handle several requests, one after another or concurrently; request-specific data should not be kept in global or static variables.
- The Rust samples use two handler styles: the quickstart template uses `#[http_component]` with a synchronous handler, and the security tutorial uses `#[http_service]` with an `async` handler and `variables::get(...).await`. No source maps either style to an SDK version (§3.3, §5.6). **General knowledge:** the Spin v4 HTTP trigger documentation identifies the Rust handler with `#[http_service]` on an `async` function. The security tutorial suggests implementing its token check "as HTTP Middleware in the latest Spin versions," which the feature table supports out of the box only with Rust SDK >7.0.0.

### 1.9 CLI and authentication constraints

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md)

The login session, the personal access token (PAT) lifetime, the usage window, and the log-retrieval window are separate limits. A number documented for one of them does not apply to the others. Unless an entry says otherwise, the sources do not state the CLI's response when a limit is exceeded.

- Every command in the command reference lists `Spin compatibility: >=v4.0.0`, and the quotas page says "Akamai Functions supports Spin CLI v4.0.0 or newer. Older Spin versions may work (especially for existing Functions projects), but are not guaranteed to." Each command shows that one line above help output for plugin v1.0.0, v0.7.6, and (except the `help` subcommands) v0.7.0; the page does not say whether it also applies to the older plugin versions. The quickstart's Windows instructions link to the Spin v3.6.2 binary release, which is older than the supported version (§4.14, §5.6).
- Deploying requires a login. The quickstart says "To deploy a new Akamai Function you first need to log into the platform," and the Property Manager tutorial says that `spin aka deploy` requires authentication with `spin aka login`. Interactive login needs a browser: `spin aka login` prints a link to a login page (for example `https://login.infra.fermyon.tech/realms/neutrino/device?user_code=...`), where the user authenticates with Akamai Control Center (ACC) credentials. Logging in also requires Akamai Functions to be enabled on the user's ACC contract (§1.1). The CLI's response to a command run without a login is not stated.
- PATs are for situations without a browser window, "such as in the middle of a Continuous Integration (CI) or Continuous Deployment (CD) workflow." `spin aka login --token <TOKEN>` authenticates with a PAT, and the help lists the `SPIN_AKA_ACCESS_TOKEN` environment variable for `--token` (`[env: SPIN_AKA_ACCESS_TOKEN=]`). A PAT impersonates the user who created it (§4.18). The sources do not describe what interactive login does where no browser is available.
- Login session: the quotas page lists a "Maximum logged-in session duration" of 15 days, and the FAQ says "Your login session started by `spin aka login` persists for 15 days without activity." One page states a maximum duration and the other an inactivity period. Neither says whether activity extends a session, what the CLI does after a session ends, or whether the limit applies to a login with `--token` (§5.6). **Inference:** after the session ends, run `spin aka login` again.
- PAT lifetime: `spin aka auth token create` sets it with `-e, --expiration-days`, shown as `[max: 90] [default: 30]` in the help for plugin v0.7.0 through v1.0.0. The CI guide gives the same 30-day default and lets the expiration be extended "up to 90 days from the time it is issued," and the quotas page lists 90 days as the "Maximum lifetime for Personal Access Tokens." The CLI's response to a larger value is not stated. Once a token expires, "you need to create a new token to continue using it in a CI/CD pipeline." The guide says to create the replacement before the old token expires.
- The quotas page adds that "`spin aka auth regenerate` currently does not reset" the 90-day maximum lifetime. The command reference has no `spin aka auth regenerate`; its command is `spin aka auth token regenerate --id <ID>` ("Regenerate a personal access token") (§5.6). The sources do not say what else regeneration changes or whether it works on an expired token. **Inference:** a regenerated token keeps the original token's expiry; a new lifetime needs a new token from `spin aka auth token create`, as in the CI guide's rotation steps.
- A new PAT is displayed once: "This is your only chance to see it, so make sure to save it somewhere secure."
- The quotas page allows at most 100 PATs. It does not say whether the count is per user or per account.
- PATs "have largely the same rights and capabilities as the user who created them, but cannot" delete a deployed Function or "Manage (create/update/delete/…) Personal Access Tokens." The account guide adds that PATs "can also manage applications in all team accounts that this user has access to (though they cannot delete them)." The error for a forbidden operation is not stated. **Inference:** a CI/CD job that logs in with a PAT cannot delete applications or create replacement tokens; do those from an interactive login (§1.6).
- The plugin "internally calls the Akamai Functions' administrative API, which is rate limited" to 50 API calls per minute per user, and `spin aka logs` is limited to 5 calls per minute. The sources do not say how many API calls a command makes or what happens when either rate is exceeded.
- Usage window: `spin aka app status --usage-since` accepts at least 5 minutes (`5m`) and at most 7 days (`7d`); the help says "A maximum of 7 days and minimum of 5 minutes is enforced." The CLI's response to an out-of-range value is not stated. For more than seven days of usage, full usage information "can be made available in Akamai Control Center Billing" on request through the Akamai representative.
- Historical data: the plugin quota table lists 7 as the "Maximum days for historical data retrieval." It does not define historical data or name the commands that the limit covers.
- Log retrieval: the logging quota table sets a "Maximum time period for log retrieval" of 60 days. `spin aka logs --since` has no documented range and defaults to 7 days. The quotas page does not reconcile the 60-day log-retrieval period with the 7-day historical-data limit (§4.10, §5.6).
- Commands run on the personal account by default (§1.6). To deploy, upgrade, or delete an application in a team account, the account guide says to pass `--account-id` or `--account-name` with each command, or to set `SPIN_AKA_ACCOUNT_ID` or `SPIN_AKA_ACCOUNT_NAME`. The environment variables need plugin v0.7.8 or higher. The v1.0.0 help lists them for the two options (`[env: SPIN_AKA_ACCOUNT_ID=]`, `[env: SPIN_AKA_ACCOUNT_NAME=]`), and the v0.7.6 help does not. What an older plugin does with the variables is not stated.
- `spin aka deploy --create-name <NEW_APP_NAME>` "is only valid when you are deploying to an app that does not exist yet" (plugin v0.7.0 through v1.0.0). The CLI's response otherwise is not stated.

### 1.10 Property Manager integration

**Sources:** [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

The Property Manager tutorial and the security tutorial put an Akamai property in front of a Function. Their settings are tutorial guidance for this integration, not platform-wide restrictions, unless an entry says otherwise. The full steps are in §4.19 and §4.23.

- Selecting **Functions** as the **Origin Type** of the Origin Server behavior is recommended, not required: "It is not required that you select Functions, but it is highly recommended." The tutorial gives no reason for the recommendation and documents no settings for another origin type. The security tutorial also calls fronting the Function's URL with your own property, "by using the Functions origin type," a best practice. With Functions selected, the Function is entered in the **Functions Origin** textbox. The tutorial copies the application URL from the `spin aka deploy` output because "we'll need it in a second to configure the Akamai Property," but it does not say whether the textbox takes the full URL or only the hostname.
- Selecting Functions automatically adds the Global Request Number (GRN) behavior to the property, which "generates a unique identifier for each request on the Akamai edge network." If you pass the GRN "with custom metadata," the tutorial says to use `AKA_GRN_HEADER` as the header name "to prevent duplication when selecting Functions as the Origin Type." The source does not describe the duplication further. The sources also do not say whether the identifier reaches the Function in the `akamai-GRN` request header, which the quotas page exempts from header stripping (§4.1).
- A property in front of a Function does not stop direct calls to the Function's public `{UUID}.fwf.app` URL. The security tutorial says that Akamai's default platform defenses "will not prevent it from being called by this URL directly," and that an attacker who obtains the URL "can still call it directly, potentially causing increased usage and costs or information leakage." Its countermeasure is a signed `AF-Verification-Token` request header that the Function validates (§4.23).
- The customer cannot add Advanced Metadata, which the security tutorial uses to generate that token: "You cannot add Advanced Metadata in your property yourself. You need to reach out to your account representative to do it for you." The tutorial first defines three PMUSER variables with the security level "sensitive" and then has the Akamai representative add the metadata. It also makes sure that the Advanced Metadata and Modify Outgoing Request Header behaviors are "in the same scope as (and applied to)" the Origin Server behavior that has the Function as its origin. The source states no consequence for a different scope.
- The secret ID in `PMUSER_FVT_SECRET_ID` "cannot contain dashes" (the metadata comment says it "must not contain dashes"), and `PMUSER_FVT_SECRET` holds a 64-character (32-byte) hexadecimal string. The token format, `[timestamp]-[secret-id]-[random-number]-[hash]`, separates its fields with dashes. The source states no consequence for a dash in the ID. **Inference:** a dash would break the field split in the tutorial's validation samples.
- Request headers that the property adds to the forward request are subject to the platform's header stripping. `akamai-*` headers (except `akamai-Bot` and `akamai-GRN`), `x-akamai-*` headers, and the other names listed in §1.1 are removed "before a request is handled by your code." The security tutorial's custom `AF-Verification-Token` header is not in that list.
- The tutorial adds a **Modify Outgoing Request Path** behavior (replace `/hello/` with `/`, first occurrence only, keep the query parameters) so that the property does not send the routing criteria `/hello/` as a path to the application, whose only route is `/`. The source does not describe the result without it. **Inference:** the request would reach the application as `/hello/`, which the sample's router does not match (§6.24).
- Property changes take effect only after the new property version is activated: "At this point, the new rule isn't active, yet!" The tutorial highly recommends activating and testing in the Staging environment before production. This is a recommendation, not a platform requirement.
- The tutorial's tip says that `spin aka login` authenticates "using your Akamai Control Center or GitHub account credentials." The quickstart says only "Authenticate using your Akamai Control Center credentials," and no other current source mentions a GitHub login (§1.1, §5.6).

---

## 2. Import Rules

The sources' samples use the following imports. They do not state a general rule that imports must be static, and they do not state that dynamic `import()` is unsupported. Install the matching package before importing it (§2.11). Web APIs that the JavaScript/TypeScript samples use without an import are listed in §2.8.

### 2.1 Router and HTTP helpers

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

Router only (`http-js` and `http-ts` templates, and the KV, cron, MySQL, PostgreSQL, and Property Manager samples):

```javascript
import { AutoRouter } from 'itty-router';
```

The MySQL and PostgreSQL samples write the specifier in double quotes (`"itty-router"`). The Property Manager sample's first line reads `Fimport { AutoRouter } from 'itty-router';`, a typo that the form above corrects (§5.6).

Router plus the `json` response helper (object-store and Supabase `src/index.ts`):

```typescript
import { AutoRouter, json } from 'itty-router';
```

Request type for middleware (Supabase `src/middlewares.ts`):

```typescript
import { IRequest } from "itty-router";
```

`itty-router` comes with the `http-js` and `http-ts` templates: the KV tutorial uses "the HTTP router, provided by the template," and the PostgreSQL tutorial notes that `itty-router` "is specified as dependency of the app." No tutorial installs it separately (§2.11). The security tutorial's TypeScript sample does not use a router (§3.1).

### 2.2 Application variables

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md)

JavaScript/TypeScript (MySQL, PostgreSQL, Supabase, and object-store samples):

```typescript
import * as Variables from "@spinframework/spin-variables";
```

The security tutorial's TypeScript sample imports the same package under a lowercase namespace name:

```typescript
import * as variables from '@spinframework/spin-variables';
```

Read a variable with `Variables.get("<name>")`, for example `Variables.get("pg_connection_string")`, or `variables.get('fvt_secret')` in the security sample (§4.3). Every JS/TS sample calls `get` without `await` and treats an empty result as missing configuration (§3.2).

Rust (security tutorial): import the module with `use spin_sdk::{http_service, variables};` and read a value with `variables::get("fvt_secret").await?` (§2.9, §3.3). The sources show no Go variables API (§4.11).

Code can read a variable only after it is declared in `[variables]` and granted to the component (§1.5, §4.3).

The webhook revision of the Supabase middleware imports `Variables` from `@spinframework/spin-kv` instead. That is a defect in the sample; every other variables sample, including the same tutorial's first middleware, imports from `@spinframework/spin-variables` (§5.6, §6.25).

### 2.3 Key-value store

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

Named import (KV tutorial):

```javascript
import { openDefault } from '@spinframework/spin-kv';
```

Namespace import (Supabase `src/cache.ts`):

```typescript
import * as Kv from "@spinframework/spin-kv";
```

Call `openDefault()` with the named import or `Kv.openDefault()` with the namespace import. Akamai Functions currently only allows the `"default"` store label (§1.3, §6.9). The sources show no Rust or Go KV API (§4.11).

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

`src/inform.ts` imports `{ ALL_ARTICLES_CACHE_KEY, buildKey, invalidate }` from `"./cache"`. The tutorial then imports the webhook processor with `import  processDatabaseUpdate  from './inform';`, which is a default import, but `src/inform.ts` declares a named export (`export function processDatabaseUpdate`). Corrected form: `import { processDatabaseUpdate } from './inform';` (§5.6).

### 2.8 S3-compatible object storage and Web API globals

**Sources:** [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

```typescript
import { S3Client, GetObjectCommand, ListObjectsV2Command } from '@aws-sdk/client-s3';
```

The JavaScript/TypeScript samples use these Web APIs without importing them:

| API | Used in |
|---|---|
| `addEventListener('fetch', ...)`; `FetchEvent` as a TypeScript type after `//@ts-ignore` | `addEventListener` in every JS/TS entry point, `FetchEvent` in the TypeScript ones (§3.1) |
| `Response`; `Request` and `Headers` as parameter types | `Response` in every sample; `Request` in the security sample, `Headers` in the Supabase webhook handler |
| `URL` | Cron sample |
| `TextDecoder`, `TextEncoder` | `TextDecoder` in the KV, MySQL, PostgreSQL, Supabase, and object-store samples; `TextEncoder` in the object-store and security samples |
| `TransformStream`, `ReadableStream` | Object-store sample |
| `crypto.subtle.importKey(...)`, `crypto.subtle.verify(...)`, `atob(...)` | Security tutorial's TypeScript sample (§4.23) |
| `console.log(...)` | Cron, Supabase, and object-store samples |
| `fetch(...)` | Quotas page examples of outbound calls (§3.1) |

**Inference:** the JavaScript runtime provides these as globals. The sources do not list which Web APIs are available.

### 2.9 Rust

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md)

Quickstart (`http-rust` template, `src/lib.rs`):

```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;
```

Security tutorial (request-signing sample; the full sample is in §4.23):

```rust
use base64::{engine::general_purpose::STANDARD, Engine};
use hmac::{Hmac, Mac};
use sha2::Sha256;
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::{http_service, variables};
```

Both handlers refer to `anyhow::Result` by its full path. The security sample also uses the third-party `base64`, `hmac`, and `sha2` crates. Neither page shows `Cargo.toml` or a command that adds a crate (§2.11).

The two import sets belong to two handler styles, `#[http_component]` and `#[http_service]` (§3.3). The sources do not say which Spin Rust SDK version either one requires. **General knowledge** (spin-sdk crate documentation on docs.rs, not Akamai documentation): spin-sdk releases through 5.2.0 export `http_component`; from 6.0.0, the crate root exports `http_service` instead and no longer exports `http_component`. Keep each import set with its own handler style.

### 2.10 Go

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

```go
import (
	"fmt"
	"net/http"

	spinhttp "github.com/spinframework/spin/sdk/go/v2/http"
)
```

The quickstart's TinyGo build output shows the SDK module `github.com/spinframework/spin/sdk/go v0.10.0` being downloaded (see §5.6 for the `/v2` import-path mismatch).

The quotas page names "v4.0 for the Go SDK" as an example of the "up-to-date Wasi-p3 compatible SDKs" that instance reuse requires (§4.12). No source shows a Go SDK v4 import. **General knowledge** (Go module proxy, not Akamai documentation): Go SDK v3 and v4 are published under the module paths `github.com/spinframework/spin-go-sdk/v3` and `github.com/spinframework/spin-go-sdk/v4`, not under the quickstart's `github.com/spinframework/spin/sdk/go/v2` path.

### 2.11 Package installation by integration

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md)

| Integration | Template used by the tutorial | Exact install command(s) after `spin new` |
|---|---|---|
| Starter app (quickstart) | `http-js` or `http-ts` | `npm install` |
| Cron | `http-js` | `npm install` |
| Property Manager | `http-js` | None shown. The tutorial goes from `spin new` to `spin build`. |
| Key-value store | `http-js` | `npm install @spinframework/spin-kv` (installs the template defaults plus the KV SDK) |
| MySQL | `http-ts` (the prose says `http-js`; §5.6) | `npm install @spinframework/spin-mysql @spinframework/spin-variables`, then `npm install uuid --save` |
| PostgreSQL | `http-js` | `npm install`, then `npm install  @spinframework/spin-postgres @spinframework/spin-variables uuid` (the note after it names `@spinframework/spin-mysql` instead; §5.6) |
| Supabase cache proxy | `http-ts` | `npm install @spinframework/spin-variables @spinframework/spin-kv @supabase/supabase-js --save` |
| Linode Object Storage | `http-ts` | `npm install @spinframework/spin-variables @aws-sdk/client-s3` |
| Request signing, TypeScript (security tutorial) | Not named | None shown. The sample imports `@spinframework/spin-variables` (§2.2). |
| Rust starter (quickstart) | `http-rust` | No npm packages. The quickstart adds the Rust target beforehand with `rustup target add wasm32-wasip1` (§1.8). |
| Request signing, Rust (security tutorial) | Not named | None shown. The sample uses `spin_sdk` and the `base64`, `hmac`, and `sha2` crates (§2.9), and the page shows no `Cargo.toml`. |
| Go starter (quickstart) | `http-go` | No npm packages. The quickstart installs the TinyGo compiler beforehand (§1.8). |

- The quickstart installs dependencies "using your package manager of choice (we'll use `npm` here)." The KV and MySQL notes say that their `npm install <packages>` command also installs the template's default packages.
- Node.js version recommendations differ between pages (§1.8).
- **Inference:** run `npm install` after `spin new` even where a tutorial omits it (Property Manager), so the template's dependencies, including `itty-router`, are present. Before using the security tutorial's TypeScript sample, install `@spinframework/spin-variables` as the other variables tutorials do.
- **General knowledge:** add the Rust crates with Cargo, for example `cargo add base64 hmac sha2`. The sources pin no crate versions, so choose versions that provide the APIs the sample calls.

---

## 3. Event Handler Reference

Akamai Functions currently supports Spin's `http` trigger type. Redis and custom triggers are not supported, and cron is a Tech Preview service that calls an HTTP path of the deployed application rather than a separate language-level handler (§1.1, §3.5, §4.13). The documented entry points are the JavaScript/TypeScript `fetch` listener (§3.1), the Rust `#[http_component]` and `#[http_service]` handlers (§3.3), and the Go `spinhttp.Handle` callback (§3.4).

### 3.1 JavaScript/TypeScript `fetch` event

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

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

**Request-signing handler (security tutorial).** The TypeScript validation sample does not use a router. It imports `* as variables from '@spinframework/spin-variables'` and declares `async function handleRequest(request: Request): Promise<Response>`, which reads `request.headers.get('AF-Verification-Token')`, verifies the token with `crypto.subtle`, and returns `new Response('Forbidden', { status: 403 })` or `new Response('Hello, verified caller!')`. The full sample is in §4.23. Two defects (§5.6):

- The published code ends without the function's closing `}`.
- Nothing registers `handleRequest`: the sample has no `addEventListener('fetch', ...)` call.

**Inference:** as published, the sample neither compiles nor serves requests. Illustration (not from a source) of closing the function and registering it the way the other TypeScript samples register their handlers:

```typescript
//@ts-ignore
addEventListener('fetch', async (event: FetchEvent) => {
    event.respondWith(handleRequest(event.request));
});
```

The tutorial adds that it "would also make sense to implement this as HTTP Middleware in the latest Spin versions." The quotas page lists HTTP middleware as supported since Spin v4.1.0, with the note "Currently only out-of-the-box with Rust SDK >7.0.0" (§4.13).

Objects and operations used by the documented handlers:

| Object/member | Documented use | Constraint or note |
|---|---|---|
| `addEventListener('fetch', handler)` | Registers the entry point | Present in every documented JS/TS entry point. The security tutorial's sample lacks it (above). |
| `event.request` | Incoming request passed to `router.fetch(...)` | — |
| `event.respondWith(responseOrPromise)` | Returns the response | The documented flow passes the router result here. For the defective double call in the database samples, see §3.2. |
| `router.fetch(event.request)` / `router.fetch(event.request, context)` | Dispatches to the first matching route | Properties of `context` arrive as the route handler's second argument (§3.2) |
| Route handler return value | A `Response`, `json(...)`, or a string (the template's `/hello/:name` route returns a template string) | A route that does not return acts as middleware; an unmatched route returns `404` |
| `request.params.<name>` or destructured `({ name })` / `({ params })` | Reads route parameters | Forms are listed in §4.2 |
| `request.arrayBuffer()` + `TextDecoder` | Reads the request body | The samples decode with `TextDecoder` before `JSON.parse`. Request and response bodies are limited to 10 MiB. The limit does not apply when the body is streamed, although related limits such as memory still do (§1.2). |
| `request.headers.get(name)` | Reads request headers: `x-webhook-token` (Supabase webhook) and `AF-Verification-Token` (security tutorial) | The Spin-injected headers and `true-client-ip` (§4.1) are request headers too. **Inference:** read them the same way; no JS sample does. Akamai Functions strips `x-request-id`, `x-forwarded-for`, `x-real-ip`, `x-forwarded-client-cert`, `akamai-*` (except `akamai-Bot` and `akamai-GRN`), `x-envoy-*`, `fermyon-*`, and `x-akamai-*` before the request is handled by the code. **Inference:** read the client address from `true-client-ip`, because `x-forwarded-for` and `x-real-ip` are stripped. |
| `new URL(request.url)` | Parses the URL and query | Used in the cron sample |
| `Variables.get(name)` | Reads a granted application variable | Called without `await`. The variable must be granted to the component (§1.5, §2.2). |
| `openDefault()` / `Kv.openDefault()` | Opens the `default` KV store | Requires `key_value_stores = ["default"]` |
| `Mysql.open(...)` / `Postgres.open(...)` | Opens a database connection | Requires a `mysql://` or `postgres://` entry with an explicit port in `allowed_outbound_hosts` |
| `createClient(url, key)` / `new S3Client(...)` | Third-party clients | The endpoint must be in `allowed_outbound_hosts` |
| `crypto.subtle.importKey(...)` / `crypto.subtle.verify(...)` | Verifies the HMAC-SHA256 verification token (security tutorial) | Used without an import (§2.8). Full sample in §4.23. |
| Outbound `fetch(url, init)` | Calls another Function or an HTTP API | The host must be in `allowed_outbound_hosts` (§1.4). Outbound subrequests have the same size limits as requests and are limited to 10,000 per minute per deployed Function. A call to another Function's `*.fwf.app` URL is routed through the CDN, which adds a round trip of latency. Components of the same Function can call each other through local service chaining at `*.spin.internal`, which stays in the same WebAssembly execution context and is a recommended best practice (§4.13). |
| `console.log(...)` | Writes logs | stdout and stderr are captured and retrieved with `spin aka logs`. The logs are meant for debugging at low traffic levels (§4.10). |

Practices shown by the JS/TS samples:

- Register the handler with `addEventListener('fetch', ...)` and return the result through `event.respondWith(...)`. The sources document no other JS/TS entry point.
- The samples read request bodies with `await request.arrayBuffer()` and decode them with `TextDecoder` before `JSON.parse(...)`. The sources show no other body reader.
- List every host that a database client, S3 client, Supabase client, or outbound `fetch` contacts in `allowed_outbound_hosts` (§1.4).

### 3.2 Per-request context and configuration checks

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md)

The router-based samples read configuration in one of three ways and pass it to route handlers. The security tutorial reads its variables inside the handler (Pattern D).

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

**Pattern D — read variables inside the handler (security tutorial):** both validation samples call the variables API in the request handler itself. The TypeScript sample returns `new Response('Forbidden', { status: 403 })` when `fvt_secret` is empty or the token's secret ID differs from `fvt_secret_id`. The Rust sample reads both values with `variables::get(...).await?`, which returns any lookup error from the handler, and answers status `403` with the body `Forbidden` when validation fails. The sources do not document the HTTP response for a handler that returns an error (§3.1, §3.3, §4.23).

### 3.3 Rust HTTP handlers

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

The sources show two Rust handler styles, and both are documented. They do not say which Spin Rust SDK version either style requires or whether one replaces the other (§5.6).

**`#[http_component]` (quickstart).** The `http-rust` template generates `src/lib.rs`:

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

- The template marks a synchronous `fn` with `#[http_component]`. The handler receives `spin_sdk::http::Request` and returns `anyhow::Result<impl IntoResponse>`.
- `req.header(name)` reads a header, such as the injected `spin-full-url` (§4.1). `println!` writes to stdout, which Akamai Functions captures for `spin aka logs` (§4.10).
- The response is built with `Response::builder().status(..).header(..).body(..).build()`.
- `spin build` runs `cargo build --target wasm32-wasip1 --release`.

**`#[http_service]` (security tutorial).** Handler shape of the request-signing sample. This is an excerpt: `// …` marks omitted lines, and the full sample is in §4.23.

```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::{http_service, variables};

#[http_service]
async fn handle_request(req: Request) -> anyhow::Result<impl IntoResponse> {
    let token = req
        .headers()
        .get("AF-Verification-Token")
        .and_then(|v| v.to_str().ok())
        .unwrap_or_default();
    // …
    let secret = variables::get("fvt_secret").await?;
    // …
    Ok(Response::builder().status(status).body(body.to_string())?)
}
```

- `#[http_service]` marks an `async fn` with the same parameter and return types as the quickstart handler.
- Headers are read with `req.headers().get(name)` and converted with `to_str()`. Variables are read with `variables::get(name).await?`.
- The sample applies `?` to `Response::builder().status(..).body(..)` and does not call `.build()`.
- The page shows no template, `Cargo.toml`, or build command for this sample (§2.11).

**Inference:** the two samples call different request and response APIs (`req.header` versus `req.headers().get`, and `.build()` versus `?`). Keep each sample's imports, attribute, and calls together instead of mixing them.

**General knowledge** (spin-sdk crate documentation on docs.rs, not Akamai documentation): spin-sdk releases through 5.2.0 provide `#[http_component]`, and the 5.2.0 README builds with `--target wasm32-wasip1`. From spin-sdk 6.0.0 on, the crate provides `#[http_service]` for `async fn` handlers instead, `variables::get` is `async`, and the README builds with `--target wasm32-wasip2`.

The quickstart notes that the build command Spin runs for a component is in the manifest's `component.(id).build` section. The quotas page names "v7.0.0 of the Rust SDK" as an example of the "up-to-date Wasi-p3 compatible SDKs" that instance reuse requires, and lists HTTP middleware as "Currently only out-of-the-box with Rust SDK >7.0.0" (§4.12, §4.13).

### 3.4 Go HTTP handler

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md)

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

- Register the handler with `spinhttp.Handle(...)` inside `init()`, and keep an empty `main()`, as the template does.
- The callback uses the standard `http.ResponseWriter` and `*http.Request` types.
- `spin build` runs `tinygo build -target=wasi -gc=leaking -no-debug -o main.wasm main.go`, the command in the component's `build` section of `spin.toml`. If the build fails, the quickstart says to check that TinyGo is installed and up to date (the Spin SDK needs TinyGo 0.27 or above) and that `CGO_ENABLED=1` is set, because the Go SDK is built using CGO (§1.8).
- The logs page's sample output comes from a Go application that logs with the `log/slog` package. Everything written to stdout and stderr is captured for `spin aka logs` (§4.10).

### 3.5 Cron invocation of an HTTP route

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

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

The sample parses `url` but never uses it, and its `console.log` template string ends with a stray `"` (§5.6).

- `spin aka cron` invokes the configured path and optional query of the deployed application, and the code receives an ordinary HTTP request through the `fetch` listener.
- The sources do not state which HTTP method the cron service uses. The tutorial registers its handler with `router.get` and schedules the path `/`.
- Write any time of day in a schedule in UTC. Each combination of schedule and path and query has to be unique within the application (§1.7, §4.17). Verify invocations with `spin aka logs`.
- Cron is a Tech Preview. The quotas page says crons are not 100% guaranteed to run, nor guaranteed to run at exactly the scheduled time, and allows at most 10 configured crons per account across all deployed Functions (§1.7). **Inference:** design the route so that a skipped or late run is harmless.

---

## 4. API Reference

### 4.1 HTTP trigger manifest and injected headers

**Sources:** [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

Akamai Functions "currently supports the `http` trigger type for Spin applications." Scheduled cron jobs also reach the application as HTTP requests to a route (§3.5).

```toml
[[trigger.http]]
route = "/..."                # the route that the trigger matches
component = "my-application"  # the name of the component to handle this route
```

`spin up` and `spin aka deploy` print this route as `(wildcard)` under "Available Routes" or "App Routes."

**Headers added to the request.** In addition to any headers passed by the client, several Spin-related headers are included in the request passed to the component:

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

**Headers removed from the request.** Akamai Functions strips these request headers and header prefixes "before a request is handled by your code":

- `x-request-id`
- `x-forwarded-for`
- `x-real-ip`
- `x-forwarded-client-cert`
- `akamai-*`, except `akamai-Bot` and `akamai-GRN`
- `x-envoy-*`
- `fermyon-*`
- `x-akamai-*`

Because `x-forwarded-for` and `x-real-ip` are removed, `true-client-ip` is the documented source of the client IP address. The sources do not say when the exempted `akamai-Bot` and `akamai-GRN` headers are present or what they contain. Selecting the **Functions** origin type in a Property Manager Origin Server behavior automatically adds the Global Request Number behavior to the property (§4.19).

Custom headers outside this list are not documented as removed. For example, the security tutorial's handler reads the `AF-Verification-Token` header that the Akamai property adds to each request to the Function (§4.23).

**Request and response limits.** These limits "apply to each request handled by a Function, as well as outbound subrequests made from within a Function, for example, using the JavaScript `fetch()` API":

| Limit | Value |
|---|---|
| Maximum request URI size | 16 KiB |
| Maximum request body size | 10 MiB |
| Maximum request headers count | 64 |
| Maximum request headers size | 32 KiB |
| Maximum response body size | 10 MiB |
| Maximum response headers count | 64 |
| Maximum response headers size | 32 KiB |

- Outbound subrequests are further limited to 10,000 requests per minute per deployed Function.
- These limits "can be increased to custom values if needed" through an Akamai representative.
- The body-size limits "do not apply when streaming the body through an Akamai Function. In that case, there is no directly enforced limit besides related limits such as total memory usage." The object-store tutorial returns an object's body stream as the response (§4.8). **Inference:** a body that is read completely into memory, for example with `request.arrayBuffer()`, is not streamed, so the 10 MiB limits apply to it.
- The sources do not state the status code, error, or truncation behavior when a request, response, or subrequest exceeds a limit.
- Connection pooling for subrequests is disabled by default. "This creates a new connection for each subrequest, which can potentially impact performance." Pooling can be enabled per Function through an Akamai representative (§4.13).
- The platform "does not directly enforce specific limits on request rates per second (RPS) or minute (RPM)." Achievable rates depend on the programming language, the computational complexity of the use case, and the use of outbound connections. CPU-time, memory, and wall-time limits depend on the resource tier (§1.2).

### 4.2 JavaScript/TypeScript HTTP and routing APIs

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md)

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
crypto.subtle.importKey('raw', keyBytes, { name: 'HMAC', hash: 'SHA-256' }, false, ['verify'])
crypto.subtle.verify('HMAC', key, signature, data)
atob(base64Text)
```

The `crypto.subtle` calls and `atob` appear only in the security tutorial's TypeScript token-validation sample, which is incomplete as published (§4.23).

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
| `403` | Missing or invalid `AF-Verification-Token` (security tutorial, §4.23) |
| `404` | Missing key or record, or an unmatched route |
| `500` | Missing configuration (`Connection String not specified`, `Application not configured correctly`) or a backend error |

Request and response sizes are subject to the limits in §4.1.

### 4.3 Application variables — `@spinframework/spin-variables`

**Sources:** [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md)

```text
Variables.get(name)
```

- `Variables.get(name)` returns the value of an application variable granted to the component. Most samples import the module as `Variables`. The security tutorial imports it as `variables` and calls `variables.get('fvt_secret')`. The samples treat a falsy result as missing configuration.
- Variable values "can be updated without modifying the application," which supports rotating secrets, updating API endpoints, and more.
- Application variables "are encrypted by default on the Akamai Functions platform," so they can hold secrets. Once deployed, they are encrypted at rest and in transit "for the entirety of the lifetime of the application." The cryptographic implementations "have not been assessed for PCI compliance" (§1.5).
- Encryption does not depend on a manifest attribute. The security tutorial says variables "are encrypted by default on the platform and can be explicitly marked as holding secrets," and marks its secret with `secret = true`. It also suggests distributing API access tokens for calls to an origin "as encrypted Spin variables" (§4.23).
- The quotas page limits a single application variable to 1024 bytes and all application variables combined to 4096 bytes. It does not say how the size is measured, for example whether variable names count, or what happens when a limit is exceeded.

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

A secret variable from the security tutorial:

```toml
[variables]
fvt_secret = { required = true, secret = true }
fvt_secret_id = { required = true }

[component.my-secure-component.variables]
fvt_secret = "{{ fvt_secret }}"
fvt_secret_id = "{{ fvt_secret_id }}"
```

A component variable can be composed from several application variables (MySQL tutorial):

```toml
[component.linode-mysql.variables]
mysql_connection_string = "mysql://{{ mysql_user}}:{{ mysql_password }}@{{ mysql_host }}:{{ mysql_port }}/{{ mysql_database }}"
```

Variable attributes in the sources are `default = "..."`, `required = true`, and `secret = true`. The samples combine `secret = true` with `required = true` (MySQL password, object-store secret key, Supabase webhook token, security tutorial) and with `default = ""` (the security tutorial's secret-rotation variables, §4.23). The Supabase tutorial instead marks `supabase_key` with `sensitive = true` (§5.6). The object-store and Supabase snippets show component variable values as empty strings (`""`, or `"https://"` for `endpoint`), even though the Supabase prose says the grants use "the interpolation syntax." Use the interpolation form shown above (§5.6).

Supplying values:

| Context | Documented mechanism |
|---|---|
| Local `spin up` | Environment variables named `SPIN_VARIABLE_<NAME>` in uppercase, for example `SPIN_VARIABLE_MYSQL_HOST` or `SPIN_VARIABLE_PG_CONNECTION_STRING`. They "will be accessible by your applications, if a corresponding variable is defined as part of the application manifest." The security tutorial also says values can be passed "using the `--variable` CLI parameter to `spin up` or `spin aka deploy`." |
| Deployment | `spin aka deploy --variable key=value`. In the plugin v0.7.0 through v1.0.0 help, the option is repeatable, also accepts `@file.json` or `@file.toml`, and uses the last value when the same key is given more than once. |
| Upgrade | The update guide says to specify the application's variables when upgrading, with `spin aka deploy --variable <key>=<value>` (§1.5, §4.18). |
| CI | `spin aka deploy --variable compression_level=${{ secrets.COMPRESSION_LEVEL }}` in a GitHub Actions step |

```shell
spin aka deploy --variable compression_level=3
```

The variables page also says that `spin aka deploy` "can point to a `spin.toml` file by using the `--file` option." The command reference documents `-f, --from <PATH>` and no `--file` option (§6.23).

Deploy-time output shows that a variable change is a new deployment:

```text
Deploying updated version of app my-app in account your-account (version 1 → 2)
OK to continue? yes
Waiting for app to be ready... ready

App Routes:
- my-app: https://ec8a19d8-6d10-4056-bb69-cc864306b489.fwf.app (wildcard)
```

### 4.4 Key-value store — `@spinframework/spin-kv`

**Sources:** [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

The Akamai Functions key-value store is in **Limited Availability**. Its default limits "are intentionally low," it "is not subject to the same expectations of scalability as the rest of the platform," and its backends "are not deployed to the same level of geographical distribution as the rest of the platform, so there can be higher latencies when using it from certain regions."

```text
openDefault()
Kv.openDefault()
store.exists(key)
store.getJson(key)
store.setJson(key, value)
store.delete(key)
```

- `openDefault()` and `Kv.openDefault()` open the store labeled `"default"`. "Akamai Functions currently only allows the `"default"` label," which "signals the platform to automatically provision a key value store for your Spin application." `Kv.open("mylabel")` appears only in a tutorial code comment and cannot be used with another label on Akamai Functions (§1.3).
- `exists(key)` checks whether a key exists, `getJson(key)` loads JSON data stored at a key, `setJson(key, value)` stores JSON data at a key, and `delete(key)` removes a key.
- The platform provisions and manages the store ("no-ops"). Data persists across application restarts and updates. The KV page describes the store as low-latency, persisted, and globally replicated, with "a replica of the key value store ... in the same general geographic area of each Akamai Functions compute region." The Limited Availability statements above say that the backends are less widely distributed than the rest of the platform; the sources do not reconcile the two descriptions (§5.6). All standard key-value operations have read-your-writes behavior within a request.
- "Spin key value stores are isolated to a single application." They "are currently scoped to applications and cannot be shared between applications." A component can use the store only after the manifest grants it access.
- At the WASI level, `wasi:keyvalue/store` and `wasi:keyvalue/batch` are supported. `wasi:keyvalue/atomic` is not, "because it requires a consistency guarantee not provided by our global store." The sources do not say how the Spin KV SDK maps onto these interfaces.
- The Functions KV store "is different and separate from EdgeKV. EdgeKV is not currently compatible with Akamai Functions" (§4.13).
- The sources document no native key expiration. The Supabase tutorial implements a time to live (TTL) by storing an `expiresAt` timestamp next to the data.
- The KV tutorial points to the Spin key value store API guide (`https://spinframework.dev/kv-store-api-guide`) for the SDK and for granting store permissions to components.

Functions KV quota limits:

| Limit | Value |
|---|---|
| Read requests per second per Function | 1000 |
| Write requests per second per Function | 50 |
| Maximum value size | 1 KiB |
| Maximum key size | 1 KiB |

- The sources do not state the error or throttling behavior when a rate, value-size, or key-size limit is exceeded.
- The KV page says query rates "are limited to enable experimenting with this feature" and "can be increased to meet production needs per customer request." The quotas page adds that a customer who needs "a production-level KV store" can request a limit increase "at an additional cost" through an Akamai representative.
- The quotas page lists outbound connections, "including Functions KV store reads/writes," among the factors that "can have a strong negative impact on maximum RPS."
- "The Spin WASI Key Value interface is also compatible with other KeyValue stores, such as (self-hosted) Redis or the Akamai ValKey Managed Database." The sources do not describe how a deployed Function would use such a store through this interface, given that only the `"default"` label is allowed (§4.13, §5.6).

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

The tutorial stores the full article list as one value. Its sample `GET /articles` response is 1090 bytes (`Content-Length: 1090`) before the `expiresAt` wrapper is added, which is larger than the current 1 KiB maximum value size. The sources do not state what `setJson` does with an oversized value (§5.6). **Inference:** keep each stored value under 1 KiB, for example by caching individual records or smaller pages instead of an unbounded list.

### 4.5 MySQL — `@spinframework/spin-mysql`

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md)

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

Database setup and access (tutorial): the database is a Linode Managed Databases MySQL cluster, and the comparison page describes MySQL support as compatible with Akamai's Linode DBaaS MySQL offering. The schema is created with `USE defaultdb;` and `CREATE TABLE IF NOT EXISTS Products (Id varchar(36) PRIMARY KEY, Name TEXT NOT NULL, Price DOUBLE PRECISION);`. The cluster accepts only inbound connections that it explicitly allows by IPv4 or IPv6 address. "For the sake of this tutorial," the tutorial allows `0.0.0.0/0`, which admits any host (§1.4).

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

**Sources:** [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md)

```text
Postgres.open(connectionString)
connection.execute(sql, params)   -> treated by the samples as the affected-row count
connection.query(sql, params)     -> result with .rows
```

- `Postgres.open` opens a PostgreSQL connection using the connection string from `pg_connection_string`. The tutorial uses a NEON-hosted database and copies the connection string from NEON's project dashboard. The comparison page says PostgreSQL protocol support "is not yet compatible with Linode DBaaS" and that teams can connect to self-managed or third-party hosted PostgreSQL instead (§1.4).
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

**Sources:** [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

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

`storeInCache` and `invalidate` also drop the `all-articles` list (§4.4). The tutorial's sample article list is larger than the current 1 KiB maximum KV value size (§4.4).

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

**Sources:** [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

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

The quotas page says the request and response body-size limits "do not apply when streaming the body through an Akamai Function"; related limits such as total memory usage still apply (§4.1). **Inference:** the S3 client's calls are outbound subrequests, so the subrequest limits in §4.1, including 10,000 subrequests per minute per deployed Function, apply to them.

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

- Both functions come from the `uuid` npm package, imported as `import { v4 as uuidv4 } from 'uuid';` and `import { validate as uuidValidate } from 'uuid';`. The MySQL tutorial installs it with `npm install uuid --save`, and the PostgreSQL tutorial with `npm install @spinframework/spin-postgres @spinframework/spin-variables uuid` (§2.6, §2.11).
- `uuidv4()` generates a new product ID (a UUID v4 string) in the create handlers.
- `uuidValidate(id)` validates a route parameter. An invalid ID returns `400 "Invalid identifier received via URL"`.

### 4.10 Logging

**Sources:** [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

```text
console.log(message)
spin aka logs [OPTIONS]
spin aka app logs [OPTIONS]
```

- "Everything your Spin application writes to `stdout` and `stderr` (for example, via JavaScript's `console.log`) is captured by Akamai Functions and made accessible via the `spin aka logs` command." The command "prints all log messages to `stdout`."
- The logging page's example messages come from a Go application that uses the `log/slog` package. The JS/TS samples log with `console.log`, and the cron and Supabase tutorials check their `console.log` output with `spin aka logs`.
- The logs are a debugging aid. The quotas page says they "are intended to help you debug an application during development and should not be used as a full, production-level observability system," which "is also reflected in the conservative logs limits." The logging page says to use Akamai Functions logging only for debugging at low traffic levels, because "It does not provide full large scale observability."

Logging quota limits:

| Limit | Value | Documented behavior |
|---|---|---|
| Maximum log line size | 1 MiB | "Once the maximum size is reached any additional logs are silently dropped." |
| Maximum total logs emitted per Function invocation | 10 MiB | "Once the maximum size is reached any additional logs are dropped after a warning." |
| Maximum calls to `spin aka logs` per minute | 5 | Not stated |
| Maximum time period for log retrieval | 60 days | Not stated |

The quotas page also limits the administrative API that every `spin aka` command calls to 50 calls per minute per user, and it lists a separate "maximum days for historical data retrieval" of 7 for the plugin (§4.21). The `--since` option defaults to 7 days. The sources do not reconcile the 7-day figure with the 60-day log-retrieval period (§5.6). **Inference:** the 7-day figure matches the maximum `--usage-since` period of `spin aka app status`, so it may describe usage data rather than logs.

Selecting the application and account (full option lists in §4.15):

- By default, `spin aka logs` returns logs for the application linked to the workspace. If the workspace is not linked, the logging page says to "specify the application name using the `--app-name` and `--account-name` flags, or run `spin aka link`." The command reference has `spin aka app link` and no top-level `link` command (§6.22).
- `--app-name <APP_NAME>` or `--app-id <APP_ID>` selects the application. "If neither `app-id` nor `app-name` is provided, the app will be inferred from the workspace config." `-f, --from <PATH>` points to the application's manifest or directory and defaults to `./spin.toml`.
- `--account-id <ACCOUNT_ID>` or `--account-name <ACCOUNT_NAME>` selects the account. When neither is given, the command "defaults to the current account context." In the plugin v1.0.0 help, these options also read the `SPIN_AKA_ACCOUNT_ID` and `SPIN_AKA_ACCOUNT_NAME` environment variables. The account guide says that by default all spin commands run on the personal account, and that the environment variables require plugin v0.7.8 or higher. **Inference:** to read the logs of an application in a team account, name the account with an option or an environment variable; the sources do not say whether a linked workspace also records the account (§6.18).

Filters (plugin v0.7.0 through v1.0.0): `-n, --max-lines` ("Number of lines to show from the end of the logs," default `10`), `--since` (an RFC3339 timestamp, a Unix epoch timestamp in seconds, or a duration such as `30m`; default `7d`), `--component-id` (default: all components), `--deployment-version` (default: the latest deployment version), and `--region` (default: all regions). `spin aka app logs` has the same options.

The logging page says that enabling verbose Spin error messages requires the `--verbose` flag, without naming the command. `spin aka logs` documents `-v, --verbose` ("Verbose output").

Locally, `spin up` logs component stdio to `.spin/logs/`. The logging page refers local logging questions to the Spin observability guide at `https://spinframework.dev/observing-apps#application-logs`.

The same page, titled "Application logs and usage," documents usage metrics. `spin aka app status` reports the number of invocations over a period set with `--usage-since`, which accepts 5 minutes (`5m`) to 7 days (`7d`) and defaults to `7d`. Full usage information beyond seven days can be made available in Akamai Control Center Billing on request (§4.15). The page's usage sample writes the option as `-–usage-since`, with an en dash, and its Usage section says that "The `spin aka app status` command prints all log messages to `stdout`" (§5.6).

Log line format:

```text
2025-01-16 13:31:46 [hello-akamai-functions]  2025/01/16 13:31:36 INFO GET https://11077e3b-d632-4df3-921f-f7ebefb9aaca.fwf.app/hello: Handled by handle_hello func
2025-02-13 14:50:54 [supabase-proxy]  Storing data in Cache at all-articles
```

### 4.11 Rust and Go HTTP APIs

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md)

Rust, quickstart (`#[http_component]` style, §3.3):

```text
spin_sdk::http::Request
spin_sdk::http::Response            (Response::builder().status(..).header(..).body(..).build())
spin_sdk::http::IntoResponse
spin_sdk::http_component            (#[http_component] on a synchronous fn)
req.header(name)
anyhow::Result<impl IntoResponse>
```

Rust, security tutorial (`#[http_service]` style, §3.3):

```text
spin_sdk::http::{IntoResponse, Request, Response}
spin_sdk::http_service              (#[http_service] on an async fn)
spin_sdk::variables                 (variables::get(name).await?)
req.headers().get(name)             (.and_then(|v| v.to_str().ok()))
Response::builder().status(..).body(..)?
anyhow::Result<impl IntoResponse>
```

Go (TinyGo):

```text
spinhttp.Handle(func(w http.ResponseWriter, r *http.Request))
w.Header().Set(name, value)
fmt.Fprintln(w, ...)
```

Apart from the Rust `variables::get` call in the security tutorial, the sources document no Rust or Go bindings for variables, KV, databases, or outbound HTTP. The security sample's HMAC and Base64 code comes from the third-party `hmac`, `sha2`, and `base64` crates (§2.9). The CI guide links the Spin language guides for Rust, Go, JavaScript/TypeScript, and Python components. For the SDK versions behind the two Rust styles, see the **General knowledge** note in §3.3.

### 4.12 WebAssembly language support

**Sources:** [docs/_source/techdocs-akamai-com/webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md)

The language-matrix page states the support rule in two ways:

1. "Spin, SpinKube, and Akamai Functions require WASI support. Any language supported for WASI should be supported on the Akamai Functions."
2. "Anything with WASI or Spin SDK support runs on Spin, and Akamai Functions."

These differ for languages that have a Spin SDK but no WASI support: TypeScript and Prolog (WASI ✗, Spin SDK ✓). TypeScript is documented through the `http-ts` template and several TypeScript tutorials, which is consistent with the second statement. No Akamai page documents Prolog.

Support categories: **Core** means a WebAssembly 1.0 implementation exists, **Browser** means at least one browser implementation, **WASI** means support for at least WASI Preview 1, and **Spin SDK** means a Spin SDK is available. For production-grade WebAssembly, the page suggests Rust, JavaScript/TypeScript, Python, and Go. This is a recommendation, not an exclusive list.

Other pages name these languages:

- Welcome page: "SDK support for Rust, Go, JavaScript, and Python that allows you to write in your language of choice and compile to WebAssembly."
- Comparison page: functions can be written "in a variety of languages such as Rust, Go, Python, JavaScript."
- Quickstart: Spin "provides SDKs for a variety of programming languages, including, but not limited to, Rust, Go, JavaScript and TypeScript." The quickstart and the welcome page say that the quickstart has instructions and samples for JavaScript, TypeScript, and Rust; the quickstart also has TinyGo tabs.
- Code samples on Akamai pages cover JavaScript, TypeScript, Rust (quickstart and security tutorial), and Go with TinyGo (quickstart). No page has a Python sample (§4.11).

Language-specific statements on the quotas page (feature-level details in §4.13):

- "Use Rust if you need optimal performance. JavaScript and especially Python tend to scale worse due to their interpreted nature (sometimes two or three times worse than Rust depending on use case)."
- Instance reuse, supported since Spin v4.0.0 and automatically enabled, "Requires up-to-date Wasi-p3 compatible SDKs, such as v7.0.0 of the Rust SDK, v4.0 for the Go SDK or v5.0 of the Python SDK. Not yet supported for JavaScript."
- HTTP middleware, supported since Spin v4.1.0: "Currently only out-of-the-box with Rust SDK >7.0.0".
- WebAssembly garbage collection, supported since Spin v4.2.0 and enabled by default: "For languages that use WasmGC, such as Kotlin, Scala or Dart". Compare the matrix rows for these languages below.
- For per-language feature support, the page points to the Spin Language Support Guide and notes that "Some Spin SDK triggers and APIs are not yet supported on Akamai Functions."

| Matrix status | Languages |
|---|---|
| Spin SDK ✓ | JavaScript, TypeScript, Python, Rust, Go, C# and .NET, Prolog |
| WASI ✓, Spin SDK in progress | Java, Swift, Scala (JVM), Kotlin (JVM), Clojure |
| WASI ✓, no Spin SDK | PHP, C++, Ruby, C, Kotlin (Wasm), Haskell, Zig, AssemblyScript, Grain, Motoko |
| WASI in progress, no Spin SDK | Dart (`ip`), COBOL, Erlang (BEAM), Lisp |
| Neither WASI nor Spin SDK | R, Objective-C, Scala (native), PowerShell, Lua, Perl |
| Not applicable | CSS, Shell |

### 4.13 Spin feature support and other platform interfaces

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md)

The quotas page says that "some Spin SDK triggers and APIs are not yet supported on Akamai Functions" and lists support as follows. Supported Spin CLI versions are in §4.14. For feature support by programming language, the page points to the Spin Language Support Guide (`https://spinframework.dev/language-support-overview`).

| Spin feature | Akamai Functions support |
|---|---|
| **Triggers** | |
| HTTP | Supported |
| Cron | Partial support: Tech Preview |
| Redis | Not supported |
| Custom triggers | Not supported |
| **APIs** | |
| Outbound HTTP | Supported |
| Application variables | Supported (§4.3) |
| Key-value storage | Supported; the store is in Limited Availability (§4.4) |
| SQLite storage | Not supported |
| Service chaining | Supported |
| MySQL | Supported (§4.5) |
| PostgreSQL | Supported (§4.6) |
| Outbound Redis | Supported |
| **Features** | |
| Component dependencies | Supported since Spin v4.0.0 |
| WebAssembly garbage collection | Supported since Spin v4.2.0 and enabled by default, for languages that use WasmGC, such as Kotlin, Scala, or Dart |
| HTTP middleware | Supported since Spin v4.1.0. "Currently only out-of-the-box with Rust SDK >7.0.0"; the link points to the Rust SDK 7.0.0 documentation. |
| Instance reuse | Supported since Spin v4.0.0 and automatically enabled. It requires "up-to-date Wasi-p3 compatible SDKs, such as v7.0.0 of the Rust SDK, v4.0 for the Go SDK or v5.0 of the Python SDK," and is "not yet supported for JavaScript." |
| Connection pooling | "Supported since Spin v3.4.0 but not enabled by default." Enablement is requested through an Akamai representative. |

Notes on the table:

- **Cron.** The row links to the cron tutorial, in which `spin aka cron` invokes "the Spin application's HTTP endpoint on a scheduled basis" (§3.5, §4.17). The HTTP trigger reference names `http` as the supported trigger type. Cron is a Tech Preview that "is not subject to the same expectations of stability as the rest of the platform": crons "are not 100% guaranteed to run, nor are they guaranteed to run at exactly the scheduled time," and an account can configure at most 10 crons across all deployed Functions (§1.7). **General knowledge:** this is not Spin's separate cron trigger plugin (`[[trigger.cron]]`), which no Akamai source documents.
- **Instance reuse.** The quotas page says that "for some use cases, the new Instance Reuse feature can have a strong positive impact on maximum RPS." **General knowledge (Spin v4 documentation, not an Akamai source):** a WASI P3 HTTP component can handle several requests in one instance, one after another or concurrently, while a WASI P2 component is not reused. Keep request-specific data out of global and static variables. The sources do not say which SDK version each Akamai template installs (§3.3, §4.11).
- **HTTP middleware.** The security tutorial suggests implementing its token check "as HTTP Middleware in the latest Spin versions" (§4.23). **General knowledge (Spin v4 documentation, not an Akamai source):** middleware components are attached to an HTTP trigger with `dependencies.middleware = [{ component = "<name>" }]`. They have no capabilities of their own and can only inherit the application component's capabilities through `inherit_configuration`.
- **Connection pooling.** Without pooling, each subrequest opens a new connection (§4.1). The row links to Spin's outbound HTTP runtime-configuration documentation. The sources do not document deploying a runtime configuration file with a Function.
- **Outbound Redis.** Outbound Redis is for customer-managed Redis and is distinct from the unsupported Redis trigger. The comparison page says "Akamai does not currently offer a managed Redis service, so teams need to bring their own Redis instance." The quotas page names the "Akamai ValKey Managed Database" as a store compatible with the Spin WASI Key Value interface (§4.4, §5.6). The sources give no SDK binding or manifest example for outbound Redis.
- **Runtime engine.** "Akamai Functions is committed to always running a supported version of the underlying wasmtime engine and to downstream security patches as soon as possible. In practice, this means we keep the platform updated to one of the two latest versions of wasmtime and the related Spin releases."

Calls between Functions and between components (the quotas page's platform limits):

Akamai Functions are "currently deployed as a distributed setup in Akamai Cloud behind the `fwf.app` CDN property," so "calling function A from inside of function B can lead to degraded performance." A request from Function B to Function A's `fwf.app` URL travels from Akamai Cloud through the nearest Akamai CDN edge node and back into Akamai Cloud. "Even though function A and B are likely deployed in the same cloud cluster, they cannot immediately access each other's endpoints without an added round trip of latency via the CDN."

```javascript
let result = await fetch("https://FUNC-A.fwf.app/endpoint?param=val");
```

Local service chaining between components of the same Function avoids this round trip. "The outbound call to `COMPONENT.spin.internal` is abstracted out completely and the endpoint invocation stays within the same WebAssembly execution context, never leaving the local server." "Local service chaining is a recommended best practice within Akamai Functions when using multiple components."

```javascript
let result = await fetch("https://COMPONENT-Y.spin.internal/endpoint?param=val");
```

**General knowledge (Spin documentation, not an Akamai source):** the host name is `<component-id>.spin.internal`, and the calling component must still list the target in `allowed_outbound_hosts`, for example `"http://component-y.spin.internal"`, or `"http://*.spin.internal"` for any component of the application. Either the `http` or the `https` scheme can be used. The Akamai sources show no manifest for service chaining.

Other Akamai services and AI:

- The welcome page says that any Akamai CDN, Security, or Cloud service can be used with a Functions application, for example API Acceleration, App & API Protector, or Akamai's managed databases. Other pages qualify this: PostgreSQL support "is not yet compatible with Linode DBaaS" (§4.6), Akamai offers no managed Redis service (above), and "EdgeKV is not currently compatible with Akamai Functions" (§4.4).
- The use-cases page describes Functions pushing data into the EdgeKV admin APIs, writing origin-health status to EdgeKV, and reconciling revoked tokens to EdgeKV (§4.22). The sources do not reconcile these use cases with the KV page's compatibility statement (§5.6). **Inference:** such integrations call EdgeKV as an external service; they do not give access to the Functions KV store.
- The comparison page places AI inference in Akamai Functions and lists "AI inference endpoints" among its workloads. The use-cases page describes an AI agent that "integrates with AI inference calls (inference itself runs outside of functions)." No source documents an inference API for Functions, and the quotas page's feature table does not list Spin's Serverless AI API (§5.6). **Inference:** call external inference services over outbound HTTP (§1.4).

### 4.14 Project setup, local development, and builds

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md)

The quickstart's workflow is: install Spin, install the `aka` plugin, install the language tooling, create an application from a template, build it, test it locally with `spin up`, log in, and deploy. Deployment and CI are in §4.18.

Supported Spin version: "Akamai Functions supports Spin CLI v4.0.0 or newer. Older Spin versions may work (especially for existing Functions projects), but are not guaranteed to." Every command in the `spin aka` command reference lists `Spin compatibility: >=v4.0.0` (§1.9). Check the installed version with `spin --version`.

Install Spin, which is both a CLI tool and a runtime:

| Platform | Documented steps |
|---|---|
| Linux (amd64), macOS (amd64, arm64) | `curl -fsSL https://developer.fermyon.com/downloads/fwf_install.sh \| bash`, then move the `spin` binary to a directory on the path, for example `sudo mv ./spin /usr/local/bin/spin` |
| Windows (amd64) | Download the Windows binary release of Spin from GitHub, unzip it, place `spin.exe` on the system path, and install the Spin templates or plugins for the language. The quickstart's download link points to Spin v3.6.2, which is older than the supported v4.0.0 (§1.9, §5.6). |
| GitHub Actions (§4.18) | `curl -fsSL https://wasm-functions.fermyon.app/downloads/install.sh \| bash`, then `mv spin /usr/local/bin/spin` |

The two install scripts have different URLs (§5.6), and neither command names a Spin version. The CI workflow has no `spin plugin install aka` step, and the sources do not say whether its script installs the plugin (§4.18).

Install the `aka` plugin, which the quickstart says is needed to interact with Akamai Functions:

```shell
spin plugin install aka
```

If the plugin is already installed, the quickstart says to upgrade it "to ensure compatibility with the latest features and fixes":

```shell
spin plugins update
spin plugins upgrade aka
```

The command reference shows `--help` output for plugin v1.0.0, v0.7.6, and v0.7.0 (§4.15). The `SPIN_AKA_ACCOUNT_ID` and `SPIN_AKA_ACCOUNT_NAME` environment variables need plugin v0.7.8 or higher (§1.9).

Language tooling (quickstart):

- JavaScript and TypeScript need Node.js: "We recommend Node.js version 22 (or newer)." The tutorials' Node.js versions are in §1.8.
- Rust needs the Rust toolchain plus the `wasm32-wasip1` target: `rustup target add wasm32-wasip1`.
- Go needs the TinyGo compiler, "as the standard Go compiler does not yet support WASI exports" (installation guide: `https://tinygo.org/getting-started/install/`). The quickstart's checks for a failed TinyGo build are in §1.8.
- In CI, install additional build tools, such as the Rust target, before `spin build` (§4.18).

Create an application from an Akamai Functions template. Every documented `spin new` command includes `-E akamai-functions`; the sources do not explain that option. Illustration, generalized from the quickstart's commands (not a source command):

```shell
spin new -E akamai-functions -t <template> --accept-defaults <app-name>
```

**Inference:** the Property Manager, MySQL, PostgreSQL, Supabase, and object-store tutorials use `-a` where the quickstart, KV, and cron tutorials use `--accept-defaults`, so `-a` appears to be its short form.

| Template | Language | Generated source | `spin build` runs |
|---|---|---|---|
| `http-js` | JavaScript | `src/index.js` | `npm run build` (webpack and `j2w`, producing `target/<app>.wasm`) |
| `http-ts` | TypeScript | `src/index.ts` | `npm run build`. The MySQL tutorial's build also runs `npm install` first and writes `dist/linode-mysql.wasm`. |
| `http-rust` | Rust | `src/lib.rs` | `cargo build --target wasm32-wasip1 --release` |
| `http-go` | Go (TinyGo) | `main.go` | `tinygo build -target=wasi -gc=leaking -no-debug -o main.wasm main.go` |

For `http-js` and `http-ts`, change to the application directory and run `npm install`. The tutorials name their extra packages in this step; for example, `npm install @spinframework/spin-kv` "installs the default packages in the template as well as" that package (§2.11). Instead of a template, an app can also be written from scratch. The Spin Hub (`https://spinframework.dev/hub`) has reference examples and templates, and the Akamai Functions samples repository (`https://github.com/akamai-developers/akamai-functions-samples`) has code samples sorted by use case.

Build: `spin build` compiles the application to WebAssembly. Spin runs each component's build command from the manifest's `component.(id).build` section, for example:

```toml
[component.hello-spin.build]
command = "tinygo build -target=wasi -gc=leaking -no-debug -o main.wasm main.go"
```

In the database tutorials, the component's `source` is the file that the build writes: `source = "target/hello-postgresql.wasm"` (PostgreSQL), and `source = "dist/linode-mysql.wasm"` with `exclude_files = ["**/node_modules"]` (MySQL). `spin aka deploy --build` runs `spin build` before deploying a local app (§1.8).

Local testing:

- `spin up` "starts an HTTP server on your local machine (port 3000 by default) and instantiates and invokes your Spin application for every request sent to the endpoint." It logs component stdio to `.spin/logs/` (§4.10).
- If port `3000` is in use, pass `--listen`, for example `spin up --listen 127.0.0.1:3001`.
- `spin up --build` (KV tutorial) and `spin build --up` (cron tutorial) build the application and run it in one step.
- From a separate terminal, test with `curl -i http://localhost:3000/`, and stop the server with `CTRL+C`. The quickstart's sample response, `Hello, Fermyon`, matches none of its template responses (§5.6).
- Environment variables prefixed with `SPIN_VARIABLE_` "will be accessible by your applications, if a corresponding variable is defined as part of the application manifest," for example `SPIN_VARIABLE_PG_CONNECTION_STRING` for the variable `pg_connection_string` (MySQL and PostgreSQL tutorials). The object-store tutorial exports its required variables before `spin up`. The security tutorial passes values with `--variable` "to `spin up` or `spin aka deploy`" (§4.3).
- Locally, the key-value store is the SQLite file `.spin/sqlite_key_value.db`, which persists across invocations and updates (§4.4).

Log in and deploy: run `spin aka login`, open the printed link, and authenticate with Akamai Control Center credentials. Logging in requires Akamai Functions to be enabled on the user's ACC contract (§1.1, §1.9). `spin aka deploy` then deploys to the personal account by default; "For production use, you need to deploy the Function in a Team Account," for example by passing `--account-name` (§1.6, §4.18).

### 4.15 CLI command reference (plugin v1.0.0)

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md)

The "Spin aka command reference" shows `--help` output for plugin v1.0.0 (the newest), v0.7.6, and v0.7.0. Each command heading has a single `Spin compatibility: >=v4.0.0` line above all of its version blocks, and the page does not map plugin versions to Spin versions. The signatures and options below are from v1.0.0; §4.16 compares the older versions. For installing the plugin, the page refers to the quickstart (§4.14).

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

`spin aka app` subcommands are `list` ("List apps"), `delete`, `status` ("Display information about an app"), `deploy`, `logs`, `cron`, `link` ("Link your local workspace to an existing Akamai Functions app"), `unlink`, `history` ("Lists past events for an app"), and `help`. `spin aka auth` has `login`, `token` ("Manage personal access tokens"), and `help`. `spin aka auth token` has `create`, `list` ("List personal access tokens for the current user"), `delete`, `regenerate`, and `help`. `spin aka cron` and `spin aka app cron`, both headed "(Tech Preview)" in the reference, have `list`, `create`, `delete`, and `help` (§4.17). No version of the command reference lists a top-level `spin aka link`; linking is `spin aka app link` (§6.22).

Signatures (v1.0.0):

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

Apart from the usage line, `spin aka app deploy`, `spin aka app logs`, and `spin aka auth login` have the same help text and options as `spin aka deploy`, `spin aka logs`, and `spin aka login`, and each `spin aka app cron` subcommand matches its `spin aka cron` counterpart. The six `help` subcommands (`spin aka help`, `spin aka app help`, `spin aka app cron help`, `spin aka auth help`, `spin aka auth token help`, `spin aka cron help`) print the parent command's help. Every command has `-h, --help`; `-V, --version` ("Print version") appears only on the top-level command.

Shared selector options:

- `--account-id <ACCOUNT_ID>` ("The account to perform the operation in") and `--account-name <ACCOUNT_NAME>` select the account: "If neither `--account-id` nor `--account-name` is provided, defaults to the current account context." In v1.0.0 they are bound to `[env: SPIN_AKA_ACCOUNT_ID=]` and `[env: SPIN_AKA_ACCOUNT_NAME=]`. They exist on `deploy`, `logs`, `app status`, `app list`, `app history`, `app link`, `app delete`, and the cron subcommands, including the `app` forms, but not on `app unlink`, `info`, `login`, the `auth token` subcommands, or `send-feedback`.
- The account guide says that "By default, all spin commands run on your personal account." To deploy, upgrade, or delete an application in a team account, pass `--account-id` or `--account-name` with each command, or set `SPIN_AKA_ACCOUNT_ID` or `SPIN_AKA_ACCOUNT_NAME`, which "are automatically picked up by spin" and need "spin aka plugin v0.7.8 or higher." The guide's examples also select a team account for `app list` and `app link`. The quickstart adds that `spin aka deploy` deploys to the personal account by default and that production use requires a team account, "for example passing `--account-name`." The CLI's "current account context" and the guide's "personal account" are not reconciled (§5.6). The sources do not say which value wins when an option and its environment variable are both set. **General knowledge:** in CLIs built with Rust's clap library, whose help format this output matches, a value given on the command line overrides the environment variable.
- `--app-id <APP_ID>` and `--app-name <APP_NAME>` select the app on `logs`, `app status`, `app history`, `app delete`, and the cron subcommands: "If neither `app-id` nor `app-name` is provided, the app will be inferred from the workspace config." On `app link` they name the app to link to, and if neither is given, "the app will be selected from an interactive prompt." `deploy` has `--app-id` but no `--app-name` in any version shown (§6.26).
- `-f, --from <PATH>` is "A path to the app" (on `app link` and `app unlink`, the workspace to link or unlink). It "may be a manifest (spin.toml) file or a directory containing a spin.toml file" and defaults to `./spin.toml`. There is no `--file` option (§6.23).
- `--format <FORMAT>` accepts `plain` (default) or `json` on `app list`, `app status`, `app history`, and `info`. `auth token create` accepts `plain`, `table`, `json`, or `yaml` (default `plain`); `auth token list` accepts the same values (default `table`).

Per-command options (v1.0.0):

| Command | Options and defaults |
|---|---|
| `deploy` / `app deploy` | `--build` (for local apps, run `spin build` before deploying; "ignored on remote apps, as they are already built"; env `SPIN_ALWAYS_BUILD`); `--profile <PROFILE>` ("Build profile to use when building and loading the app"; "If not specified, the default (anonymous) profile is used"); `--cache-dir <CACHE_DIR>` (cache for downloaded components and assets); `--variable <KEY=VALUE \| @FILE.json \| @FILE.toml>` (repeatable; a file is given as `@file.json` or `@file.toml`; for a repeated key "the last value will be used"); `-f, --from`; `--app-id` (if omitted, the app is inferred from the workspace config, and "If no app is inferred a new app will be created"); `--create-name <NEW_APP_NAME>` (only when deploying to an app that does not exist yet); account selectors; `--no-confirm` (skip the deploy confirmation prompt); `--skip-readiness-check` (skip the readiness check after deployment). Deployment flow: §4.18. |
| `logs` / `app logs` | `-v, --verbose` ("Verbose output"); `-n, --max-lines <MAX_LINES>` (lines from the end of the logs, default `10`); `--since <SINCE>` (default `7d`); `--component-id <COMPONENT_ID>` (default: all components); `--deployment-version <DEPLOYMENT_VERSION>` (default: the latest deployment version); `--region <REGION>` (default: all regions); account selectors; `-f, --from`; app selectors (§4.10) |
| `app status` | `--format`; `--usage-since <USAGE_SINCE>` ("Only show app usage since the given time"; default `7d`; "A maximum of 7 days and minimum of 5 minutes is enforced"); `-f, --from`; app and account selectors |
| `app list` | `--format`; `--verbose` ("Show more detailed information"); account selectors |
| `app history` | `--format`; `-f, --from`; app and account selectors |
| `app link` | Account selectors; `-f, --from` (the workspace to link); `--app-name` / `--app-id` (the app to link to; interactive prompt if both are omitted) |
| `app unlink` | `-f, --from` (the workspace to unlink) only |
| `app delete` | `--no-confirm` (skip the delete confirmation prompt); `-f, --from`; app and account selectors |
| `cron create` / `app cron create` | `-s, --schedule <SCHEDULE>` (required); `-p, --path-and-query <PATH_AND_QUERY>`; `--name <NAME>`; `-f, --from`; app and account selectors (§4.17) |
| `cron delete` / `app cron delete` | Positional `<NAME>` ("The name of the cron job to delete"); `-f, --from`; app and account selectors |
| `cron list` / `app cron list` | `-f, --from`; app and account selectors |
| `login` / `auth login` | `--token <TOKEN>` ("A personal access token to use for authentication"; env `SPIN_AKA_ACCESS_TOKEN`) |
| `auth token create` | `-n, --name <NAME>` (required); `-d, --description <DESCRIPTION>`; `-e, --expiration-days <EXPIRATION_DAYS>` ("How many days before the token expires", `[max: 90] [default: 30]`); `-s, --short` ("Show only the token, without additional information"); `--format` |
| `auth token list` | `--format`; `--verbose` ("Show more detailed information") |
| `auth token delete` | `-i, --id <ID>` (required); `--no-confirm` (skip the delete confirmation prompt) |
| `auth token regenerate` | `-i, --id <ID>` (required). The usage line has no `[OPTIONS]`. |
| `info` | `--format` |
| `send-feedback` | No options besides `-h, --help` |

Time values for `--since` and `--usage-since` can be an RFC3339 timestamp, a Unix epoch timestamp in seconds, or a duration from the present: a number followed by `s`, `m`, `h`, or `d` (for example `30m` for 30 minutes ago). Both default to 7 days.

Plugin limits from the quotas page:

- The plugin calls Akamai Functions' rate-limited administrative API: at most 50 API calls per minute per user. `spin aka logs` also has its own limits, including 5 calls per minute (§4.10).
- The plugin table lists 7 days as the maximum for historical data retrieval (§4.10 discusses how this relates to the 60-day log-retrieval period) and 15 days as the maximum logged-in session duration (§4.21).
- The maximum number of personal access tokens (PATs) is 100, and the maximum PAT lifetime is 90 days. The quotas page says "`spin aka auth regenerate` currently does not reset" the lifetime; the CLI command is `spin aka auth token regenerate` (§5.6). PATs have "largely the same rights and capabilities as the user who created them" but cannot delete a deployed Function or manage PATs. The account guide adds that a PAT impersonates its creator and can manage applications in all of that user's team accounts, "though they cannot delete them."

Workspace and inspection commands from the lifecycle guides:

- A workspace is the local directory that contains the application code and `spin.toml`. Any child directory where the manifest is located also belongs to the workspace.
- The first `spin aka deploy` links the workspace to the new application. After that, `spin aka deploy` upgrades the linked application, and `spin aka logs` and other app-scoped commands target it. The link guide says this avoids passing `--app-name` each time, although `deploy` has no `--app-name` option (§5.6, §6.26).
- Link with `spin aka app link` (interactive prompt) or `spin aka app link --app-name <app-name>`; the link guide's first example is written `spin aka link` (§6.22). Linking helps when the workspace was not linked on first deploy, for example after cloning a repository, switching machines, or joining a team. `spin aka app unlink` removes the link but does not delete the application.
- `spin aka info` shows the accounts and whether the workspace is linked (link guide):

```text
Auth Info
  Accounts: your-account
Workspace Info
  Root dir: /Users/user/src/hello-spin
  Linked app: hello-spin
```

- In the account guide, `spin aka info` lists each account as `name (id: ...)`: the personal account, named after the Akamai Control Center username (`info@example.com` appears as `info-example-com`), one default team account for each linked contract that has Akamai Functions enabled, and any requested team accounts. These are the values for `--account-name` and `--account-id`:

```text
Auth Info
  Accounts:
    - info-example-com (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
    - X-ABC-DEF-extended-default (id: yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyy)
    - X-ABC-DEF-dev-team-2 (id: zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzz)
```

- `spin aka app list` prints app names as plain text; `--format json` prints a JSON array of names, and `--verbose` prints `name (app-id)`.
- `spin aka app status` reports the linked app, or the app given by `--app-name` (the logging page also names `--account-name`). Its plain output has `Name`, `ID`, the public origin (`URL:` in the inspection guide, a `URLs:` list in the logging page), `Created at`, and `Invocations` (for example `229 in the past 7 days` or `86502 in the last 3 days`). `--format json` returns:

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

- For usage beyond seven days, "full usage information can be made available in Akamai Control Center Billing" upon request; the logging page says to contact the Akamai representative.
- `spin aka app delete --app-name <name>` asks `Are you sure you want to delete the app '<name>' (<id>)?` and prints `Deleted app successfully.` Deletion "is permanent and cannot be undone" (§1.6).

Examples from the sources:

```shell
spin aka app list --format json
spin aka app list --verbose
spin aka app status --app-name hello-akamai-functions --format json
spin aka app delete --app-name validate-jwt-tokens
spin aka app list --account-name X-ABC-DEF-extended-default
spin aka app link --app-name pw_checker --account-id yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyy
spin aka logs --app-name hello-akamai-functions
```

The logging page writes its `--usage-since` example as `-–usage-since`, with an en dash, and the account guide writes its team-account deletion as `spin aka delete app ...` (§6.20). Corrected forms:

```shell
# Corrected
spin aka app status --app-name hello-akamai-functions --usage-since 3d
spin aka app delete --app-name graphql --account-name X-ABC-DEF-extended-default
```

Illustration (not from a source) of the environment-variable form, which needs plugin v0.7.8 or higher:

```shell
export SPIN_AKA_ACCOUNT_NAME=X-ABC-DEF-extended-default
spin aka app list
```

### 4.16 CLI differences in older plugin versions

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md)

Besides v1.0.0 (§4.15), the command reference shows v0.7.6 help for every command and v0.7.0 help for every command except the six `help` subcommands. It shows no other versions. Every command heading lists only `Spin compatibility: >=v4.0.0`, so the page does not say whether the older plugins need a different Spin version.

| Area | v1.0.0 | v0.7.6 | v0.7.0 |
|---|---|---|---|
| Help layout | `Usage:`, `Commands:`, `Arguments:`, and `Options:`; no version banner | Same as v1.0.0 | A banner such as `spin-aka-deploy 0.7.0 (887b0b3 2026-03-20)`; `USAGE:`, `SUBCOMMANDS:`, `ARGS:`, and `OPTIONS:`; `<SUBCOMMAND>` placeholder; subcommands and options in a different, mostly alphabetical order |
| `-V, --version` | Top-level command only ("Print version") | Same as v1.0.0 | Every command ("Print version information") |
| `-h, --help` text | "Print help", or "Print help (see a summary with '-h')" on commands with long help | Same as v1.0.0 | "Print help information" |
| `deploy` / `app deploy` `--profile <PROFILE>` | Present | Absent | Absent |
| `[env: SPIN_AKA_ACCOUNT_ID=]` / `[env: SPIN_AKA_ACCOUNT_NAME=]` on the account selectors | Shown | Not shown | Not shown |
| `app unlink` options | `-f, --from` only | Same as v1.0.0 | `--account-id`, `--account-name`, and `-f, --from` |
| `--variable` placeholder | `<KEY=VALUE \| @FILE.json \| @FILE.toml>` | Same as v1.0.0 | The same placeholder followed by `...` |

Everything else is the same in all three versions: the command and subcommand sets and descriptions, the usage lines, option names and short forms, defaults and possible values (including `[max: 90] [default: 30]` on `--expiration-days`), `--skip-readiness-check`, the `logs` filters, `info --format`, the cron options, and the `SPIN_ALWAYS_BUILD` (`--build`) and `SPIN_AKA_ACCESS_TOKEN` (`--token`) bindings. Apart from `--profile` and the account env bindings, the v0.7.6 and v1.0.0 blocks differ only in line wrapping.

The account guide says the `SPIN_AKA_ACCOUNT_ID` and `SPIN_AKA_ACCOUNT_NAME` environment variables need "spin aka plugin v0.7.8 or higher." The reference does not show v0.7.8, and the sources do not say in which version `--profile` first appeared. **Inference:** with plugin v0.7.6 or v0.7.0, pass `--account-id` or `--account-name` on each command rather than relying on the environment variables, and upgrade the plugin (§4.14) before using `--profile`.

### 4.17 Cron CLI

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md)

Cron is a Tech Preview. The command reference heads `spin aka cron` and `spin aka app cron` with "(Tech Preview)", and their help reads "UNSTABLE: Manage cron jobs for an app." The tutorial says "Support for Cron jobs currently in Tech Preview." The quotas page says the cron system "is currently still in a tech preview phase and is not subject to the same expectations of stability as the rest of the platform": "crons are not 100% guaranteed to run, nor are they guaranteed to run at exactly the scheduled time." An account can have at most 10 configured crons across all of its deployed Functions (§1.7). The quotas page's Spin feature table lists the cron trigger as "Partial support" (§4.13).

The two forms have identical subcommands and options in v1.0.0, v0.7.6, and v0.7.0:

```text
spin aka cron create [OPTIONS] --schedule <SCHEDULE>
spin aka cron delete [OPTIONS] <NAME>
spin aka cron list [OPTIONS]
spin aka app cron create [OPTIONS] --schedule <SCHEDULE>
spin aka app cron delete [OPTIONS] <NAME>
spin aka app cron list [OPTIONS]
```

The subcommands are `list` ("List cron jobs for the current app"), `create` ("Create a cron job for the current app"), `delete` ("Delete a cron job from the current app"), and `help`.

`create` options:

- `-s, --schedule <SCHEDULE>` (required): "The cron schedule configuration," for example `"0 0 * * *"` "for every day at midnight."
- `-p, --path-and-query <PATH_AND_QUERY>`: "The path and query of the request to make to the app," for example `"/api/cron?foo=bar"`. The help neither marks it as required nor gives a default, and the sources do not say which path is requested when it is omitted.
- `--name <NAME>`: "Optional name of the cron job." It "Will default to an auto-generated name."
- `-f, --from <PATH>`, `--app-name` / `--app-id`, and `--account-id` / `--account-name` work as described in §4.15. In v1.0.0 the account selectors are bound to `SPIN_AKA_ACCOUNT_ID` and `SPIN_AKA_ACCOUNT_NAME`.

`delete` takes the job's name as the positional `<NAME>` ("The name of the cron job to delete"), and `list` takes no arguments. Both accept only the `--from`, app, and account selectors.

The tutorial says a job created with `spin aka cron create` "will be associated with the Spin application in your current working directory that you deployed to Akamai Functions," and that "You need a Spin application deployed to Akamai Functions to associate a cron job." In the CLI, the app "will be inferred from the workspace config" unless `--app-name` or `--app-id` is given. The account defaults to "the current account context"; the account guide says all spin commands run on the personal account by default and that a team account is selected by its ID or name, given as an option or through the environment variables (§4.15).

Schedules use standard crontab syntax. The tutorial says `spin aka cron` "supports multiple digits in each cron field, as well as intervals in any position, for example `* */12 * * *` to run every 12 hours" and also accepts comma-separated lists and ranges. A schedule that includes a time of day has to be in UTC; local times may need converting "to ensure correct execution" (§6.14). **General knowledge:** in standard five-field crontab syntax, `* */12 * * *` matches every minute of hours 0 and 12, while `0 */12 * * *` runs once every 12 hours. The source does not discuss this (§5.6).

An application can have multiple cron jobs as long as each combination of schedule and path and query is unique (§6.15), for example to run different tasks on separate schedules or to sync with several external services independently.

Example assembled from the documented options (an illustration, not from a source):

```shell
spin aka cron create --schedule "*/5 * * * *" --path-and-query "/" --name cron-job-1
```

The tutorial gives positional forms instead and says `create` "takes three arguments" (schedule, path and query, and name):

```shell
spin aka cron create "*/5 * * * *" "/" "cron-job-1"
spin aka cron list
spin aka cron delete cron-job-1
```

The positional `create` form conflicts with the command reference, which requires `--schedule` and lists no positional arguments for `create`. Keep it as tutorial evidence, but generate commands with `--schedule`, `--path-and-query`, and `--name` (§6.21). The tutorial's prose for this step also describes a `/*` path with a `msg` query parameter set to "fwf", which its command does not use.

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

Deleting prints `Deleted cron job 'cron-job-1' with schedule '*/5 * * * *'`. The source's rendering of the schedule (`'_/5 _ \* \* \*'`) is garbled by Markdown escaping. The application itself persists "unless you explicitly run the `spin aka app delete` command." The tutorial checks runs with `spin aka logs --app-name hello-world` (§4.10); its sample log line is stamped `2025-04-02 04:00:00` but reports `Cron job triggered at 2025-04-12T04:00:00Z`. The handler side is in §3.5.

The tutorial suggests cron jobs for data processing, report generation, background maintenance, data backups, periodic API polling, log file rotation, and scheduled notifications, and, in the handler, for querying a database for stale records, syncing data with an API, sending a report, or cleaning up expired sessions.

### 4.18 Deployment, updates, and CI

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/sign-up-for-akamai-functions.md](../_source/techdocs-akamai-com/sign-up-for-akamai-functions.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

#### First deployment

After logging in with `spin aka login` (§4.21), run `spin aka deploy` in the application directory. It reads `spin.toml` in the current directory to know what application to deploy, asks for a name for the new application, asks for confirmation, links the workspace to the new app, and waits until the app is ready:

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

The output names the target account. The route is the public URL that the platform generates for the Function, in the format `{UUID}.fwf.app`. It remains directly callable even when an Akamai property fronts the Function (§4.19, §4.23). `spin aka app status` prints it again later (§4.15).

#### Target account

The quickstart and the account guide state the account rules with different obligation levels:

- Quickstart: "By default, `spin aka deploy` deploys the Function in your Personal Account. For production use, you need to deploy the Function in a Team Account by for example passing `--account-name` to the command."
- Account guide: "Your personal account is visible and accessible only to you. You can create, update, remove, and even deploy applications within this account, but it should not be used for production workloads." Personal accounts are for "experimentation and testing" and "support lower limits and fewer requests per month." Team accounts are for "collaboration and production deployments" and "support access to the full limits and request counts specified in your contract."

No source describes enforcement beyond the personal account's lower limits (§1.6). Generated instructions for production deployments should therefore name a team account.

After the first login, a user has a personal account named after the Akamai Control Center username and at least one team account: one default team account is created for each linked Akamai Control Center contract that has Akamai Functions enabled. Further team accounts are requested through a form (§4.21). `spin aka info` lists the accounts of the logged-in user (account guide example):

```shell
Auth Info
  Accounts:
    - info-example-com (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
    - X-ABC-DEF-extended-default (id: yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyy)
```

"By default, all spin commands run on your personal account." To deploy, upgrade, or delete an application in a team account, select the account in one of two ways:

1. Pass `--account-id` or `--account-name` with each command.
2. Set `SPIN_AKA_ACCOUNT_ID` or `SPIN_AKA_ACCOUNT_NAME`, "which are automatically picked up by spin. To use this option you need spin aka plugin v0.7.8 or higher."

The v1.0.0 help shows these bindings (`[env: SPIN_AKA_ACCOUNT_ID=]`, `[env: SPIN_AKA_ACCOUNT_NAME=]`) on all 15 commands that accept account selectors, including `deploy`, `app deploy`, `app delete`, `app link`, and `app list`. The v0.7.6 help does not show them (§4.20). The help describes the default as "the current account context," a term that the sources do not define (§5.6). Account guide examples:

```shell
# Team account apps
spin aka app list --account-name X-ABC-DEF-extended-default
```

```shell
spin aka app link --app-name pw_checker --account-id yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyy
```

Illustration (not from a source): deploying to the example team account with either selection method.

```shell
spin aka deploy --account-name X-ABC-DEF-extended-default

export SPIN_AKA_ACCOUNT_NAME=X-ABC-DEF-extended-default   # plugin v0.7.8 or higher
spin aka deploy
```

#### `spin aka deploy` options (plugin v1.0.0)

`spin aka app deploy` has the same options. The full help is in §4.15.

| Option | v1.0.0 help |
|---|---|
| `--build` | For local apps, runs `spin build` before deploying. "This is ignored on remote apps, as they are already built." `[env: SPIN_ALWAYS_BUILD=]` |
| `--profile <PROFILE>` | "Build profile to use when building and loading the app. If not specified, the default (anonymous) profile is used." Added in v1.0.0. The sources do not show how a profile is defined. |
| `--cache-dir <CACHE_DIR>` | Cache directory for downloaded components and assets |
| `--variable <KEY=VALUE \| @FILE.json \| @FILE.toml>` | Variables passed to the app, as `key=value` or as a JSON or TOML file. The option may be repeated. "If the same key is specified multiple times the last value will be used." |
| `-f, --from <PATH>` | A `spin.toml` file or a directory that contains one. Defaults to `./spin.toml`. |
| `--app-id <APP_ID>` | The app to deploy to. Without it, the app is inferred from the workspace config, and "if no app is inferred a new app will be created." |
| `--create-name <NEW_APP_NAME>` | Name of the new app. "This is only valid when you are deploying to an app that does not exist yet." |
| `--account-id <ACCOUNT_ID>`, `--account-name <ACCOUNT_NAME>` | The target account (above) |
| `--no-confirm` | Skips the deploy confirmation prompt |
| `--skip-readiness-check` | Skips the readiness check after deployment |

`deploy` has no `--app-name` option in any version shown (§6.26). The variables guide says "`spin aka deploy` can point to a `spin.toml` file by using the `--file` option," but the command reference lists only `-f, --from` (§6.23). **Inference:** `--create-name` (for a new app) or `--app-id` (for an existing app) avoids the new-app name prompt, and `--no-confirm` avoids the confirmation prompt.

#### Application variables

The variables guide declares a variable in `spin.toml` and overrides it at deploy time:

```toml
[variables]
compression_level = { default = "1" }
```

```shell
spin aka deploy --variable compression_level=3
```

```text
Deploying updated version of app my-app in account your-account (version 1 → 2)
OK to continue? yes
Waiting for app to be ready... ready

App Routes:
- my-app: https://ec8a19d8-6d10-4056-bb69-cc864306b489.fwf.app (wildcard)
```

- A deploy that changes only variables is "propagated as a new deployment, so you will see the version increment" (§1.5).
- Variables are encrypted by default. Once deployed, they are "encrypted at rest and in transit for the entirety of the lifetime of the application," but "the underlying cryptographic implementations have not been assessed for PCI compliance" (§1.5, §4.3).
- A single variable can be at most 1024 bytes, and all variables combined at most 4096 bytes (§1.2).
- The security tutorial passes its secrets "using the `--variable` CLI parameter to `spin up` or `spin aka deploy`" (§4.23). Its multi-line deploy commands have no `\` line continuations. Source sample:

```text
spin aka deploy
--variable fvt_secret=30a9c75577e68744078d7acb574955c43b3f0e740d03461ae2082c0edfd21286
--variable fvt_secret_id=secret_nr_95
```

**General knowledge:** a POSIX shell runs each of these lines as a separate command, so `spin aka deploy` runs without the variables, and each `--variable` line fails as an unknown command. Corrected form (line continuations added):

```shell
spin aka deploy \
  --variable fvt_secret=30a9c75577e68744078d7acb574955c43b3f0e740d03461ae2082c0edfd21286 \
  --variable fvt_secret_id=secret_nr_95
```

The tutorial's five-variable secret-rotation command has the same defect (§4.23, §5.6).

#### Updating an application

- Redeploy with `spin aka deploy` after changing the code or the version. "Your application's name and URL will remain the same after an update. Any existing integrations or links will also continue to work without interruption." In-flight requests "are gracefully completed by the previous version while all new traffic is routed to the updated version." Built-in support for running multiple versions simultaneously, "for example, canary or blue-green deployments," is not available (§1.6, §6.17).
- Changing the version is optional. Either edit `version` in `spin.toml` (the update guide changes `version = "0.1.0"` to `version = "0.1.1"`) or "accept the major version default upgrade prompted during the deployment process." The CLI help documents no option for this prompt.
- "Remember to specify your application's variables when upgrading": `spin aka deploy --variable <key>=<value>`. The guide does not say what happens to a previously supplied value that is omitted (§1.5).
- In a linked workspace, `spin aka deploy` upgrades the linked app and prints `Deploying updated version of app <app> in account <account> (version 1 → 2)`. The first deploy links the workspace automatically. A workspace that "wasn't automatically linked on first deploy," for example after cloning an existing repo, switching machines, or joining a team, is linked with `spin aka app link` (which prompts for the app) or `spin aka app link --app-name <app-name>`. The link guide also shows `spin aka link`, which the command reference does not list (§6.22).
- For an application in a team account, pass the account selector or set the environment variable again. The account guide says this "also applies if you would like to deploy, update, or delete an application running in a team account."
- Each deploy, including a variables-only deploy, creates a new version. The quotas page allows 2147483647 versions per deployed Function.

#### Deployment quotas

| Quota (quotas page) | Value |
|---|---|
| Function bundle size | 128 MiB; "Cannot currently be increased" |
| Deployed Functions per account | 50; the page says nothing about increasing it |
| Versions per deployed Function | 2147483647 |
| Function deploys per account per hour | 20; "Cannot currently be increased" |
| Single application variable / all variables combined | 1024 bytes / 4096 bytes |
| `spin aka` administrative API calls per minute per user | 50 |

The bundle size is the sum of the component sizes. The quotas page suggests the Spin dashboard project (`https://github.com/radu-matei/dash`) to view component sizes before deploying. The deploy-time behavior when a quota is exceeded is not documented (§1.2). **Inference:** a CI workflow that deploys on every push, like the one below, counts each run toward the 20 deploys per account per hour.

#### CI deployment with a personal access token (GitHub Actions)

The CI guide authenticates with a personal access token (PAT), which is used "in situations where you do not have access to a browser window," such as a CI or CD workflow.

1. Install Spin, log in with `spin aka login`, and create a token with `spin aka auth token create --name mytoken`:

```text
A personal access token has been created! The token will expire 30 days from now.
Here is your access token: pat_**************************
```

2. Save the token immediately: "This is your only chance to see it." Store it as the repository secret `SPIN_AKA_ACCESS_TOKEN` (**Settings** → **Secrets and Variables** → **Actions** → **New repository secret**, then **Add secret**), or with `gh secret set SPIN_AKA_ACCESS_TOKEN` (which prompts for the value) or `gh secret set SPIN_AKA_ACCESS_TOKEN < access_token.txt`. Any secret name works if the workflow references the same name.
3. Create `.github/workflows/deploy.yml`. The workflow runs on every push to `main`:

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

Notes on the workflow:

- `spin aka login --token <TOKEN>` logs in with a PAT. The option also reads the `SPIN_AKA_ACCESS_TOKEN` environment variable (`[env: SPIN_AKA_ACCESS_TOKEN=]` in every plugin version shown), although the workflow passes the token as an argument. **Inference:** exposing the secret to the login step as that environment variable keeps the token off the command line.
- The workflow passes no account selector, so it deploys to the personal account by default. **Inference:** for production, set `SPIN_AKA_ACCOUNT_NAME` or `SPIN_AKA_ACCOUNT_ID` in the job environment (plugin v0.7.8 or higher) or pass `--account-name`.
- The workflow runs `spin aka deploy` without `--no-confirm`, `--app-id`, or `--create-name`, and the sources do not explain how the prompts behave in CI. A fresh clone is not necessarily linked to an app (link guide), and without `--app-id` or a link, deploy creates a new app. **Inference:** for non-interactive deployments of an existing app, pass `--app-id` (shown by `spin aka app list --verbose`) and `--no-confirm`.
- The workflow never runs `spin plugin install aka`, although the quickstart installs the plugin to interact with Akamai Functions. The workflow's install script differs from the quickstart's (§4.14), and the sources do not say whether it installs the plugin. **Inference:** add `spin plugin install aka` if `spin aka` is unavailable in CI.

Add build tools before `spin build` when needed, for example the Rust target. This excerpt from the guide omits the `mv spin /usr/local/bin/spin` line of the full workflow:

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

#### Personal access tokens: rights, lifetime, and rotation

- **Rights.** PATs "impersonate the user that created them using the `spin aka login --token {YOUR-PAT}` command" and "can also manage applications in all team accounts that this user has access to (though they cannot delete them)" (account guide). The quotas page says PATs have "largely the same rights and capabilities as the user who created them," but cannot delete a deployed Function or manage ("create/update/delete/…") PATs. The error returned when a PAT attempts either is not documented.
- **Lifetime.** Tokens expire after 30 days by default. `--expiration-days` shows `[max: 90] [default: 30]`. The quotas page gives a maximum PAT lifetime of 90 days, which "`spin aka auth regenerate` currently does not reset." The command reference names the command `spin aka auth token regenerate --id <ID>` and lists no `spin aka auth regenerate` (§5.6). The quotas page also gives a maximum of 100 PATs.
- **Login sessions** are a separate concept with their own limit (§4.21). Do not apply the PAT lifetime to a login session, or the reverse.
- **Rotation.** "Once 30 days are up, the token will expire and you need to create a new token to continue using it in a CI/CD pipeline." Before the old token expires, create a new one, optionally with a longer expiration "up to 90 days from the time it is issued," and replace the repository secret:

```shell
spin aka auth token create --name mynewtoken --expiration-days 90
```

```text
A personal access token has been created! The token will expire 90 days from now.
Here is your access token: pat_**************************
```

**Inference:** because a PAT cannot manage PATs, a CI job cannot rotate its own token. Create the replacement in an interactive `spin aka login` session.

#### Deleting an application

- Find the app with `spin aka app list`, which prints the app names of the selected account; `--verbose` adds app IDs (§4.15).
- Delete it with `spin aka app delete`. "Deleting an application is permanent and cannot be undone." The command asks for confirmation unless `--no-confirm` is passed. Without `--app-name` or `--app-id`, the app is inferred from the workspace config.

```shell
spin aka app delete --app-name validate-jwt-tokens
```

```text
Are you sure you want to delete the app 'validate-jwt-tokens' (21077e3b-d632-4df3-921f-f7ebefb9aaca)? yes
Deleted app successfully.
```

- Any member of a team account can delete any application in it, because there is no role-based access control or per-application permission (§1.6). A PAT cannot delete a deployed Function (above).
- An application persists until it is deleted: "Your application will persist unless you explicitly run the `spin aka app delete` command" (cron tutorial). Unlinking a workspace "does not delete the application on Akamai Functions."
- The account guide's team-account example puts the words in a non-canonical order:

```shell
# Delete an app from a team account
spin aka delete app --app-name graphql --account-name X-ABC-DEF-extended-default
```

The command reference has no top-level `delete` command. Corrected form (§6.20):

```shell
spin aka app delete --app-name graphql --account-name X-ABC-DEF-extended-default
```

### 4.19 Property Manager integration

**Sources:** [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md)

The welcome page lists "Integration with your existing properties in Property Manager" among the platform's features. The tutorial routes a specific path on an existing property, for example `https://www.mydomain.com/hello`, to a Function. Its prerequisites are a property created and configured in Akamai Control Center, signing up for Akamai Functions, and installing Spin and the `aka` plugin.

#### Build and deploy the application

1. Create the application from the `http-js` template and move into its directory:

```shell
spin new -E akamai-functions -t http-js -a hello-akamai-functions

cd hello-akamai-functions
```

2. Replace the contents of `src/index.js`. Corrected form: the source's first line reads `Fimport { AutoRouter } from 'itty-router';`, a typo that is fixed here (§5.6).

```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

router.get("/", () => new Response("Hello, Akamai Functions"));

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

3. Build and deploy with `spin build` and `spin aka deploy` (§4.18).
4. Copy the app URL from the deploy output, for example `https://ec8a19d8-6d10-4056-bb69-cc864306b489.fwf.app`; the property configuration needs it. `spin aka app status` also prints this URL, "the public origin, that can be used to access the Spin application" (§4.15).

The tutorial's deploy tip says: "Use the `spin aka login` command to authenticate using your Akamai Control Center or GitHub account credentials." This conflicts with the quickstart, whose login step is "Authenticate using your Akamai Control Center credentials" and which requires Akamai Functions to be enabled on the user's Akamai Control Center contract. The FAQ and the account guide say that the account system uses Akamai Control Center as an identity provider, and no other current page mentions GitHub credentials (§4.21, §5.6).

#### Route a path to the Function

The tutorial's property steps follow. This list numbers them sequentially. The source numbers steps 6 and 7 of this list both as "6," so its steps 7 and 8 are steps 8 and 9 here (§5.6).

1. In Akamai Control Center, find the property.
2. Open its latest version and select **Edit New Version**.
3. In the property configuration settings, select **+ Rule**, choose **Blank Rule Template**, and name the rule.
4. In the **Criteria** panel, select **+ Match** and configure `Path` `matches one of` with the value `/hello/*`.
5. Add the **Origin Server** behavior with **+ Behavior** → **Standard Property Behavior**.
6. Select **Functions** as the **Origin Type**. "It is not required that you select Functions, but it is highly recommended." Selecting it automatically adds the Global Request Number behavior to the property, which "generates a unique identifier for each request on the Akamai edge network." The tutorial adds: "If you pass the Global Request Number with custom metadata you should use `AKA_GRN_HEADER` as the header name to prevent duplication when selecting Functions as the Origin Type."
7. Enter "the Akamai Functions origin that you want to use to retrieve the content" in the **Functions Origin** textbox.
8. Add a **Modify Outgoing Request Path** behavior (**Standard Property Behavior**) so that the property does not send the routing criteria (`/hello/`) as a path to the application:

| Field name | Desired value |
|---|---|
| Action | Replace Part of the incoming path |
| Find what | `/hello/` |
| Replace with | `/` |
| Occurrences | First occurrence only |
| Keep the query parameters | Yes |

9. Select **Save**.

Notes on the Origin Server settings:

- The tutorial documents only the **Functions** origin type. It gives no settings, and no consequences, for configuring the Function's origin with another origin type.
- The tutorial says to copy the URL from the deploy output for this configuration, and the security tutorial calls the origin the Function's "newly generated `{UUID}.fwf.app` URL from `spin aka deploy`" (§4.23). Neither page states whether the **Functions Origin** textbox expects the full `https://` URL or only the host name.
- The quotas page lists `akamai-*` among the request header prefixes stripped before a request reaches the Function's code, except `akamai-Bot` and `akamai-GRN` (§4.1). The sources do not say which header name the Global Request Number behavior uses by default or how `AKA_GRN_HEADER` relates to `akamai-GRN`.

#### Activate and test

"At this point, the new rule isn't active, yet!" Activate the latest property version on the **Activate** tab for the changes to take effect. "We highly recommend activating and testing the property modifications using the Staging environment instead of going straight to production." This is a recommendation, not a platform requirement.

To test, the tutorial sends a `GET` request to `https://engineerd.xyz/hello/`, where `https://engineerd.xyz` is replaced with the domain associated with the property:

```shell
curl https://engineerd.xyz/hello/
```

The response should be `Hello, Akamai Functions`, the same as a `GET` request to the application's root route. The `http-js` template, the root-route response, and the `/hello/` path are tutorial choices, not requirements for every Property Manager integration.

#### Restricting direct calls to the Function

- The security tutorial calls fronting the `{UUID}.fwf.app` URL with your own property "by using the Functions origin type in the Origin Server behavior" a best practice, because it lets you add security measures such as Akamai Web Application Firewall and Bot Manager in front of the Function. "However, even with this setup, if an attacker obtains the `{UUID}.fwf.app` URL they can still call it directly, potentially causing increased usage and costs or information leakage."
- Its request-signing method has the property add a signed `AF-Verification-Token` header to each request to the Function, through Advanced Metadata that only an Akamai representative can add and a **Modify Outgoing Request Header** behavior. Both are placed in the same scope as the Origin Server behavior that uses the Function as its origin. The Function validates the token and returns `403 Forbidden` for direct calls. The steps, samples, and secret rotation are in §4.23.

### 4.20 Version and compatibility ledger

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md)

This ledger collects the version statements in the current sources with their level of obligation. Example and observed versions are labeled as such and are not requirements. Spin feature support is detailed in §4.13, toolchain constraints in §1.8, project setup in §4.14, and templates and packages per tutorial in §2.11.

`spin aka` plugin and Spin CLI:

| Item | What the sources state | Level |
|---|---|---|
| Plugin versions documented | The command reference shows `--help` output for plugin v1.0.0 (the newest shown), v0.7.6, and v0.7.0 (banner `887b0b3 2026-03-20`). All 36 command headings show v1.0.0 and v0.7.6 output. v0.7.0 output is shown for 30 of them, all except the six `help` subcommands. The block labels are written `v.1.0.0`, `v.0.7.6`, and `v0.7.0` (once `v.0.7.0`). | Reference output. Current syntax is in §4.15, older versions in §4.16. |
| Spin compatibility of the plugin | Every command heading carries one line, `Spin compatibility: >=v4.0.0`, above all of its version blocks. The page does not map individual plugin versions to Spin versions. | Stated for all 36 commands |
| Spin CLI supported by the platform | Quotas page: "Akamai Functions supports Spin CLI v4.0.0 or newer. Older Spin versions may work (especially for existing Functions projects), but are not guaranteed to." This agrees with the command reference. | Support statement. Older versions are not guaranteed, not prohibited; no failure mode is documented. |
| Changes from v0.7.6 to v1.0.0 | `deploy` and `app deploy` gain `--profile <PROFILE>` (§4.18). `--account-id` and `--account-name` show `[env: SPIN_AKA_ACCOUNT_ID=]` and `[env: SPIN_AKA_ACCOUNT_NAME=]` on the 15 commands that accept them: `deploy`, `logs`, `app deploy`, `app delete`, `app history`, `app link`, `app list`, `app logs`, `app status`, and `create`, `delete`, and `list` under both `cron` and `app cron`. The remaining differences are line wrapping. | CLI help |
| Account environment variables | `SPIN_AKA_ACCOUNT_ID` and `SPIN_AKA_ACCOUNT_NAME` are "automatically picked up by spin. To use this option you need spin aka plugin v0.7.8 or higher." No v0.7.8 help is shown. | Plugin requirement stated by the account guide |
| `--token` environment variable | `spin aka login` and `spin aka auth login` read `SPIN_AKA_ACCESS_TOKEN` (`[env: SPIN_AKA_ACCESS_TOKEN=]`) in v1.0.0, v0.7.6, and v0.7.0. | CLI help |
| PAT expiration | `--expiration-days` shows `[max: 90] [default: 30]` in all three versions. The quotas page gives a maximum PAT lifetime of 90 days that regenerating does not reset (§4.18). | CLI help and quota |
| Cron commands | `cron` is described as "UNSTABLE: Manage cron jobs for an app" in all three versions, and the command reference headings mark cron "(Tech Preview)". | See the status table below |
| Version checks and upgrades | `spin --version` shows the installed Spin version. The top-level `spin aka` help lists `-V, --version` ("Print version"). For an existing plugin installation, the quickstart says to "take a moment to upgrade it to ensure compatibility with the latest features and fixes" with `spin plugins update` and `spin plugins upgrade aka`. | Recommendation |

Spin installation:

| Context | Documented command or link | Version |
|---|---|---|
| Quickstart, Linux (amd64) and macOS (amd64, arm64) | `curl -fsSL https://developer.fermyon.com/downloads/fwf_install.sh \| bash` | Not pinned |
| Quickstart, Windows (amd64) | Links the GitHub release of Spin v3.6.2 (`https://github.com/spinframework/spin/releases/tag/v3.6.2`) | Below the quotas page's "v4.0.0 or newer" and the command reference's `>=v4.0.0`. The sources do not reconcile the link with either statement (§5.6). |
| GitHub Actions guide | `curl -fsSL https://wasm-functions.fermyon.app/downloads/install.sh \| bash`, on `runs-on: ubuntu-latest` with `actions/checkout@v4` | Not pinned. The runner and action versions are example workflow values (§4.18). |

Spin features, SDKs, and runtime (details in §4.13):

| Item | What the sources state |
|---|---|
| Feature minimums | Quotas page feature table: component dependencies and instance reuse are supported since Spin v4.0.0, HTTP middleware since v4.1.0, and WebAssembly garbage collection since v4.2.0 (enabled by default). Connection pooling is "Supported since Spin v3.4.0 but not enabled by default." |
| SDK versions | Instance reuse "Requires up-to-date Wasi-p3 compatible SDKs, such as v7.0.0 of the Rust SDK, v4.0 for the Go SDK or v5.0 of the Python SDK. Not yet supported for JavaScript." HTTP middleware is "Currently only out-of-the-box with Rust SDK >7.0.0." The instance-reuse versions are examples ("such as"), and the sources do not say whether Rust SDK 7.0.0 itself provides middleware (§4.13). |
| Runtime engine | "In practice, this means we keep the platform updated to one of the two latest versions of wasmtime and the related Spin releases." |
| Rust handler styles | The quickstart template uses `#[http_component]` on a synchronous function. The security tutorial uses `#[http_service]` on an `async` function with `variables::get(...).await`. No source maps either style to a Rust SDK version (§3.3). |
| Go SDK | The quickstart's `main.go` imports `github.com/spinframework/spin/sdk/go/v2/http`, and its build output downloads `github.com/spinframework/spin/sdk/go v0.10.0` (observed output, §5.6). The quotas page names "v4.0 for the Go SDK" for instance reuse. The sources do not say which Go SDK version the `http-go` template uses. |

Toolchains and WASI:

| Item | What the sources state | Level |
|---|---|---|
| Node.js | Quickstart: "We recommend Node.js version 22 (or newer)," with the example output `v22.13.0`. Object-store tutorial: Node.js "version `22` or later" as a prerequisite. MySQL tutorial: "We recommend at least Node.js 21." | Recommendations and a tutorial prerequisite, not platform minimums (§1.8) |
| Rust | The `wasm32-wasip1` target (quickstart, CI guide) | Documented build target (§1.8) |
| TinyGo | "The Spin SDK needs TinyGo 0.27 or above," and `CGO_ENABLED=1` has to be set | Quickstart build-failure checklist (§1.8) |
| WASI | The language matrix's **WASI** category means "The language supports at least Preview 1 of the WASI proposal." The KV store supports the `wasi:keyvalue/store` and `wasi:keyvalue/batch` interfaces, not `wasi:keyvalue/atomic`. Instance reuse needs "Wasi-p3 compatible SDKs." No current source gives WASI snapshot dates. | §4.4, §4.12 |

Feature status:

| Item | What the sources state |
|---|---|
| Platform | No current source assigns a preview or availability status to the platform as a whole. |
| Key-value store | Limited Availability: the KV page's title and callout, and the quotas page's KV section (§1.3, §4.4) |
| Cron | Tech Preview: the cron tutorial and the quotas page ("Partial support"; crons "are not 100% guaranteed to run"), with `UNSTABLE` in the CLI help (§1.7, §4.17) |

Example and observed versions in samples, which are not requirements:

| Item | Where |
|---|---|
| Application version | The update guide changes `version = "0.1.0"` to `version = "0.1.1"` in `spin.toml`. Changing the version is optional (§4.18). |
| Build output | `webpack 5.97.1` in the quickstart and KV tutorial builds, `v22.13.0` from `node --version`, and Go SDK `v0.10.0` (above) |

### 4.21 Platform and operational reference

**Sources:** [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/sign-up-for-akamai-functions.md](../_source/techdocs-akamai-com/sign-up-for-akamai-functions.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md)

This subsection collects operational facts: availability, sign-up, accounts, authentication, plugin quotas, usage and logs, scaling, URLs, and escalation. Hard limits are in §1.2 and §1.9; recommendations here stay recommendations.

#### Availability and routing

- The FAQ says Akamai Functions is "currently deployed throughout the world in more than 25 regions." The quotas page says "Functions are deployed across 25+ regions" and that "The more geographically distributed your audience, the better Functions will scale."
- The current sources describe no preview or limited-availability status for the platform as a whole. Individual features keep their own status: the key value store is in **Limited availability** and cron is a **Tech Preview** (§1.3, §1.7).
- The welcome page describes a globally distributed PaaS hosted on Akamai Cloud, with "global geo replication by default." Client requests are forwarded "to the fastest responding region where your application is available." The comparison page says execution is routed automatically by the user's location, to the nearest region.
- There are no servers to provision, patch, or maintain.
- Functions are currently deployed "as a distributed setup in Akamai Cloud behind the `fwf.app` CDN property," so a call from one Function to another Function's `fwf.app` URL takes an extra round trip through the CDN (§4.13).

#### Sign-up and access

- The sign-up page offers a free trial. "To access Functions, you currently need an Akamai Control Center account."
- Without an ACC account, follow the page's "Create an Akamai Functions trial account" steps: fill in the form in the "Book a demo" section of the Akamai Functions homepage (`https://www.akamai.com/products/akamai-functions#demo`) and submit it. When Akamai approves the demo request, an email asks you to reset your password and activate your account. Accept the terms and conditions and click **Start Free Trial**; it "might take a few moments for Akamai to finish provisioning." When onboarding is complete, activate Akamai Functions in Marketplace.
- To activate in Marketplace, "you need an active Akamai contract and login credentials for Akamai Control Center to sign up for the 30-day free trial." Log in to ACC, open Marketplace (shopping cart icon), search for Akamai Functions, click **Learn More**, click **Try** on the Trial Details page, select "I accept the Terms and Conditions," and click **Start Trial**. The page's tip links "Create a trial account" to an empty target (§5.6).
- Users who cannot get an ACC account are told to "contact your Akamai account team for information about other options." Access through Cloud Manager is planned: "In the future, Akamai Functions will also support access via Cloud Manager." It is not available yet.
- Logging in requires the product to be enabled on the user's ACC contract; otherwise, sign up or contact the Akamai representative. "Only one person in your team needs to add Akamai Functions to your contract. From then on, any Akamai Control Center user coupled to that contract automatically has access to Akamai Functions."
- After activation, the sign-up page says: "Once you login you'll have access to your personal account and at least one team account. A team account is available for each contract where Akamai Functions is enabled."
- The sources do not say what happens to accounts or applications when the 30-day trial ends, and they do not state the error that a user without access sees.

#### Accounts, ownership, visibility, and collaboration

- Akamai Functions "uses its own account system, which is not directly controlled by Akamai Control Center (ACC) or Cloud Manager identity and access management." It uses ACC as an identity provider "to let you log in with your Akamai credentials and link you to the correct Akamai Functions accounts" (account guide, FAQ, quotas page).
- **Personal accounts:** one per user, for experimentation and testing. They "support lower limits and fewer requests per month" (no values are given; §1.2). A personal account "is visible and accessible only to you." You can create, update, remove, and deploy applications in it, "but it should not be used for production workloads."
- **Team accounts:** multiple per contract, for collaboration and production deployments, with "the full limits and request counts specified in your contract." A team account is visible and accessible to all of its members.
- On the first `spin aka login`, the system creates a personal account "named after your Akamai Control Center username" (in the example, `info@example.com` becomes `info-example-com`). It also adds the user to "one or more default team accounts. One default team account is created for each linked Akamai Control Center contract that has Akamai Functions enabled." The example default team account for contract `X-ABC-DEF` on the Extended plan is `X-ABC-DEF-extended-default`. The FAQ instead says the user is added to "the default team account for your contract," in the singular. The sources do not reconcile the two (§5.6).
- The "default" contract team account "includes all users of your company with an Akamai Control Center account tied to that contract."
- Akamai Functions does not currently support the ACC identity and access management system or any other role-based access control (RBAC): "all users in a team account currently have full administrative access. Every team member can create, update, permanently remove, and deploy an application" (§1.6).
- The `spin aka` plugin will be able to create team accounts and manage membership "In a future update." Until then, request a new team account tied to your contract through the team-account form (`https://fibsu0jcu2g.typeform.com/to/coitknMl?typeform-source=developer.fermyon.com`). Provide a team-account name and a list of active Akamai Functions usernames (personal account names). Each user must have logged in successfully at least once with `spin aka login`. To add or remove members, use the same form and select "Modify existing account" on question two. The form "is currently manually processed, so allow up to 48 hours." After the confirmation email, members see the account in `spin aka info` while logged in with a member profile (example: `X-ABC-DEF-dev-team-2`).
- There are currently no limits on the number of users or team accounts per ACC contract, on users per team account, or on team accounts a user can join.
- Account selection: "By default, all spin commands run on your personal account." To work in a team account, pass `--account-id` or `--account-name` with each command, or set `SPIN_AKA_ACCOUNT_ID` or `SPIN_AKA_ACCOUNT_NAME` ("you need spin aka plugin v0.7.8 or higher"). The command reference says an omitted selector "defaults to the current account context" (§5.6). The quickstart says `spin aka deploy` deploys to the personal account by default and that "For production use, you need to deploy the Function in a Team Account," for example with `--account-name`. The account guide's team-account delete example is written `spin aka delete app`; the command is `spin aka app delete` (§5.6, §6.20).
- Personal access tokens "impersonate the user that created them." They can manage applications in every team account that the user can access, but they cannot delete applications or manage tokens (§1.6).

#### Authentication and distinct lifetimes

- `spin aka login` prints a device-login URL, for example `https://login.infra.fermyon.tech/realms/neutrino/device?user_code=...`. The user follows it and authenticates "using your Akamai Control Center credentials."
- The Property Manager tutorial still says to log in with "your Akamai Control Center or GitHub account credentials." No other current source mentions GitHub as an identity provider; the quickstart, FAQ, account guide, and quotas page describe only ACC (§1.1, §5.6).
- **Login session.** The FAQ says: "Your login session started by `spin aka login` persists for 15 days without activity." The quotas page lists a "Maximum logged-in session duration" of 15 days. The FAQ describes an inactivity window, and the quotas page a maximum duration. The sources do not say whether activity extends a session or whether 15 days is an absolute cap (§5.6). They also do not say how either rule applies to a login with `--token`.
- **Personal access token (PAT).** A PAT is a separate credential for contexts without a browser, such as CI/CD. `spin aka auth token create` issues it; it expires after 30 days by default, and `--expiration-days` allows up to 90 (§1.9). It is shown only once. Supply it with `spin aka login --token` or the `SPIN_AKA_ACCESS_TOKEN` environment variable (§4.18). Do not apply PAT rules to the login session, or the reverse.
- **Application lifecycle.** The FAQ question also asks whether applications persist after logout, but the answer covers only the session. Other pages say an application persists until it is explicitly deleted with `spin aka app delete`; deletion is permanent, and unlinking a workspace does not delete the application (§1.6).

#### `spin aka` plugin quotas, usage, and logs

The plugin calls the Akamai Functions administrative API, "which is rate limited." The quotas page lists these maximums (the last two rows come from its logging table):

| Quota (maximum) | Value |
|---|---|
| API calls per minute per user | 50 |
| Days for historical data retrieval | 7 |
| Logged-in session duration | 15 days |
| Personal access tokens | 100 (the page does not say per what) |
| PAT lifetime | 90 days; "`spin aka auth regenerate` currently does not reset this" |
| `spin aka logs` calls per minute | 5 |
| Time period for log retrieval | 60 days |

- The quotas page names `spin aka auth regenerate`, but the CLI command is `spin aka auth token regenerate --id <ID>` (§4.15, §5.6).
- The 7-day historical-data limit and the 60-day log-retrieval period are separate rows. The sources do not say which data the 7-day limit covers (§4.10, §5.6).
- **Usage.** `spin aka app status` reports invocations over a `--usage-since` period of 5 minutes (`5m`) to 7 days (`7d`), defaulting to 7 days. "Upon request, full usage information can be made available in Akamai Control Center Billing so you can track usage across more than seven days" through the Akamai representative (§4.10).
- **Logs.** Akamai Functions captures stdout and stderr, retrievable with `spin aka logs`. The logs are a debugging aid: they "should not be used as a full, production-level observability system," and the logging page says to use them "for debugging at low traffic levels." Log size limits are in §1.2, and log commands in §4.10 and §4.15.

#### Scaling, load testing, and limit increases

- Akamai Functions "does not directly enforce specific limits on request rates per second (RPS) or minute (RPM)." Performance depends on the language, the computational complexity, and outbound connections. Internal load tests ranged from thousands to several millions of RPS per region.
- Guidance from the quotas page: a more geographically distributed audience scales better. "Use Rust if you need optimal performance"; JavaScript and especially Python tend to scale worse, "sometimes two or three times worse than Rust." Instance Reuse can strongly improve maximum RPS for some use cases (§4.13). Outbound connections, including KV reads and writes, can strongly reduce it.
- "We do not recommend running your own (high scale) load tests without involvement from your Account team." Limits of both Functions and the CDN in front of the Function can apply, and "Functions has strong fairness restrictions in place which prevent a single app from taking up too many resources without manual overrides." For capacity checks, your own load tests, or manual limit overrides, contact the Akamai representative.
- Connection pooling for subrequests is disabled by default, so each subrequest opens a new connection, "which can potentially impact performance." It can be enabled per Function through the Akamai representative.
- Resource-tier and request limits "can be increased to custom values" through the representative. The bundle size and the deploys-per-hour quota "Cannot currently be increased." KV limits can be raised "at an additional cost" (§1.2, §1.3).

#### Application identity and URLs

- A deployed application has "A stable URL that persists across deployments." After an update, the application's name and URL stay the same, and existing integrations and links keep working.
- The security tutorial says the platform "automatically generates a public URL" of the form `{UUID}.fwf.app`. Example URLs in other pages use three host patterns: `https://<uuid>.fwf.app` (quickstart, variables guide, list and inspect, logs, KV, Property Manager), `https://<uuid>.aka.fermyon.tech` (cron, MySQL, PostgreSQL, Supabase; the PostgreSQL page also shows `https://rust-pg-12345678.aka.fermyon.tech`), and `https://<uuid>.aka.akamai.tech` (object storage). Take the real URL from the `spin aka deploy` output or `spin aka app status` rather than constructing it (§5.6).
- The default URL can be called directly by anyone who has it, even when the Function sits behind your own property. §4.23 describes the recommended request-signing setup.
- The application ID is a UUID, shown by `spin aka app list --verbose` and `spin aka app status`.
- Sample responses from deployed applications include headers such as `Server: envoy`, `x-envoy-upstream-service-time`, `Akamai-GRN`, and `Set-Cookie: akaalb_...`. These are observed sample output, not documented behavior.

#### Configuration, data, and networking

- Changing an application variable is a new deployment that increments the version, not a runtime hot swap. Variables are encrypted at rest and in transit for the application's lifetime, but the cryptographic implementations "have not been assessed for PCI compliance" (§1.5, §4.3).
- The managed KV store is in Limited availability. It is scoped to one application, needs an explicit per-component grant, and accepts only the `"default"` label. A replica exists "in the same general geographic area" as each compute region, but the KV backends are less geographically distributed than the rest of the platform (§1.3, §4.4).
- A Linode Managed MySQL cluster accepts only inbound connections that it explicitly allows. The MySQL tutorial allows `0.0.0.0/0` (any host) "For the sake of this tutorial." The sources publish no egress IP ranges. The security tutorial says that allowlisting Akamai-controlled IP ranges "does not currently work well for Akamai Functions," because the platform "can use any IP address in the Cloud's considerable range" (§1.4, §4.23).

#### Platform updates

- The quotas page says "Akamai Functions supports Spin CLI v4.0.0 or newer"; older versions "may work ... but are not guaranteed to." The command reference lists `Spin compatibility: >=v4.0.0` (§4.20). For the wasmtime update policy, which keeps the platform on one of the two latest wasmtime versions and related Spin releases, see §4.13.

#### Support and escalation

- The FAQ says: "Please contact your Akamai representative if you need help." The CLI also has `spin aka send-feedback` ("Send us your feedback!").
- The sources route these requests through the Akamai representative or account team: access without an ACC account, sign-up help, enabling the product on a contract, custom resource-tier and request limits, connection pooling, capacity checks and load tests, manual limit overrides, usage history beyond seven days, KV limit increases, adding the Advanced Metadata for request signing, routing origin traffic through an Akamai property, and feedback on mTLS for Function-to-origin traffic (§4.23).

### 4.22 Akamai Functions, EdgeWorkers, and workload placement

**Sources:** [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

The comparison page presents EdgeWorkers and Akamai Functions as "complementary layers." Logic about how traffic flows (routing, authentication, cache key construction, header enforcement, request transformation) belongs in EdgeWorkers. Logic about "what happens to the data" (business rules, API orchestration, AI inference, data transformation, server-side rendering) belongs in Functions.

| Area | EdgeWorkers | Akamai Functions |
|---|---|---|
| Runtime | JavaScript (V8) | WebAssembly ("aka Spin"); Spin leverages Wasmtime |
| Execution layer | CDN / HTTP pipeline, at "every one of Akamai's thousands of edge locations" | Akamai Cloud regions; execution is routed automatically by the user's location |
| Primary use | Traffic orchestration and request/response manipulation | Application logic, APIs, microservices, and AI inference (see the AI inference note below) |
| Execution time | Less than 10 seconds, varying by event and tier | "30 seconds default, extendable" (conflicts with the quotas page; see below) |
| Trigger model | HTTP lifecycle events: `onClientRequest`, `onOriginRequest`, `onOriginResponse`, `onClientResponse`, and `responseProvider` | HTTP requests |
| Infrastructure | Fully managed | Fully managed |
| Data access | Outbound HTTP to Akamized hostnames; EdgeKV | Outbound HTTP to any hostname; Akamai Functions KV; customer-managed MySQL, PostgreSQL, and Redis |

- **Execution time conflict.** The quotas page has no single default execution time. Maximum wall time is 15 seconds on the Standard tier and 30 seconds on the Extended tier, maximum CPU time is 500 or 1000 milliseconds, and "These limits can be increased to custom values" through the Akamai representative. The comparison page's 30 seconds matches only the Extended wall time. Use the quotas page for limits (§1.2, §5.6).
- **Triggers.** The quotas feature table lists HTTP as supported, Cron as "Partial support" (Tech Preview), and the Redis trigger and custom triggers as not supported. The cron Tech Preview invokes an application's HTTP endpoint on a schedule through `spin aka cron` (§1.1, §1.7, §4.17).
- **Outbound HTTP.** Functions can call any hostname, not just Akamized endpoints, "without needing to create a CDN property to act as proxy to the 3rd-party endpoint." Each component still needs its hosts granted in `allowed_outbound_hosts` (§1.4).

Functions key features on the comparison page: fully managed, with no infrastructure to provision, scale, or maintain; a Wasm-based runtime that is language-agnostic, with fast cold starts and strong security sandboxing; auto-routing of requests to the nearest region; longer execution, suitable for more complex compute than CDN-layer edge execution; and the Spin framework. The page names Rust, Go, Python, and JavaScript as example languages.

EdgeWorkers on the comparison page: the `onClientRequest`, `onOriginRequest`, `onOriginResponse`, and `onClientResponse` events run within Akamai CDN metadata stages. CPU, memory, and execution-time limits are kept low so that heavy workloads cannot cause contention at small CDN regions. With `responseProvider`, EdgeWorkers can act as the origin to the CDN. Its limits are "a bit higher" than those of other events, but it is "still fundamentally limited by the compute power available in small regions."

Data stores on the comparison page:

- **Functions KV** (platform managed) is "similar in concept to EdgeKV but with access from the compute layer rather than the CDN layer." The KV page and the quotas page put it in Limited availability, with intentionally low default limits and backends that "are not deployed to the same level of geographical distribution as the rest of the platform" (§1.3, §4.4).
- **MySQL** (customer managed) is compatible with Linode DBaaS MySQL. "MySQL with Linode DBaaS is the smoothest path today for teams wanting a fully managed Akamai-native persistence layer in a single region." A multi-region MySQL cluster needs extra effort.
- **PostgreSQL** (customer managed) is "not yet compatible with Linode DBaaS." Teams can use self-managed or third-party hosted PostgreSQL "in the interim."
- **Redis** (customer managed): "Akamai does not currently offer a managed Redis service," so teams bring a self-managed (for example, on Linode) or third-party instance. The page lists session caches, rate limit counters, real-time leaderboards, pub/sub messaging, and distributed locks as Redis workloads. Separately, the quotas page says that the Spin WASI Key Value interface "is also compatible with other KeyValue stores, such as (self-hosted) Redis or the Akamai ValKey Managed Database" (§4.4).
- The page says "the platform roadmap indicates managed options are coming" for PostgreSQL and Redis. This is a roadmap statement, not current availability.

Documented Functions use cases (use-cases page). Choose Functions for "application-level compute such as a microservice, an API backend, building an AI agent that integrates with AI inference calls (inference itself runs outside of functions)," or for workloads that benefit from WebAssembly's portability and performance:

- Edge API endpoints and microservices, served from the nearest region.
- Real-time data transformation and enrichment.
- Server-side rendering with lightweight frameworks such as Preact.
- WebAssembly-based image and media processing.
- Stateful CRUD APIs against a self-managed PostgreSQL instance.
- Session validation against a customer-managed Redis cluster co-located with the nearest Functions region, keeping total validation latency under 50 ms in the example.

**AI inference conflict.** The comparison page lists AI inference as a primary Functions use and "AI inference endpoints" among its workloads. The use-cases page says inference "itself runs outside of functions." The sources do not reconcile the two (§1.1, §5.6).

Documented EdgeWorkers use cases: advanced request routing, A/B testing and feature flagging, authentication and token validation (with EdgeKV as a distributed blocklist for revocation checks), personalized caching and cache-key customization, dynamic header injection and security-policy enforcement, and geography-based content adaptation. The comparison page adds URL rewriting and conditional origin selection.

Combined designs treat EdgeWorkers as "the traffic controller" and Functions as "the application server." "EdgeWorkers can make requests to Akamai Functions, or Akamai Functions can push data into the EdgeKV admin APIs." Documented examples:

- Personalized content assembly: EdgeWorkers serves cached default or cohort pages from the edge and leaves authenticated requests uncached. Cache misses for cohort pages and fully personalized pages are routed to a Function, in a pattern "similar to Edge Side Includes but with fully programmable logic."
- Multi-region failover and traffic shaping: a Function polls origin health endpoints and writes status to "a shared data store such as EdgeKV," and EdgeWorkers reads it on every request to make routing decisions.
- Token revocation: a Function keeps the revocation list in MySQL as the source of truth, reconciles revoked tokens to EdgeKV for EdgeWorkers, and exposes its control plane both as an API described with an OpenAPI specification and as an MCP server for AI agents.

**EdgeKV conflict.** The KV page says the Functions key value store "is different and separate from EdgeKV. EdgeKV is not currently compatible with Akamai Functions." The use-cases page has Functions push data into the EdgeKV admin APIs, write health status to EdgeKV, and reconcile tokens to EdgeKV. Both statements are kept, and the sources do not reconcile them (§1.3, §5.6). The sources define no EdgeWorkers configuration, EdgeKV admin-API call, or credentials for these integrations.

To put an Akamai property in front of a Function, see §4.19. To restrict a Function to calls from your own property, see §4.23.

### 4.23 Securing a Function: request signing and origin protection

**Sources:** [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

This subsection follows the "Secure your Akamai Function" tutorial. It restricts calls into a Function to Akamai properties that you control, and then lists the documented options for protecting traffic from the Function to your origin. The tutorial's steps are recommended practice, not platform requirements.

#### Why sign requests

- Deploying a Function generates a public URL of the form `{UUID}.fwf.app`. Akamai's default platform defenses "will protect your Function from typical hacking attempts," but they do not prevent direct calls to this URL.
- "As a best practice," the tutorial says to front the URL with your own Akamai property by using the **Functions** origin type in the Origin Server behavior. That lets you add your own protections, such as Akamai Web Application Firewall and Bot Manager, in front of the Function. The Property Manager tutorial says that selecting **Functions** as the Origin Type "is not required ... but it is highly recommended." Selecting it automatically adds the Global Request Number behavior, and the origin is entered in the **Functions Origin** textbox. If you pass the Global Request Number with custom metadata, use `AKA_GRN_HEADER` as the header name to prevent duplication (§4.19).
- Even behind a property, anyone who obtains the `{UUID}.fwf.app` URL can still call it directly, "potentially causing increased usage and costs or information leakage." Request signing is meant to prevent this. It protects only the property-to-Function leg; for the Function-to-origin leg, see the last part of this subsection.

#### The verification token

The property adds a per-request `AF-Verification-Token` HTTP header, signed with a pre-shared secret that only the property and the Function know. The Function validates the value and can discard requests whose header is absent or not properly signed.

- Format: `[timestamp]-[secret-id]-[random-number]-[hash]`.
- `[hash]` is a SHA256-HMAC of `[timestamp]-[secret-id]-[random-number]`, generated with the shared secret. The secret itself is not present in the token.
- `[secret-id]` names the secret, to support key rotation.
- Source example: `1748898524-35a4-57533-ylTbN1WW0b8/T2JJcZ2g+Cti6cOLTm/p28cD9M3Yf+Q=`. In the metadata below, the timestamp is `%(AK_CURRENT_TIME)` and the random number is between 1 and 65535. The example hash is Base64-encoded, and both validation samples decode it as standard Base64.

#### Generate the token at the edge

1. Create three custom PMUSER variables with the security level "sensitive":

| Variable | Tutorial name | Content and constraints |
|---|---|---|
| `PMUSER_FVT_SECRET` | "current secret" | A 64-character (32 byte) hexadecimal string: the symmetric secret used to verify the token |
| `PMUSER_FVT_SECRET_ID` | "current secret-id" | A name you choose for the secret, for example `my_cool_key1`. It cannot contain dashes. |
| `PMUSER_FVT_VALUE` | "current token" | Holds the constructed token so that it can be sent to the Function in a request header |

2. Generate the secret with "any sufficiently random generator" or with the Akamai-provided generator at `https://debug.akamai.com/generate/key`. **General knowledge:** `openssl rand -hex 32` also prints 64 hexadecimal characters.
3. Ask your Akamai representative to add the following Advanced Metadata to the property. "You cannot add Advanced Metadata in your property yourself."

```xml
<!----
This metadata requires the existence of three separate PMUSER variables:

PMUSER_FVT_SECRET - a 64-character hexadecimal string used to generate the token.
PMUSER_FVT_SECRET_ID - a 'name' for the above key, e.g. "my_cool_key1"  used to generate the token. This value must not contain dashes.
PMUSER_FVT_VALUE - the variable into which the token is generated.
-->

<!-- Generate random number -->

<assign:variable>
    <name>FVT_CRT_RAND</name>
    <transform>
        <rand>
            <min>1</min>
            <max>65535</max>
        </rand>
    </transform>
    <hidden>on</hidden>
</assign:variable>

<!-- Set initial value as "[time]-[secret-id]-[rand]" -->

<assign:variable>
    <name>FVT_CRT_VALUE</name>
    <value>%(AK_CURRENT_TIME)-%(PMUSER_FVT_SECRET_ID)-%(FVT_CRT_RAND)</value>
    <hidden>on</hidden>
</assign:variable>

<!-- Create SHA256-HMAC of value using key -->

<assign:variable>
    <name>FVT_CRT_HASH</name>
    <value>%(FVT_CRT_VALUE)</value>
    <transform>
        <hmac>
            <algorithm>SHA256</algorithm>
            <key>%(PMUSER_FVT_SECRET)</key>
        </hmac>
    </transform>
    <hidden>on</hidden>
</assign:variable>

<!-- Copy token value to PMUSER variable -->

<assign:variable>
    <name>PMUSER_FVT_VALUE</name>
    <value>%(FVT_CRT_VALUE)-%(FVT_CRT_HASH)</value>
</assign:variable>

<!-- Delete temporary variables after use -->

<assign:variable-delete>FVT_CRT_RAND</assign:variable-delete>
<assign:variable-delete>FVT_CRT_VALUE</assign:variable-delete>
<assign:variable-delete>FVT_CRT_HASH</assign:variable-delete>
```

#### Send the token to the Function

Configure the Modify Outgoing Request Header behavior:

| Field | Value |
|---|---|
| Action | Modify |
| Select header name | Other |
| Custom Header Name | AF-Verification-Token |
| Header Value | `{{user.PMUSER_FVT_VALUE}}` |
| Avoid Duplicate Headers | Yes |

After the Function is deployed, put the Advanced Metadata and Modify Outgoing Request Header behaviors "in the same scope as (and applied to)" the Origin Server behavior that uses the Function as its origin.

As an alternative, an EdgeWorker can call the Function. It retrieves the token value in code and sets the header. The source marks this as pseudocode:

```javascript
// pseudocode
var token = request.getVariable("PMUSER_FVT_VALUE");
request.setHeader("AF-Verification-Token", token);
```

The quotas page's list of request headers that the platform strips before the code runs does not include `AF-Verification-Token` (§4.1).

#### Validate the token in the Function

Pass the secret and the secret ID as Spin application variables. The tutorial says these variables "are encrypted by default on the platform and can be explicitly marked as holding secrets." Only `fvt_secret` is marked `secret = true`:

```toml
[variables]
fvt_secret = { required = true, secret = true }
fvt_secret_id = { required = true }

[component.my-secure-component.variables]
fvt_secret = "{{ fvt_secret }}"
fvt_secret_id = "{{ fvt_secret_id }}"
```

The variables guide adds that deployed application variables are "encrypted at rest and in transit for the entirety of the lifetime of the application," but "the underlying cryptographic implementations have not been assessed for PCI compliance" (§1.5). Variable syntax and APIs are in §4.3.

The tutorial calls its samples "basic code examples" that show "the overall concept and proper token validation method." It says production code "should include logic to check for proper header format etc." and that "It would also make sense to implement this as HTTP Middleware in the latest Spin versions" (HTTP middleware support: §4.13).

TypeScript sample, as published:

```typescript
import * as variables from '@spinframework/spin-variables';

async function handleRequest(request: Request): Promise<Response> {

  const token = request.headers.get('AF-Verification-Token') ?? '';
  const [timestamp, secretId, random, hash] = token.split('-');

  const secret = variables.get('fvt_secret');
  if (!secret || secretId !== variables.get('fvt_secret_id'))
    return new Response('Forbidden', { status: 403 });

  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey('raw', encoder.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['verify']);

  const signature = Uint8Array.from(atob(hash), (c) => c.charCodeAt(0));
  const valid = await crypto.subtle.verify('HMAC', key, signature, encoder.encode(`${timestamp}-${secretId}-${random}`));

  if (!valid)
    return new Response('Forbidden', { status: 403 });

  return new Response('Hello, verified caller!');

```

Defects (§5.6): the sample ends without the closing `}` of `handleRequest`, and nothing registers the handler (there is no `addEventListener('fetch', ...)` call). As published, it is not a complete entry point. §3.1 has a labeled illustration that closes the function and registers it the way the other TypeScript samples do. The sample also uses Web APIs without imports (`crypto.subtle`, `atob`, `TextEncoder`; §2.8).

Rust sample, as published:

```rust
use base64::{engine::general_purpose::STANDARD, Engine};
use hmac::{Hmac, Mac};
use sha2::Sha256;
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::{http_service, variables};

#[http_service]
async fn handle_request(req: Request) -> anyhow::Result<impl IntoResponse> {
    let token = req
        .headers()
        .get("AF-Verification-Token")
        .and_then(|v| v.to_str().ok())
        .unwrap_or_default();

    let (signed_value, hash) = token.rsplit_once('-').unwrap_or_default();
    let secret_id = signed_value.split('-').nth(1).unwrap_or_default();

    let secret = variables::get("fvt_secret").await?;
    let mut mac = Hmac::<Sha256>::new_from_slice(secret.as_bytes())?;
    mac.update(signed_value.as_bytes());

    let valid = secret_id == variables::get("fvt_secret_id").await?
        && mac
            .verify_slice(&STANDARD.decode(hash).unwrap_or_default())
            .is_ok();

    let (status, body) = if valid {
        (200, "Hello, verified caller!")
    } else {
        (403, "Forbidden")
    };
    Ok(Response::builder().status(status).body(body.to_string())?)
}
```

- Besides `spin_sdk` and `anyhow`, the sample uses the crates `hmac`, `sha2`, and `base64`. The tutorial shows no `Cargo.toml`, crate versions, template, or build command.
- It uses the `#[http_service]` attribute on an `async fn` and awaits `variables::get(...)`. This differs from the quickstart's `#[http_component]` handler; §3.3 compares the two styles, and the sources state no SDK version for either (§5.6).
- If a `variables::get(...)` call fails, the handler returns the error through `?`. The HTTP response for that case is not documented (§3.2).

Notes that apply to both samples:

- Both use the secret string's UTF-8 bytes as the HMAC key and do not hex-decode it. The tutorial describes the secret as a "64-character (32 byte) hexadecimal string" and does not say how the metadata's `<key>` element interprets it. **Inference:** a port to another language should keep the samples' key handling.
- Neither sample checks the token's timestamp or implements the previous-secret fallback described under secret rotation below. **Inference:** without a freshness check, a captured token remains valid for as long as its secret is accepted.

#### Deploy with the secret values

The tutorial passes the values with `--variable`, which it says works with both `spin up` and `spin aka deploy`. As published:

```shell
spin aka deploy
--variable fvt_secret=30a9c75577e68744078d7acb574955c43b3f0e740d03461ae2082c0edfd21286
--variable fvt_secret_id=secret_nr_95
```

Defect (§5.6): the command is split across lines without `\` continuations. **General knowledge:** a shell would run `spin aka deploy` alone and treat each `--variable` line as a separate command. Corrected form:

```shell
spin aka deploy \
  --variable fvt_secret=30a9c75577e68744078d7acb574955c43b3f0e740d03461ae2082c0edfd21286 \
  --variable fvt_secret_id=secret_nr_95
```

The command reference says `--variable` "may be repeated," takes `key=value` or a JSON or TOML file given as `@file.json` or `@file.toml`, and uses the last value when a key is repeated (§4.15). A variable-only deployment is still a new deployment that increments the version (§1.5).

Finally, configure the deployed Function's `{UUID}.fwf.app` URL as the origin for the path that generates the token. With the sample code, a request through the CDN property returns "Hello, verified caller," and a direct request to the `{UUID}.fwf.app` URL returns `403 Forbidden`.

#### Rotate secrets

The tutorial rotates the secrets periodically "As a security best practice." Because the CDN property and the Function have different deployment pipelines and durations, the secrets are not updated in both at the same time. The Function is always updated first and accepts the old secret for a short time while the property is updated.

Declare the current secret, the previous secret, and the deployment time of the current version:

```toml
[variables]
fvt_secret = { required = true, secret = true }
fvt_secret_id = { required = true }
fvt_prev_secret = { default = "", secret = true }
fvt_prev_secret_id = { default = "" }
fvt_deploy_time = { default = "" }

[component.my-secure-component.variables]
fvt_secret = "{{ fvt_secret }}"
fvt_secret_id = "{{ fvt_secret_id }}"
fvt_prev_secret = "{{ fvt_prev_secret }}"
fvt_prev_secret_id = "{{ fvt_prev_secret_id }}"
fvt_deploy_time = "{{ fvt_deploy_time }}"
```

The code can then try `fvt_prev_secret` when the token contains `fvt_prev_secret_id` or when verification with the current secret fails, but only during a predefined grace period. The tutorial's example grace period is a maximum of 30 minutes between the current timestamp at execution time and `fvt_deploy_time`. After that, only the new values are accepted. The sources show no code for this fallback.

Rotation example, starting from `PMUSER_FVT_SECRET = 30a9c75577e68744078d7acb574955c43b3f0e740d03461ae2082c0edfd21286` and `PMUSER_FVT_SECRET_ID = secret_nr_95` live on the CDN:

1. Generate a new secret (`a455085783e634d4f6133ac36f90f22817ca07b09dd43f40bdecae5bf2bca3ca`) and secret ID (`secret_nr_96`).
2. Deploy a new Function version with the new and previous values. As published (same missing-`\` defect as above):

```shell
spin aka deploy
--variable fvt_secret=a455085783e634d4f6133ac36f90f22817ca07b09dd43f40bdecae5bf2bca3ca
--variable fvt_secret_id=secret_nr_96
--variable fvt_prev_secret=30a9c75577e68744078d7acb574955c43b3f0e740d03461ae2082c0edfd21286
--variable fvt_prev_secret_id=secret_nr_95
--variable fvt_deploy_time=2026-11-10T23:55:44Z
```

Corrected form:

```shell
spin aka deploy \
  --variable fvt_secret=a455085783e634d4f6133ac36f90f22817ca07b09dd43f40bdecae5bf2bca3ca \
  --variable fvt_secret_id=secret_nr_96 \
  --variable fvt_prev_secret=30a9c75577e68744078d7acb574955c43b3f0e740d03461ae2082c0edfd21286 \
  --variable fvt_prev_secret_id=secret_nr_95 \
  --variable fvt_deploy_time=2026-11-10T23:55:44Z
```

3. Wait until the new Function version is "fully deployed and actively accepting traffic." The Function still validates the CDN's tokens with `fvt_prev_secret`.
4. Update the property's `PMUSER_FVT_SECRET` and `PMUSER_FVT_SECRET_ID` to the new values.
5. Activate the new property version in staging or directly in production "(within 30 minutes)."

In the example, `fvt_deploy_time` is a date-time string (`2026-11-10T23:55:44Z`), while the example token's timestamp is a number (`1748898524`). The grace period is measured from `fvt_deploy_time` to the current time at execution, not from the token's timestamp. **Inference:** if the property is not active with the new secret before the grace period ends, the Function rejects requests signed with the old secret.

#### Secure Function-to-origin traffic

Request signing validates only traffic from the CDN into the Function, not traffic from the Function to your origin. The tutorial lists these options:

1. Implement your own authorization and authentication layer. You can distribute API access tokens with the Function as encrypted Spin variables.
2. Reuse the signing method. Either pass the `AF-Verification-Token` header in every subrequest to the origin and check the hash there again, or set up the same scheme between the Function and the origin with separate secrets.
3. Allowlist Akamai-controlled IP ranges on the origin firewall, for example with the Site Shield or Origin IP Access Control Lists behaviors. This common CDN setup "does not currently work well for Akamai Functions": the platform runs on Akamai Cloud and "can use any IP address in the Cloud's considerable range," so you would have to allowlist all of Akamai Cloud, "severely weakening this approach." Alternatively, route origin traffic through an Akamai property first, so that the request again comes from the CDN and Site Shield or Origin IP Access Control can apply. This "can, however, have severe latency and scalability issues when used at large scale," so consult your Akamai account team first.
4. Mutual TLS (mTLS). Functions uses mTLS internally "to ensure only Akamai properties can call the Functions backend," but this option is not currently exposed to customers for Function-to-origin traffic. If that limits your use case, the tutorial asks you to give feedback through your account team.

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
| Inter-application `fetch` | The other Function's public `*.fwf.app` URL, granted in `allowed_outbound_hosts` like any outbound host; components of one Function can use local service chaining (`*.spin.internal`) | A call to another Function's URL is routed through the CDN and "can lead to degraded performance"; local service chaining is "a recommended best practice" (§1.4, §6.8) |
| Cron job | A deployed HTTP application, a UTC schedule, and a unique schedule/path-and-query pair | The duplicate-job error is not stated |
| Rust build | `rustup target add wasm32-wasip1` | The CI guide says such projects "need" the target before they compile |
| Go build | TinyGo 0.27+ and `CGO_ENABLED=1` | Listed by the quickstart as checks when the build fails |

### 5.4 CLI context and lifecycle interactions

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md)

| Command | Implicit context | Related commands and data |
|---|---|---|
| Any account-aware command | `--account-id` / `--account-name`, or `SPIN_AKA_ACCOUNT_ID` / `SPIN_AKA_ACCOUNT_NAME` (plugin v0.7.8 or higher) | Without a selector, commands use "the current account context"; the account guide and quickstart describe the personal account as the default (§4.18, §5.6) |
| PAT-authenticated automation | `spin aka login --token` or `SPIN_AKA_ACCESS_TOKEN` | A PAT impersonates the user who created it and can manage apps in that user's team accounts, but cannot delete deployed Functions or manage PATs (§4.18, §6.28) |
| `spin aka deploy` / `spin aka app deploy` | The current account context and `./spin.toml`, unless selectors override them. The app is inferred from the workspace config; if none is inferred, a new app is created and the workspace is linked. | `--variable`, `--create-name`, `--no-confirm`, `--skip-readiness-check`, `--build`, `--profile` (v1.0.0), and `--app-id`. Each deploy is a new version. |
| `spin aka app link` / `app unlink` | The workspace at `--from` | `link` prompts for the app when `--app-name`/`--app-id` is omitted. In v1.0.0 and v0.7.6, `unlink` accepts only `--from`. Unlinking does not delete the app. |
| `spin aka info` | The logged-in user and the current workspace | Shows the accounts (the account guide's example lists names and IDs), the workspace root, and the linked app; v1.0.0 adds `--format` (`plain` or `json`) |
| `spin aka app list` | The current account context (the account guide says the personal account) unless an account selector is given | `--verbose` shows app IDs; `--format json` emits JSON |
| `spin aka app status` | The workspace-linked app unless `--app-name`/`--app-id` is given | Name, ID, URL, creation time, and invocations over `--usage-since` (5 minutes to 7 days) |
| `spin aka app history` | The workspace-linked app unless selected | Past events for the app. `--format plain\|json`. |
| `spin aka logs` / `app logs` | The workspace-linked app unless selected; latest deployment version; all components; all regions | Captured stdout and stderr. `--since` (default `7d`), `-n/--max-lines` (default `10`), `--component-id`, `--deployment-version`, and `--region`. |
| `spin aka app delete` | The selected or current account and app | Permanent. Any team member can do it because RBAC is absent. `--no-confirm` skips the prompt. |
| `spin aka cron create/list/delete` | The deployed app of the current workspace unless selected | Calls an HTTP path. Tech Preview / `UNSTABLE`. Schedules are UTC. |
| `spin aka login` / `auth login` | Interactive device login, or `--token` / `SPIN_AKA_ACCESS_TOKEN` | The FAQ says a login session started by `spin aka login` persists for 15 days without activity; the quotas page lists a 15-day maximum logged-in session duration (§5.6). Neither says how this applies to `--token` logins. PATs have their own expiration (90 days at most). |
| `spin aka auth token create/list/delete/regenerate` | The current user | Save a new token immediately, store it as a CI secret (the guide names it `SPIN_AKA_ACCESS_TOKEN`, but any name works if the workflow matches), and rotate it before expiration. `--token` also reads the `SPIN_AKA_ACCESS_TOKEN` environment variable. |

### 5.5 Cross-platform and data-service interactions

**Sources:** [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md)

| Interaction | Documented purpose | Capability or boundary |
|---|---|---|
| Akamai property → Akamai Functions | Route a property path to a Functions application | Origin Server behavior with Origin Type **Functions** ("not required ... but it is highly recommended"), the origin entered in **Functions Origin**, and the path rewritten with Modify Outgoing Request Path; the Global Request Number behavior is added automatically, and `AKA_GRN_HEADER` is the header name for passing it with custom metadata (§4.19, §6.19) |
| Akamai property or EdgeWorker → Akamai Functions | Accept traffic only from your own property | Sign each request with an `AF-Verification-Token` header (SHA256-HMAC with a pre-shared secret held in sensitive PMUSER variables and in Spin variables marked `secret = true`) and validate it in the Function; the `{UUID}.fwf.app` URL otherwise stays directly callable (§4.23) |
| Akamai Functions → your origin | Verify that origin traffic comes from your Function | Own authentication, reusing the token scheme, or a CDN detour; IP allowlisting is weak because Functions can use any Akamai Cloud IP address, and mTLS for this leg is not exposed to customers (§4.23) |
| EdgeWorkers → Akamai Functions | Route selected requests from the CDN pipeline to application logic | The sources state this interaction but give no EdgeWorkers configuration signature |
| Akamai Functions → third-party HTTP APIs | API orchestration, external services, and inference calls | The target must be in the component's `allowed_outbound_hosts`. In the AI-agent use case, inference runs outside Functions. |
| Akamai Functions → MySQL/PostgreSQL | Customer-managed relational persistence | Use the `mysql://` or `postgres://` capability with an explicit port. MySQL works with Linode DBaaS; PostgreSQL does not yet (§4.22). |
| Akamai Functions → Redis | Caching, sessions, pub/sub, rate limits, leaderboards, and locks | Outbound Redis is supported, but the sources give no SDK binding or manifest example. Akamai offers no managed Redis today. |
| Akamai Functions → EdgeKV admin APIs | Publish control-plane data, such as revocation lists or origin health, for EdgeWorkers | The use-cases page states the integration but gives no binding. EdgeKV stays separate from Functions KV. |
| Akamai Functions → another Functions application | Inter-application calls | Use the other Function's public URL; the call is routed through the CDN and can degrade performance. Components of one Function can instead use local service chaining via `*.spin.internal`, a recommended best practice (§4.13, §6.8) |
| Cron service → Akamai Functions HTTP route | Periodic polling, maintenance, synchronization, and notifications | Tech Preview, UTC schedules, and a unique schedule/path pair |
| Akamai Functions with other Akamai services | API Acceleration, App & API Protector, and managed databases | The welcome page says any Akamai CDN, Security, or Cloud service can be used with Functions applications. Other pages add exceptions: PostgreSQL is not yet compatible with Linode DBaaS, and the KV page says Edge is not currently compatible (§5.6). |

### 5.6 Source conflicts and sample defects

**Sources:** [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md), [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/faq.md](../_source/techdocs-akamai-com/faq.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/sign-up-for-akamai-functions.md](../_source/techdocs-akamai-com/sign-up-for-akamai-functions.md), [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md), [docs/_source/techdocs-akamai-com/deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md), [docs/_source/techdocs-akamai-com/delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md), [docs/_source/techdocs-akamai-com/webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md), [docs/_source/techdocs-akamai-com/welcome.md](../_source/techdocs-akamai-com/welcome.md), [docs/_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md), [docs/_source/techdocs-akamai-com/use-cases.md](../_source/techdocs-akamai-com/use-cases.md), [docs/_source/techdocs-akamai-com/use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md), [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md), [docs/_source/techdocs-akamai-com/secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md), [docs/_source/techdocs-akamai-com/query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md), [docs/_source/techdocs-akamai-com/stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md), [docs/_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md)

Cross-source conflicts:

| Topic | What the sources say | Guidance for generated output |
|---|---|---|
| Execution time | Comparison page: "30 seconds default, extendable." Quotas page: Standard tier 500 milliseconds CPU time and 15 seconds wall time; Extended tier 1000 milliseconds and 30 seconds; "These limits can be increased to custom values." | The 30-second figure matches only the Extended wall time. **Inference:** unless the tier is known, design for the Standard limits (§1.2, §4.22) |
| Login session | FAQ: the session "persists for 15 days without activity." Quotas page: "Maximum logged-in session duration" is 15 days. | Unresolved: an inactivity period versus a maximum duration. Neither page says whether activity extends a session or how it applies to `--token` logins (§1.9, §4.21) |
| Data retrieval windows | Quotas page: "Maximum days for historical data retrieval" is 7, and "Maximum time period for log retrieval" is 60 days. Logging page: `--usage-since` allows at most 7 days. | Unresolved: the 7-day row does not say which data it covers. Keep usage queries within 7 days (§1.9, §4.10) |
| PAT regeneration command | Quotas page: "`spin aka auth regenerate` currently does not reset" the 90-day token lifetime. Command reference: only `spin aka auth token regenerate` exists. | Use `spin aka auth token regenerate` (§1.9, §4.15) |
| Login identity | Property Manager tutorial: `spin aka login` authenticates "using your Akamai Control Center or GitHub account credentials." Quickstart: "Authenticate using your Akamai Control Center credentials." FAQ and account guide: Akamai Control Center is the identity provider. | Use Akamai Control Center credentials (§1.10, §4.19, §4.21) |
| Production account | Quickstart: "For production use, you need to deploy the Function in a Team Account." Account guide: the personal account "should not be used for production workloads." | The obligation levels differ and neither page describes enforcement. Deploy production Functions to a team account (§1.6, §4.18) |
| Default account | Command reference: without `--account-id` or `--account-name`, commands use "the current account context." Account guide: "By default, all spin commands run on your personal account." Quickstart: by default, `spin aka deploy` deploys "in your Personal Account." | Pass `--account-name` or `--account-id`, or set `SPIN_AKA_ACCOUNT_NAME` or `SPIN_AKA_ACCOUNT_ID`, explicitly (§4.15, §4.18) |
| Default team accounts | FAQ: a new user is added to "the default team account for your contract." Account guide: "one or more default team accounts," one for "each linked Akamai Control Center contract that has Akamai Functions enabled." Sign-up page: "at least one team account." | Follow the account guide; `spin aka info` lists the available accounts (§4.21) |
| Supported Spin version | Command reference: "Spin compatibility: >=v4.0.0." Quotas page: "Spin CLI v4.0.0 or newer. Older Spin versions may work ... but are not guaranteed to." Windows quickstart: links Spin v3.6.2. | Use Spin v4.0.0 or newer (§1.8, §4.14, §4.20) |
| `cron create` syntax | Command reference: `create [OPTIONS] --schedule <SCHEDULE>` with `-p, --path-and-query` and `--name`. Tutorial: `spin aka cron create "*/5 * * * *" "/" "cron-job-1"`. | Use the option form (§4.17, §6.21) |
| Deleting an app | Command reference: `spin aka app delete`. Account guide: `spin aka delete app --app-name graphql --account-name X-ABC-DEF-extended-default`. | Use `spin aka app delete` (§6.20) |
| Linking a workspace | Command reference: `spin aka app link`, with no top-level `link` in any version. Link guide and both tips on the logs page: `spin aka link`. | Use `spin aka app link` (§6.22) |
| Manifest path option | Command reference: `-f, --from <PATH>`. Variables guide: "`spin aka deploy` can point to a `spin.toml` file by using the `--file` option." | Use `-f` / `--from` (§6.23) |
| Deploy target selection | Link guide: once linked, `spin aka deploy` targets the application "without needing to pass `--app-name` each time." Command reference: `deploy` has `--app-id` and `--create-name` but no `--app-name` in any version shown. | Use a linked workspace or `--app-id` (§6.26) |
| Spin install script | Quickstart: `https://developer.fermyon.com/downloads/fwf_install.sh`. CI guide: `https://wasm-functions.fermyon.app/downloads/install.sh`. | Both are documented; use the one matching the context (§4.14) |
| Language support rule | "Require WASI support" versus "anything with WASI or Spin SDK support runs" | TypeScript (SDK without WASI) is documented as working. Prolog (also SDK without WASI) is not documented by any Akamai page (§4.12). |
| Rust handler styles | Quickstart: `#[http_component]` on a synchronous handler. Security tutorial: `#[http_service]` on an `async` handler that awaits `variables::get(...)`. No source states the SDK version for either. | Both are documented; match the macro to the `spin-sdk` version in use (§3.3, §4.11) |
| Rust SDK version for HTTP middleware | Quotas page: HTTP middleware is "Currently only out-of-the-box with Rust SDK >7.0.0," while instance reuse cites "v7.0.0 of the Rust SDK." | Unresolved whether 7.0.0 itself provides middleware (§4.13) |
| Example app URLs | `*.fwf.app` (quickstart, variables, list-and-inspect, logs, KV, Property Manager, quotas, and security pages), `*.aka.fermyon.tech` (cron, MySQL, PostgreSQL, and Supabase tutorials), and `*.aka.akamai.tech` (object-store tutorial) | Use the URL printed by `spin aka deploy` or `spin aka app status` (§4.21) |
| AI inference placement | Comparison page: AI inference "belongs in Akamai Functions," including "AI inference endpoints." Use-cases page: "(inference itself runs outside of functions)." | Do not assume in-runtime inference. Call external inference APIs through `allowed_outbound_hosts` (§4.13, §4.22) |
| EdgeKV | KV page: "EdgeKV is not currently compatible with Akamai Functions." Use-cases page: Functions push data into the EdgeKV admin APIs, write origin-health status to EdgeKV, and reconcile revoked tokens to EdgeKV. | **Inference:** the KV statement concerns the store, while the use cases call EdgeKV's admin APIs. The sources do not reconcile the two (§1.3, §4.22). |
| Other Akamai services | Welcome page: any Akamai CDN, Security, or Cloud service can be used. Comparison page: PostgreSQL is not yet compatible with Linode DBaaS. KV page: the EdgeKV statement above. | Treat the welcome statement as general positioning, and check the specific service (§4.13) |
| KV label | "currently only allows the `"default"` label" versus a code comment that mentions `Kv.open("mylabel")` | Use only `"default"` (§6.9) |

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
| Multi-line commands | The MySQL, PostgreSQL, object-store, and security-tutorial deploy commands, and the MySQL and PostgreSQL `POST` `curl` examples, are split across lines without shell line continuations. The `curl` examples also wrap the URL in `<…>`. | Use `\` continuations or one line, and pass the bare URL (§4.5, §4.6, §4.8, §4.23) |
| GitHub Actions variables step | The `run:` line is over-indented relative to `- name:` | Indent `run:` at the same level as `name:` (§4.18) |
| Property Manager sample | The first line reads `Fimport { AutoRouter } from 'itty-router';` | `import { AutoRouter } from 'itty-router';` (§4.19) |
| Cron interval example | `* */12 * * *` is described as "every 12 hours" | **General knowledge:** use `0 */12 * * *` for once every 12 hours (§4.17) |
| Cron tutorial step 2 | The prose mentions a `/*` path with a `msg=fwf` query, but the command uses `/` and no query | Pass the query in `--path-and-query` when one is needed |
| Go SDK version in build output | The import path is `github.com/spinframework/spin/sdk/go/v2/http`, but the build output shows `github.com/spinframework/spin/sdk/go v0.10.0` being downloaded | **General knowledge:** a `/v2` import path belongs to a v2 module. Treat `v0.10.0` as sample output, not a version requirement (§2.10). |
| Quickstart sample response | The local test output shows `Hello, Fermyon`, which matches none of the template responses (`hello universe`, `Hello, Akamai`, `Hello Akamai!`) | Expect the response your template returns |
| Cron sample log line | The `console.log` template string ends with a stray `"`, and the sample log line's timestamp (2025-04-12) differs from its log date (2025-04-02) | Remove the stray quote, and treat the log output as illustrative |
| Security tutorial TypeScript sample | `handleRequest` has no closing `}` and is never registered as the `fetch` handler | Close the function and register it (labeled illustration in §3.1; §4.23) |
| Security tutorial expected output | The prose expects "Hello, verified caller", while both samples return `Hello, verified caller!` | Expect the string the code returns (§4.23) |
| Security tutorial secret | The secret is "A 64-character (32 byte) hexadecimal string", but both samples use the string's bytes as the HMAC key without hex-decoding it | The sources do not say how the Advanced Metadata `<key>` interprets the value; keep the property and the Function consistent (§4.23) |
| Logs page usage command | `spin aka app status --app-name hello-akamai-functions -–usage-since 3d` uses an en dash in `-–usage-since` | Use `--usage-since` (§4.15) |
| Logs page usage section | States that `spin aka app status` "prints all log messages to `stdout`" above sample status output | The command reports application information, including invocation counts (§4.10) |
| Property Manager tutorial steps | Two consecutive steps are numbered 6 | Follow the steps in order (§4.19) |
| Sign-up page tip | The "Create a trial account" link has an empty target | Use the page's "Create an Akamai Functions trial account" section (§4.21) |
| Delete guide | Links "team account" to `manage-accounts#request-a-team-account`, a heading the rewritten account guide no longer has | See §4.21 for team-account requests |
| Cron tutorial delete output | The output shows the deleted schedule as `'_/5 _ \* \* \*'` | The schedule created in the tutorial is `*/5 * * * *` (§4.17) |

### Source Coverage

This table accounts for every active entry in `docs/reference-manifest.json`. `Included` rows name substantive subsections that incorporate the source's unique reference facts. `Excluded` is reserved for a source that contains no source-specific Akamai Functions API, constraint, operational fact, or working code pattern.

| Active exact source | Status | Compiled coverage or exclusion reason |
|---|---|---|
| [aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md) | Included | §1.1 platform, runtime, and triggers; §1.6 updates, deletion, and accounts; §1.7 cron jobs; §1.8 language and toolchain constraints; §1.9 CLI and authentication constraints; §4.3 application variables; §4.10 logging; §4.14 project setup, local development, and builds; §4.15 CLI command reference (plugin v1.0.0); §4.16 CLI differences in older plugin versions; §4.17 cron CLI; §4.18 deployment, updates, and CI; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §4.23 securing a Function: request signing and origin protection; §5.4 CLI context and lifecycle interactions; §5.6 source conflicts and sample defects; §6.14 local-time cron expression; §6.20 non-canonical delete app ordering; §6.21 cron positional syntax; §6.22 spin aka link instead of spin aka app link; §6.23 --file instead of -f, --from; §6.26 spin aka deploy --app-name |
| [akamai-functions-and-edgeworkers-comparison.md](../_source/techdocs-akamai-com/akamai-functions-and-edgeworkers-comparison.md) | Included | §1.1 platform, runtime, and triggers; §1.2 execution, request, and deployment quotas; §1.3 key-value store; §1.4 outbound networking and databases; §4.5 mySQL; §4.6 postgreSQL; §4.12 webAssembly language support; §4.13 spin feature support and other platform interfaces; §4.21 platform and operational reference; §4.22 akamai Functions, EdgeWorkers, and workload placement; §5.5 cross-platform and data-service interactions; §5.6 source conflicts and sample defects |
| [application-logs.md](../_source/techdocs-akamai-com/application-logs.md) | Included | §1.2 execution, request, and deployment quotas; §1.9 CLI and authentication constraints; §3.1 javaScript/TypeScript fetch event; §3.3 rust HTTP handlers; §3.4 go HTTP handler; §4.10 logging; §4.15 CLI command reference (plugin v1.0.0); §4.21 platform and operational reference; §5.1 API and event-handler availability matrix; §5.4 CLI context and lifecycle interactions; §5.6 source conflicts and sample defects; §6.18 logs fetched from the wrong app; §6.22 spin aka link instead of spin aka app link |
| [build-a-supabase-cache-proxy.md](../_source/techdocs-akamai-com/build-a-supabase-cache-proxy.md) | Included | §1.3 key-value store; §1.4 outbound networking and databases; §1.5 application variables and deployment versions; §2.1 router and HTTP helpers; §2.2 application variables; §2.3 key-value store; §2.7 supabase; §2.8 S3-compatible object storage and Web API globals; §2.11 package installation by integration; §3.1 javaScript/TypeScript fetch event; §3.2 per-request context and configuration checks; §4.2 javaScript/TypeScript HTTP and routing APIs; §4.3 application variables; §4.4 key-value store; §4.7 supabase client; §4.10 logging; §4.14 project setup, local development, and builds; §4.21 platform and operational reference; §5.1 API and event-handler availability matrix; §5.2 object/method interactions; §5.3 required manifest/deployment capability by API; §5.6 source conflicts and sample defects; §6.4 missing component variable mapping; §6.5 request body not decoded before JSON parsing; §6.6 missing outbound host capability; §6.9 wrong KV label; §6.11 optional Supabase match without a null check; §6.13 KV list cache not invalidated; §6.25 application variables imported from the KV package |
| [delete-an-application.md](../_source/techdocs-akamai-com/delete-an-application.md) | Included | §1.6 updates, deletion, and accounts; §4.15 CLI command reference (plugin v1.0.0); §4.18 deployment, updates, and CI; §4.21 platform and operational reference; §5.4 CLI context and lifecycle interactions; §5.6 source conflicts and sample defects |
| [deploy-app-variables.md](../_source/techdocs-akamai-com/deploy-app-variables.md) | Included | §1.2 execution, request, and deployment quotas; §1.5 application variables and deployment versions; §4.3 application variables; §4.18 deployment, updates, and CI; §4.21 platform and operational reference; §4.23 securing a Function: request signing and origin protection; §5.3 required manifest/deployment capability by API; §5.4 CLI context and lifecycle interactions; §5.6 source conflicts and sample defects; §6.16 treating a variable change as a hot swap or omitting update inputs; §6.23 --file instead of -f, --from |
| [deploy-using-github-actions.md](../_source/techdocs-akamai-com/deploy-using-github-actions.md) | Included | §1.1 platform, runtime, and triggers; §1.2 execution, request, and deployment quotas; §1.8 language and toolchain constraints; §1.9 CLI and authentication constraints; §4.3 application variables; §4.11 rust and Go HTTP APIs; §4.14 project setup, local development, and builds; §4.18 deployment, updates, and CI; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §5.3 required manifest/deployment capability by API; §5.4 CLI context and lifecycle interactions; §5.6 source conflicts and sample defects |
| [faq.md](../_source/techdocs-akamai-com/faq.md) | Included | §1.1 platform, runtime, and triggers; §1.2 execution, request, and deployment quotas; §1.6 updates, deletion, and accounts; §1.9 CLI and authentication constraints; §4.19 property Manager integration; §4.21 platform and operational reference; §5.4 CLI context and lifecycle interactions; §5.6 source conflicts and sample defects |
| [http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md) | Included | §1.1 platform, runtime, and triggers; §3.1 javaScript/TypeScript fetch event; §4.1 HTTP trigger manifest and injected headers; §4.13 spin feature support and other platform interfaces; §5.1 API and event-handler availability matrix; §5.2 object/method interactions; §5.3 required manifest/deployment capability by API; §6.1 unsupported trigger type |
| [integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md) | Included | §1.1 platform, runtime, and triggers; §1.9 CLI and authentication constraints; §1.10 property Manager integration; §2.1 router and HTTP helpers; §2.11 package installation by integration; §3.1 javaScript/TypeScript fetch event; §4.1 HTTP trigger manifest and injected headers; §4.14 project setup, local development, and builds; §4.19 property Manager integration; §4.21 platform and operational reference; §4.23 securing a Function: request signing and origin protection; §5.5 cross-platform and data-service interactions; §5.6 source conflicts and sample defects; §6.2 missing JavaScript fetch registration; §6.19 global Request Number header name with the Functions origin type |
| [link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md) | Included | §1.6 updates, deletion, and accounts; §4.15 CLI command reference (plugin v1.0.0); §4.18 deployment, updates, and CI; §4.21 platform and operational reference; §5.4 CLI context and lifecycle interactions; §5.6 source conflicts and sample defects; §6.18 logs fetched from the wrong app; §6.22 spin aka link instead of spin aka app link; §6.26 spin aka deploy --app-name |
| [list-and-inspect-your-applications.md](../_source/techdocs-akamai-com/list-and-inspect-your-applications.md) | Included | §4.15 CLI command reference (plugin v1.0.0); §4.18 deployment, updates, and CI; §4.19 property Manager integration; §4.21 platform and operational reference; §5.4 CLI context and lifecycle interactions; §5.6 source conflicts and sample defects |
| [manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md) | Included | §1.1 platform, runtime, and triggers; §1.2 execution, request, and deployment quotas; §1.6 updates, deletion, and accounts; §1.9 CLI and authentication constraints; §4.10 logging; §4.14 project setup, local development, and builds; §4.15 CLI command reference (plugin v1.0.0); §4.16 CLI differences in older plugin versions; §4.17 cron CLI; §4.18 deployment, updates, and CI; §4.19 property Manager integration; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §5.4 CLI context and lifecycle interactions; §5.6 source conflicts and sample defects; §6.20 non-canonical delete app ordering; §6.27 production deployment to the default personal account; §6.28 deleting a Function with a personal access token |
| [query-relational-databases-mysql.md](../_source/techdocs-akamai-com/query-relational-databases-mysql.md) | Included | §1.4 outbound networking and databases; §1.5 application variables and deployment versions; §1.8 language and toolchain constraints; §2.1 router and HTTP helpers; §2.2 application variables; §2.4 mySQL; §2.6 UUID; §2.8 S3-compatible object storage and Web API globals; §2.11 package installation by integration; §3.1 javaScript/TypeScript fetch event; §3.2 per-request context and configuration checks; §4.2 javaScript/TypeScript HTTP and routing APIs; §4.3 application variables; §4.5 mySQL; §4.9 UUID; §4.14 project setup, local development, and builds; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §5.1 API and event-handler availability matrix; §5.2 object/method interactions; §5.3 required manifest/deployment capability by API; §5.5 cross-platform and data-service interactions; §5.6 source conflicts and sample defects; §6.3 spin SDK package not installed or imported; §6.5 request body not decoded before JSON parsing; §6.6 missing outbound host capability; §6.7 wrong database protocol or missing port; §6.12 missing required configuration; §6.25 application variables imported from the KV package |
| [query-relational-databases-postgresql.md](../_source/techdocs-akamai-com/query-relational-databases-postgresql.md) | Included | §1.4 outbound networking and databases; §1.5 application variables and deployment versions; §2.1 router and HTTP helpers; §2.2 application variables; §2.5 postgreSQL; §2.6 UUID; §2.8 S3-compatible object storage and Web API globals; §2.11 package installation by integration; §3.1 javaScript/TypeScript fetch event; §3.2 per-request context and configuration checks; §4.2 javaScript/TypeScript HTTP and routing APIs; §4.3 application variables; §4.6 postgreSQL; §4.9 UUID; §4.14 project setup, local development, and builds; §4.21 platform and operational reference; §5.1 API and event-handler availability matrix; §5.2 object/method interactions; §5.3 required manifest/deployment capability by API; §5.5 cross-platform and data-service interactions; §5.6 source conflicts and sample defects; §6.3 spin SDK package not installed or imported; §6.4 missing component variable mapping; §6.7 wrong database protocol or missing port |
| [quickstart.md](../_source/techdocs-akamai-com/quickstart.md) | Included | §1.1 platform, runtime, and triggers; §1.6 updates, deletion, and accounts; §1.8 language and toolchain constraints; §1.9 CLI and authentication constraints; §1.10 property Manager integration; §2.1 router and HTTP helpers; §2.8 S3-compatible object storage and Web API globals; §2.9 rust; §2.10 go; §2.11 package installation by integration; §3.1 javaScript/TypeScript fetch event; §3.3 rust HTTP handlers; §3.4 go HTTP handler; §4.1 HTTP trigger manifest and injected headers; §4.2 javaScript/TypeScript HTTP and routing APIs; §4.10 logging; §4.11 rust and Go HTTP APIs; §4.12 webAssembly language support; §4.14 project setup, local development, and builds; §4.15 CLI command reference (plugin v1.0.0); §4.18 deployment, updates, and CI; §4.19 property Manager integration; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §5.1 API and event-handler availability matrix; §5.2 object/method interactions; §5.3 required manifest/deployment capability by API; §5.4 CLI context and lifecycle interactions; §5.6 source conflicts and sample defects; §6.2 missing JavaScript fetch registration; §6.24 requested path differs from the registered route; §6.27 production deployment to the default personal account |
| [quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md) | Included | §1.1 platform, runtime, and triggers; §1.2 execution, request, and deployment quotas; §1.3 key-value store; §1.4 outbound networking and databases; §1.5 application variables and deployment versions; §1.6 updates, deletion, and accounts; §1.7 cron jobs; §1.8 language and toolchain constraints; §1.9 CLI and authentication constraints; §1.10 property Manager integration; §2.8 S3-compatible object storage and Web API globals; §2.10 go; §3.1 javaScript/TypeScript fetch event; §3.3 rust HTTP handlers; §3.5 cron invocation of an HTTP route; §4.1 HTTP trigger manifest and injected headers; §4.3 application variables; §4.4 key-value store; §4.7 supabase client; §4.8 S3-compatible object storage; §4.10 logging; §4.12 webAssembly language support; §4.13 spin feature support and other platform interfaces; §4.14 project setup, local development, and builds; §4.15 CLI command reference (plugin v1.0.0); §4.17 cron CLI; §4.18 deployment, updates, and CI; §4.19 property Manager integration; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §4.22 akamai Functions, EdgeWorkers, and workload placement; §4.23 securing a Function: request signing and origin protection; §5.3 required manifest/deployment capability by API; §5.4 CLI context and lifecycle interactions; §5.5 cross-platform and data-service interactions; §5.6 source conflicts and sample defects; §6.1 unsupported trigger type; §6.8 function-to-Function calls through the CDN; §6.10 atomic KV or EdgeKV used for the managed store; §6.28 deleting a Function with a personal access token |
| [related-standards.md](../_source/techdocs-akamai-com/related-standards.md) | Excluded | A curated list of external WebAssembly, WASI, Component Model, Wagi, and Spin Improvement Proposal links. It defines no Akamai Functions API, constraint, operational fact, or working code pattern. |
| [schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md) | Included | §1.1 platform, runtime, and triggers; §1.6 updates, deletion, and accounts; §1.7 cron jobs; §2.1 router and HTTP helpers; §2.8 S3-compatible object storage and Web API globals; §2.11 package installation by integration; §3.1 javaScript/TypeScript fetch event; §3.5 cron invocation of an HTTP route; §4.2 javaScript/TypeScript HTTP and routing APIs; §4.10 logging; §4.13 spin feature support and other platform interfaces; §4.14 project setup, local development, and builds; §4.17 cron CLI; §4.18 deployment, updates, and CI; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §4.22 akamai Functions, EdgeWorkers, and workload placement; §5.1 API and event-handler availability matrix; §5.2 object/method interactions; §5.3 required manifest/deployment capability by API; §5.4 CLI context and lifecycle interactions; §5.5 cross-platform and data-service interactions; §5.6 source conflicts and sample defects; §6.1 unsupported trigger type; §6.14 local-time cron expression; §6.15 duplicate cron schedule and path; §6.21 cron positional syntax |
| [secure-an-akamai-function.md](../_source/techdocs-akamai-com/secure-an-akamai-function.md) | Included | §1.4 outbound networking and databases; §1.5 application variables and deployment versions; §1.8 language and toolchain constraints; §1.10 property Manager integration; §2.2 application variables; §2.8 S3-compatible object storage and Web API globals; §2.9 rust; §2.11 package installation by integration; §3.1 javaScript/TypeScript fetch event; §3.2 per-request context and configuration checks; §3.3 rust HTTP handlers; §4.1 HTTP trigger manifest and injected headers; §4.2 javaScript/TypeScript HTTP and routing APIs; §4.3 application variables; §4.11 rust and Go HTTP APIs; §4.12 webAssembly language support; §4.13 spin feature support and other platform interfaces; §4.14 project setup, local development, and builds; §4.18 deployment, updates, and CI; §4.19 property Manager integration; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §4.23 securing a Function: request signing and origin protection; §5.5 cross-platform and data-service interactions; §5.6 source conflicts and sample defects |
| [sign-up-for-akamai-functions.md](../_source/techdocs-akamai-com/sign-up-for-akamai-functions.md) | Included | §1.1 platform, runtime, and triggers; §4.18 deployment, updates, and CI; §4.21 platform and operational reference; §5.6 source conflicts and sample defects |
| [stream-data-from-linode-object-store.md](../_source/techdocs-akamai-com/stream-data-from-linode-object-store.md) | Included | §1.4 outbound networking and databases; §1.5 application variables and deployment versions; §1.8 language and toolchain constraints; §2.1 router and HTTP helpers; §2.2 application variables; §2.8 S3-compatible object storage and Web API globals; §2.11 package installation by integration; §3.1 javaScript/TypeScript fetch event; §3.2 per-request context and configuration checks; §4.1 HTTP trigger manifest and injected headers; §4.2 javaScript/TypeScript HTTP and routing APIs; §4.3 application variables; §4.8 S3-compatible object storage; §4.14 project setup, local development, and builds; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §5.1 API and event-handler availability matrix; §5.2 object/method interactions; §5.3 required manifest/deployment capability by API; §5.6 source conflicts and sample defects; §6.4 missing component variable mapping; §6.6 missing outbound host capability; §6.12 missing required configuration; §6.24 requested path differs from the registered route |
| [update-an-application.md](../_source/techdocs-akamai-com/update-an-application.md) | Included | §1.5 application variables and deployment versions; §1.6 updates, deletion, and accounts; §4.3 application variables; §4.18 deployment, updates, and CI; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §5.4 CLI context and lifecycle interactions; §6.16 treating a variable change as a hot swap or omitting update inputs; §6.17 assuming canary or blue-green version routing |
| [use-cases.md](../_source/techdocs-akamai-com/use-cases.md) | Included | §1.1 platform, runtime, and triggers; §1.3 key-value store; §4.13 spin feature support and other platform interfaces; §4.22 akamai Functions, EdgeWorkers, and workload placement; §5.5 cross-platform and data-service interactions; §5.6 source conflicts and sample defects; §6.10 atomic KV or EdgeKV used for the managed store |
| [use-the-key-value-store.md](../_source/techdocs-akamai-com/use-the-key-value-store.md) | Included | §1.1 platform, runtime, and triggers; §1.3 key-value store; §2.1 router and HTTP helpers; §2.3 key-value store; §2.8 S3-compatible object storage and Web API globals; §2.11 package installation by integration; §3.1 javaScript/TypeScript fetch event; §4.2 javaScript/TypeScript HTTP and routing APIs; §4.4 key-value store; §4.13 spin feature support and other platform interfaces; §4.14 project setup, local development, and builds; §4.20 version and compatibility ledger; §4.21 platform and operational reference; §4.22 akamai Functions, EdgeWorkers, and workload placement; §5.1 API and event-handler availability matrix; §5.2 object/method interactions; §5.3 required manifest/deployment capability by API; §5.5 cross-platform and data-service interactions; §5.6 source conflicts and sample defects; §6.3 spin SDK package not installed or imported; §6.5 request body not decoded before JSON parsing; §6.9 wrong KV label; §6.10 atomic KV or EdgeKV used for the managed store |
| [webassembly-language-support-matrix.md](../_source/techdocs-akamai-com/webassembly-language-support-matrix.md) | Included | §1.1 platform, runtime, and triggers; §4.12 webAssembly language support; §4.20 version and compatibility ledger; §5.6 source conflicts and sample defects |
| [welcome.md](../_source/techdocs-akamai-com/welcome.md) | Included | §1.1 platform, runtime, and triggers; §4.12 webAssembly language support; §4.13 spin feature support and other platform interfaces; §4.19 property Manager integration; §4.21 platform and operational reference; §5.5 cross-platform and data-service interactions; §5.6 source conflicts and sample defects |

## 6. Known Failure Patterns

Each pattern is supported by the sources. When a source does not state the exact error, the entry says so.

### 6.1 Unsupported trigger type

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/http-trigger-reference.md](../_source/techdocs-akamai-com/http-trigger-reference.md), [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md)

```text
WRONG: a component reached through a Redis trigger or a custom trigger.
```

```toml
# CORRECT — the http trigger, the trigger type Akamai Functions "currently supports".
[[trigger.http]]
route = "/..."                # the route that the trigger matches
component = "my-application"  # the name of the component to handle this route
```

**Documented consequence:** Redis and custom triggers are listed as not supported. The quotas page lists cron as "Partial support" (Tech Preview); scheduled work uses `spin aka cron` jobs that call an HTTP route (§1.7, §3.5). The sources do not state the error for an unsupported trigger.

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

### 6.8 Function-to-Function calls through the CDN

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md)

```javascript
// SLOWER — function B calls function A through its public URL; the request is routed via the nearest
// Akamai CDN edge node and back into Akamai Cloud.
let result = await fetch("https://FUNC-A.fwf.app/endpoint?param=val");

// RECOMMENDED — when the code can be components of one Function, use local service chaining.
let result = await fetch("https://COMPONENT-Y.spin.internal/endpoint?param=val");
```

**Documented consequence:** calling function A from inside function B "can lead to degraded performance": even when both are likely deployed in the same cloud cluster, the call takes "an added round trip of latency via the CDN." A local service chaining call "stays within the same WebAssembly execution context, never leaving the local server," and local service chaining "is a recommended best practice within Akamai Functions when using multiple components." A call to a different Function still uses its public URL, and the target must be granted in `allowed_outbound_hosts` (§1.4).
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

**Documented consequence:** Akamai Functions "currently only allows" the `"default"` label, which signals the platform to provision the store automatically. The error for another label is not stated. The tutorial comment's `Kv.open("mylabel")` therefore does not apply on Akamai Functions.

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

### 6.19 Global Request Number header name with the Functions origin type

**Sources:** [docs/_source/techdocs-akamai-com/integrate-with-property-manager.md](../_source/techdocs-akamai-com/integrate-with-property-manager.md)

```text
AVOID (Origin Type = Functions, Global Request Number passed with custom metadata):
  a header name other than AKA_GRN_HEADER

RECOMMENDED:
  header name AKA_GRN_HEADER
```

**Documented consequence:** selecting Functions as the Origin Type automatically adds the Global Request Number behavior to the property, and the tutorial says that when you pass the Global Request Number with custom metadata you "should use `AKA_GRN_HEADER` as the header name to prevent duplication." The form the duplication takes is not described. Selecting Functions is "not required ... but it is highly recommended" (§1.10, §4.19).
### 6.20 Non-canonical `delete app` ordering

**Sources:** [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# SOURCE DISCREPANCY — shown by the account guide.
spin aka delete app --app-name graphql --account-name X-ABC-DEF-extended-default

# CANONICAL — matches the dedicated command reference.
spin aka app delete --app-name graphql --account-name X-ABC-DEF-extended-default
```

**Documented consequence:** the command reference has no top-level `delete` command, so the first form matches no documented signature. The CLI's response to it is not documented.

### 6.21 Cron positional syntax

**Sources:** [docs/_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md](../_source/techdocs-akamai-com/schedule-tasks-with-cron-jobs-in-spin.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# TUTORIAL FORM
spin aka cron create "*/5 * * * *" "/" "cron-job-1"

# CANONICAL COMMAND-REFERENCE FORM (v1.0.0 options)
spin aka cron create --schedule "*/5 * * * *" --path-and-query "/" --name cron-job-1
```

**Documented consequence:** the two forms conflict. The command reference makes `--schedule` required and exposes the path and name as `--path-and-query` and `--name`. The CLI's response to the positional form is not reproduced.

### 6.22 `spin aka link` instead of `spin aka app link`

**Sources:** [docs/_source/techdocs-akamai-com/link-an-application.md](../_source/techdocs-akamai-com/link-an-application.md), [docs/_source/techdocs-akamai-com/application-logs.md](../_source/techdocs-akamai-com/application-logs.md), [docs/_source/techdocs-akamai-com/aka-command-reference.md](../_source/techdocs-akamai-com/aka-command-reference.md)

```shell
# SOURCE DISCREPANCY — shown by the link guide and in both tips on the logs page.
spin aka link

# CANONICAL — the dedicated command reference.
spin aka app link
spin aka app link --app-name <app-name>
```

**Documented consequence:** no version of the command reference lists a top-level `link` command (v1.0.0 top-level commands: `app`, `cron`, `deploy`, `logs`, `auth`, `login`, `send-feedback`, `info`, `help`). The CLI's response to `spin aka link` is not documented.

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
### 6.27 Production deployment to the default personal account

**Sources:** [docs/_source/techdocs-akamai-com/quickstart.md](../_source/techdocs-akamai-com/quickstart.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md)

```shell
# DEFAULT — deploys to your personal account.
spin aka deploy

# PRODUCTION — deploy to a team account (illustration of the documented --account-name option).
spin aka deploy --account-name <team-account-name>
```

**Documented consequence:** by default, `spin aka deploy` deploys the Function to the personal account, and the quickstart says: "For production use, you need to deploy the Function in a Team Account by for example passing `--account-name` to the command." The account guide says the personal account "should not be used for production workloads" and that personal accounts "support lower limits and fewer requests per month," while team accounts get "the full limits and request counts specified in your contract." No enforcement or error is described (§4.18, §4.21).
### 6.28 Deleting a Function with a personal access token

**Sources:** [docs/_source/techdocs-akamai-com/quotas-and-limits.md](../_source/techdocs-akamai-com/quotas-and-limits.md), [docs/_source/techdocs-akamai-com/manage-accounts.md](../_source/techdocs-akamai-com/manage-accounts.md)

```shell
# NOT PERMITTED — a session authenticated with a personal access token cannot delete a deployed Function.
spin aka login --token <PAT>
spin aka app delete --app-name <app-name>

# USE — delete from an interactive login (illustration composed from documented commands).
spin aka login
spin aka app delete --app-name <app-name>
```

**Documented consequence:** Personal Access Tokens "cannot: Delete a deployed Function" or "Manage (create/update/delete/…) Personal Access Tokens" (quotas page), and PATs can manage applications in all team accounts that the user can access "(though they cannot delete them)" (account guide). The error returned is not stated (§1.6, §4.18).
