---
updatedAt: 2026-11-09T20:54:19.000Z
agentTools:
  siteIndex: https://techdocs.akamai.com/llms.txt
  projectIndex: https://techdocs.akamai.com/akamai-functions/llms.txt
---

# Quotas and limits

Keep these limitations in mind when designing your [Spin](https://spinframework.dev/) applications to run on Akamai Functions. You can also refer to the [FAQ](https://techdocs.akamai.com/akamai-functions/docs/faq) section to learn more about Akamai Functions.

# Resource tier limits

These limitations are unique for each Akamai Functions resource tier. There are currently two resource tiers available, Standard and Extended. Standard is intended for more lightweight use cases, while Extended allows more computationally intensive applications.

| Description          | Standard         | Extended          |
| :------------------- | :--------------- | :---------------- |
| Maximum CPU time     | 500 milliseconds | 1000 milliseconds |
| Maximum memory usage | 20 MiB           | 128 MiB           |
| Maximum wall time    | 15 seconds       | 30 seconds        |

These limits can be increased to custom values. Reach out to your Akamai representative for more information

The rest of the limits on this page apply to all Functions regardless of their resource tier.

# Request limits

These limits apply to each request handled by a Function, as well as outbound subrequests made from within a Function, for example, using the JavaScript `fetch()` API.

| Description                    | Value  |
| :----------------------------- | :----- |
| Maximum request URI size       | 16 KiB |
| Maximum request body size      | 10 MiB |
| Maximum request headers count  | 64     |
| Maximum request headers size   | 32 KiB |
| Maximum response body size     | 10 MiB |
| Maximum response headers count | 64     |
| Maximum response headers size  | 32 KiB |

Outbound subrequests are further limited to 10000 requests per minute per deployed Akamai Function.

> 📘
>
> These limits can be increased to custom values if needed. Reach out to your Akamai representative to inquire about options.

By default, connection pooling for subrequests is disabled. This creates a new connection for each subrequest, which can potentially impact performance. You can enable connection pooling on a per-Function basis if needed. Reach out to your Akamai representative for more information.

> 📘
>
> The maximum request and response body sizes do not apply when streaming the body through an Akamai Function. In that case, there is no directly enforced limit besides related limits such as total memory usage.

Akamai Functions strips out the following request headers and request header prefixes before a request is handled by your code:

* `x-request-id`
* `x-forwarded-for`
* `x-real-ip`
* `x-forwarded-client-cert`
* `akamai-*` (except `akamai-Bot` and `akamai-GRN`)
* `x-envoy-*`
* `fermyon-*`
* `x-akamai-*`

Akamai Functions does not directly enforce specific limits on request rates per second (RPS) or minute (RPM). This is because the expected performance can vary significantly depending on factors such as chosen programming language, computational complexity of the use case, and the use of outbound connections. Internal load test results range anywhere between thousands (complex, resource intensive) to several millions (simple, fully optimized) of RPS per region. Below you can find some high-level guidance on what to expect.

* Functions are deployed across 25+ regions. The more geographically distributed your audience, the better Functions will scale.
* Use Rust if you need optimal performance. JavaScript and especially Python tend to scale worse due to their interpreted nature (sometimes two or three times worse than Rust depending on use case).
* For some use cases, the new [Instance Reuse](https://spinframework.dev/v4/http-trigger#controlling-instance-reuse) feature can have a strong positive impact on maximum RPS.
* Outbound connections (including Functions KV store reads/writes) can have a strong negative impact on maximum RPS.
* We do not recommend running your own (high scale) load tests without involvement from your Account team. There are many different limits that can come into play, both for Functions itself but also for the CDN you choose to front the Function with. Additionally, Functions has strong fairness restrictions in place which prevent a single app from taking up too many resources without manual overrides.

If you require additional information, need to make sure the platform can support your intended traffic numbers, want to run your own load tests, or get manual limit overrides in place, reach out to your Akamai representative.

# Function quota limits

[block:parameters]
{
  "data": {
    "h-0": "Description",
    "h-1": "Value",
    "0-0": "Maximum function bundle size",
    "0-1": "128 MiB  \nCannot currently be increased",
    "1-0": "Maximum amount of deployed functions per account",
    "1-1": "50",
    "2-0": "Maximum amount of versions per deployed function",
    "2-1": "2147483647",
    "3-0": "Maximum amount of function deploys per account per hour",
    "3-1": "20  \nCannot currently be increased",
    "4-0": "Maximum size of a single [Spin application variable](https://techdocs.akamai.com/akamai-functions/docs/deploy-app-variables)",
    "4-1": "1024 bytes",
    "5-0": "Maximum size of all [Spin application variables](https://techdocs.akamai.com/akamai-functions/docs/deploy-app-variables) combined",
    "5-1": "4096 bytes"
  },
  "cols": 2,
  "rows": 6,
  "align": [
    "left",
    "left"
  ]
}
[/block]

To get the total Function bundle size from Spin before deploying you can use the [Spin dashboard project](https://github.com/radu-matei/dash) to view the the size of each individual component in the Akamai Function. The total bundle size is the sum of the component sizes. This project can also show you other information, such as how much memory your Akamai Function is using during local execution.

# Account quota limits

As explained in [Manage  accounts](https://techdocs.akamai.com/akamai-functions/docs/manage-accounts), Akamai Functions has its own account system that uses Akamai Control Center as an identity provider to let you log in with your Akamai credentials.

There are currently no limits on the maximum number of Akamai Functions users or team accounts per Akamai Control Center contract. There is also no limit on the maximum number of users per team account or maximum team accounts a user can join.

# Spin aka plugin quota limits

The `spin aka` plugin internally calls the Akamai Functions’ administrative API, which is rate limited. Additionally, some commands have their own limitations.

[block:parameters]
{
  "data": {
    "h-0": "Description",
    "h-1": "Value",
    "0-0": "Maximum API calls per minute per user",
    "0-1": "50",
    "1-0": "Maximum days for historical data retrieval",
    "1-1": "7",
    "2-0": "Maximum logged-in session duration",
    "2-1": "15 days",
    "3-0": "Maximum amount of Personal Access Tokens `spin aka auth`",
    "3-1": "100",
    "4-0": "Maximum lifetime for Personal Access Tokens `spin aka auth`",
    "4-1": "90 days  \n`spin aka auth regenerate` currently does not reset this",
    "5-0": "Extra limitations on `spin aka logs`",
    "5-1": "See [Logging quote limits](https://techdocs.akamai.com/akamai-functions/docs/quotas-and-limits#logging-quota-limits) below"
  },
  "cols": 2,
  "rows": 6,
  "align": [
    "left",
    "left"
  ]
}
[/block]

Personal Access Tokens generated with `spin aka auth` for automation purposes have largely the same rights and capabilities as the user who created them, but cannot:

* Delete a deployed Function
* Manage (create/update/delete/…) Personal Access Tokens

# Logging quota limits

As described in [Application logs and usage](https://techdocs.akamai.com/akamai-functions/docs/application-logs), Akamai Functions automatically captures stdout and stderr logs from your Akamai Functions and makes them available via `spin aka logs`.

These logs are intended to help you debug an application during development and should not be used as a full, production-level observability system. This is also reflected in the conservative logs limits.

[block:parameters]
{
  "data": {
    "h-0": "Description",
    "h-1": "Value",
    "0-0": "Maximum log line size  \nOnce the maximum size is reached any additional logs are silently dropped.",
    "0-1": "1 MiB",
    "1-0": "Maximum total logs emitted per Function invocation  \nOnce the maximum size is reached any additional logs are dropped after a warning.",
    "1-1": "10 MiB",
    "2-0": "Maximum amount of calls to `spin aka logs` per minute",
    "2-1": "5",
    "3-0": "Maximum time period for log retrieval",
    "3-1": "60 days"
  },
  "cols": 2,
  "rows": 4,
  "align": [
    "left",
    "left"
  ]
}
[/block]

# Functions cron quota limits (Tech preview)

The Akamai Functions [cron system for scheduling tasks](https://techdocs.akamai.com/akamai-functions/docs/schedule-tasks-with-cron-jobs-in-spin) using `spin aka cron` is currently still in a tech preview phase and is not subject to the same expectations of stability as the rest of the platform.

For example, crons are not 100% guaranteed to run, nor are they guaranteed to run at exactly the scheduled time. Additionally, crons are limited in number.

| Description                                                                  | Value |
| :--------------------------------------------------------------------------- | :---- |
| Maximum amount of configured crons per account across all deployed Functions | 10    |

# Functions KV quota limits (Limited availability)

The Akamai Functions [Key Value store](https://techdocs.akamai.com/akamai-functions/docs/use-the-key-value-store) is currently in **Limited Availability** and is not subject to the same expectations of scalability as the rest of the platform. Additionally, the Functions KV backends are not deployed to the same level of geographical distribution as the rest of the platform, so there can be higher latencies when using it from certain regions.

This Limited Availability status is also reflected in the limits.

| Description                            | Value |
| :------------------------------------- | :---- |
| Read requests per second per Function  | 1000  |
| Write requests per second per Function | 50    |
| Maximum value size                     | 1 KiB |
| Maximum key size                       | 1 KiB |

If these limits are not sufficient for your use case and you need a production-level KV store you can request a limit increase at an additional cost. Reach out to your Akamai representative for more information.

The Spin WASI Key Value interface is also compatible with other KeyValue stores, such as (self-hosted) Redis or the [Akamai ValKey Managed Database](https://techdocs.akamai.com/cloud-computing/docs/aiven-valkey).

# Spin limits

Akamai Functions supports Spin CLI v4.0.0 or newer. Older Spin versions may work (especially for existing Functions projects), but are not guaranteed to. Some Spin SDK triggers and APIs are not yet supported on Akamai Functions.

To view the feature support for various programming languages, go to the [Spin Language Support Guide](https://spinframework.dev/language-support-overview).

[block:parameters]
{
  "data": {
    "h-0": "Spin feature",
    "h-1": "Akamai Functions support",
    "0-0": "**Triggers**",
    "0-1": "",
    "1-0": "[HTTP](https://spinframework.dev/http-trigger)",
    "1-1": "Supported",
    "2-0": "[Cron](https://techdocs.akamai.com/akamai-functions/docs/schedule-tasks-with-cron-jobs-in-spin)",
    "2-1": "Partial support  \nTech Preview, see above",
    "3-0": "[Redis](https://spinframework.dev/redis-trigger)",
    "3-1": "Not supported",
    "4-0": "[Custom Triggers](https://spinframework.dev/extending-and-embedding)",
    "4-1": "Not supported",
    "5-0": "**APIs**",
    "5-1": "",
    "6-0": "[Outbound HTTP](https://spinframework.dev/rust-components#sending-outbound-http-requests)",
    "6-1": "Supported",
    "7-0": "[Application Variables](https://spinframework.dev/variables)",
    "7-1": "Supported",
    "8-0": "[Key Value Storage](https://spinframework.dev/kv-store-api-guide)",
    "8-1": "Supported",
    "9-0": "[SQLite Storage](https://spinframework.dev/sqlite-api-guide)",
    "9-1": "Not supported",
    "10-0": "[Service Chaining](https://spinframework.dev/http-outbound#local-service-chaining)",
    "10-1": "Supported",
    "11-0": "[MySQL](https://spinframework.dev/rdbms-storage#using-mysql-and-postgresql-from-applications)",
    "11-1": "Supported",
    "12-0": "[PostgreSQL](https://spinframework.dev/rdbms-storage#using-mysql-and-postgresql-from-applications)",
    "12-1": "Supported",
    "13-0": "[Outbound Redis](https://spinframework.dev/rust-components#storing-data-in-redis-from-rust-components)",
    "13-1": "Supported",
    "14-0": "**Features**",
    "14-1": "",
    "15-0": "[Component dependencies](https://spinframework.dev/writing-apps#using-component-dependencies)",
    "15-1": "Supported since Spin v4.0.0",
    "16-0": "[WASM Garbage collection](https://bytecodealliance.org/articles/wasmtime-gc)",
    "16-1": "Supported since Spin v4.2.0 and enabled by default  \nFor languages that use WasmGC, such as Kotlin, Scala or Dart",
    "17-0": "[HTTP Middleware](https://spinframework.dev/http-trigger#http-middleware)",
    "17-1": "Supported since Spin v4.1.0  \nCurrently only out-of-the-box with [Rust SDK >7.0.0](https://docs.rs/spin-sdk/7.0.0/spin_sdk/macro.dependencies.html)",
    "18-0": "[Instance Reuse](https://spinframework.dev/v4/http-trigger#controlling-instance-reuse)",
    "18-1": "Supported since Spin v4.0.0  \nAutomatically enabled  \nRequires up-to-date Wasi-p3 compatible SDKs, such as [v7.0.0 of the Rust SDK](https://crates.io/crates/spin-sdk), v4.0 for the Go SDK or v5.0 of the Python SDK. Not yet supported for JavaScript.",
    "19-0": "[Connection pooling](https://spinframework.dev/v4/dynamic-configuration#outbound-http-runtime-configuration)",
    "19-1": "Supported since Spin v3.4.0 but not enabled by default.  \nContact your Akamai representative to inquire about enablement."
  },
  "cols": 2,
  "rows": 20,
  "align": [
    "left",
    "left"
  ]
}
[/block]

Akamai Functions is committed to always running a supported version of the underlying wasmtime engine and to downstream security patches as soon as possible. In practice, this means we keep the platform updated to one of the two latest versions of wasmtime and the related Spin releases.

# Platform limits

Due to the way Akamai Functions are currently deployed as a distributed setup in Akamai Cloud behind the `fwf.app` CDN property, calling function A from inside of function B can lead to degraded performance.

For example, if function B at FUNC-B.fwf.app executes the following JavaScript code, the platform will route the request starting from the Akamai Cloud into FUNC-A.fwf.app via the nearest Akamai CDN edge node, before coming back into the Akamai Cloud to call function A’s actual endpoint.

```javascript
let result = await fetch("https://FUNC-A.fwf.app/endpoint?param=val");
```

Even though function A and B are likely deployed in the same cloud cluster, they cannot immediately access each other’s endpoints without an added round trip of latency via the CDN.

This is explicitly NOT the case for the [Local Service Chaining](https://spinframework.dev/http-outbound#local-service-chaining) feature, where components within the same Function can call each other over an HTTP abstraction. In those cases, the outbound call to `COMPONENT.spin.internal` is abstracted out completely and the endpoint invocation stays within the same WebAssembly execution context, never leaving the local server.

For example, if Function C consists of component X and component Y, the following request inside component X would be fully optimized and call the correct endpoint handler within Y directly. Local service chaining is a recommended best practice within Akamai Functions when using multiple components.

```javascript
let result = await fetch("https://COMPONENT-Y.spin.internal/endpoint?param=val");
```