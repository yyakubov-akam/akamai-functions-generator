## Runtime Constraints

- Do not use the `wasi:keyvalue/atomic` interface (not supported)
- Key value stores are scoped to a single application and cannot be shared
- Key value query rates are limited; contact support to increase for production
- Akamai Functions key value store is separate from EdgeKV and not compatible

## Supported APIs and Syntax

`openDefault()` — Opens the default key value store for the application
`store.exists(key)` — Checks if a key exists in the store
`store.getJson(key)` — Retrieves JSON data stored at the specified key
`store.setJson(key, value)` — Stores JSON data at the specified key
`Kv.open(label)` — Opens a key value store with a specific label (use instead of openDefault if a different label is specified)

## Required Patterns

### Application Manifest Configuration
```toml
[component.hello-key-value-store]
key_value_stores = [ "default" ]
```

### HTTP Router Setup
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

### GET Handler Pattern
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

### POST Handler Pattern
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

- Unlike standard Node.js file systems, Akamai Functions uses a WASI-based key value store that requires the `@spinframework/spin-kv` package
- Unlike standard Node.js, Akamai Functions only allows the `"default"` label for key_value_stores in the manifest; custom labels are not supported
- Unlike standard Node.js, Akamai Functions does not support the `wasi:keyvalue/atomic` interface
- Unlike standard Node.js, Akamai Functions key value stores are isolated to a single application and cannot be shared between applications
- Unlike standard Node.js, Akamai Functions key value stores are separate from EdgeKV and not compatible

## Version and Compatibility Notes

- The `@spinframework/spin-kv` package is required for key value store functionality
- The `http-js` template is used to create new Spin applications
- Local testing uses SQLite file (`sqlite_key_value.db`) in the `.spin` folder
- Deployment is performed using the `spin aka deploy` command