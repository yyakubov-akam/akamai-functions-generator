---
updatedAt: 2026-06-12T01:15:19.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further.

# Stream data from Linode Object Store

This tutorial shows you how to build a Spin application in TypeScript that streams data from [Linode Object Storage.](https://techdocs.akamai.com/cloud-computing/docs/object-storage) You'll learn how to configure Spin variables for object storage, set up routes to list and stream files, and apply real-time transformations using the `@aws-sdk/client-s3` package. Once we’ve built and tested the app locally, we’ll deploy it to Akamai Functions.

# Prerequisites

Before you start this tutorial, make sure you have the following prerequisites. You can also follow the steps in the [Quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart) guide to get up and running with Akamai Functions in less than two minutes.

* Sign up for the public preview so you can [login](https://techdocs.akamai.com/akamai-functions/docs/quickstart#login-to-akamai-functions) to Akamai Functions. If you haven’t already requested access, please complete the [Onboarding form](https://fibsu0jcu2g.typeform.com/fwf-preview?typeform-source=developer.fermyon.com).
* [Install Spin](https://techdocs.akamai.com/akamai-functions/docs/quickstart#install-spin) and the [aka Plugin for Spin](https://techdocs.akamai.com/akamai-functions/docs/quickstart#install-the-aka-plugin-for-spin).
* [Node.js](https://nodejs.org/en) (version `22` or later).

We’ll use an existing Linode Object Storage bucket. If you want to use your own instance, permissions for deploying a new Object Storage bucket to Linode are required. For more information, go to the [Object Storage](https://techdocs.akamai.com/cloud-computing/docs/getting-started-with-object-storage) guide.

# Introduction

Linode Object Storage is an S3-compatible cloud storage service designed for storing and serving large amounts of unstructured data. We'll use the `@aws-sdk/client-s3` NPM package to interact with Linode’s Object Storage in our Spin application.

The Spin application will expose three routes:

* `GET /files`. Lists all files in a Linode Object Storage bucket.
* `GET /file/:name`. Streams the contents of a specified file.
* `GET /transformed-file/:name`. Streams the file’s contents while transforming text to uppercase.

[block:image]
{
  "images": [
    {
      "image": [
        "https://techdocs.akamai.com/akamai-functions/img/functions-stream-data-object-storage-v2.png",
        null,
        "Linode Object Storage is an S3-compatible cloud storage service workflow"
      ],
      "align": "center",
      "sizing": "900px",
      "border": true
    }
  ]
}
[/block]

# Step 1: Set up the Spin application

Run the following commands to initialize a new Spin application using the `http-ts` template.

```shell
spin new -E akamai-functions -t http-ts -a linode-streaming-app

cd linode-streaming-app
```

# Step 2: Install AWS S3 Client SDK

Install the `@aws-sdk/client-s3` dependency using `npm`.

```shell
npm install @spinframework/spin-variables @aws-sdk/client-s3
```

# Step 3: Configure Spin application variables

1. Edit the application manifest (`spin.toml`) and introduce application variables to ensure that the application configuration can be changed without having to modify the actual application code.

```
[variables]  
region = { required = true }  
endpoint = { required = true }  
bucket_name = { required = true }  
access_key_id = { required = true }  
secret_access_key = { required = true, secret = true}
```

2. Update the component configuration and grant the component access to the desired variables. To do so, add a new table to `spin.toml`.

```
[component.linode-streaming-app.variables]  
region = ""  
endpoint = "https://"  
bucket_name = ""  
access_key_id = ""  
secret_access_key = ""
```

3. Allow the `linode-streaming-app` component doing outbound network requests towards our Linode bucket. Update the component configuration and set the `allowed_outbound_hosts` property as shown in the following snippet.

```
[component.linode-streaming-app]
# ...
allowed_outbound_hosts = ['https://.']
```

With the updated application manifest in place, we can move on and start implementing the Spin application.

# Step 4: Implement the Spin application

1. Replace the contents of the `src/index.ts`file using the TypeScript code shown in the code snippets in this section.

```typescript
import { AutoRouter, json } from 'itty-router';
import { S3Client, GetObjectCommand, ListObjectsV2Command } from '@aws-sdk/client-s3';
import * as Variables from '@spinframework/spin-variables';

const dec = new TextDecoder();
const enc = new TextEncoder();

let router = AutoRouter();

// a custom config interface holding all configuration data
interface Config {
    region: string,
    endpoint: string,
    accessKeyId: string,
    secretAccessKey: string,
    bucketName: string
}

router
    .get("/files", async (_, {config}) => await listFiles(config))
    .get('/files/:name', async ({ name }, {config}) => await streamFile(name, config))
    .get("/transformed-files/:name", async ({ name }, {config}) => await streamAndTransformFile(name, config));

//@ts-ignore
addEventListener('fetch', async (event: FetchEvent) => {
  
				// load application variables
    const endpoint = Variables.get("endpoint");
    const accessKeyId = Variables.get("access_key_id");
    const secretAccessKey = Variables.get("secret_access_key");
    const bucketName = Variables.get("bucket_name");
    const region = Variables.get("region");

 		// if any variable is not specified or empty, terminate and send a HTTP 500
    if (!endpoint || !accessKeyId || !secretAccessKey || !bucketName || !region) {
        return new Response("Application not configured correctly", { status: 500 });
    }

    // Pass the Configuration to the Router
    event.respondWith(router.fetch(event.request, {
        config: {
            endpoint,
            accessKeyId,
            secretAccessKey,
            bucketName,
            region
        } as Config
    }));
});
```

2. Add the `listFiles` function to load a list of all files stored in the S3 bucket and return them as JSON array.

```typescript
const listFiles = async (config: Config): Promise<Response> => {
    // construct a new S3 client using configuration data
    const s3 = new S3Client({
        region: config.region,
        endpoint: config.endpoint,
        credentials: {
            accessKeyId: config.accessKeyId,
            secretAccessKey: config.secretAccessKey,
        }
    });
    try {
		const input = { Bucket: config.bucketName };
		// load metadata of all files in our S3 bucket
        const { Contents } = await s3.send(new ListObjectsV2Command(input));
		// grab all files names, fallback to an empty array
        const files = Contents?.map((file) => file.Key) || [];
		// return list of files as JSON
        return json({ files });
    } catch (error) {
        console.log(error);
        return new Response(JSON.stringify(error), { status: 500 })
    }
}
```

3. Add the `streamFile` function to stream a particular file from the S3 bucket as it is.

```typescript
const streamFile = async (name: string, config: Config): Promise<Response> => {
    const s3 = new S3Client({
        region: config.region,
        endpoint: config.endpoint,
        credentials: {
            accessKeyId: config.accessKeyId,
            secretAccessKey: config.secretAccessKey,
        }
    });

    try {
		// construct command input for receiving the desired file
        const input = { Bucket: config.bucketName, Key: name };
		// request the desired file
        const { Body } = await s3.send(new GetObjectCommand(input));
		// pipe the file contents to the response
        return new Response(Body as ReadableStream, {
            status: 200,
        });

    } catch (error: any) {
        return new Response(`error : ${error.message}`, { status: 500 });
    }
}
```

4. Add the `streamAndTransformFile` function to define and apply a `TransformStream` to convert the entire contents of a particular file to uppercase.

```typescript
const streamAndTransformFile = async (name: string, config: Config): Promise<Response> => {
	// define the transform operation
    const upperCaseTransform = new TransformStream({
        transform(chunk, controller) {
			// decode the byte array using TextDecoder
            const txt = dec.decode(chunk, { stream: true });
			// apply transformation and encode the transformed chunk again
            controller.enqueue(enc.encode(txt.toUpperCase()));
        }
    });

    const s3 = new S3Client({
        region: config.region,
        endpoint: config.endpoint,
        credentials: {
            accessKeyId: config.accessKeyId,
            secretAccessKey: config.secretAccessKey,
        }
    });

    try {
        const input = { Bucket: config.bucketName, Key: name };
        const { Body } = await s3.send(new GetObjectCommand(input));
		// pipe the file contents through the custom transformation
        const transformed = (Body as ReadableStream).pipeThrough(upperCaseTransform);
		// pipe the transformed stream to the response
        return new Response(transformed, {
            status: 200,
        });
    } catch (error: any) {
        return new Response(`error : ${error.message}`, { status: 500 });
    }
}
```

# Step 5: Compile and run the Spin application

Use the `spin build` command to compile the source code down to WebAssembly and `spin up`to run it on our local machine.

All of our variables are marked required, so we need to specify them before running the application. There are different ways to do this. In this example we’ll simply export all necessary variables before invoking `spin up`.

> 📘
>
> As mentioned at the beginning of this tutorial, we’ll use a pre-existing S3 bucket. The access key generated for this tutorial has **ReadOnly** permissions. If you want to use your own instance of Linode Object Storage, you need to provide your individual values when setting the application variables in the following snippet.

```shell
spin build

export SPIN_VARIABLE_REGION=se  
export SPIN_VARIABLE_ENDPOINT=se-sto-1.linodeobjects.com  
export SPIN_VARIABLE_ACCESS_KEY_ID=LOJ4PC86TOZX5ABQKA4E  
export SPIN_VARIABLE_SECRET_ACCESS_KEY=KhdjljQCAarOoNEpVA9PfcbL9u4qUN4cgtoMVnMQ  
export SPIN_VARIABLE_BUCKET_NAME=fwf-tech-docs-tutorials

spin up
```

When you run `spin up` it should generate an output similar to the following, indicating that our application is now served on `http://localhost:3000`.

```shell
Logging component stdio to ".spin/logs/"

Serving http://127.0.0.1:3000
Available Routes:
  linode-streaming-app: http://127.0.0.1:3000 (wildcard)
```

# Step 6: Test the Endpoints

Use `curl` to test the different endpoints exposed by our Spin application.

## List files

```curl
curl http://127.0.0.1:3000/files
```

```
{"files":["large.txt","small.txt","tiny.txt"]}
```

## Get a specific file

```curl
curl http://127.0.0.1:3000/file/tiny.txt
```

```
lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.
```

## Get a transformed file in uppercase text

```curl
curl http://127.0.0.1:3000/transformed-file/tiny.txt
```

```shell
LOREM IPSUM DOLOR SIT AMET, CONSETETUR SADIPSCING ELITR, SED DIAM NONUMY EIRMOD TEMPOR INVIDUNT UT LABORE ET DOLORE MAGNA ALIQUYAM ERAT, SED DIAM VOLUPTUA.
```

# Step 7: Deploy to Akamai Functions

Now that the application has been successfully tested on our local machine, we can use the [`spin aka` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka) to deploy the application to Akamai Functions.

> 📘
>
> As mentioned at the beginning of this tutorial, we’ll use a pre-existing S3 bucket. The access key generated for this tutorial has **ReadOnly** permissions. If you want to use your own instance of Linode Object Storage, you need to provide your individual values when setting the application variables in the following snippet.

```shell
spin aka deploy --variable region=se  
  --variable endpoint=se-sto-1.linodeobjects.com  
  --variable access_key_id=LOJ4PC86TOZX5ABQKA4E  
  --variable secret_access_key=KhdjljQCAarOoNEpVA9PfcbL9u4qUN4cgtoMVnMQ  
  --variable bucket_name=fwf-tech-docs-tutorials
```

Deployment to Akamai Functions will take a couple of seconds, once the deployment is finished, you'll see output similar to this.

```shell
Name of new app: linode-streaming-app
Creating new app linode-streaming-app in account your-account
Note: If you would instead like to deploy to an existing app, cancel this deploy and link this workspace to the app with `spin aka app link`
OK to continue? yes
Workspace linked to app linode-streaming-app
Waiting for app to be ready... ready

App Routes:
- linode-streaming-app: https://ec8a19d8-6d10-4056-bb69-cc864306b489.aka.akamai.tech (wildcard)
```

# Conclusion

You've successfully built a Spin application that uses TypeScript to integrate with Linode Object Storage. This app uses streaming to list files, stream file content, and apply transformations. To extend this application further you can add add authentication or additional transformations.

# Sibling pages

* [Integrate with Property Manager](https://techdocs.akamai.com/akamai-functions/docs/integrate-with-property-manager.md)
* [Query relational databases: MySQL](https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-mysql.md)
* [Query relational databases: PostgreSQL](https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-postgresql.md)
* [Build a Supabase cache proxy](https://techdocs.akamai.com/akamai-functions/docs/build-a-supabase-cache-proxy.md)
* [Schedule tasks with cron jobs in Spin (Tech Preview)](https://techdocs.akamai.com/akamai-functions/docs/schedule-tasks-with-cron-jobs-in-spin.md)
* [Use the Key Value store](https://techdocs.akamai.com/akamai-functions/docs/use-the-key-value-store.md)