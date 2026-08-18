## Runtime Constraints

- Do not use local hostnames (e.g., `localhost`) or short service names to communicate between Spin applications
- Do not use Redis triggers
- Do not use SQLite Storage
- Do not use wasi-blobstore
- Do not use wasi-messaging
- Do not use Custom Triggers
- Maximum memory (RAM) per function execution is 128 MiB
- Maximum app size is 50 MiB
- Maximum request handler duration is 30 seconds
- Maximum request/response size is 10 MiB
- Maximum KV value size is 1 MB
- Maximum KV key size is 8 KB
- Maximum KV read requests per app is 1,000 RPS
- Maximum KV write requests per app is 50 RPS
- Maximum KV storage (across all store instances) is 2 GB
- Runtime configuration is not supported

## Supported APIs and Syntax

- `wasi-config` — Supported (2024-09-27 snapshot)
- `wasi:keyvalue/store` — Supported (2024-10-17 snapshot)
- `wasi:keyvalue/batch` — Supported (2024-10-17 snapshot)
- HTTP Trigger — Supported
- Outbound HTTP — Supported
- Application Variables — Supported
- Key Value Storage — Supported
- Serverless AI — Limited Access
- Service Chaining — Supported
- MySQL — Supported
- PostgreSQL — Supported
- Outbound Redis — Supported
- Component dependencies — Supported

## Required Patterns

```javascript
// Service Chaining Pattern
// To call another Spin application, use its full public URL
const response = await fetch('https://<app-id>.fwf.app', {
  method: 'POST',
  body: JSON.stringify({ /* data */ })
});
```

## Common Mistakes and Gotchas

- Unlike standard Docker Compose or Kubernetes environments, you cannot use local hostnames such as `localhost` or short service names to communicate between Spin applications. You must use the full public URL (e.g., `https://<app-id>.fwf.app`) instead.
- Unlike standard Node.js or browser JS environments, runtime configuration is not supported at this time.

## Version and Compatibility Notes

- Akamai Functions supports Spin CLI v0.6.0 or newer
- Support for Cron jobs is currently in Tech Preview
- Serverless AI access is limited and requires specific access permissions