# Source: https://techdocs.akamai.com/akamai-functions/docs/quotas-and-limits
Date: 2026-08-16T09:24:18.364806
Model: gpt-oss:120b-cloud
## Runtime Constraints

- Do not allocate more than **128 MiB** of RAM per function execution.  
- Do not exceed an **app bundle size** of **50 MiB**.  
- Do not run a request handler longer than **30 seconds**.  
- Do not send or receive request/response bodies larger than **10 MiB**.  
- Do not store more than **2 GB** total in Functions KV across all store instances.  
- Do not issue more than **1,000 KV read requests per second** per app.  
- Do not issue more than **50 KV write requests per second** per app.  
- Do not store KV values larger than **1 MiB**.  
- Do not use KV keys larger than **8 KB**.  
- Do not reference `localhost` or short service names when communicating between Spin applications; always use the full public URL (`https://<app-id>.fwf.app`).  
- Do not rely on runtime configuration; it is not supported.  
- Do not use unsupported triggers such as **Redis** or **Custom Triggers**.  
- Do not use unsupported APIs: **SQLite Storage**, **wasi-blobstore**, **wasi-messaging**.  
- Do not expect full Serverless AI access; only limited access is provided.  
- Use **Spin CLI v0.6.0** or newer; older versions are unsupported.  

## Supported APIs and Syntax

- `fetch(url, options)` — Outbound HTTP request.  
- `process.env.VAR_NAME` — Access Application Variables.  
- `kv.get(key)` — Retrieve a value from Functions KV (wasi:keyvalue/store).  
- `kv.put(key, value)` — Store a value in Functions KV (wasi:keyvalue/store).  
- `kv.batch(operations[])` — Perform batch KV operations (wasi:keyvalue/batch).  
- `wasi:config.get(name)` — Retrieve a configuration value (wasi-config).  
- `mysql.query(sql, params)` — Execute a MySQL query.  
- `postgresql.query(sql, params)` — Execute a PostgreSQL query.  
- `redis.connect(url)` — Outbound Redis connection (supported).  
- `serviceChain.call(serviceName, payload)` — Invoke another service in the chain.  

## Required Patterns

**Pattern: Calling another Spin application**

```javascript
// Use full public URL; never use localhost or short names
const response = await fetch('https://my-app-id.fwf.app/endpoint', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ key: 'value' })
});
const data = await response.json();
```

**Pattern: Using Functions KV (wasi:keyvalue/store)**

```javascript
import { kv } from 'wasi:keyvalue/store';

// Put a value (max 1 MiB)
await kv.put('myKey', Buffer.from('myValue'));

// Get a value
const value = await kv.get('myKey');
if (value) {
  console.log(value.toString());
}
```

**Pattern: Batch KV operations (wasi:keyvalue/batch)**

```javascript
import { kv } from 'wasi:keyvalue/batch';

await kv.batch([
  { type: 'put', key: 'key1', value: Buffer.from('val1') },
  { type: 'delete', key: 'key2' },
  { type: 'get', key: 'key3' }
]);
```

## Common Mistakes and Gotchas

- Unlike standard Docker/Kubernetes environments, Akamai Functions **cannot use `localhost`** or short service names for inter‑app communication.  
- Unlike a full Node.js runtime, Akamai Functions **do not support runtime configuration**; attempts to read dynamic config files will fail.  
- Unlike typical serverless platforms, **Redis triggers are not supported**; only outbound Redis connections work.  
- Unlike local development, **SQLite storage is unavailable**; attempts to open SQLite files will error.  
- Unlike generic WASI runtimes, **wasi-blobstore and wasi-messaging are not supported** in Akamai Functions.  
- Unlike unrestricted KV services, **KV value size is limited to 1 MiB** and **key size to 8 KB**.  

## Version and Compatibility Notes

- Requires **Spin CLI v0.6.0** or newer.  
- `wasi-config` support is available starting with the **2024‑09‑27 snapshot**.  
- `wasi:keyvalue/store` and `wasi:keyvalue/batch` interfaces are available starting with the **2024‑10‑17 snapshot**.  
- Serverless AI is **limited access**; full capabilities may be added in future releases.  
- Cron job scheduling is currently in **Tech Preview**; not guaranteed to be stable.  