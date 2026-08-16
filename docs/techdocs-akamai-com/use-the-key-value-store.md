# Source: https://techdocs.akamai.com/akamai-functions/docs/use-the-key-value-store
Date: 2026-08-16T09:25:47.585878
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use the `wasi:keyvalue/atomic` interface; it is not supported.
- Do not attempt to share a key‑value store between multiple Spin applications; stores are scoped to a single application.
- Do not exceed the default key‑value query rate limits (limits can be raised per‑customer request).
- Do not use any store label other than `"default"`; Akamai Functions only provisions the default label.
- Do not rely on EdgeKV for persistence; the Akamai Functions key‑value store is a separate, incompatible capability.
- When running locally, the store persists only in the SQLite file `.spin/sqlite_key_value.db` located in the workspace’s `.spin` directory.

## Supported APIs and Syntax
- `openDefault()` — Opens the provisioned key‑value store with the `"default"` label. Returns a `KvStore` instance.  
- `KvStore.exists(key: string): boolean` — Returns `true` if the given key exists in the store.  
- `KvStore.getJson<T>(key: string): T` — Retrieves and parses JSON data stored at the given key.  
- `KvStore.setJson(key: string, value: any): void` — Serializes `value` to JSON and stores it at the given key.  
- `KvStore.open(label: string): KvStore` — Opens a store with a custom label (use only if a non‑default label is provisioned).  
- `new TextDecoder()` — Standard Web API for decoding `ArrayBuffer` payloads.  
- `new Response(body?: BodyInit, init?: ResponseInit)` — Constructs an HTTP response.  
- `AutoRouter()` (from `itty-router`) — Creates a router instance.  
- `router.get(path: string, handler: (request: RequestInfo) => Response | Promise<Response>)` — Registers a GET handler.  
- `router.post(path: string, handler: (request: RequestInfo) => Response | Promise<Response>)` — Registers a POST handler.  
- `router.fetch(request: Request): Promise<Response>` — Handles an incoming request via the router.  
- `addEventListener('fetch', (event: FetchEvent) => void)` — Registers the entry point for incoming HTTP requests.

## Required Patterns
**Pattern: Router Setup & Event Listener**
```js
import { AutoRouter } from 'itty-router';
const router = AutoRouter();

addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

**Pattern: GET /get/:key Handler**
```js
function handleGetValue(key) {
  const store = openDefault();               // open default KV store
  if (!store.exists(key)) {
    return new Response(null, { status: 404 });
  }
  const data = store.getJson(key);
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: { "content-type": "application/json" },
  });
}
router.get("/get/:key", ({ key }) => handleGetValue(key));
```

**Pattern: POST /set/:key Handler**
```js
const decoder = new TextDecoder();

async function handleSetValue(key, requestBody) {
  const payload = JSON.parse(decoder.decode(requestBody));
  if (!payload || !payload.firstName || !payload.lastName) {
    return new Response(
      "Invalid payload received.\nExpecting {\"firstName\": \"some\", \"lastName\": \"some\"}",
      { status: 400 }
    );
  }
  const store = openDefault();               // open default KV store
  store.setJson(key, payload);
  return new Response(null, { status: 200 });
}
router.post("/set/:key", async (req) =>
  handleSetValue(req.params.key, await req.arrayBuffer())
);
```

## Common Mistakes and Gotchas
- **Unlike** standard Node.js or browser environments, **Akamai Functions** does **not** support the `wasi:keyvalue/atomic` interface; attempts to use atomic operations will fail.
- **Unlike** typical multi‑tenant key‑value services, **Akamai Functions** stores are **isolated per application**; you cannot access another app’s store.
- **Unlike** EdgeKV, **Akamai Functions** provides its own globally replicated store; using EdgeKV APIs will not work.
- **Unlike** a fresh local run, **Akamai Functions** automatically provisions a persistent store; you must declare the `"default"` label in `spin.toml` or the store will not be created.
- **Unlike** a regular file system, the local test store persists only in `.spin/sqlite_key_value.db`; deleting this file clears all stored data.

## Version and Compatibility Notes
- The key‑value store capability is **separate** from EdgeKV and is **not** compatible with EdgeKV APIs.
- Only the `"default"` store label is currently provisioned automatically; custom labels require explicit provisioning (not covered in this tutorial).
- The `@spinframework/spin-kv` package must be installed (`npm install @spinframework/spin-kv`) to access the KV APIs.
- The tutorial assumes the **http‑js** Spin template; other templates may require different router setup.