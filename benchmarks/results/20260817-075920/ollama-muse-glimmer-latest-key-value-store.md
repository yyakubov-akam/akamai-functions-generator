## Runtime Constraints

- Do not use `wasi:keyvalue/atomic` interface
- Do not share a key value store between applications; stores are scoped to a single application
- Do not use a key value store label other than `"default"` on Akamai Functions
- Do not assume EdgeKV compatibility; Edge is not currently compatible with Akamai Functions
- Do not exceed the limited key value query rates without a per-customer increase request

## Supported APIs and Syntax

`openDefault()` — opens Key Value store with label "default"
`store.exists(key)` — check if key exists
`store.getJson(key)` — load JSON data at key from key value store
`store.setJson(key, payload)` — store data in Key Value store at key
`Kv.open(label)` — open a Key Value store with a custom label
`AutoRouter()` — creates router instance
`router.get(path, handler)` — register GET endpoint
`router.post(path, handler)` — register POST endpoint
`router.fetch(request)` — handle incoming requests using the HTTP router
`addEventListener(eventType, callback)` — listen for fetch events
`event.respondWith(promise)` — respond to event
`new Response(body, init)` — create HTTP response
`TextDecoder()` — decode request body bytes to string
`JSON.parse(string)` — parse request body
`JSON.stringify(value)` — serialize response payload

## Required Patterns

Pattern: spin.toml permission grant
```toml
[component.hello-key-value-store]
key_value_stores = [ "default" ]
```

Pattern: Import and router setup
```javascript
import { openDefault } from '@spinframework/spin-kv';
import { AutoRouter } from 'itty-router'

const router = AutoRouter();
const decoder = new TextDecoder();

router.get("/get/:key", ({key}) => handleGetValue(key));
router.post("/set/:key", async (req) => handleSetValue(req.params.key, await req.arrayBuffer()));

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

Pattern: GET handler
```javascript
function handleGetValue(key) {
    const store = openDefault();
    if (!store.exists(key)) {
        return new Response(null, { status: 404 });
    }
    let found = store.getJson(key);
    return new Response(
      JSON.stringify(found),
      { status: 200, headers: { "content-type": "application/json" } }
    );
}
```

Pattern: POST handler
```javascript
function handleSetValue(key, requestBody) {
    let payload = JSON.parse(decoder.decode(requestBody));
    if (!payload || !payload.firstName || !payload.lastName) {
        return new Response("Invalid payload received.\nExpecting {\"firstName\": \"some\", \"lastName\": \"some\"}", { status: 400 });
    }
    const store = openDefault();
    store.setJson(key, payload);
    return new Response(null, { status: 200 });
}
```

## Common Mistakes and Gotchas

Unlike standard WASI keyvalue spec which includes atomic interface, Akamai Functions does not support `wasi:keyvalue/atomic` interface because it requires a consistency guarantee not provided by the global store
Unlike standard multi-application KV, Akamai Functions key value stores are isolated to a single application and cannot be shared between applications
Unlike EdgeKV, Akamai Functions key value store is different and separate and Edge is not currently compatible with Akamai Functions
Unlike unlimited query rates, Akamai Functions key value query rates are limited to enable experimenting with this feature
Unlike standard Node.js in-memory KV, local Spin testing persists data to `.spin/sqlite_key_value.db` across Spin application invocations and updates

## Version and Compatibility Notes

`wasi:keyvalue/store` and `wasi:keyvalue/batch` interfaces are supported; `wasi:keyvalue/atomic` interface is not supported
Key value stores are scoped to applications and cannot be shared between applications
Query rates are limited for experimentation and can be increased to meet production needs per customer request
Akamai Functions only allows the `"default"` label for key value stores; it signals the platform to automatically provision a store for the Spin application