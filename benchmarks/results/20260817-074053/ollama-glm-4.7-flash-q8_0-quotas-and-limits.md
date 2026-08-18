## Runtime Constraints

- Maximum memory (RAM) per function execution is 128 MiB
- Maximum app size is 50 MiB
- Maximum request handler duration is 30 seconds
- Maximum request/response size is 10 MiB
- Maximum KV storage size across all store instances is 2 GB
- Maximum read requests per app is 1,000 RPS
- Maximum write requests per app is 50 RPS
- Maximum KV value size is 1 MB
- Maximum KV key size is 8 KB
- Do not use Redis Trigger
- Do not use SQLite Storage
- Do not use wasi-messaging
- Do not use Custom Triggers
- Do not use Runtime configuration

## Supported APIs and Syntax

*Note: The provided source text lists feature support rather than specific method signatures. The following are the confirmed available features.*

- HTTP Trigger — Supported
- Outbound HTTP — Supported
- Application Variables — Supported
- Key Value Storage — Supported
- Service Chaining — Supported
- MySQL — Supported
- PostgreSQL — Supported
- Outbound Redis — Supported
- wasi-config — Supported (2024-09-27 snapshot)
- wasi-keyvalue — Supported (`wasi:keyvalue/store` and `wasi:keyvalue/batch` interfaces, 2024-10-17 snapshot)
- Component dependencies — Supported

## Required Patterns

**Service Chaining URL Format**
To communicate between Spin applications, use the full public URL instead of local hostnames.

```javascript
// Example URL format for calling another Spin app
const targetUrl = 'https://<app-id>.fwf.app';
```

## Common Mistakes and Gotchas

- Unlike Docker Compose or Kubernetes, you cannot use local hostnames such as `localhost` or short service names to communicate between Spin applications.
- Unlike standard Node.js or browser environments, Serverless AI is currently in Limited Access.
- Unlike standard Node.js or browser environments, Cron jobs and task scheduling are currently in Tech Preview.
- Unlike standard Node.js or browser environments, SQLite Storage is not supported.

## Version and Compatibility Notes

- Requires Spin CLI v0.6.0 or newer
- Serverless AI is in Limited Access
- Cron jobs are in Tech Preview