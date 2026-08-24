---
updatedAt: 2026-03-31T21:38:10.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Welcome to Akamai Functions (Limited availability)

Use Akamai Functions to build and run serverless functions hosted on [Akamai Cloud](https://techdocs.akamai.com/cloud-computing/docs/welcome).

Akamai Functions is a globally distributed PaaS (Platform-as-a-Service) that uses  [Spin](https://spinframework.dev/) to run edge native applications. Spin is an open source framework for building and running event-driven applications that are fast, portable, and sandboxed by design thanks to a WebAssembly based runtime. You can use Spin to build and test your applications locally before deploying to the Akamai Functions platform.

Akamai Functions offers:

* Fast and resilient hosting for Spin applications, with global geo replication by default.
* SDK support for Rust, Go, JavaScript, and Python that allows you to write in your language of choice and compile to WebAssembly.
* Zero infrastructure overhead, meaning no servers to provision, patch, or maintain.
* Fast application start-up time and execution.
* A stable URL that persists across deployments.
* Integration with your existing properties in Property Manager.

[block:image]
{
  "images": [
    {
      "image": [
        "https://techdocs.akamai.com/akamai-functions/img/functions-welcome-page-v2.png",
        null,
        "Akamai Functions overview diagram"
      ],
      "align": "center",
      "sizing": "900px",
      "border": true
    }
  ]
}
[/block]

# Where to start

To get started, you need you need access to the public preview of Akamai Functions. If you haven’t already requested access, please complete the [Onboarding form](https://fibsu0jcu2g.typeform.com/fwf-preview?typeform-source=developer.fermyon.com). The Akamai Functions team will review your request and follow up shortly.

> 📘
>
> For information about building your first Spin application, go to the [Spin documentation](https://spinframework.dev/) or the [Quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart)  tutorial in this guide.

Review these core concepts before you use the Quickstart to help you get up and running with Akamai Functions.

|                                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Spin                                   | With [Spin](https://spinframework.dev/) you can build applications using a wide variety of different programming languages. The [Quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart) includes instructions and samples for JavaScript, TypeScript and Rust.                                                                                                                                                                                                                                                                                                                     |
| Application Deployment                 | You can deploy Spin applications to Akamai Functions with a single command using the `spin aka` plugin. Check out the deployment guide and the [`spin aka deploy` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-deploy) for more details.                                                                                                                                                                                                                                                                                                                 |
| Traffic Routing                        | Akamai Functions uses the Akamai Cloud infrastructure and services to ensure client requests are forwarded to the fastest responding region where your application is available.                                                                                                                                                                                                                                                                                                                                                                        |
| Integration With Other Akamai Services | You can use any Akamai CDN, Security and Cloud service with your Akamai Functions Spin applications. Whether you want to use Akamai’s [API Acceleration](https://techdocs.akamai.com/api-acceleration/docs/welcome-api-accel) to secure and cache requests and responses to and from your application, secure your application with [App & API Protector](https://techdocs.akamai.com/app-api-protector/docs/welcome), or integrate with Akamai’s managed databases, this is all possible, and fast, as your Akamai Functions runs within Akamai Cloud. |

# Sibling pages

* [Quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart.md)
* [Akamai Functions & EdgeWorkers comparison](https://techdocs.akamai.com/akamai-functions/docs/akamai-functions-and-edgeworkers-comparison.md)
* [Manage  accounts](https://techdocs.akamai.com/akamai-functions/docs/manage-accounts.md)
* [Tutorials](https://techdocs.akamai.com/akamai-functions/docs/tutorials.md)