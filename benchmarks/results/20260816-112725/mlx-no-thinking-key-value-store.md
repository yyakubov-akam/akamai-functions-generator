## Runtime Constraints

- Do not use the `wasi:keyvalue/atomic` interface.
- Key value stores must be scoped to a single application; they cannot be shared between applications.
- Key value query rates are limited (production increases available via customer request).
- EdgeKV is not compatible with Akamai Functions.

## Supported APIs and Syntax

`@spinframework/spin-kv` — Package providing the Spin SDK for JavaScript key-value operations.

`openDefault()` — Opens the default key-value store provided by the platform.
`store.exists(key)` — Returns a boolean indicating if the key exists in the store.
`store.getJson(key)` — Retrieves JSON data associated with the specified key.
`store.setJson(key, value)` — Stores JSON data at the specified key.

## Required Patterns

### Key-Value Store Access (Default)
```javascript
import { openDefault } from '@spinframework/spin-kv';

const store = openDefault();
// Perform operations
store.setJson("my-key", { data: "value" });
const data = store.getJson("my-key");
```

### HTTP Route Handling with KV
```javascript
import { openDefault } from '@spinframework/spin-kv';
import { AutoRouter } from 'itty-router';

const router = AutoRouter();

router.get("/get/:key", ({key}) => {
    const store = openDefault();
    if (!store.exists(key)) {
        return new Response(null, { status: 404 });
    }
    const found = store.getJson(key);
    return new Response(JSON.stringify(found), { 
        status: 200, 
        headers: { "content-type": "application/json" } 
    });
});

addEventListener('fetch', async (event) => {  
    event.respondWith(router.fetch(event.request));
});
```

## Common Mistakes and Gotwas

- Unlike standard distributed databases, Akamai Functions key-value stores are isolated to a single application and cannot be accessed by other applications.
- Unlike standard Node.js environments, the `wasi:keyvalue/atomic` interface is not supported due to consistency model differences.
- Unlike EdgeKV, Akamai Functions key-value stores are a separate, incompatible service.

## Version and Compatibility Notes

- The `default` label in `spin.toml` is the only allowed label for automatic provisioning in Akamai Functions.
- Local testing uses a local SQLite file (`sqlite_key_value.db`) in the `.spin` folder to simulate the key-value store.