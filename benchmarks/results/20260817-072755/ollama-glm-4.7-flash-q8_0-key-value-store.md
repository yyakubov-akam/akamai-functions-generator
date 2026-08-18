## Runtime Constraints

- Do not use the `wasi:keyvalue/atomic` interface
- Key value stores are scoped to a single application and cannot be shared
- Query rates are limited to experimentation levels
- Akamai Functions is not compatible with EdgeKV

## Supported APIs and Syntax

`openDefault()` — Opens the default key-value store provisioned by Akamai Functions

`store.exists(key)` — Checks if a key exists in the store

`store.getJson(key)` — Retrieves JSON data stored at the specified key

`store.setJson(key, value)` — Stores JSON data at the specified key

## Required Patterns

### Manifest Configuration
Configure the component manifest (`spin.toml`) to enable the default key-value store.

```toml
[component.hello-key-value-store]
key_value_stores = [ "default" ]
```

### GET Handler Pattern
Initialize the store, check for key existence, and return JSON or 404.

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
Initialize the store, validate payload, and set JSON data.

```javascript
function handleSetValue(key, requestBody) {
    const decoder = new TextDecoder();
    let payload = JSON.parse(decoder.decode(requestBody));

    if (!payload || !payload.firstName || !payload.lastName) {
        return new Response("Invalid payload received.\nExpecting {\"firstName\": \"some\", \"lastName\": \"some\"}", { status: 400 });
    }

    const store = openDefault();
    store.setJson(key, payload);

    return new Response(null, { status: 200 });
}
```

### Router Setup
Import the KV package and configure routes using `itty-router`.

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

## Common Mistakes and Gotchas

- Unlike standard Node.js behavior, Akamai Functions does not support the `wasi:keyvalue/atomic` interface
- Unlike local development (which uses SQLite files), Akamai Functions only allows the `"default"` label for `key_value_stores`
- Data operations exhibit read-your-writes behavior within a single request
- Key value stores are isolated to a single application and cannot be accessed by other applications

## Version and Compatibility Notes

- Requires the `@spinframework/spin-kv` package
- Must use the `http-js` template for the tutorial (`spin new -E akamai-functions -t http-js`)
- Local testing uses SQLite (`sqlite_key_value.db`), while Akamai Functions uses a globally replicated, low-latency store provisioned by the platform