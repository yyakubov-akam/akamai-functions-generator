# Source: https://techdocs.akamai.com/akamai-functions/docs/build-a-supabase-cache-proxy
Date: 2026-08-16T10:56:15.407414
Model: gpt-oss:120b-cloud
## Runtime Constraints
- **Do not use any key‑value store label other than `"default"`** – Akamai Functions only provisions the default store.  
- **Do not omit variable declarations** – every secret or configuration (`supabase_url`, `supabase_key`, `cache_ttl`, `supabase_webhook_token`) must be declared in `spin.toml` and linked to the component; otherwise the function will fail to start.  
- **Do not forget to list outbound hosts** – the component must include an `allowed_outbound_hosts` array containing the Supabase project URL; requests to any other host will be blocked.  
- **Do not exceed the built‑in KV store size limits** – the platform enforces a per‑key and total store quota (implementation‑defined). Store only JSON‑serializable data and keep values small.  
- **Do not rely on Node.js built‑in modules** – the runtime is a WebAssembly sandbox; only the Spin SDK APIs and standard Web APIs are available.  
- **Do not use dynamic `import()`** – all modules must be statically imported at the top of the file.  
- **Do not assume `cache_ttl` is a string** – convert it to a number (`+(Variables.get('cache_ttl') ?? "5")`) before arithmetic.  
- **Do not forget to return a `Response` object** from every route handler; returning plain objects will cause a runtime error.  

---

## Supported APIs and Syntax
```
Variables.get(name: string): string | undefined
```
*Retrieves the value of a Spin variable.*

```
Kv.openDefault(): KvStore
```
*Opens the default key‑value store.*

```
KvStore.exists(key: string): boolean
```
*Checks whether a key is present in the store.*

```
KvStore.getJson(key: string): any
```
*Retrieves a JSON‑serializable value stored under `key`.*

```
KvStore.setJson(key: string, value: any): void
```
*Stores a JSON‑serializable value under `key`.*

```
KvStore.delete(key: string): void
```
*Removes `key` from the store.*

```
createClient(supabaseUrl: string, supabaseKey: string): SupabaseClient
```
*Creates a Supabase client (from `@supabase/supabase-js`).*

```
SupabaseClient.from(table: string): SupabaseQueryBuilder
```
*Begins a query against `table`.*

```
SupabaseQueryBuilder.select(...columns: string[]): SupabaseQueryBuilder
```
*Selects columns (or all columns if omitted).*

```
SupabaseQueryBuilder.order(column: string, options: { ascending: boolean }): SupabaseQueryBuilder
```
*Orders results.*

```
SupabaseQueryBuilder.eq(column: string, value: any): SupabaseQueryBuilder
```
*Adds an equality filter.*

```
SupabaseQueryBuilder.maybeSingle(): Promise<{ data: any | null, error: PostgrestError | null }>
```
*Returns at most one row; `data` may be `null`.*

```
SupabaseQueryBuilder.insert(row: object): SupabaseQueryBuilder
```
*Inserts a new row.*

```
SupabaseQueryBuilder.update(row: object): SupabaseQueryBuilder
```
*Updates matching rows.*

```
SupabaseQueryBuilder.delete(): SupabaseQueryBuilder
```
*Deletes matching rows.*

```
SupabaseQueryBuilder.select(): SupabaseQueryBuilder
```
*Requests the updated rows after insert/update/delete.*

```
SupabaseQueryBuilder.single(): SupabaseQueryBuilder
```
*Ensures exactly one row is returned.*

```
AutoRouter(): Router
```
*Creates an itty‑router instance.*

```
router.all(path: string, handler: (req: IRequest) => void | Promise<void>): Router
router.get(path: string, handler: (req: IRequest) => Response | Promise<Response>): Router
router.post(path: string, handler: (req: IRequest) => Response | Promise<Response>): Router
router.put(path: string, handler: (req: IRequest) => Response | Promise<Response>): Router
router.delete(path: string, handler: (req: IRequest) => Response | Promise<Response>): Router
```
*Registers HTTP methods.*

```
json(data: any, init?: ResponseInit): Response
```
*Convenient helper to return a JSON response (itty‑router).*

```
addEventListener('fetch', (event: FetchEvent) => void): void
```
*Entry point for Akamai Functions.*

```
new Response(body?: BodyInit | null, init?: ResponseInit): Response
```
*Standard Web API response.*

```
new TextDecoder(): TextDecoder
```
*Decodes `ArrayBuffer` to string.*

```
Headers.get(name: string): string | null
```
*Retrieves a request header.*

---

## Required Patterns
### 1. Middleware that injects configuration
```ts
// middlewares.ts
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

  if (!url || !key) throw new Error("Required Configuration data not set");

  request.config = { url, key, cacheTtl: ttl, webhookToken } as Config;
}
```

### 2. Router bootstrap
```ts
// src/index.ts
import { AutoRouter, json } from 'itty-router';
import { Config, withConfig } from './middlewares';
import { createClient } from '@supabase/supabase-js';
import {
  ALL_ARTICLES_CACHE_KEY,
  buildKey,
  invalidate,
  readFromCache,
  storeInCache,
} from './cache';
import processDatabaseUpdate from './inform';

let router = AutoRouter();

router
  .all('*', withConfig)                     // apply config middleware
  .get('/articles', ({ config }) => readArticles(config))
  .get('/articles/:id', ({ id, config }) => readArticleById(id, config))
  .post('/articles', async (req) => createArticle(await req.arrayBuffer(), req.config as Config))
  .put('/articles/:id', async (req) => updateArticleById(req.params.id, await req.arrayBuffer(), req.config as Config))
  .delete('/articles/:id', ({ id, config }) => deleteArticleById(id, config))
  .post('/inform', async (req) => onDatabaseUpdate(req.headers, await req.arrayBuffer(), req.config as Config));

addEventListener('fetch', (e: FetchEvent) => e.respondWith(router.fetch(e.request)));
```

### 3. Cache helper module
```ts
// src/cache.ts
import * as Kv from "@spinframework/spin-kv";

interface CacheData { expiresAt: string; data: any }

export const ALL_ARTICLES_CACHE_KEY = "all-articles";

export function buildKey(id: string): string { return `article-${id}`; }

export function readFromCache(key: string): any | undefined {
  const store = Kv.openDefault();
  if (!store.exists(key)) return undefined;
  const cache = store.getJson(key) as CacheData;
  return onlyValidCacheData(cache);
}

export function storeInCache(key: string, value: any, ttl: number) {
  const store = Kv.openDefault();
  store.setJson(key, buildCacheData(value, ttl));
  if (key !== ALL_ARTICLES_CACHE_KEY && store.exists(ALL_ARTICLES_CACHE_KEY)) {
    store.delete(ALL_ARTICLES_CACHE_KEY);
  }
}

export function invalidate(key: string) {
  const store = Kv.openDefault();
  if (store.exists(key)) store.delete(key);
  if (key !== ALL_ARTICLES_CACHE_KEY && store.exists(ALL_ARTICLES_CACHE_KEY)) {
    store.delete(ALL_ARTICLES_CACHE_KEY);
  }
}

/* internal helpers */
function buildCacheData(data: any, ttl: number): CacheData {
  return { expiresAt: new Date(Date.now() + ttl * 60_000).toISOString(), data };
}
function onlyValidCacheData(item: CacheData): any | undefined {
  return new Date() > new Date(item.expiresAt) ? undefined : item.data;
}
```

### 4. CRUD handler skeleton (read‑all example)
```ts
const readArticles = async (config: Config): Promise<Response> => {
  const cached = readFromCache(ALL_ARTICLES_CACHE_KEY);
  if (cached) return json(cached, { status: 200, headers: { 'x-served-via-cache': 'true' } });

  const supabase = createClient(config.url, config.key);
  const { data, error } = await supabase.from('articles')
    .select()
    .order('created_at', { ascending: false });

  if (error) return new Response(error.message, { status: 500 });
  storeInCache(ALL_ARTICLES_CACHE_KEY, data, config.cacheTtl);
  return json(data, { status: 200 });
};
```

### 5. Webhook processing pattern
```ts
// src/inform.ts
import { ALL_ARTICLES_CACHE_KEY, buildKey, invalidate } from "./cache";

interface InformPayload {
  type: string;
  table: string;
  record: { id: string } | null;
  old_record: { id: string } | null;
}

export function processDatabaseUpdate(body: ArrayBuffer): Response {
  let payload: InformPayload;
  try {
    payload = JSON.parse(new TextDecoder().decode(body)) as InformPayload;
  } catch {
    return new Response('Bad Request', { status: 400 });
  }

  switch (payload.type.toLowerCase()) {
    case "insert":
      invalidate(ALL_ARTICLES_CACHE_KEY);
      break;
    case "update":
      if (payload.record) invalidate(buildKey(payload.record.id));
      break;
    case "delete":
      if (payload.old_record) invalidate(buildKey(payload.old_record.id));
      break;
    default:
      return new Response('Bad Request', { status: 400 });
  }
  return new Response(null, { status: 200 });
}
```

```ts
// webhook route handler (in src/index.ts)
const onDatabaseUpdate = (headers: Headers, body: ArrayBuffer, config: Config): Response => {
  const token = headers.get("x-webhook-token");
  if (!token || token !== config.webhookToken) return new Response(null, { status: 401 });
  return processDatabaseUpdate(body);
};
```

---

## Common Mistakes and Gotchas
- **Unlike standard Node.js, Akamai Functions does not automatically expose environment variables.** All configuration must be declared as Spin variables and accessed via `Variables.get`.  
- **Unlike a regular HTTP server, outbound network access is blocked unless the host is listed in `allowed_outbound_hosts`.** Forgetting to add the Supabase URL results in connection failures.  
- **Unlike typical KV libraries, the Akamai Functions KV store only supports a single label `"default"`**; attempting to use a custom label causes deployment errors.  
- **Unlike browser fetch, the `fetch` event handler must be registered with `addEventListener('fetch', …)`**; omitting this entry point means the function never receives requests.  
- **Unlike plain JavaScript objects, the KV store stores JSON **only**; attempting to store non‑serializable values (e.g., functions, circular references) will throw at runtime.**  
- **Unlike typical Express middleware, the `withConfig` function must **mutate** the incoming `IRequest` object (`request.config = …`)**; returning a new object has no effect.  
- **Unlike regular Node.js, the runtime does not provide a built‑in `process.env`.** All secrets must be passed via Spin variables.  

---

## Version and Compatibility Notes
- The tutorial targets the **public preview / tech preview** of Akamai Functions; access requires an onboarding form and the `aka` plugin for Spin.  
- The **Key‑Value Store** feature is currently limited to the **single default store**; future releases may allow named stores.  
- The **`spin aka deploy`** command is the only supported deployment method for Functions; other Spin deployment targets are not compatible with the `aka` runtime.  
- The **`@supabase/supabase-js`** client version bundled via `npm install` must be compatible with the WebAssembly sandbox (no native Node modules).  
- The **`@spinframework/spin-variables`** and **`@spinframework/spin-kv`** SDKs are version‑locked to the Spin runtime used by Akamai Functions; ensure the same Spin version is used when building (`spin build`).  