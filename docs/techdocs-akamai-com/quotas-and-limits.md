# Source: https://techdocs.akamai.com/akamai-functions/docs/quotas-and-limits
Date: 2026-06-30T09:38:41.143122
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not allocate more than **128 MiB** of RAM per function execution.  
- Do not exceed an **app bundle size** of **50 MiB**.  
- Do not let a request handler run longer than **30 seconds**.  
- Do not send or receive request/response bodies larger than **10 MiB**.  
- Do not store more than **2 GB** total in Functions KV across all store instances.  
- Do not issue more than **1,000 read requests per second (RPS)** to KV storage per app.  
- Do not issue more than **50 write requests per second (RPS)** to KV storage per app.  
- Do not write KV values larger than **1 MiB**.  
- Do not use KV keys larger than **8 KB**.  
- Do not reference `localhost` or short service names; always use the full public URL of another Spin app (e.g., `https://<app-id>.fwf.app`).  
- Do not rely on runtime configuration; it is not supported.  
- Do not use custom triggers; they are not supported.  
- Do not use the Redis trigger; it is not supported.  
- Do not use SQLite storage; it is not supported.  
- Do not use `wasi-blobstore` or `wasi-messaging`; both are not supported.  
- Do not assume full Serverless AI access; only limited access is provided.  
- Use Spin CLI **v0.6.0 or newer**.  

## Required Patterns

**Pattern: Calling another Spin application**  
```js
// Use the full public URL of the target Spin app
const response = await fetch('https://<target-app-id>.fwf.app/endpoint', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ key: 'value' })
});
const data = await response.json();
```

**Pattern: Using Functions KV (wasi:keyvalue/store)**  
```js
import { store } from 'wasi:keyvalue/store';

// Write a value (max 1 MiB, key max 8 KB)
await store.set('my-key', new Uint8Array(Buffer.from('my value')));

// Read a value
const value = await store.get('my-key');
if (value) {
  const text = Buffer.from(value).toString();
  console.log('KV value:', text);
}
```

**Pattern: Batch KV operations (wasi:keyvalue/batch)**  
```js
import { batch } from 'wasi:keyvalue/batch';

// Example batch get
const keys = ['key1', 'key2', 'key3'];
const results = await batch.get(keys);
results.forEach((val, i) => {
  if (val) console.log(`${keys[i]} => ${Buffer.from(val).toString()}`);
});
```

**Pattern: Accessing configuration variables**  
```js
// Configuration variables are exposed as environment variables
const dbHost = process.env.DB_HOST;   // Example variable set in the Spin config
```

## Common Mistakes and Gotchas
- Unlike standard Node.js, **Akamai Functions does not allow `localhost`** for inter‑service calls; you must use the full public URL.  
- Unlike typical serverless platforms, **runtime configuration (dynamic env var changes) is not supported**.  
- Unlike Docker/Kubernetes, **short service names cannot be used** to reach other Spin apps.  
- Unlike full Spin, **custom triggers are not supported**.  
- Unlike some serverless runtimes, **Redis trigger support is missing**.  
- Unlike local development, **SQLite storage is unavailable**.  
- Unlike generic WASI, **`wasi-blobstore` and `wasi-messaging` interfaces are not supported**.  

## Version and Compatibility Notes
- Akamai Functions requires **Spin CLI v0.6.0 or newer**.  
- `wasi-config` support is available starting with the **2024‑09‑27 snapshot**.  
- `wasi:keyvalue/store` and `wasi:keyvalue/batch` interfaces are supported starting with the **2024‑10‑17 snapshot**.  
- Limits listed under “Quota app limits” and “Functions KV quota limits” are **subject to change** during public preview; contact your Akamai representative for higher limits.  
- Cron job scheduling is in **Tech Preview** and may have additional constraints.  