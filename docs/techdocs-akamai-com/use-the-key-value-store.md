# Source: https://techdocs.akamai.com/akamai-functions/docs/use-the-key-value-store
Date: 2026-06-30T09:39:56.348360
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use the `wasi:keyvalue/atomic` interface; it is **not supported**.
- Only the `"default"` key‑value store label is allowed in `spin.toml`.  
  ```toml
  [component.<component-name>]
  key_value_stores = [ "default" ]
  ```
- Key‑value stores are **scoped to a single Spin application**; they cannot be shared between applications.
- Query rates are **limited** (experiment‑level limits). Increase only via a customer request.
- The only supported WASI key‑value interfaces are `wasi:keyvalue/store` and `wasi:keyvalue/batch`.

## Supported APIs and Syntax
| API / Method | Signature | Description |
|--------------|-----------|-------------|
| `openDefault()` | `openDefault(): KvStore` | Opens the key‑value store provisioned for the application (label `"default"`). |
| `Kv.open(label)` | `Kv.open(label: string): KvStore` | Opens a store with a custom label (not usable on Akamai Functions; only for other runtimes). |
| `store.exists(key)` | `store.exists(key: string): boolean` | Returns `true` if the given key is present in the store. |
| `store.getJson(key)` | `store.getJson<T = any>(key: string): T` | Retrieves the JSON value stored at `key`. |
| `store.setJson(key, value)` | `store.setJson(key: string, value: any): void` | Persists `value` (JSON‑serializable) at `key`. |
| `router.get(path, handler)` | `router.get(path: string, handler: (req: Request) => Response | Promise<Response>)` | Registers a GET route. |
| `router.post(path, handler)` | `router.post(path: string, handler: (req: Request) => Response | Promise<Response>)` | Registers a POST route. |
| `addEventListener('fetch', listener)` | `addEventListener('fetch', (event: FetchEvent) => void)` | Connects the router to incoming HTTP requests. |
| `new TextDecoder()` | `new TextDecoder(encoding?: string): TextDecoder` | Decodes `ArrayBuffer` payloads (UTF‑8 by default). |
| `Response(body?, init?)` | `new Response(body?: BodyInit | null, init?: ResponseInit): Response` | Constructs an HTTP response. |
| `request.arrayBuffer()` | `request.arrayBuffer(): Promise<ArrayBuffer>` | Reads the raw request body. |
| `request.params` (itty‑router) | `request.params: Record<string,string>` | Contains path parameters (e.g., `:key`). |

## Required Patterns
### 1. Router & Event Listener Boilerplate
```js
import { AutoRouter } from 'itty-router';
const router = AutoRouter();
addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

### 2. GET `/get/:key` Handler
```js
function handleGetValue(key) {
  const store = openDefault();               // open default KV store
  if (!store.exists(key)) {
    return new Response(null, { status: 404 });
  }
  const value = store.getJson(key);
  return new Response(JSON.stringify(value), {
    status: 200,
    headers: { "content-type": "application/json" },
  });
}
router.get("/get/:key", ({ key }) => handleGetValue(key));
```

### 3. POST `/set/:key` Handler
```js
const decoder = new TextDecoder();

async function handleSetValue(key, requestBody) {
  const payload = JSON.parse(decoder.decode(requestBody));
  if (!payload || !payload.firstName || !payload.lastName) {
    return new Response(
      'Invalid payload received.\nExpecting {"firstName": "some", "lastName": "some"}',
      { status: 400 }
    );
  }
  const store = openDefault();               // default store only
  store.setJson(key, payload);
  return new Response(null, { status: 200 });
}
router.post("/set/:key", async (req) =>
  handleSetValue(req.params.key, await req.arrayBuffer())
);
```

## Common Mistakes and Gotchas
- **Unlike EdgeKV**, the Akamai Functions key‑value store is a separate service and **cannot be accessed with EdgeKV APIs**.
- **Unlike standard WASI**, the `wasi:keyvalue/atomic` interface is **not available**; attempts to use it will fail.
- **Unlike generic Spin manifests**, only the label `"default"` is accepted; any other label will cause deployment errors.
- **Unlike a shared global store**, each application gets its **own isolated store**; cross‑application access is prohibited.
- **Unlike a non‑persistent in‑memory map**, the local development store persists in `.spin/sqlite_key_value.db` across restarts.

## Version and Compatibility Notes
- The key‑value store capability is **currently experimental**; query‑rate limits may be adjusted per‑customer.
- No explicit feature‑flag or bundle‑version requirements are documented; the functionality is available as soon as the `@spinframework/spin-kv` package is installed and the `"default"` label is declared.