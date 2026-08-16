# Source: https://techdocs.akamai.com/akamai-functions/docs/stream-data-from-linode-object-store
Date: 2026-08-16T09:24:52.944760
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use a Node.js runtime older than **v22**.  
- Only the following npm packages are guaranteed to be available: `@aws-sdk/client-s3`, `@spinframework/spin-variables`, `itty-router`. Importing any other third‑party module may cause a build failure.  
- All outbound network requests must be whitelisted via the `allowed_outbound_hosts` manifest property; requests to hosts not listed will be blocked.  
- The function must run within the **Akamai Functions** sandbox, which imposes a maximum **WebAssembly binary size of 5 MiB** and a **memory limit of 256 MiB** per request.  
- The environment does **not support** Node.js built‑in modules such as `fs`, `net`, or `child_process`.  

## Supported APIs and Syntax
- `AutoRouter()` — creates an itty‑router instance for declarative route handling.  
- `json(data)` — returns a `Response` with `Content‑Type: application/json` and the JSON‑encoded `data`.  
- `S3Client(options)` — constructs an AWS‑SDK S3 client.  
  ```ts
  new S3Client({
    region: string,
    endpoint: string,
    credentials: { accessKeyId: string, secretAccessKey: string }
  })
  ```
- `ListObjectsV2Command(input)` — SDK command to list objects.  
  ```ts
  new ListObjectsV2Command({ Bucket: string })
  ```
- `GetObjectCommand(input)` — SDK command to retrieve an object.  
  ```ts
  new GetObjectCommand({ Bucket: string, Key: string })
  ```
- `Variables.get(name)` — reads a Spin variable (string).  
- `new TextDecoder()` / `new TextEncoder()` — UTF‑8 decode/encode utilities.  
- `new TransformStream({ transform(chunk, controller) { … } })` — creates a streaming transform.  
- `Response(body?, init?)` — constructs an HTTP response; `body` may be a `ReadableStream`.  
- `addEventListener('fetch', (event: FetchEvent) => { … })` — registers the entry point for Akamai Functions.  
- `router.fetch(request, { config: Config })` — forwards the request to the router with a custom context object.  

## Required Patterns
### 1. Router and Event Listener Boilerplate
```ts
import { AutoRouter, json } from 'itty-router';
import * as Variables from '@spinframework/spin-variables';

const router = AutoRouter();

router
  .get("/files", async (_, { config }) => await listFiles(config))
  .get("/files/:name", async ({ name }, { config }) => await streamFile(name, config))
  .get("/transformed-files/:name", async ({ name }, { config }) => await streamAndTransformFile(name, config));

//@ts-ignore
addEventListener('fetch', async (event: FetchEvent) => {
  const endpoint = Variables.get("endpoint");
  const accessKeyId = Variables.get("access_key_id");
  const secretAccessKey = Variables.get("secret_access_key");
  const bucketName = Variables.get("bucket_name");
  const region = Variables.get("region");

  if (!endpoint || !accessKeyId || !secretAccessKey || !bucketName || !region) {
    return new Response("Application not configured correctly", { status: 500 });
  }

  event.respondWith(
    router.fetch(event.request, {
      config: { endpoint, accessKeyId, secretAccessKey, bucketName, region } as Config
    })
  );
});
```

### 2. S3 Client Construction (reused in each handler)
```ts
const s3 = new S3Client({
  region: config.region,
  endpoint: config.endpoint,
  credentials: {
    accessKeyId: config.accessKeyId,
    secretAccessKey: config.secretAccessKey,
  },
});
```

### 3. List Files Handler
```ts
const listFiles = async (config: Config): Promise<Response> => {
  const s3 = new S3Client({ /* as above */ });
  const { Contents } = await s3.send(new ListObjectsV2Command({ Bucket: config.bucketName }));
  const files = Contents?.map(f => f.Key) || [];
  return json({ files });
};
```

### 4. Stream File Handler
```ts
const streamFile = async (name: string, config: Config): Promise<Response> => {
  const s3 = new S3Client({ /* as above */ });
  const { Body } = await s3.send(new GetObjectCommand({ Bucket: config.bucketName, Key: name }));
  return new Response(Body as ReadableStream, { status: 200 });
};
```

### 5. Upper‑case Transform Stream Handler
```ts
const streamAndTransformFile = async (name: string, config: Config): Promise<Response> => {
  const upperCaseTransform = new TransformStream({
    transform(chunk, controller) {
      const txt = dec.decode(chunk, { stream: true });
      controller.enqueue(enc.encode(txt.toUpperCase()));
    },
  });

  const s3 = new S3Client({ /* as above */ });
  const { Body } = await s3.send(new GetObjectCommand({ Bucket: config.bucketName, Key: name }));
  const transformed = (Body as ReadableStream).pipeThrough(upperCaseTransform);
  return new Response(transformed, { status: 200 });
};
```

## Common Mistakes and Gotchas
- **Unlike standard Node.js**, Akamai Functions does **not** allow returning a `Buffer` or `string` directly for large payloads; you must return a `Response` whose body is a `ReadableStream` for streaming data.  
- **Unlike browser fetch**, the `fetch` event handler must call `event.respondWith(...)`; simply returning a `Response` from the listener has no effect.  
- **Unlike a typical Node.js process**, environment variables are accessed via `Variables.get(...)` (defined in `spin.toml`), not via `process.env`.  
- **Unlike unrestricted network environments**, outbound HTTP requests are blocked unless the target host matches an entry in `allowed_outbound_hosts`.  

## Version and Compatibility Notes
- Requires **Node.js ≥ 22** (the runtime used by the Akamai Functions preview).  
- The `@aws-sdk/client-s3` package is fully supported, but only the subset of commands used in the tutorial (`ListObjectsV2Command`, `GetObjectCommand`) have been tested.  
- All Spin variables referenced (`region`, `endpoint`, `bucket_name`, `access_key_id`, `secret_access_key`) must be declared as **required** in `spin.toml`; otherwise the build will fail.  
- The `allowed_outbound_hosts` manifest entry must include the full scheme and host pattern (e.g., `['https://*.linodeobjects.com']`).  
- The application must be deployed with the `spin aka deploy` command; local `spin up` runs the same Wasm bundle but does not affect production routing.  