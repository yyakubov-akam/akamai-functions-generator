## Runtime Constraints

- Memory per function execution: 128 MiB
- App size: 50 MiB
- Request handler duration: 30 seconds
- Request/response size: 10 MiB
- KV Storage (across all store instances): 2 GB
- Read requests supported per app: 1,000 RPS
- Write requests supported per app: 50 RPS
- Maximum value size: 1 MB
- Maximum key size: 8 KB

## Supported APIs and Syntax

- HTTP Trigger — Supported
- Redis Trigger — Not supported
- Outbound HTTP — Supported
- Application Variables — Supported
- Key Value Storage — Supported
- SQLite Storage — Not supported
- Serverless AI — Limited Access
- Service Chaining — Supported
- MySQL — Supported
- PostgreSQL — Supported
- Outbound Redis — Supported
- wasi-blobstore — Not supported
- wasi-config — Supported (2024-09-27 snapshot)
- wasi-keyvalue — Supported (2024-10-17 snapshot)
- wasi-messaging — Not supported
- Component dependencies — Supported
- Custom Triggers — Not supported

## Required Patterns

```javascript
// Inter-app communication
// Use the full public URL instead of localhost or short service names
const response = await fetch('https://<app-id>.fwf.app');
```

## Common Mistakes and Gotchas

- Unlike Docker Compose or Kubernetes, Akamai Functions does not support local hostnames (`localhost`) or short service names for inter-app communication.
- Unlike standard Node.js environments, Akamai Functions does not support SQLite Storage.
- Unlike standard Node.js environments, Akamai Functions does not support wasi-messaging.

## Version and Compatibility Notes

- Spin CLI v0.6.0 or newer required.
- Serverless AI is in Limited Access.
- Cron jobs are in Tech Preview.
- Runtime configuration is not supported.