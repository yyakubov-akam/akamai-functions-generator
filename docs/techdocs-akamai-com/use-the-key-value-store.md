# Source: https://techdocs.akamai.com/akamai-functions/docs/use-the-key-value-store
Date: 2026-07-22T11:13:45.928847
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use the `wasi:keyvalue/atomic` interface; it is not supported.
- Only the `wasi:keyvalue/store` and `wasi:keyvalue/batch` interfaces are available.
- Key‑value stores are scoped to a single Spin application; they cannot be shared between applications.
- Only the label `"default"` is allowed for a key‑value store in the manifest. Using any other label will cause deployment failure.
- Query rates for the key‑value store are throttled; they may be increased only by a customer request to Akamai Functions.
- The Akamai Functions key‑value store is **not** compatible with EdgeKV; do not attempt to use EdgeKV APIs.

## Supported APIs and Syntax
- `openDefault()` — opens the key‑value store labeled `"default"` and returns a store object.  
  ```js
  const store = openDefault();
  ```
- `store.exists(key: string): boolean` — returns `true` if the given key exists.  
- `store.getJson<T>(key: string): T` — retrieves JSON‑serializable data stored at `key`.  
- `store.setJson(key: string, value: any): void` — stores a JSON‑serializable `value` at `key`.  
- `Kv.open(label: string)` — opens a store with a custom label (unsupported in Akamai Functions; only `"default"` works).  
- `import { openDefault } from '@spinframework/spin-kv'` — imports the default store opener.  
- `import { AutoRouter } from 'itty-router'` — imports the HTTP router used in the template.  
- `router.get(path: string, handler: (request) => Response | Promise<Response>)` — registers a GET route.  
- `router.post(path: string, handler: (request) => Response | Promise<Response>)` — registers a POST route.  
- `addEventListener('fetch', (event) => { event.respondWith(router.fetch(event.request)); })` — binds the router to incoming fetch events.

## Required Patterns
**Manifest permission**
```toml
[component.hello-key-value-store]
key_value_stores = [ "default" ]
```

**Router setup**
```js
import { openDefault } from '@spinframework/spin-kv';
import { AutoRouter } from 'itty-router';

const router = AutoRouter();
const decoder = new TextDecoder();

router.get("/get/:key", ({key}) => handleGetValue(key));
router.post("/set/:key", async (req) => 
  handleSetValue(req.params.key, await req.arrayBuffer())
);

addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

**GET handler**
```js
function handleGetValue(key) {
  const store = openDefault();
  if (!store.exists(key)) {
    return new Response(null, { status: 404 });
  }
  const found = store.getJson(key);
  return new Response(JSON.stringify(found), {
    status: 200,
    headers: { "content-type": "application/json" },
  });
}
```

**POST handler**
```js
function handleSetValue(key, requestBody) {
  const payload = JSON.parse(decoder.decode(requestBody));
  if (!payload || !payload.firstName || !payload.lastName) {
    return new Response(
      "Invalid payload received.\nExpecting {\"firstName\": \"some\", \"lastName\": \"some\"}",
      { status: 400 }
    );
  }
  const store = openDefault();          // only "default" label is allowed
  store.setJson(key, payload);
  return new Response(null, { status: 200 });
}
```

**Local testing persistence**
- When running `spin up`, the SQLite file `.spin/sqlite_key_value.db` stores the key‑value data across invocations.

## Common Mistakes and Gotchas
- **Unlike** EdgeKV, **Akamai Functions** key‑value store **is not compatible** with EdgeKV APIs.  
- **Unlike** generic WASI environments, **Akamai Functions** does **not support** the `wasi:keyvalue/atomic` interface.  
- **Unlike** typical multi‑store setups, **Akamai Functions** only accepts the label `"default"`; any other label will cause a deployment error.  
- **Unlike** some cloud KV services, **Akamai Functions** enforces read‑your‑writes behavior **only within a single request**; subsequent requests must re‑read to see prior writes.  
- **Unlike** unrestricted KV services, **Akamai Functions** imposes query‑rate limits that must be requested to raise for production workloads.

## Version and Compatibility Notes
- The key‑value store capability is part of the Akamai Functions platform; no additional feature flags are required.  
- The supported WASI interfaces are `wasi:keyvalue/store` and `wasi:keyvalue/batch`; `wasi:keyvalue/atomic` is deliberately excluded.  
- The `@spinframework/spin-kv` package version bundled with the `http-js` template is the reference implementation; ensure it remains installed (`npm install @spinframework/spin-kv`).  
- No current compatibility with EdgeKV; attempts to use EdgeKV APIs will fail.  