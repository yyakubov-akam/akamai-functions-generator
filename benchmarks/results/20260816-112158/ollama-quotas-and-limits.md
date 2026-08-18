## Runtime Constraints
- Do not allocate more than **128 MiB** of RAM per function execution.  
- Do not exceed an **app bundle size** of **50 MiB**.  
- Do not run a request handler longer than **30 seconds**.  
- Do not send or receive a request/response larger than **10 MiB**.  
- Do not store more than **2 GB** total across all KV store instances.  
- Do not issue more than **1,000 KV read requests per second** per app.  
- Do not issue more than **50 KV write requests per second** per app.  
- Do not write a KV value larger than **1 MiB**.  
- Do not use a KV key larger than **8 KB**.  
- Do not reference **`localhost`** or short service names when calling another Spin app; always use the full public URL (`https://<app-id>.fwf.app`).  
- Do not rely on **runtime configuration** (dynamic config) – it is not supported.  
- Do not schedule cron jobs unless you are prepared for **Tech Preview** behavior (limited stability).  
- Do not use Spin triggers or APIs marked **“Not supported”** (e.g., Redis trigger, SQLite storage, custom triggers, wasi‑blobstore, wasi‑messaging).  

## Supported APIs and Syntax
| API / Feature | Signature (as documented) | Description |
|---------------|---------------------------|-------------|
| `spin.trigger.http(request)` | `export async function handle(request: Request): Promise<Response>` | HTTP trigger – entry point for inbound HTTP requests. |
| `spin.outbound.http.fetch(url, options)` | `await fetch(url, options)` | Outbound HTTP requests from the function. |
| `spin.variables.get(name)` | `const value = await spin.variables.get("VAR_NAME")` | Retrieve an application variable. |
| `spin.kv.get(store, key)` | `const value = await spin.kv.get("my-store", "my-key")` | Read a value from a KV store. |
| `spin.kv.set(store, key, value)` | `await spin.kv.set("my-store", "my-key", "my-value")` | Write a value to a KV store. |
| `spin.kv.batch(store, ops[])` | `await spin.kv.batch("my-store", [{ op: "set", key: "...", value: "..." }, …])` | Perform batch KV operations (store and batch interfaces). |
| `spin.service.chain(url, request)` | `await spin.service.chain("https://<app-id>.fwf.app/endpoint", request)` | Local service chaining – forward a request to another Spin app. |
| `spin.mysql.query(connectionString, sql, params?)` | `const rows = await spin.mysql.query("mysql://user:pass@host/db", "SELECT …", [params])` | Execute a MySQL query. |
| `spin.postgresql.query(connectionString, sql, params?)` | `const rows = await spin.postgresql.query("postgres://user:pass@host/db", "SELECT …", [params])` | Execute a PostgreSQL query. |
| `spin.redis.command(connectionString, command, args…)` | `const result = await spin.redis.command("redis://host:6379", "GET", "my-key")` | Outbound Redis command execution. |
| `spin.wasi.config.get(key)` | `const val = await spin.wasi.config.get("my-config-key")` | Retrieve a value from the `wasi-config` snapshot (2024‑09‑27). |
| `spin.wasi.keyvalue.store.get(store, key)` | `const val = await spin.wasi.keyvalue.store.get("my-store", "my-key")` | KV get using the `wasi:keyvalue/store` interface (2024‑10‑17). |
| `spin.wasi.keyvalue.batch.apply(store, ops[])` | `await spin.wasi.keyvalue.batch.apply("my-store", [{ op: "set", key: "...", value: "..." }])` | KV batch using the `wasi:keyvalue/batch` interface (2024‑10‑17). |
| `spin.serverlessAI.invoke(model, payload)` | *Limited access – only available to approved accounts.* | Invoke a server‑less AI model (restricted). |

## Required Patterns
### 1. HTTP Trigger Boilerplate
```javascript
// src/main.js
export async function handle(request) {
  // Your logic here
  return new Response("OK", { status: 200 });
}
```

### 2. Outbound HTTP Request
```javascript
export async function handle(request) {
  const resp = await fetch("https://api.example.com/data", {
    method: "GET",
    headers: { "Accept": "application/json" }
  });
  const data = await resp.json();
  return new Response(JSON.stringify(data), { status: 200 });
}
```

### 3. KV Store Read / Write
```javascript
export async function handle(request) {
  // Write
  await spin.kv.set("my-store", "counter", "1");

  // Read
  const value = await spin.kv.get("my-store", "counter");
  return new Response(`Counter = ${value}`, { status: 200 });
}
```

### 4. KV Batch Operation (store & batch interfaces)
```javascript
export async function handle(request) {
  await spin.wasi.keyvalue.batch.apply("my-store", [
    { op: "set", key: "a", value: "1" },
    { op: "set", key: "b", value: "2" }
  ]);

  const a = await spin.wasi.keyvalue.store.get("my-store", "a");
  const b = await spin.wasi.keyvalue.store.get("my-store", "b");
  return new Response(`a=${a}, b=${b}`, { status: 200 });
}
```

### 5. Service Chaining to Another Spin App
```javascript
export async function handle(request) {
  const chainedResp = await spin.service.chain(
    "https://12345.fwf.app/endpoint",
    request
  );
  return chainedResp; // forward the response
}
```

### 6. MySQL Query Example
```javascript
export async function handle(request) {
  const rows = await spin.mysql.query(
    "mysql://user:pass@db-host/database",
    "SELECT id, name FROM users WHERE active = ?",
    [true]
  );
  return new Response(JSON.stringify(rows), { status: 200 });
}
```

### 7. PostgreSQL Query Example
```javascript
export async function handle(request) {
  const rows = await spin.postgresql.query(
    "postgres://user:pass@db-host/database",
    "SELECT id, email FROM contacts WHERE subscribed = $1",
    [true]
  );
  return new Response(JSON.stringify(rows), { status: 200 });
}
```

### 8. Outbound Redis Command
```javascript
export async function handle(request) {
  const result = await spin.redis.command(
    "redis://redis-host:6379",
    "INCR",
    "page_views"
  );
  return new Response(`Page views = ${result}`, { status: 200 });
}
```

## Common Mistakes and Gotchas
- **Unlike standard Node.js**, Akamai Functions **cannot** use `localhost` or Docker‑style short hostnames to reach other services; you must use the full public URL.  
- **Unlike typical serverless platforms**, the **request handler timeout is hard‑capped at 30 seconds**; long‑running tasks must be off‑loaded.  
- **Unlike generic KV stores**, Akamai Functions **enforce a 1 MiB maximum value size** and an **8 KB maximum key size**.  
- **Unlike a full Spin runtime**, **runtime (dynamic) configuration is not supported**; environment variables must be set at build time.  
- **Unlike local development**, **SQLite storage is not available**; attempts to import or use SQLite APIs will fail.  
- **Unlike other Edge platforms**, **custom triggers and the `wasi-blobstore`/`wasi-messaging` APIs are unavailable**.  
- **Unlike unrestricted outbound networking**, only the **Outbound HTTP, Redis, MySQL, PostgreSQL, and Service Chaining APIs** are permitted; other network protocols are blocked.  

## Version and Compatibility Notes
- Akamai Functions requires **Spin CLI v0.6.0 or newer**.  
- **`wasi-config`** support is based on the **2024‑09‑27 snapshot**.  
- **`wasi-keyvalue`** (`store` and `batch` interfaces) are supported from the **2024‑10‑17 snapshot**.  
- **Serverless AI** is **limited‑access only**; developers must obtain explicit permission via the provided Typeform link.  
- Features marked **“Not supported”** (e.g., Redis trigger, SQLite, custom triggers, `wasi-blobstore`, `wasi-messaging`) are permanently unavailable in the current preview.  
- **Cron job scheduling** is in **Tech Preview** and may change before GA.  