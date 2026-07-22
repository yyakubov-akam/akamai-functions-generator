# Source: https://techdocs.akamai.com/akamai-functions/docs/quotas-and-limits
Date: 2026-07-22T11:12:26.778775
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not allocate more than **128 MiB** of RAM per function execution.  
- Do not exceed an **app bundle size** of **50 MiB**.  
- Do not let a request handler run longer than **30 seconds**.  
- Do not send or receive a request/response larger than **10 MiB**.  
- Do not store more than **2 GB** total in Functions KV across all stores.  
- Do not issue more than **1,000 KV read requests per second** per app.  
- Do not issue more than **50 KV write requests per second** per app.  
- Do not write a KV value larger than **1 MiB**.  
- Do not use a KV key larger than **8 KB**.  
- Do not reference **`localhost`** or any short service name when calling another Spin app; always use the full public URL (`https://<app-id>.fwf.app`).  
- Do not rely on **runtime configuration** – it is not supported.  
- Do not create **custom triggers** – they are not supported.  
- Do not use **Redis trigger**, **SQLite storage**, **wasi‑blobstore**, **wasi‑messaging**, or any **Spin‑only** features that are listed as “Not supported”.  
- Do not assume full access to **Serverless AI** – only limited access is available.  

## Supported APIs and Syntax
| API / Interface | Signature / Identifier | Description |
|---|---|---|
| `HTTP` trigger | `http.handle(request, response)` | Handles inbound HTTP requests. |
| Outbound HTTP | `fetch(url, options)` | Perform HTTP requests to external services. |
| Configuration Variables | `process.env.VAR_NAME` | Access environment‑style configuration values. |
| Key‑Value Storage | `kv.get(key)`, `kv.put(key, value)` | Read/write to Functions KV store. |
| `wasi-config` | `wasi:config/get(name)` | Retrieve configuration via WASI config snapshot (2024‑09‑27). |
| `wasi:keyvalue/store` | `wasi:keyvalue/store.get(key)`, `wasi:keyvalue/store.put(key, value)` | KV store interface (2024‑10‑17 snapshot). |
| `wasi:keyvalue/batch` | `wasi:keyvalue/batch.getMany(keys)`, `wasi:keyvalue/batch.putMany(pairs)` | Batch KV operations (2024‑10‑17 snapshot). |
| Service Chaining | `service.chain(targetUrl, request)` | Forward a request to another Spin app. |
| MySQL | `mysql.connect(config)`, `connection.query(sql, params)` | Interact with a MySQL database. |
| PostgreSQL | `pg.connect(config)`, `client.query(sql, params)` | Interact with a PostgreSQL database. |
| Outbound Redis | `redis.connect(options)`, `client.get(key)`, `client.set(key, value)` | Communicate with external Redis instances. |
| Serverless AI (Limited) | `ai.invoke(model, payload)` | Call AI models with limited capabilities. |
| Component dependencies | `import { … } from 'component'` | Use declared component libraries. |

*(Only the method names and signatures explicitly mentioned in the source are listed; do not invent additional APIs.)*

## Required Patterns
### 1. HTTP Request Handler (max 30 s)
```js
export async function handle(request, response) {
  // your logic here – must finish within 30 seconds
}
```

### 2. Calling Another Spin Application
```js
const targetUrl = 'https://<app-id>.fwf.app/path';
const res = await fetch(targetUrl, { method: 'POST', body: JSON.stringify(data) });
```

### 3. KV Read / Write (respecting size limits)
```js
// Write (value ≤ 1 MiB, key ≤ 8 KB)
await kv.put('myKey', Buffer.from('value'));

// Read
const value = await kv.get('myKey');
```

### 4. Batch KV Operations (snapshot‑supported interfaces)
```js
// Batch get
const values = await wasi:keyvalue/batch.getMany(['key1', 'key2']);

// Batch put
await wasi:keyvalue/batch.putMany([
  ['key1', Buffer.from('val1')],
  ['key2', Buffer.from('val2')]
]);
```

### 5. Outbound HTTP Call (respecting 10 MiB request/response limit)
```js
const resp = await fetch('https://api.example.com/data', {
  method: 'GET',
  // optional: headers, body (≤10 MiB)
});
const data = await resp.json(); // response body ≤10 MiB
```

## Common Mistakes and Gotchas
- **Unlike standard Node.js**, Akamai Functions **does not allow `localhost`** or short service names for inter‑app communication. Use the full public URL.  
- **Unlike typical serverless platforms**, **runtime configuration** (e.g., dynamic env var changes) **is not supported**.  
- **Unlike a full Spin environment**, **custom triggers** and the **Redis trigger** are **not supported**.  
- **Unlike local development**, **SQLite storage** is unavailable; attempts to import or use it will fail.  
- **Unlike generic WASI runtimes**, only **`wasi-config` (2024‑09‑27 snapshot)** and **`wasi:keyvalue/*` (2024‑10‑17 snapshot)** are supported; other WASI modules are rejected.  
- **Unlike unrestricted HTTP servers**, request handlers **must complete within 30 seconds** or will be terminated.  
- **Unlike unlimited KV stores**, the **total KV size is capped at 2 GB** and **individual keys/values have strict size limits**.  

## Version and Compatibility Notes
- Akamai Functions requires **Spin CLI v0.6.0 or newer**.  
- **`wasi-config`** support is tied to the **2024‑09‑27 snapshot**; earlier snapshots lack this API.  
- **`wasi:keyvalue/store`** and **`wasi:keyvalue/batch`** are available starting with the **2024‑10‑17 snapshot**.  
- Features marked **“Limited Access”** (e.g., Serverless AI) may require additional permissions or a special plan.  
- Cron‑job scheduling is **Tech Preview only**; not guaranteed in production.  