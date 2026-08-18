## Runtime Constraints

- Do not use the `wasi:keyvalue/atomic` interface.
- Key value stores must be scoped to a single application; they cannot be shared between applications.
- Key value query rates are limited.
- EdgeKV is not compatible with Akamai Functions.

## Supported APIs and Syntax

`@spinframework/spin-kv.openDefault()` — Opens the default key-value store provided by the platform.
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

### Permission Configuration (spin.toml)
```toml
[component.your-component-name]
key_value_stores = [ "default" ]
```

## Common Mistakes and Gotwas

- Unlike standard distributed databases, Akamai Functions key-value stores do not support the `wasi:keyvalue/atomic` interface due to consistency model differences.
- Unlike EdgeKV, the Akamai Functions key-value store is a separate, incompatible service.
- Unlike standard Node.js environments, the key-value store is scoped to the application and requires explicit permission in `spin.toml` using the `"default"` label.

## Version and Compatibility Notes

- The `"default"` label in `spin.toml` is the only allowed label for automatic provisioning in Akamai Functions.
- Local testing uses a local SQLite file (`sqlite_keyvalue.db`) in the `.spin` folder to simulate the key-value store.