# Source: https://techdocs.akamai.com/akamai-functions/docs/stream-data-from-linode-object-store
Date: 2026-07-22T11:12:52.966468
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use Node.js versions earlier than **22**; the runtime requires Node 22 or later.  
- Do not import modules other than those declared in the manifest (e.g., `@aws-sdk/client-s3`, `@spinframework/spin-variables`, `itty-router`).  
- Do not exceed the default **WebAssembly binary size limit** for an Akamai Functions component (implicit – keep source size reasonable).  
- Do not perform outbound network requests to hosts not listed in `allowed_outbound_hosts`.  
- Do not store secret values (e.g., `secret_access_key`) in plain‑text code; they must be supplied via **Spin variables** marked `secret = true`.  
- Do not use APIs that require a full Node.js runtime (e.g., `fs`, `net`, `child_process`).  

## Supported APIs and Syntax
- `AutoRouter()` — creates an itty‑router instance for declarative route handling.  
- `json(object)` — returns a `Response` with `Content‑Type: application/json` and the JSON‑encoded body.  
- `S3Client(config)` — AWS SDK S3 client; `config` includes `region`, `endpoint`, and `credentials`.  
- `new ListObjectsV2Command(input)` — lists objects in a bucket; `input` shape `{ Bucket: string }`.  
- `new GetObjectCommand(input)` — retrieves a single object; `input` shape `{ Bucket: string, Key: string }`.  
- `new TransformStream({ transform(chunk, controller) { … } })` — creates a streaming transform; `chunk` is a `Uint8Array`.  
- `new TextDecoder()` — decodes `Uint8Array` to string; `decode(chunk, { stream: true })` for streaming.  
- `new TextEncoder()` — encodes string to `Uint8Array`.  
- `addEventListener('fetch', async (event: FetchEvent) => { … })` — registers the entry point for Akamai Functions.  
- `event.respondWith(response)` — sends a `Response` back to the client.  
- `Variables.get("variable_name")` — retrieves a Spin variable (string).  
- `new Response(body, init?)` — constructs an HTTP response; `body` may be a `ReadableStream`.  

## Required Patterns
**Pattern: Component bootstrap & variable loading**  
```ts
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

**Pattern: List files endpoint**  
```ts
const listFiles = async (config: Config): Promise<Response> => {
  const s3 = new S3Client({
    region: config.region,
    endpoint: config.endpoint,
    credentials: {
      accessKeyId: config.accessKeyId,
      secretAccessKey: config.secretAccessKey,
    },
  });

  const { Contents } = await s3.send(new ListObjectsV2Command({ Bucket: config.bucketName }));
  const files = Contents?.map(f => f.Key) || [];
  return json({ files });
};
```

**Pattern: Stream raw file**  
```ts
const streamFile = async (name: string, config: Config): Promise<Response> => {
  const s3 = new S3Client({ /* same config as above */ });
  const { Body } = await s3.send(new GetObjectCommand({ Bucket: config.bucketName, Key: name }));
  return new Response(Body as ReadableStream, { status: 200 });
};
```

**Pattern: Stream with Transform (uppercase)**  
```ts
const streamAndTransformFile = async (name: string, config: Config): Promise<Response> => {
  const upperCaseTransform = new TransformStream({
    transform(chunk, controller) {
      const txt = dec.decode(chunk, { stream: true });
      controller.enqueue(enc.encode(txt.toUpperCase()));
    },
  });

  const s3 = new S3Client({ /* same config as above */ });
  const { Body } = await s3.send(new GetObjectCommand({ Bucket: config.bucketName, Key: name }));
  const transformed = (Body as ReadableStream).pipeThrough(upperCaseTransform);
  return new Response(transformed, { status: 200 });
};
```

**Pattern: Router definition**  
```ts
let router = AutoRouter()
  .get("/files", (_, { config }) => listFiles(config))
  .get("/file/:name", ({ name }, { config }) => streamFile(name, config))
  .get("/transformed-file/:name", ({ name }, { config }) => streamAndTransformFile(name, config));
```

## Common Mistakes and Gotchas
- Unlike a standard Node.js server, **Akamai Functions does not expose a global `process.env`**; all configuration must be read via `Variables.get`.  
- Unlike the browser `fetch` API, the **`event.respondWith`** call must be used inside the `fetch` event listener; returning a value from the listener does **not** send a response.  
- Unlike typical S3 SDK usage, the **`Body`** returned by `GetObjectCommand` is a **`ReadableStream`**, not a Buffer; you must pipe it directly to a `Response` or through a `TransformStream`.  
- Unlike generic outbound networking, Akamai Functions **blocks all outbound traffic unless the host pattern is listed** in `allowed_outbound_hosts`; forgetting the trailing wildcard (`'https://*'`) will cause request failures.  
- Unlike regular TypeScript projects, the **runtime does not support dynamic `import()`**; all imports must be static at the top of the file.  
- Unlike a full Node environment, **global constructors like `TransformStream`, `TextEncoder`, and `TextDecoder` are available, but `require` is not**; use ES module syntax.  

## Version and Compatibility Notes
- Requires **Spin template `http-ts`** and the **Akamai Functions preview** (public preview access).  
- The application must be built with **`spin build`** to compile to WebAssembly before deployment.  
- The `@aws-sdk/client-s3` package version must be compatible with the **ESM target** used by Spin (no CommonJS only features).  
- Deployment commands (`spin aka deploy`) accept variables via `--variable name=value`; variable names are case‑sensitive and must match those defined in `spin.toml`.  
- Outbound host pattern in `spin.toml` should be written as `allowed_outbound_hosts = ['https://*']` to allow any HTTPS endpoint under the specified domain.  