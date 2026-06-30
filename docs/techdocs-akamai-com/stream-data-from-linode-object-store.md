# Source: https://techdocs.akamai.com/akamai-functions/docs/stream-data-from-linode-object-store
Date: 2026-06-30T09:39:14.062544
Model: gpt-oss:120b-cloud
## Runtime Constraints
- **Node version** – The function must run on **Node.js 22 or later**.  
- **Web‑only APIs** – Only Web standard APIs are available; native Node modules such as `fs`, `net`, `child_process`, etc., are **not supported**.  
- **Outbound network whitelist** – All external requests must be permitted via the `allowed_outbound_hosts` array in `spin.toml`.  
- **Required variables** – Every variable declared under `[variables]` is required; if any is missing or empty the function must return **HTTP 500**.  
- **Wasm bundle** – The code is compiled to WebAssembly; only packages that can be bundled to WASM (e.g., `@aws-sdk/client-s3`, `@spinframework/spin-variables`, `itty-router`) may be used.  
- **No dynamic import of non‑Wasm modules** – Importing modules that rely on Node‑only features will cause a build failure.  

## Supported APIs and Syntax
| API / Construct | Signature | Description |
|-----------------|-----------|-------------|
| `AutoRouter()` | `new AutoRouter(): Router` | Creates an itty‑router instance for defining HTTP routes. |
| `router.get()` | `router.get(path: string, handler: (request: Request, ctx: {config: Config}) => Promise<Response>)` | Registers a GET route. |
| `json()` | `json(data: any): Response` | Returns a `Response` with `Content‑Type: application/json` and the JSON‑encoded body. |
| `S3Client()` | `new S3Client({ region: string, endpoint: string, credentials: { accessKeyId: string, secretAccessKey: string } })` | AWS SDK S3 client configured for Linode Object Storage. |
| `ListObjectsV2Command` | `new ListObjectsV2Command(input: { Bucket: string })` | Command that lists objects in a bucket. |
| `GetObjectCommand` | `new GetObjectCommand(input: { Bucket: string, Key: string })` | Command that retrieves a single object. |
| `TransformStream` | `new TransformStream({ transform(chunk: Uint8Array, controller: TransformStreamDefaultController): void })` | Creates a streaming transform; used here to convert text to uppercase. |
| `TextDecoder` | `new TextDecoder(): TextDecoder` | Decodes UTF‑8 bytes to string. |
| `TextEncoder` | `new TextEncoder(): TextEncoder` | Encodes string to UTF‑8 bytes. |
| `Variables.get` | `Variables.get(name: string): string | undefined` | Reads a Spin variable (environment‑injected). |
| `addEventListener('fetch')` | `addEventListener('fetch', (event: FetchEvent) => void)` | Registers the entry point for incoming HTTP requests. |
| `event.respondWith` | `event.respondWith(response: Response): void` | Sends the response for the current request. |
| `router.fetch` | `router.fetch(request: Request, ctx?: any): Promise<Response>` | Executes the router logic with optional context (e.g., config). |
| `new Response` | `new Response(body?: BodyInit, init?: ResponseInit): Response` | Constructs an HTTP response. |
| `ReadableStream.pipeThrough` | `(stream as ReadableStream).pipeThrough(transform: TransformStream): ReadableStream` | Pipes a readable stream through a transform. |

## Required Patterns
### 1. Load variables, validate, and invoke the router
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

### 2. List files handler
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

  try {
    const { Contents } = await s3.send(new ListObjectsV2Command({ Bucket: config.bucketName }));
    const files = Contents?.map(f => f.Key) || [];
    return json({ files });
  } catch (e) {
    console.log(e);
    return new Response(JSON.stringify(e), { status: 500 });
  }
};
```

### 3. Stream raw file handler
```ts
const streamFile = async (name: string, config: Config): Promise<Response> => {
  const s3 = new S3Client({ /* same as above */ });
  try {
    const { Body } = await s3.send(new GetObjectCommand({ Bucket: config.bucketName, Key: name }));
    return new Response(Body as ReadableStream, { status: 200 });
  } catch (e: any) {
    return new Response(`error : ${e.message}`, { status: 500 });
  }
};
```

### 4. Upper‑case transform stream handler
```ts
const streamAndTransformFile = async (name: string, config: Config): Promise<Response> => {
  const upperCaseTransform = new TransformStream({
    transform(chunk, controller) {
      const txt = dec.decode(chunk, { stream: true });
      controller.enqueue(enc.encode(txt.toUpperCase()));
    },
  });

  const s3 = new S3Client({ /* same as above */ });
  try {
    const { Body } = await s3.send(new GetObjectCommand({ Bucket: config.bucketName, Key: name }));
    const transformed = (Body as ReadableStream).pipeThrough(upperCaseTransform);
    return new Response(transformed, { status: 200 });
  } catch (e: any) {
    return new Response(`error : ${e.message}`, { status: 500 });
  }
};
```

## Common Mistakes and Gotchas
- **Unlike a typical Node.js server, Akamai Functions do not expose the `fs` module** – attempting to read files from the local filesystem will fail.  
- **Unlike a regular browser environment, outbound HTTP calls are blocked unless the host is listed in `allowed_outbound_hosts`** – forgetting to add `https://<your‑linode‑endpoint>` results in connection errors.  
- **Unlike a plain TypeScript project, missing any required Spin variable causes the function to return HTTP 500** – always validate variables before proceeding.  
- **Unlike the AWS SDK for browsers, the S3 client’s `Body` is a `ReadableStream` that must be passed directly to `Response` or piped through a `TransformStream`; treating it as a Buffer will cause type errors.**  
- **Unlike a typical Express app, route registration uses `router.get()` from `itty-router`; using Express‑style middleware will not work.**  

## Version and Compatibility Notes
- **Node.js 22+** is mandatory for the Spin build process.  
- The tutorial targets the **public preview of Akamai Functions**; features may change before GA.  
- Deployment uses the **`spin aka deploy`** command; variables are supplied via `--variable name=value` flags.  
- The application must be built with `spin build` (produces a WASM bundle) before `spin up` or `spin aka deploy`.  
- All referenced packages (`@aws-sdk/client-s3`, `@spinframework/spin-variables`, `itty-router`) are compatible with the current Akamai Functions runtime as of the preview release.