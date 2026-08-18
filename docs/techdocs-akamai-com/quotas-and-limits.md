# Source: https://techdocs.akamai.com/akamai-functions/docs/quotas-and-limits
Date: 2026-08-17T08:37:42.959879
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Do not exceed 128 MiB of memory per function execution
- Do not exceed 50 MiB of total app size
- Do not exceed 30 seconds for request handler duration
- Do not exceed 10 MiB for request/response size
- Do not exceed 2 GB total KV Storage across all store instances
- Do not exceed 1,000 RPS for KV Read requests
- Do not exceed 50 RPS for KV Write requests
- Do not exceed 1 MB for KV value size
- Do not exceed 8 KB for KV key size

## Supported APIs and Syntax

- `HTTP` — Supported trigger for handling incoming requests
- `Outbound HTTP` — Supported API for sending outbound HTTP requests
- `Application Variables` — Supported API for managing application variables
- `Key Value Storage` — Supported API for storing and retrieving key-value pairs
- `MySQL` — Supported API for connecting to MySQL databases
- `PostgreSQL` — Supported API for connecting to PostgreSQL databases
- `Outbound Redis` — Supported API for connecting to Redis
- `wasi-config` — Supported interface (requires 2024-09-27 snapshot)
- `wasi-keyvalue` — Supported interfaces: `wasi:keyvalue/store` and `wasi:keyvalue/batch` (requires 2024-10-17 snapshot)
- `Component dependencies` — Supported feature for managing component dependencies

## Required Patterns

```javascript
// Service Chaining Pattern
// Unlike local environments, use the full public URL for inter-app communication
const response = await fetch('https://<app-id>.fwf.app', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data: 'payload' })
});
```

## Common Mistakes and Gotchas

- Unlike Docker Compose or Kubernetes, Akamai Functions does not support local hostnames such as `localhost` or short service names; use full public URLs (e.g., `https://<app-id>.fwf.app`) to communicate between applications
- Unlike standard Node.js environments, Akamai Functions does not support Runtime configuration at this time
- Unlike standard environments, Akamai Functions does not support Custom Triggers

## Version and Compatibility Notes

- Spin CLI version must be v0.6.0 or newer
- Serverless AI is available but under Limited Access
- Cron jobs are currently in Tech Preview
- SQLite Storage is not supported
- Redis Trigger is not supported
- wasi-blobstore and wasi-messaging are not supported in Spin or Akamai Functions