## Runtime Constraints

- Do not use the `wasi:keyvalue/atomic` interface
- Key value stores are scoped to a single application and cannot be shared between applications
- Akamai Functions only allows the `"default"` label for key value stores
- Key value query rates are limited for experimentation (rates can be increased per customer request)

## Supported APIs and Syntax

- `openDefault()` — Opens the default key value store provisioned by Akamai Functions
- `store.exists(key)` — Checks if a specific key exists in the store
- `store.getJson(key)` — Retrieves and parses JSON data stored at the specified key
- `store.setJson(key, value)` — Stores the provided value as JSON at the specified key

## Required Patterns

### Configuration (spin.toml)
Add the default label to the component configuration to enable store access.

```toml
[component.hello-key-value-store]
key_value_stores = [ "default" ]
```

### Application Implementation
Import the KV store SDK, set up an HTTP router, and define routes for GET and POST operations.

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

### Value Retrieval Handler
Open the store, check for key existence, and return JSON data.

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

### Value Storage Handler
Parse the request body, open the store, and persist JSON data.

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

- Unlike standard Spin configurations, Akamai Functions does not support custom key value store labels; you must use the `"default"` label
- Unlike standard relational databases, Akamai Functions key value stores cannot be shared between applications
- Unlike standard Node.js behavior, local testing uses a SQLite file (`sqlite_key_value.db`) located in the `.spin` folder, while deployment uses a global, replicated store
- The `wasi:keyvalue/atomic` interface is not supported due to consistency guarantees not provided by the global store

## Version and Compatibility Notes

- Requires the `@spinframework/spin-kv` package
- Requires the `http-js` template
- EdgeKV is not currently compatible with Akamai Functions
- The `npm install` command in the template installs both default packages and `@spinframework/spin-kv`