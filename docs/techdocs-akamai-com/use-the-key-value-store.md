# Source: https://techdocs.akamai.com/akamai-functions/docs/use-the-key-value-store
Date: 2026-06-05T09:04:42.992561
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use the `wasi:keyvalue/atomic` interface; it is not supported.
- Only the `wasi:keyvalue/store` and `wasi:keyvalue/batch` interfaces are supported.
- Key‑value stores are scoped to a single Spin application; they cannot be shared between applications.
- The manifest may only specify the `"default"` label for `key_value_stores`; any other label will be rejected.
- Query rates for the key‑value store are limited by default; production‑level rates must be requested from Akamai.
- The Akamai Functions key‑value store is separate from EdgeKV and is not compatible with EdgeKV APIs.

## Supported APIs and Syntax
- `openDefault()` — Opens the default key‑value store (label `"default"`).  
- `Kv.open(label)` — Opens a key‑value store with the given label (use only if a non‑default label is provisioned).  
- `store.exists(key)` — Returns `true` if the given `key` exists in the store.  
- `store.getJson(key)` — Retrieves the JSON value stored at `key`.  
- `store.setJson(key, payload)` — Stores `payload` (a JSON‑serializable object) at `key`.  

Additional runtime APIs used in the example:
- `new TextDecoder()` — Decodes an `ArrayBuffer` to a string.  
- `router.get(path, handler)` / `router.post(path, handler)` — Registers GET and POST routes with `itty-router`.  
- `addEventListener('fetch', listener)` — Handles incoming HTTP requests in the Spin runtime.  

## Required Patterns
### Router Setup & Event Listener
```js
import { openDefault } from '@spinframework/spin-kv';
import { AutoRouter } from 'itty-router';

const router = AutoRouter();
const decoder = new TextDecoder();

router.get("/get/:key", ({ key }) => handleGetValue(key));
router.post("/set/:key", async (req) =>
  handleSetValue(req.params.key, await req.arrayBuffer())
);

addEventListener('fetch', async (event) => {
  event.respondWith(router.fetch(event.request));
});
```

### GET Handler
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

### POST Handler
```js
function handleSetValue(key, requestBody) {
  const payload = JSON.parse(decoder.decode(requestBody));
  if (!payload || !payload.firstName || !payload.lastName) {
    return new Response(
      "Invalid payload received.\nExpecting {\"firstName\": \"some\", \"lastName\": \"some\"}",
      { status: 400 }
    );
  }
  const store = openDefault();          // use Kv.open("mylabel") for non‑default stores
  store.setJson(key, payload);
  return new Response(null, { status: 200 });
}
```

## Common Mistakes and Gotchas
- Unlike standard Node.js key‑value libraries, Akamai Functions **does not support** the `wasi:keyvalue/atomic` interface.
- Unlike EdgeKV, the Akamai Functions key‑value store **cannot be accessed** via EdgeKV APIs; they are separate systems.
- Unlike generic manifests, the `key_value_stores` array **must contain only** `"default"`; other labels are rejected.
- Unlike eventually consistent stores, all standard key‑value operations **exhibit read‑your‑writes behavior within a request**.

## Version and Compatibility Notes
- The key‑value store capability is provisioned automatically when deploying a Spin app with the `"default"` label; no additional SDK version flags are required.
- The feature is currently in experimental rollout; query‑rate limits may be tightened unless a production increase is requested.