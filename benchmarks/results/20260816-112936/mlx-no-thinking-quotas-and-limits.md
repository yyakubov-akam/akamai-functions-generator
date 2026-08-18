## Runtime Constraints

- Maximum memory per function execution is 128 MiB
- Maximum App Size is 50 MiB
- Maximum request handler duration is 30 seconds
- Maximum request/response size is 10 MiB
- Maximum total KV Storage across all store instances is 2 GB
- Maximum KV read requests per app is 1,000 RPS
- Maximum KV write requests per app is 50 RPS
- Maximum KV value size is 1 MB
- Maximum KV key size is 8 KB
- Do not use `localhost` or short service names for inter-app communication
- Do not use SQLite Storage
- Do not use Redis triggers
- Do not use `wasi-blobstore`
- Do not use `wasi-messaging`
- Do not use Runtime configuration

## Supported APIs and Syntax

`HTTP Trigger` — Supported trigger mechanism for applications.
`Outbound HTTP` — Supported method for sending outbound HTTP requests.
`Application Variables` — Supported access to application variables.
`Key Value Storage` — Supported KV store API.
`Service Chaining` — Supported method for calling other services.
`MySQL` — Supported database connectivity.
`PostgreSQL` — Supported database connectivity.
`Outbound Redis` — Supported method for storing data in Redis from components.
`wasi-config` — Supported (2024-09-27 snapshot).
`wasi:keyvalue/store` — Supported interface (2024-10-17 snapshot).
`wasi:keyvalue/batch` — Supported interface (2024-10-17 snapshot).
`Component dependencies` — Supported feature for managing dependencies.

## Required Patterns

**Inter-App Communication**
When calling another Spin application, use the full public URL.
```text
https://<app-id>.fwf.app
```

## Common Mistakes and Gotchas

- Unlike standard Docker Compose or Kubernetes environments, Akamai Functions do not support `localhost` or short service names for inter-app communication; you must use the full public URL.

## Version and Compatibility Notes

- Spin CLI v0.6.0 or newer is required.
- KV storage and trigger support are subject to change as part of public preview.
- Cron jobs and scheduled tasks are currently in Tech Preview.
- Serverless AI access is limited.