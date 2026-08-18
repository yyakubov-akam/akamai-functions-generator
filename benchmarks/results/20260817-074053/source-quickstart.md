---
updatedAt: 2026-07-21T20:45:33.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further.

# Quickstart

Follow the steps in this Quickstart guide to get up and running with Akamai Functions in less than two minutes. Akamai Functions is the platform for running [Spin](https://spinframework.dev/) applications on Akamai Cloud.

> 📘
>
> To complete this tutorial you need access to the public preview of Akamai Functions. If you haven’t already requested access, please [complete this form](https://fibsu0jcu2g.typeform.com/fwf-preview). The Akamai Functions team will review your request and follow up shortly.

[block:image]
{
  "images": [
    {
      "image": [
        "https://techdocs.akamai.com/akamai-functions/img/functions-quick-start-v2.png",
        null,
        "Akamai Functions dev workflow"
      ],
      "align": "center",
      "sizing": "900px",
      "border": true
    }
  ]
}
[/block]

# Install Spin

[Spin](https://spinframework.dev/) is an open-source project you can use to build, run, and deploy Spin applications. It's both a CLI tool and a runtime. It provides SDKs for a variety of programming languages, including, but not limited to, Rust, Go, JavaScript and TypeScript.

<AkamaiTabs>
<AkamaiTab title="Linux">

### Linux

The Spin project provides installers that are supported on Linux (amd64).

1. Download the `spin` binary using the `install.sh` script hosted on this site.

```curl
curl -fsSL https://developer.fermyon.com/downloads/fwf_install.sh | bash
```

2. Then move the `spin` binary somewhere in your path, so you can run it from anywhere. For example:

```shell
sudo mv ./spin /usr/local/bin/spin
```

</AkamaiTab>

<AkamaiTab title="macOS">

### macOS

The Spin project provides installers that are supported on macOS (amd64 and arm64).

1. Download the `spin` binary using the `install.sh` script hosted on this site:

```curl
curl -fsSL https://developer.fermyon.com/downloads/fwf_install.sh | bash
```

2. Then move the `spin` binary somewhere in your path, so you can run it from anywhere. For example:

```shell
sudo mv ./spin /usr/local/bin/spin
```

</AkamaiTab>

<AkamaiTab title="Windows">

### Windows

The Spin project provides installers that are supported on Windows (amd64).

1. Download the [Windows binary release of Spin](https://github.com/spinframework/spin/releases/tag/v3.6.2) from GitHub.
2. Unzip the binary release and place the `spin.exe` in your system path.
3. Install the Spin templates or plugins for the programming language that you want to use. For a starter list, see the [Installing Templates and Plugins](https://spinframework.dev/v3/install#installing-templates-and-plugins) section in the [Spin](https://spinframework.dev/v3/index) documentation.

</AkamaiTab>

</AkamaiTabs>

To find the Spin version installed on your machine run, `spin --version`.

# Install the `aka` plugin for Spin

To interact with Akamai Functions, you need to install the Akamai Functions for Akamai Spin plugin, `aka`. Use this command to install the plugin.

```shell
spin plugin install aka
```

If you’ve previously installed the `aka` plugin, take a moment to upgrade it to ensure compatibility with the latest features and fixes.

```shell
spin plugins update  
spin plugins upgrade aka
```

You can learn more about managing Spin plugins in this [article](https://spinframework.dev/v3/managing-plugins.md).

> 👍
>
> Go to the [aka spin command reference](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference) for a complete list of supported commands.

# Install language specific tooling

With Spin you can build applications using a wide variety of different programming languages. This quickstart, contains instructions and samples for JavaScript, TypeScript and Rust.

Follow these instructions to install language specific tooling on your machine.

> 👍
>
> Go to, [WebAssembly language support matrix](https://techdocs.akamai.com/akamai-functions/docs/webassembly-language-support-matrix) for more information about the supported languages.

<AkamaiTabs>
 <AkamaiTab title="JavaScript">

### JavaScript

To build Spin apps with JavaScript, you need [Node.js](https://nodejs.org/en) installed on your system. Head over to <https://nodejs.org/en/download>, to download Node.js.

Once Node.js is installed on your machine, you can check its version using the following command.

```shell
node --version  
v22.13.0
```

We recommend Node.js version 22 (or newer).

</AkamaiTab>

<AkamaiTab title="TypeScript">

### TypeScript

To build Spin apps with TypeScript, you need [Node.js](https://nodejs.org/en) installed on your system. Head over to <https://nodejs.org/en/download>, to download Node.js.

Once Node.js is installed on your machine, you can check its version using the following command.

```shell
node --version  
v22.13.0
```

We recommend Node.js version 22 (or newer).

</AkamaiTab>

<AkamaiTab title="Rust">

### Rust

To build Spin apps with Rust, you need to install Rust tooling on your machine. Head over to <https://www.rust-lang.org/tools/install>, to find detailed installation instructions for your operating system.

Once Rust tooling is installed, you’ll need the `wasm32-wasip1` target for Rust.

```shell
rustup target add wasm32-wasip1
```

</AkamaiTab>

<AkamaiTab title="TinyGo">

### TinyGo

You’ll need the TinyGo compiler, as the standard Go compiler does not yet support WASI exports. See the [TinyGo installation guide](https://tinygo.org/getting-started/install/).

</AkamaiTab>

</AkamaiTabs>

# Create a new Spin application

Next we’ll prepare an application with Spin. There are code samples below for you to use, but you can write an [app from scratch](https://spinframework.dev/v3/writing-apps) or use an [existing template](https://spinframework.dev/hub). The [Spin Hub](https://spinframework.dev/hub) has many reference examples and templates. You can also find several code samples, sorted by use case in the [Akamai Functions GitHub repo](https://github.com/akamai-developers/akamai-functions-samples).

<AkamaiTabs>
<AkamaiTab title="JavaScript">

## JavaScript

```shell
spin new -E akamai-functions -t http-js --accept-defaults hello-spin
```

The `http-js` template creates the application boilerplate for you. Once it's finished, change to the application directory (`hello-spin`).

```shell
cd hello-spin
```

From within the application directory, install the necessary dependencies using your package manager of choice (we'll use `npm` here).

```shell
npm install
```

The `http-js` template generates an idiomatic JavaScript application. Take a few seconds and explore the source code generated by the template in `src/index.js`.

```javascript
// For AutoRouter documentation refer to <https://itty.dev/itty-router/routers/autorouter>  
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

// Route ordering matters, the first route that matches will be used  
// Any route that does not return will be treated as a middleware  
// Any unmatched route will return a 404  
router  
    .get("/", () => new Response("hello universe"))  
    .get('/hello/:name', ({ name }) => `Hello, ${name}!`)

addEventListener('fetch', async (event) => {  
    event.respondWith(router.fetch(event.request));  
});
```

</AkamaiTab>
<AkamaiTab title="TypeScript">

## TypeScript

```shell
spin new -E akamai-functions -t http-ts --accept-defaults hello-spin
```

The `http-ts` template creates the application boilerplate for you. Once it's finished, change to the application directory (`hello-spin`).

```shell
cd hello-spin
```

From within the application directory, install the necessary dependencies using your package manager of choice (we'll use `npm` here).

```shell
npm install
```

The `http-ts` template generates an idiomatic TypeScript application. Take a few seconds and explore the source code generated by the template in `src/index.ts`.

```typescript
// For AutoRouter documentation refer to <https://itty.dev/itty-router/routers/autorouter>  
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

// Route ordering matters, the first route that matches will be used  
// Any route that does not return will be treated as a middleware  
// Any unmatched route will return a 404  
router  
    .get("/", () => new Response("hello universe"))  
    .get('/hello/:name', ({ name }) => `Hello, ${name}!`)

//@ts-ignore  
addEventListener('fetch', async (event: FetchEvent) => {  
    event.respondWith(router.fetch(event.request));  
});
```

</AkamaiTab>
<AkamaiTab title="Rust">

## Rust

```shell
spin new -E akamai-functions -t http-rust --accept-defaults hello-spin
```

The `http-rust` template creates the application boilerplate for you. Once it's finished, change to the application directory (`hello-spin`).

```shell
cd hello-spin
```

The `http-rust` template generates an idiomatic Rust application. Take a few seconds and explore the source code generated by the template in `src/lib.rs`.

```rust
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;

/// A simple Spin HTTP component.
#[http_component]
fn handle_hello_spin(req: Request) -> anyhow::Result<impl IntoResponse> {
    println!("Handling request to {:?}", req.header("spin-full-url"));
    Ok(Response::builder()
        .status(200)
        .header("content-type", "text/plain")
        .body("Hello, Akamai")
        .build())
}
```

</AkamaiTab>
<AkamaiTab title="TinyGo">

## TinyGo

```shell
spin new -E akamai-functions -t http-go --accept-defaults hello-spin
```

The `http-go` template creates the application boilerplate for you. Once it's finished change to the application directory (`hello-spin`).

```shell
cd hello-spin
```

The `http-go` template generates an idiomatic Go(lang) application. Take a few seconds and explore the source code generated by the template in `main.go`.

```go
package main

import (
	"fmt"
	"net/http"

	spinhttp "github.com/spinframework/spin/sdk/go/v2/http"
)

func init() {
	spinhttp.Handle(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/plain")
		fmt.Fprintln(w, "Hello Akamai!")
	})
}

func main() {}
```

</AkamaiTab>
</AkamaiTabs>

# Compile the application

Use the `spin build` command to compile your Spin app to WebAssembly.

```shell
spin build
```

<AkamaiTabs>

<AkamaiTab title="JavaScript">

```javascript
Building component hello-spin with `npm run build`

> hello-spin@1.0.0 build
> npx webpack --mode=production && npx mkdirp target && npx j2w -i dist.js -d combined-wit -n combined -o target/hello-spin.wasm

asset dist.js 5.93 KiB [compared for emit] [javascript module] (name: main)
orphan modules 25.5 KiB [orphan] 25 modules
./src/spin.js + 2 modules 5.95 KiB [built] [code generated]
webpack 5.97.1 compiled successfully in 66 ms
Using user provided wit in: combined-wit
Successfully written component
Finished building all Spin components
```

</AkamaiTab>
<AkamaiTab title="TypeScript">

```typescript
Building component hello-spin with `npm run build`

> hello-spin@1.0.0 build
> npx webpack --mode=production && npx mkdirp target && npx j2w -i dist.js -d combined-wit -n combined -o target/hello-spin.wasm

asset dist.js 6 KiB [emitted] [javascript module] (name: main)
orphan modules 25.4 KiB [orphan] 25 modules
./src/spin.ts + 2 modules 5.97 KiB [built] [code generated]
webpack 5.97.1 compiled successfully in 509 ms
Using user provided wit in: combined-wit
Successfully written component
Finished building all Spin components
```

</AkamaiTab>
<AkamaiTab title="Rust">

```rust
Building component hello-spin with `cargo build --target wasm32-wasip1 --release`
    Updating crates.io index
     Locking 95 packages to latest compatible versions
     ...
     Compiling hello-spin v0.1.0 (/Users/john/hello-spin)
    Finished `release` profile [optimized] target(s) in 9.89s
Finished building all Spin components
```

</AkamaiTab>
<AkamaiTab title="TinyGo">

```go TinyGo
Executing the build command for component hello-spin: tinygo build -target=wasi -gc=leaking -no-debug -o main.wasm main.go
go: downloading github.com/spinframework/spin/sdk/go v0.10.0
Finished building all Spin components
```

If the build fails, check:

- Are you in the `hello-spin` directory?
- Did you successfully install TinyGo?
- Are your versions of Go and TinyGo up to date? The Spin SDK needs TinyGo 0.27 or above.
- Set Environment Variable `CGO_ENABLED=1`. (Since the Go SDK is built using CGO, it requires the CGO_ENABLED=1 environment variable to be set.)

You can find the build command Spin runs for a component in the manifest, in the `component.(id).build` section.

```shell
[component.hello-spin.build]
command = "tinygo build -target=wasi -gc=leaking -no-debug -o main.wasm main.go"
```

</AkamaiTab>
</AkamaiTabs>

# Test the application locally

You can test your Spin apps on your local computer by using the `spin up` command anytime. The `spin up` command starts an HTTP server on your local machine (port 3000 by default) and instantiates and invokes your Spin application for every request sent to the endpoint.

```shell
spin up
```

```shell
Logging component stdio to ".spin/logs/"

Serving <http://0.0.0.0:3000>  
Available Routes:  
  hello-spin: <http://0.0.0.0:3000> (wildcard)
```

> 📘
>
> If port `3000` is already in use, you could set a different port by specifying the `--listen` flag. For example, `spin up --listen 127.0.0.1:3001`.

From within an separate terminal instance, you can use a tool like `curl` to send an HTTP request to your Spin app

```curl
curl -i http://localhost:3000/
```

```shell
HTTP/1.1 200 OK  
content-length: 14  
content-type: text/plain;charset=UTF-8  
date: Tue, 14 Jan 2025 16:10:36 GMT

Hello, Fermyon
```

You can terminate `spin up` at anytime, by pressing `CTRL+C`.

# Log in to Akamai Functions

To log in you need access to the public preview of Akamai Functions. If you haven’t already, please complete the [Onboarding form](https://fibsu0jcu2g.typeform.com/fwf-preview?typeform-source=developer.fermyon.com). Akamai Functions supports two identity providers, **Akamai Control Center** and **GitHub**. If you have an [Akamai Control Center](https://control.akamai.com/apps/home-page/#/home) account, you can log in using your user ID and password. Otherwise, you need to use GitHub. If both accounts share the same email address, they are automatically cross-linked.

The Akamai Functions team will review your onboarding request and follow up shortly.

> 👍
>
> Before you log in using your Akamai Control Center or GitHub account information make sure that you complete the following tasks.
>
> * [Install the `aka` plugin for Spin](https://techdocs.akamai.com/akamai-functions/docs/quickstart#install-the-aka-plugin-for-spin).
> * Receive the allow-listing status for Akamai Functions.
> * Request and receive access to the public preview.

1. Run the  [`spin aka login` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-login).

```shell
spin aka login
```

2. Click the link displayed in the output from the `spin aka login` command.

```shell
Go to <https://login.infra.fermyon.tech/realms/neutrino/device?user_code=BB-AA>  
and follow the prompts.

Don't worry, we'll wait here for you. You got this.
```

3. Authenticate using your Akamai Control Center credentials or your individual GitHub account.
4. Once you're logged in you need to authorize the `spin` CLI to interact with your Akamai Functions account.

# Deploy the application

You can use the [`spin aka deploy` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-deploy) to deploy the application to Akamai Functions.

```shell
spin aka deploy
```

The `spin` command runs using the Spin binary in your system path. It reads the Spin application definition file `spin.toml` in the current (`hello-spin`) directory to know what application to deploy. It will ask you for a name for the application and then it will ask for confirmation that you want to deploy.

Here's an example of a successful Spin application deployment on Akamai Functions.

```shell
Name of new app: hello-spin
Creating new app hello-spin in account your-account
Note: If you would instead like to deploy to an existing app, cancel this deploy and link this workspace to the app with `spin aka app link`
OK to continue? yes
Workspace linked to app hello-spin
Waiting for app to be ready... ready

App Routes:
- hello-spin: https://ec8a19d8-6d10-4056-bb69-cc864306b489.fwf.app (wildcard)
```

You can `CTRL+Click` on the link in the terminal window to visit the web application you just deployed.

Congratulations, you’ve now deployed your first Spin application to Akamai Functions!

# Sibling pages

* [Welcome to Akamai Functions (Limited availability)](https://techdocs.akamai.com/akamai-functions/docs/welcome.md)
* [Manage  accounts](https://techdocs.akamai.com/akamai-functions/docs/manage-accounts.md)
* [Tutorials](https://techdocs.akamai.com/akamai-functions/docs/tutorials.md)