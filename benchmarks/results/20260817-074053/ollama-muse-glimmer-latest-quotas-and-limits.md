## Runtime Constraints

- Maximum RAM allocated per function execution is 128 MiB
- Maximum App Size is 50 MiB
- Maximum request handler duration is 30 seconds
- Maximum request/response size is 10 MiB
- Maximum KV storage across all store instances is 2 GB
- Maximum KV value size is 1 MB
- Maximum KV key size is 8 KB
- Maximum KV read requests per app is 1,000 RPS
- Maximum KV write requests per app is 50 RPS
- Do not use Redis trigger
- Do not use SQLite Storage
- Do not use wasi-blobstore
- Do not use wasi-messaging
- Do not use Custom Triggers
- Do not use local hostnames such as localhost or short service names to communicate between Spin applications
- Do not use Runtime configuration
- Do not use Serverless AI without limited access approval
- Limits are subject to change during public preview

## Required Patterns

### Inter-App Call Pattern
```text
Use full public URL for inter-app calls
https://<app-id>.fwf.app
```

## Common Mistakes and Gotchas

- Unlike standard Docker Compose or Kubernetes where local hostnames can be used for inter-service communication, Akamai Functions requires full public URL for inter-app calls
- Unlike standard Spin where Runtime configuration is supported, Akamai Functions does not support runtime configuration at this time
- Unlike standard Spin where Redis trigger is available, Akamai Functions does not support Redis trigger
- Unlike standard Spin where SQLite Storage is available, Akamai Functions does not support SQLite Storage
- Unlike standard Spin where wasi-blobstore is available, Akamai Functions does not support wasi-blobstore
- Unlike standard Spin where wasi-messaging is available, Akamai Functions does not support wasi-messaging
- Unlike standard Spin where Custom Triggers are available, Akamai Functions does not support Custom Triggers

## Version and Compatibility Notes

- Akamai Functions supports Spin CLI v0.6.0 or newer
- Some Spin SDK triggers and APIs are not yet supported on Akamai Functions
- wasi-config is supported as of 2024-09-27 snapshot
- wasi:keyvalue/store and wasi:keyvalue/batch interfaces are supported as of 2024-10-17 snapshot
- Cron jobs and Schedule tasks with cron jobs in Spin are currently in Tech Preview
- Quota app limits are subject to change as part of public preview