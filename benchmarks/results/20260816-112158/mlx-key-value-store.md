## Runtime Constraints

- Do not use the `wasi:keyvalue/atomic` interface.
- Do not attempt to share key-value stores between different applications; they are scoped to a single application.
- Do not use labels other than `"default"` in the Akamai Functions environment.
- Do not use EdgeKV with Akamai Functions as they are incompatible.

## Supported APIs and Syntax

`@spinframework/spin-kv` — Required package for key-value store capabilities.

`openDefault()` — Opens the default key-value store.
`store.exists(key)` — Checks if a key exists in the store.
`store.getJson(key)` — Retrieves JSON data associated with the specified key.
`store.setJson(key, payload)` — Stores a JSON payload at the specified key.
`Kv.open("mylabel")` — Opens a specific key-value store by label (Note: Akamai environment restricts usage to `"default"`).

## Required Patterns

### Pattern: Opening the default store
```javascript
import { openDefault } from '@spinframework/spin-kv';

const store = openDefault();
```

### Pattern: Safe JSON retrieval
```javascript
const store = openDefault();

if (!store.exists(key)) {
    return new Response(null, { status: 404 });
}

const data = store.getJson(key);
```

### Pattern: JSON persistence
```javascript
const store = openDefault();
store.setJson(key, payload);
```

## Common Mistakes and Gotchas

- Unlike standard distributed databases, Akamai Functions key-value stores are isolated to a single application and cannot be shared between applications.
- Unlike standard Node.js environments, the `wasi:keyvalue/atomic` interface is not supported because the global store does not provide the required consistency guarantees.
- Unlike EdgeKV, Akamai Functions key-value stores are a separate and incompatible capability.

## Version and Compatibility Notes

- The `wasi:keyvalue/store` and `wasi:keyvalue/batch` interfaces are supported.
- The `wasi:keyvalue/atomic` interface is unsupported.
- In the Akamai Functions environment, only the `"default"` label is permitted for automatic provisioning.