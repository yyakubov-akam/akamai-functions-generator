## Runtime Constraints
- Do not use wasi:keyvalue/atomic interface; it is not supported
- Do not share key value stores between applications; stores are scoped to a single application
- Do not use key value store labels other than "default" on Akamai Functions
- Do not use EdgeKV with Akamai Functions; Edge is not currently compatible with Akamai Functions
- Do not exceed key value query rate limits; rates are limited for experimentation

## Supported APIs and Syntax
`openDefault()` — opens the Key Value store with label "default"
`Kv.open(label)` — opens a Key Value store with specified label
`store.exists(key)` — check if key exists in the store
`store.getJson(key)` — load JSON data at key from key value store
`store.setJson(key, payload)` — store data in Key Value store at key
`AutoRouter()` — create an itty-router router instance
`router.get(path, handler)` — register GET endpoint
`router.post(path, handler)` — register POST endpoint
`router.fetch(request)` — handle incoming request with router
`addEventListener('fetch', callback)` — register fetch event listener for Spin component
`TextDecoder()` — decode ArrayBuffer to string

## Required Patterns

### Pattern: Grant key value store permission in spin.toml
```toml
[component.hello-key-value-store]
key_value_stores = [ "default" ]
```

### Pattern: Initialize router and fetch handler
```javascript
import { AutoRouter } from 'itty-router'
const router = AutoRouter();
addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

### Pattern: GET value from store
```javascript
import { openDefault } from '@spinframework/spin-kv';
function handleGetValue(key) {
    const store = openDefault();
    if (!store.exists(key)) {
        return new Response(null, { status: 404 });
    }
    let found = store.getJson(key);
    return new Response(JSON.stringify(found), { status: 200, headers: { "content-type": "application/json" } });
}
```

### Pattern: POST value to store
```javascript
import { openDefault } from '@spinframework/spin-kv';
function handleSetValue(key, requestBody) {
    const store = openDefault();
    store.setJson(key, payload);
    return new Response(null, { status: 200 });
}
```

## Common Mistakes and Gotchas
Unlike standard WASI key value support, Akamai Functions does not support wasi:keyvalue/atomic interface because it requires a consistency guarantee not provided by the global store
Unlike standard multi-application data sharing, Akamai Functions key value stores are isolated to a single application and cannot be shared between applications
Unlike EdgeKV, Akamai Functions key value store is a different and separate capability and Edge is not currently compatible with Akamai Functions
Unlike eventual consistency stores, Akamai Functions key value store exhibits read-your-writes behavior within a request

## Version and Compatibility Notes
Key value query rates are limited to enable experimenting with this feature; rates can be increased to meet production needs per customer request
Akamai Functions only allows the "default" label for key value stores; it signals the platform to automatically provision a store for the Spin application
`@spinframework/spin-kv` package is required for key value store access in JavaScript Spin components