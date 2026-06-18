# Source: https://techdocs.akamai.com/akamai-functions/docs/quotas-and-limits
Date: 2026-06-05T09:01:07.038290
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not allocate more than **128 MiB** of RAM per function execution.  
- Do not exceed an **app bundle size** of **50 MiB**.  
- Do not let a request handler run longer than **30 seconds**.  
- Do not send or receive a request/response larger than **10 MiB**.  
- Do not store more than **2 GB** total in Functions KV across all store instances.  
- Do not exceed **1,000 read requests per second (RPS)** for KV in a single app.  
- Do not exceed **50 write requests per second (RPS)** for KV in a single app.  
- Do not store a KV value larger than **1 MB**.  
- Do not use a KV key larger than **8 KB**.  
- Do not use `localhost` or short service names to communicate between Spin applications; always use the full public URL (e.g., `https://<app-id>.fwf.app`).  
- Do not rely on runtime configuration; it is not supported.  
- Do not use **custom triggers**; they are not supported.  
- Do not use **Redis trigger**, **SQLite storage**, **wasi-blobstore**, or **wasi-messaging**; they are not supported.  
- Cron‑job scheduling is only available in **Tech Preview**; treat it as optional/experimental.  

## Supported APIs and Syntax
*(No explicit method signatures are documented in the source; supported features are listed in the “Required Patterns” and “Common Mistakes” sections.)*  

## Required Patterns
### Pattern: Calling another Spin application
```js
// Use the full public URL; never use localhost or a short name.
const response = await fetch('https://<app-id>.fwf.app/endpoint', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ key: 'value' })
});
const data = await response.json();
```

### Pattern: Accessing Functions KV (wasi:keyvalue/store)
```js
// Example using the wasi:keyvalue/store interface
import { kv } from 'wasi:keyvalue/store';

await kv.set('myKey', new Uint8Array([1, 2, 3]));   // store up to 1 MiB per value
const value = await kv.get('myKey');              // returns Uint8Array
```

### Pattern: Outbound HTTP request (supported API)
```js
// Simple outbound HTTP GET
const res = await fetch('https://api.example.com/data');
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const json = await res.json();
```

## Common Mistakes and Gotchas
- Unlike standard Node.js, **Akamai Functions does not allow `localhost`** for inter‑service calls; you must use the full public URL.  
- Unlike typical serverless platforms, **runtime configuration variables cannot be set or changed at execution time**.  
- Unlike a full Spin environment, **Redis triggers and SQLite storage are not supported** on Akamai Functions.  
- Unlike generic WASI runtimes, **wasi-blobstore and wasi-messaging interfaces are unavailable**.  
- Unlike local development, **custom triggers cannot be defined**; only the built‑in HTTP trigger is supported.  
- Unlike production‑grade KV services, **KV read/write rates are capped at 1,000 RPS reads and 50 RPS writes per app**.  

## Version and Compatibility Notes
- Akamai Functions requires **Spin CLI v0.6.0 or newer**.  
- `wasi-config` support is available starting with the **2024‑09‑27 snapshot**.  
- `wasi-keyvalue` (`wasi:keyvalue/store` and `wasi:keyvalue/batch`) support is available starting with the **2024‑10‑17 snapshot**.  
- Features marked “Limited Access” (e.g., Serverless AI) may require additional enablement.  
- Cron‑job scheduling is currently in **Tech Preview** and may change.  