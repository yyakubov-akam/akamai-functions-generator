# Source: https://techdocs.akamai.com/akamai-functions/docs/build-a-supabase-cache-proxy
Date: 2026-08-17T09:22:07.296339
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Must use `addEventListener` to handle the `FetchEvent` for the application entry point.
- The Key Value Store label is restricted to exactly "default". No custom labels are allowed.
- The application follows a capabilities-based security model; outbound hosts must be explicitly defined in `spin.toml`.
- Request bodies must be accessed via `req.arrayBuffer()` and decoded using `TextDecoder`.
- Supabase queries must use the `@supabase/supabase-js` Node.js module.

## Supported APIs and Syntax

`Variables.get(key)` — Retrieves a value from application environment variables defined in `spin.toml`.

`Kv.openDefault()` — Opens the default key-value store provisioned by Akamai Functions.

`store.exists(key)` — Checks if a specific key exists in the key-value store.

`store.getJson(key)` — Retrieves a value from the store and parses it as JSON.

`store.setJson(key, value)` — Stores a value in the store as JSON.

`store.delete(key)` — Deletes a specific key-value pair from the store.

`createClient(url, key)` — Instantiates a Supabase client using the provided project URL and API key.

`supabase.from(table).select()` — Fetches rows from the specified table.

`supabase.from(table).insert(data)` — Inserts new rows into the specified table.

`supabase.from(table).update(data)` — Updates existing rows in the specified table.

`supabase.from(table).delete()` — Deletes rows from the specified table.

`supabase.from(table).eq(column, value)` — Filters rows where the column matches the value.

`supabase.from(table).maybeSingle()` — Fetches a single row, returning `null` if no match is found (does not throw an error).

`AutoRouter` — A router class for handling HTTP requests and routes.

`json(data, options)` — Returns a JSON response object.

## Required Patterns

### Configuration Middleware Pattern
Load configuration variables from the environment and attach them to the request object for downstream handlers.

```typescript
import * as Variables from "@spinframework/spin-variables";
import { IRequest } from "itty-router";

export interface Config {
  url: string;
  key: string;
  cacheTtl: number;
  webhookToken?: string;
}

export function withConfig(request: IRequest) {
  const url = Variables.get('supabase_url');
  const key = Variables.get('supabase_key');
  const ttl = +(Variables.get('cache_ttl') ?? "5");
  const webhookToken = Variables.get('supabase_webhook_token');

  if (!url || !key) {
    throw new Error("Required Configuration data not set");
  }

  request.config = {
    url,
    key,
    cacheTtl: ttl,
    webhookToken
  } as Config;
}
```

### KV Cache Wrapper Pattern
Wrap data in an object containing an expiration timestamp to manage cache validity.

```typescript
interface CacheData {
  expiresAt: string;
  data: any;
}

const buildCacheData = (data: any, ttl: number): CacheData => {
  return {
    expiresAt: new Date(Date.now() + ttl * 60 * 1000).toISOString(),
    data: data
  } as CacheData;
}

// Check if cache data is expired
const onlyValidCacheData = (cacheItem: CacheData): any | undefined => {
  const now = new Date();
  const expiresAt = new Date(cacheItem.expiresAt);
  if (now > expiresAt) {
    return undefined;
  }
  return cacheItem.data;
}
```

### Cache Invalidation Pattern
When storing a specific item, invalidate the global list cache if it exists.

```typescript
import * as Kv from "@spinframework/spin-kv";

export const ALL_ARTICLES_CACHE_KEY = "all-articles";

export function storeInCache(key: string, value: any, ttl: number) {
  const store = Kv.openDefault();
  store.setJson(key, buildCacheData(value, ttl));
  
  // Invalidate the global list if a specific item was cached
  if (key !== ALL_ARTICLES_CACHE_KEY && store.exists(ALL_ARTICLES_CACHE_KEY)) {
    store.delete(ALL_ARTICLES_CACHE_KEY);
  }
}
```

### Webhook Validation Pattern
Verify the incoming request contains a valid authentication token before processing.

```typescript
const onDatabaseUpdate = (headers: Headers, requestBody: ArrayBuffer, config: Config): Response => {
  const token = headers.get("x-webhook-token");
  if (!token || token !== config.webhookToken) {
    console.log("Webhook invoked without or with invalid token");
    return new Response(null, { status: 401 });
  }
  return processDatabaseUpdate(requestBody);
}
```

## Common Mistakes and Gotchas

- **Request Body Parsing:** Unlike standard Node.js `req.body`, Akamai Functions requests must be read as `ArrayBuffer` and decoded using `new TextDecoder().decode(buffer)`.
- **KV Store Label:** Unlike generic KV stores, Akamai Functions strictly requires the label to be "default". Attempting to use other labels will fail.
- **Supabase Single vs Maybe Single:** Unlike standard Supabase behavior where `.single()` throws an error if no row is found, `.maybeSingle()` returns `null`. You must check for `null` explicitly to return a 404.
- **Variable Access:** Variables must be explicitly linked in the `[component.name.variables]` section of `spin.toml` to be accessible via `Variables.get()`.
- **Outbound Security:** You cannot make requests to arbitrary URLs. You must explicitly list allowed outbound hosts in `allowed_outbound_hosts` in the component configuration.

## Version and Compatibility Notes

- Requires `@spinframework/spin-variables` and `@spinframework/spin-kv` packages.
- Requires `@supabase/supabase-js` package.
- Requires `itty-router` for HTTP routing.
- Requires the `http-ts` Spin template.
- Access to Akamai Functions is currently in "Public Preview" (requires sign-up and onboarding form completion).