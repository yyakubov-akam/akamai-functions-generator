# Source: https://techdocs.akamai.com/akamai-functions/docs/stream-data-from-linode-object-store
Date: 2026-08-17T08:41:40.994270
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Must use Node.js version 22 or later.
- Must compile source code to WebAssembly using `spin build` before deployment.
- Must configure `allowed_outbound_hosts` in `spin.toml` to permit outbound network requests (e.g., to S3 endpoints).
- Application variables marked as `required` in `spin.toml` must be provided at runtime; failure to provide them results in an HTTP 500 response.
- The `Body` property returned from `GetObjectCommand` is a stream that must be cast to `ReadableStream` to be used in a `Response`.

## Supported APIs and Syntax

`AutoRouter` — Routing middleware for handling HTTP requests.
`json` — Helper function to create JSON responses.
`S3Client` — AWS S3 client for interacting with S3-compatible storage services.
`GetObjectCommand` — Command to retrieve an object from S3.
`ListObjectsV2Command` — Command to list objects in an S3 bucket.
`Variables.get(key)` — Retrieves environment variable values defined in `spin.toml`.
`addEventListener('fetch', handler)` — Entry point for Spin applications to handle incoming HTTP requests.

## Required Patterns

### Variable Loading and Validation
Load configuration variables using `@spinframework/spin-variables` and validate that they are not empty before proceeding.

```typescript
import * as Variables from '@spinframework/spin-variables';

// load application variables
const endpoint = Variables.get("endpoint");
const accessKeyId = Variables.get("access_key_id");
const secretAccessKey = Variables.get("secret_access_key");
const bucketName = Variables.get("bucket_name");
const region = Variables.get("region");

// validate required variables
if (!endpoint || !accessKeyId || !secretAccessKey || !bucketName || !region) {
    return new Response("Application not configured correctly", { status: 500 });
}
```

### S3 Client Initialization
Construct the `S3Client` using the configuration variables, specifically setting the `endpoint`, `region`, and `credentials`.

```typescript
import { S3Client } from '@aws-sdk/client-s3';

const s3 = new S3Client({
    region: config.region,
    endpoint: config.endpoint,
    credentials: {
        accessKeyId: config.accessKeyId,
        secretAccessKey: config.secretAccessKey,
    }
});
```

### Streaming File Response
Cast the `Body` from the S3 command result to `ReadableStream` to pipe it directly to the HTTP response.

```typescript
import { GetObjectCommand } from '@aws-sdk/client-s3';

// ... inside request handler
const { Body } = await s3.send(new GetObjectCommand(input));
return new Response(Body as ReadableStream, {
    status: 200,
});
```

### Transforming Streams
Use `pipeThrough` with a `TransformStream` to modify data as it flows from the source to the response.

```typescript
import { TransformStream } from 'stream';

const upperCaseTransform = new TransformStream({
    transform(chunk, controller) {
        const txt = dec.decode(chunk, { stream: true });
        controller.enqueue(enc.encode(txt.toUpperCase()));
    }
});

const transformed = (Body as ReadableStream).pipeThrough(upperCaseTransform);
return new Response(transformed, { status: 200 });
```

## Common Mistakes and Gotchas

- Unlike standard Node.js environments, Akamai Functions requires explicit configuration of `allowed_outbound_hosts` in `spin.toml` to permit network requests.
- The `Body` property from `@aws-sdk/client-s3` commands is not automatically a standard Node.js stream compatible with all contexts; it must be explicitly cast to `ReadableStream`.
- Variable keys in `spin.toml` (e.g., `access_key_id`) must match the string keys passed to `Variables.get()` in the code exactly.

## Version and Compatibility Notes

- Requires Node.js version 22 or later.
- Requires the `@spinframework/spin-variables` and `@aws-sdk/client-s3` packages.
- Deployment target is Akamai Functions (Spin/Fermyon runtime).