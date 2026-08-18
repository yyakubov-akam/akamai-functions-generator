# Source: https://techdocs.akamai.com/akamai-functions/docs/use-the-key-value-store
Date: 2026-08-17T08:48:07.218033
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Do not use the `wasi:keyvalue/atomic` interface
- Key value stores are scoped to a single application and cannot be shared between applications
- Query rates are limited to experimentation levels (can be increased via customer request)
- Local testing uses SQLite (`sqlite_key_value.db`) located in the `.spin` folder
- Akamai Functions manifest only allows the `"default"` label for `key_value_stores`
- EdgeKV is not compatible with Akamai Functions

## Supported APIs and Syntax

`openDefault()` — Opens the default key value store provisioned by the platform

`store.exists(key)` — Checks if a key exists in the store

`store.getJson(key)` — Retrieves JSON data associated with a key

`store.setJson(key, payload)` — Stores JSON data at a specific key

`AutoRouter` — HTTP router for handling routes (from `itt-router`)

`addEventListener('fetch', handler)` — Entry point for handling incoming HTTP requests

## Required Patterns

### Manifest Configuration
```toml
[component.component-name]
key_value_stores = [ "default" ]
```

### Import and Router Setup
```javascript
import { openDefault } from '@spinframework/spin-kv';
import { AutoRouter } from 'itty-router'

const router = AutoRouter();

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

### Key Value Store Operations
```javascript
// Open store
const store = openDefault();

// Check existence
if (!store.exists(key)) {
    return new Response(null, { status: 404 });
}

// Get JSON
let found = store.getJson(key);

// Set JSON
store.setJson(key, payload);
```

## Common Mistakes and Gotchas

- Unlike standard Node.js, Akamai Functions does not support the `wasi:keyvalue/atomic` interface
- Unlike standard Node.js, Akamai Functions does not support raw file I/O; use `openDefault()` instead
- Unlike standard Node.js, Akamai Functions does not support EdgeKV
- The `key_value_stores` label in `spin.toml` must be `"default"` for Akamai Functions deployment

## Version and Compatibility Notes

- Requires the `@spinframework/spin-kv` package
- Requires `itt-router` (specifically `AutoRouter`)
- Local development environment uses SQLite for persistence
- Global store provides read-your-writes behavior within a request