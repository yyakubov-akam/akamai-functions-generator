## Runtime Constraints
- Do not use the `wasi:keyvalue/atomic` interface; it is not supported.
- Do not attempt to share a key‑value store between multiple Spin applications; stores are scoped to a single application.
- Do not use a store label other than `"default"` in the `spin.toml` component definition; only the default label is provisioned by Akamai Functions.
- Do not rely on EdgeKV for persistence; the Akamai Functions key‑value store is a separate, incompatible service.
- Do not exceed the default query‑rate limits for the key‑value store; rates are throttled unless increased via a customer request.

## Supported APIs and Syntax
- `openDefault()` — Returns the default key‑value store instance for the current Spin component. *(provided by `@spinframework/spin-kv`)*
- `Kv.open(label: string)` — Opens a key‑value store with the given label (use only if a non‑default label is provisioned). *(provided by `@spinframework/spin-kv`)*
- `store.exists(key: string): boolean` — Returns `true` if the given key exists in the store.
- `store.getJson<T>(key: string): T` — Retrieves and parses JSON stored at `key`.
- `store.setJson(key: string, value: any): void` — Serializes `value` to JSON and stores it at `key`.
- `new TextDecoder()` — Standard Web API for decoding `ArrayBuffer` payloads.
- `AutoRouter()` — Creates an `itty-router` instance with automatic route registration.
- `router.get(path: string, handler: (request: Request) => Response | Promise<Response>)` — Registers a GET handler.
- `router.post(path: string, handler: (request: Request) => Response | Promise<Response>)` — Registers a POST handler.
- `addEventListener('fetch', (event: FetchEvent) => void)` — Registers the entry point for incoming HTTP requests.
- `event.respondWith(responsePromise: Promise<Response>)` — Sends the response for the current request.
- `new Response(body?: BodyInit, init?: ResponseInit)` — Constructs an HTTP response.

## Required Patterns
**Pattern: Spin component manifest permission**
```toml
[component.hello-key-value-store]
key_value_stores = [ "default" ]
```

**Pattern: Router and fetch event wiring**
```javascript
import { AutoRouter } from 'itty-router';
const router = AutoRouter();

router.get("/get/:key", ({key}) => handleGetValue(key));
router.post("/set/:key", async (req) => 
    handleSetValue(req.params.key, await req.arrayBuffer())
);

addEventListener('fetch', async (event) => {
    event.respondWith(router.fetch(event.request));
});
```

**Pattern: GET handler**
```javascript
function handleGetValue(key) {
    const store = openDefault();
    if (!store.exists(key)) {
        return new Response(null, {status: 404});
    }
    const data = store.getJson(key);
    return new Response(JSON.stringify(data), {
        status: 200,
        headers: {"content-type": "application/json"}
    });
}
```

**Pattern: POST handler**
```javascript
const decoder = new TextDecoder();

function handleSetValue(key, requestBody) {
    const payload = JSON.parse(decoder.decode(requestBody));
    if (!payload || !payload.firstName || !payload.lastName) {
        return new Response(
            "Invalid payload received.\nExpecting {\"firstName\": \"some\", \"lastName\": \"some\"}",
            {status: 400}
        );
    }
    const store = openDefault();
    store.setJson(key, payload);
    return new Response(null, {status: 200});
}
```

## Common Mistakes and Gotchas
- Unlike generic WASI environments, Akamai Functions **does not support** the `wasi:keyvalue/atomic` interface.
- Unlike EdgeKV, the Akamai Functions key‑value store **cannot be accessed** from other applications or shared components.
- Unlike a typical Spin manifest, **only** the `"default"` label is accepted for key‑value store provisioning; using any other label will cause deployment failure.
- Unlike some local SQLite‑backed testing setups, the production store is **globally replicated** and read‑your‑writes only within a single request; subsequent requests may see eventual consistency if the store is updated elsewhere.

## Version and Compatibility Notes
- The key‑value store capability is **separate** from EdgeKV and is only available to Spin applications deployed on Akamai Functions.
- The `wasi:keyvalue/store` and `wasi:keyvalue/batch` interfaces are currently **supported**; the `wasi:keyvalue/atomic` interface is **not**.
- Query‑rate limits are **enforced by default** and can be increased on a per‑customer basis; plan accordingly for production workloads.