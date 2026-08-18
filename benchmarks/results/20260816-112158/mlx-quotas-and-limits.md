## Runtime Constraints

- Maximum memory per function execution is 128 MiB
- Maximum app size is 50 MiB
- Maximum request handler duration is 30 seconds
- Maximum request/response size is 10 MiB
- Maximum total KV storage is 2 GB
- Maximum KV read requests per app is 1,000 RPS
- Maximum KV write requests per app is 50 RPS
- Maximum KV value size is 1 MB
- Maximum KV key size is 8 KB
- Do not use `localhost` or short service names for inter-app communication
- Do not use SQLite storage
- Do not use `wasi-blobstore`
- Do not use `wasi-messaging`
- Do not use custom triggers

## Supported APIs and Syntax

- `HTTP Trigger`: Supported
- `Outbound HTTP`: Supported
- `Application Variables`: Supported
- `Key Value Storage`: Supported
- `Service Chaining`: Supported
- `MySQL`: Supported
- `PostgreSQL`: Supported
- `Outbound Redis`: Supported
- `wasi-config`: Supported (2024-09-27 snapshot)
- `wasi:keyvalue/store`: Supported (2024-10-17 snapshot)
- `wasi:keyvalue/batch`: Supported (2024-10-17 snapshot)

## Common Mistakes and Gotchas

- Unlike Docker Compose or Kubernetes where `localhost` or short service names can be used, Akamai Functions require the use of the full public URL (e.g., `https://<app-id>.fwf.app`) to communicate between Spin applications.
- Unlike standard Spin environments, SQLite storage, `wasi-blobstore`, and `wasi-messaging` are not supported on Akamai Functions.

## Version and Compatibility Notes

- Spin CLI v0.6.0 or newer is required.
- Cron jobs and scheduled tasks are currently in Tech Preview.
- Runtime configuration is not supported.