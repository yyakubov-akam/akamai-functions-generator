---
updatedAt: 2026-07-23T21:47:23.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Quotas and limits

Keep these limitations in mind when designing your [Spin](https://spinframework.dev/) applications. You can also refer to the [FAQ](https://techdocs.akamai.com/akamai-functions/docs/faq) section to learn more about Akamai Functions.

# Quota app limits

Limits are subject to change as part of public preview. If you’re interested in higher limits, please contact your Akamai representative for assistance.

| Description                                   | Default limit |
| :-------------------------------------------- | :------------ |
| Memory (RAM allocated per function execution) | 128 MiB       |
| App Size                                      | 50 MiB        |
| Request handler duration                      | 30 seconds    |
| Request/response size                         | 10 MiB        |

# Functions KV quota limits

| Description                             | Default limit |
| :-------------------------------------- | :------------ |
| KV Storage (across all store instances) | 2 GB          |
| Read requests supported per app         | 1,000 RPS     |
| Write requests supported per app        | 50 RPS        |
| Maximum value size                      | 1 MB          |
| Maximum key size                        | 8 KB          |

# Spin limits

Akamai Functions supports Spin CLI v0.6.0 or newer. Some Spin SDK triggers and APIs are not yet supported on Akamai Functions.

To view the feature support for various programming languages, visit the [Spin Language Support Guide](https://spinframework.dev/v3/language-support-overview).

| Spin feature                                                                                              | Akamai Functions support                                                                             |
| :-------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| **Triggers**                                                                                              |                                                                                                      |
| [HTTP](https://spinframework.dev/v3/http-trigger)                                                         | Supported                                                                                            |
| [Redis](https://spinframework.dev/v3/redis-trigger)                                                       | Not supported                                                                                        |
| **APIs**                                                                                                  |                                                                                                      |
| [Outbound HTTP](https://spinframework.dev/v3/rust-components#sending-outbound-http-requests)              | Supported                                                                                            |
| [Application Variables](https://spinframework.dev/v3/variables)                                           | Supported                                                                                            |
| [Key Value Storage](https://spinframework.dev/v3/kv-store-api-guide)                                      | Supported                                                                                            |
| [SQLite Storage](https://spinframework.dev/v3/sqlite-api-guide)                                           | Not supported                                                                                        |
| [Serverless AI](https://spinframework.dev/v3/serverless-ai-api-guide)                                     | [Limited Access](https://fibsu0jcu2g.typeform.com/to/dOFZ338a?typeform-source=developer.fermyon.com) |
| [Service Chaining](https://spinframework.dev/v3/http-outbound#local-service-chaining)                     | Supported                                                                                            |
| [MySQL](https://spinframework.dev/v3/rdbms-storage#using-mysql-and-postgresql-from-applications)          | Supported                                                                                            |
| [PostgreSQL](https://spinframework.dev/v3/rdbms-storage#using-mysql-and-postgresql-from-applications)     | Supported                                                                                            |
| [Outbound Redis](https://spinframework.dev/v3/rust-components#storing-data-in-redis-from-rust-components) | Supported                                                                                            |
| [wasi-blobstore](https://github.com/WebAssembly/wasi-blobstore)                                           | Not supported in Spin, Not supported in Akamai Functions                                             |
| [wasi-config](https://github.com/WebAssembly/wasi-config)                                                 | Supported (2024-09-27 snapshot)                                                                      |
| [wasi-keyvalue](https://github.com/WebAssembly/wasi-keyvalue)                                             | `wasi:keyvalue/store` and `wasi:keyvalue/batch` interfaces supported (2024-10-17 snapshot)           |
| [wasi-messaging]()                                                                                        | Not supported in Spin, Not supported in Akamai Functions                                             |
| **Features**                                                                                              |                                                                                                      |
| [Component dependencies](https://spinframework.dev/v3/writing-apps#using-component-dependencies)          | Supported                                                                                            |
| **Extensibility**                                                                                         |                                                                                                      |
| [Custom Triggers](https://spinframework.dev/v3/extending-and-embedding)                                   | Not supported                                                                                        |

# Other limits

You cannot use local hostnames such as `localhost` or short service names, as you might in Docker Compose or Kubernetes, to communicate between Spin applications. To call another Spin application, use its full public URL instead, for example,`https://<app-id>.fwf.app`.

[Runtime configuration](https://spinframework.dev/v3/dynamic-configuration#runtime-configuration) is not supported at this time.

Support for Cron jobs and the ability to [Schedule tasks with cron jobs in Spin](https://techdocs.akamai.com/akamai-functions/docs/schedule-tasks-with-cron-jobs-in-spin) is currently in Tech Preview.