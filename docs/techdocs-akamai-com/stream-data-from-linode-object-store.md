# Source: https://techdocs.akamai.com/akamai-functions/docs/stream-data-from-linode-object-store
Date: 2026-06-05T09:02:44.923379
Model: gpt-oss:120b-cloud
## Runtime Constraints
- **Node.js version** – Must run on Node 22 or later.  
- **Outbound network** – Components may only contact hosts listed in `allowed_outbound_hosts`. Example: `allowed_outbound_hosts = ['https://.']`.  
- **Application variables** – All variables defined under `[variables]` are required at runtime; missing or empty values must cause a `500` response.  
- **Supported modules** – Only the following NPM packages are guaranteed to be available: `@aws-sdk/client-s3`, `@spinframework/spin-variables`, `itty-router`. Importing any other third‑party module may fail.  
- **Execution environment** – Code is compiled to WebAssembly and executed in the Akamai Functions sandbox; standard Node.js APIs such as `fs`, `net`, or `child_process` are not available.  

---

## Supported APIs and Syntax
```
AutoRouter()                         — creates a router instance (itty-router)
json(data)                           — returns a Response with JSON‑encoded body
S3Client(config)                     — AWS S3 client; config: { region, endpoint, credentials }
GetObjectCommand(input)               — command to retrieve an object; input: { Bucket, Key }
ListObjectsV2Command(input)          — command to list objects; input: { Bucket }
Variables.get(name)                  — returns the value of a Spin variable (string)
TransformStream({ transform })       — creates a TransformStream; transform(chunk, controller)
addEventListener('fetch', handler)  — registers the entry point for incoming requests
router.fetch(request, options)       — routes a request; options may include custom fields (e.g., {config})
Response(body?, init?)               — standard Fetch API response object
new TextDecoder()                    — decodes Uint8Array to string
new TextEncoder()                    — encodes string to Uint8Array
```

---

## Required Patterns  

### 1. Load and validate Spin variables, then start the router
```ts
// @ts-ignore
addEventListener('fetch', async (event: FetchEvent) => {
  const endpoint          = Variables.get("endpoint");
  const accessKeyId       = Variables.get("access_key_id");
  const secretAccessKey   = Variables.get("secret_access_key");
  const bucketName        = Variables.get("bucket_name");
  const region            = Variables.get("region");

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

### 2. Router definition with typed config
```ts
interface Config {
  region: string;
  endpoint: string;
  accessKeyId: string;
  secretAccessKey: string;
  bucketName: string;
}

let router = AutoRouter()
  .get("/files",               async (_, {config}) => await listFiles(config))
  .get("/files/:name",         async ({name}, {config}) => await streamFile(name, config))
  .get("/transformed-files/:name", async ({name}, {config}) => await streamAndTransformFile(name, config));
```

### 3. List files implementation
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

### 4. Stream raw file implementation
```ts
const streamFile = async (name: string, config: Config): Promise<Response> => {
  const s3 = new S3Client({
    region: config.region,
    endpoint: config.endpoint,
    credentials: {
      accessKeyId: config.accessKeyId,
      secretAccessKey: config.secretAccessKey,
    },
  });

  try {
    const { Body } = await s3.send(new GetObjectCommand({ Bucket: config.bucketName, Key: name }));
    return new Response(Body as ReadableStream, { status: 200 });
  } catch (e: any) {
    return new Response(`error : ${e.message}`, { status: 500 });
  }
};
```

### 5. Stream with uppercase transformation
```ts
const dec = new TextDecoder();
const enc = new TextEncoder();

const streamAndTransformFile = async (name: string, config: Config): Promise<Response> => {
  const upperCaseTransform = new TransformStream({
    transform(chunk, controller) {
      const txt = dec.decode(chunk, { stream: true });
      controller.enqueue(enc.encode(txt.toUpperCase()));
    },
  });

  const s3 = new S3Client({
    region: config.region,
    endpoint: config.endpoint,
    credentials: {
      accessKeyId: config.accessKeyId,
      secretAccessKey: config.secretAccessKey,
    },
  });

  try {
    const { Body } = await s3.send(new GetObjectCommand({ Bucket: config.bucketName, Key: name }));
    const transformed = (Body as ReadableStream).pipeThrough(upperCaseTransform);
    return new Response(transformed, { status: 200 });
  } catch (e: any) {
    return new Response(`error : ${e.message}`, { status: 500 });
  }
};
```

---

## Common Mistakes and Gotchas
- **Unlike standard Node.js, Akamai Functions does not provide a filesystem.** Attempting to use `fs` or read/write files will fail; all I/O must be performed via streams or network calls.  
- **Unlike a typical Express app, the router is created with `itty-router` and invoked via `router.fetch(request, {config})`.** Directly calling route handlers without `router.fetch` bypasses the built‑in request parsing.  
- **Unlike a regular browser environment, outbound network calls are restricted to hosts listed in `allowed_outbound_hosts`.** Forgetting to add the S3 endpoint will cause request failures.  
- **Unlike regular Node, environment variables are accessed via `Variables.get` and must be prefixed with `SPIN_VARIABLE_` when exported locally.** Using `process.env` will not retrieve the values.  
- **Unlike typical TypeScript projects, the entry point must be registered with `addEventListener('fetch', …)`; omitting this listener results in no request handling.**  

---

## Version and Compatibility Notes
- **Node.js** – Minimum version **22** (as required by the Spin runtime).  
- **Spin template** – `http-ts` (TypeScript HTTP).  
- **Required NPM packages** – `@aws-sdk/client-s3` (S3‑compatible operations), `@spinframework/spin-variables` (variable access), `itty-router` (routing).  
- **Akamai Functions public preview** – Access must be granted via the onboarding form; the SDK and runtime are subject to preview‑only availability.  
- **Variable secret handling** – Variables marked `secret = true` are stored encrypted; they must be referenced exactly as defined (`secret_access_key`).  
- **Outbound host pattern** – The `allowed_outbound_hosts` entry uses a wildcard pattern (`'https://.'`); ensure the trailing dot is present.  