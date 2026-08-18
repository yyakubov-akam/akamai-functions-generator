## Runtime Constraints
- Do not allocate more than **128 MiB** of RAM per function execution.  
- Do not exceed an **app bundle size** of **50 MiB**.  
- Do not let the request handler run longer than **30 seconds**.  
- Do not send or receive a request/response larger than **10 MiB**.  
- Do not store more than **2 GB** total across all KV store instances.  
- Do not issue more than **1,000 KV read requests per second** per app.  
- Do not issue more than **50 KV write requests per second** per app.  
- Do not store a KV **value larger than 1 MiB**.  
- Do not use a KV **key larger than 8 KB**.  
- Do not reference `localhost` or short service names when calling another Spin app; always use the full public URL (`https://<app-id>.fwf.app`).  
- Do not rely on runtime configuration; it is not supported.  
- Do not use Spin triggers that are listed as **Not supported** (Redis trigger, SQLite storage, Custom Triggers, wasi‑blobstore, wasi‑messaging).  
- Do not use Spin features that are unavailable in the current preview (e.g., full Serverless AI access; only limited access is provided).  
- Use **Spin CLI v0.6.0 or newer**; older versions are unsupported.  

## Supported APIs and Syntax
- `http.outbound(request)` — Send an outbound HTTP request from the function.  
- `variables.get(name)` / `variables.set(name, value)` — Access Application Variables.  
- `kv.get(key)` — Retrieve a value from the Key‑Value store.  
- `kv.set(key, value)` — Store a value in the Key‑Value store.  
- `kv.delete(key)` — Remove a key from the Key‑Value store.  
- `kv.batch(operations[])` — Perform a batch of KV operations (supported via `wasi:keyvalue/batch`).  
- `serviceChain.call(url, request)` — Invoke another Spin application via full public URL (service chaining).  
- `mysql.query(sql, params?)` — Execute a MySQL query.  
- `postgresql.query(sql, params?)` — Execute a PostgreSQL query.  
- `redis.outbound.command(command, args[])` — Send a command to an external Redis instance (Outbound Redis).  
- `wasi-config.get(key)` — Retrieve a configuration value via the `wasi-config` snapshot (2024‑09‑27).  
- `wasi-keyvalue/store.get(key)` — Get a value using the `wasi:keyvalue/store` interface (2024‑10‑17 snapshot).  
- `wasi-keyvalue/batch.apply(operations[])` — Apply a batch of KV operations using the `wasi:keyvalue/batch` interface (2024‑10‑17 snapshot).  

## Required Patterns
### 1. Calling another Spin app (service chaining)
```javascript
import { http } from 'spin-sdk';

export async function handler(request) {
  const targetUrl = 'https://<app-id>.fwf.app/endpoint';
  const resp = await http.outbound({
    method: 'GET',
    url: targetUrl,
    headers: request.headers,
  });
  return resp;
}
```

### 2. Using the KV store within limits
```javascript
import { kv } from 'spin-sdk';

export async function handler(request) {
  const key = 'user:12345';
  const value = JSON.stringify({ name: 'Alice' });

  // Ensure key < 8 KB and value < 1 MiB
  if (new TextEncoder().encode(key).length > 8 * 1024) throw new Error('Key too large');
  if (new TextEncoder().encode(value).length > 1 * 1024 * 1024) throw new Error('Value too large');

  await kv.set(key, value);          // Write (≤ 50 RPS per app)
  const stored = await kv.get(key);   // Read (≤ 1 000 RPS per app)
  return new Response(stored);
}
```

### 3. Outbound HTTP with size guard
```javascript
import { http } from 'spin-sdk';

export async function handler(request) {
  const resp = await http.outbound({
    method: 'POST',
    url: 'https://api.example.com/ingest',
    body: request.body,               // Must be ≤ 10 MiB total request size
    headers: { 'Content-Type': 'application/json' },
  });

  // Guard response size
  const respBody = await resp.text();
  if (new TextEncoder().encode(respBody).length > 10 * 1024 * 1024) {
    throw new Error('Response exceeds 10 MiB limit');
  }
  return new Response(respBody, { status: resp.status });
}
```

## Common Mistakes and Gotchas
- **Unlike standard Node.js**, Akamai Functions **cannot** resolve `localhost` or short hostnames; use the full public URL.  
- **Unlike typical serverless platforms**, Akamai Functions **enforces a hard 128 MiB RAM limit** per execution.  
- **Unlike regular SQLite libraries**, the **SQLite storage API is not supported** on Akamai Functions.  
- **Unlike generic Spin environments**, **Redis triggers** are **not supported**; only outbound Redis commands are available.  
- **Unlike typical environment variable access**, **Application Variables** must be accessed via the `variables` API, not `process.env`.  
- **Unlike standard WASI runtimes**, **wasi‑blobstore** and **wasi‑messaging** are unavailable.  
- **Unlike a fully featured Serverless AI service**, only **limited access** is provided; attempts to use unsupported AI endpoints will fail.  
- **Unlike dynamic configuration in other runtimes**, **runtime configuration** cannot be changed at execution time.  

## Version and Compatibility Notes
- Requires **Spin CLI ≥ v0.6.0**.  
- `wasi-config` support is tied to the **2024‑09‑27 snapshot**; earlier snapshots lack this API.  
- `wasi-keyvalue` (`store` and `batch` interfaces) are available starting with the **2024‑10‑17 snapshot**.  
- Serverless AI is in **Limited Access** mode; full feature set may be gated behind future releases.  
- Cron‑job scheduling is **Tech Preview** only; production use should treat it as experimental.  