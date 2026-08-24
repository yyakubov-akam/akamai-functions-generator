---
updatedAt: 2026-08-19T15:18:51.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Akamai Functions & EdgeWorkers comparison

Akamai offers two powerful edge compute platforms, [EdgeWorkers](https://techdocs.akamai.com/edgeworkers/docs/welcome-to-edgeworkers) and Akamai Functions. While they share the same goal of bringing compute closer to users, they serve fundamentally different use cases. Understanding the distinction will help you choose the right tool for the job.

> 👍
>
> You can also review the [use cases](https://techdocs.akamai.com/akamai-functions/docs/use-cases) to you help you choose the right platform(s), [Akamai Functions](https://techdocs.akamai.com/akamai-functions/docs/use-cases#akamai-functions-use-cases), [Combined Akamai Functions and EdgeWorkers](https://techdocs.akamai.com/akamai-functions/docs/use-cases#combined-use-cases), or [EdgeWorkers](https://techdocs.akamai.com/akamai-functions/docs/use-cases#edgeworkers-use-cases).

## About the Akamai compute platform

EdgeWorkers and Akamai Functions are complementary layers in the complete edge compute architecture. The question is not which to use, but which layer a given piece of logic belongs in.

If the logic is about how traffic flows such as routing, authentication, cache key construction, header enforcement, or request transformation, then it belongs in EdgeWorkers. The CDN pipeline is exactly where that logic should live, and EdgeWorkers gives it access to every edge node on Akamai's network with the performance characteristics of the delivery layer itself.

If the logic is about what happens to the data, such as business rules, API orchestration, AI inference, data transformation, or server-side rendering, then it belongs in Akamai Functions. The Wasm runtime used by Functions gives this logic the performance and portability it needs, close to users without any infrastructure management burden.

When used together, these platforms enable architectures that were previously difficult to build: edge-native APIs with intelligent traffic shaping, personalized content with cached performance, and security enforcement that responds to real-time signals. All without the complexity and cost of managing origin infrastructure at scale.

The edge is no longer just a caching layer. With EdgeWorkers and Akamai Functions, it is a full compute platform. The organizations that learn to build natively on it will have a lasting performance, resilience, and cost advantage over those still shipping every workload to a centralized origin.

## EdgeWorkers and Akamai Functions comparison

[block:parameters]
{
  "data": {
    "h-0": "Feature",
    "h-1": "EdgeWorkers",
    "h-2": "Akamai Functions",
    "0-0": "**Runtime  **",
    "0-1": "JavaScript (V8) ",
    "0-2": "WebAssembly (aka Spin)",
    "1-0": "**Execution Layer  \n**",
    "1-1": "CDN / HTTP pipeline  ",
    "1-2": "Akamai Cloud regions. ",
    "2-0": "**Primary Use Case  **",
    "2-1": "Traffic orchestration, request/response manipulation  ",
    "2-2": "Application logic, APIs, microservices, AI inference",
    "3-0": "**Execution Time**  ",
    "3-1": "\\<10 seconds (varies by event and tier)  ",
    "3-2": "30 seconds default, extendable",
    "4-0": "**Trigger Model ** ",
    "4-1": "HTTP lifecycle events (`onClientRequest`, `onOriginRequest`, `onOriginResponse`, `onClientResponse`, `responseProvider`)  ",
    "4-2": "HTTP requests",
    "5-0": "**Infrastructure  **",
    "5-1": "Fully managed  ",
    "5-2": "Fully managed",
    "6-0": "**Data Access  **",
    "6-1": "Outbound HTTP to Akamized hostnames  \nEdgeKV  ",
    "6-2": "Outbound HTTP to any hostname  \nAkamai Functions KV  \nCustomer-managed databases: MySQL,  \nPostgreSQL,  \nRedis"
  },
  "cols": 3,
  "rows": 7,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]

# About EdgeWorkers

EdgeWorkers is Akamai's event-driven serverless platform built directly into the CDN. It runs JavaScript at the HTTP request/response lifecycle. This lets developers intercept and manipulate traffic at the edge, before it even leaves the edge server.

EdgeWorkers executes within Akamai's CDN delivery layer, which means it operates at every one of Akamai's thousands of edge locations worldwide. Code runs in tight integration with the HTTP pipeline, enabling use cases such as:

* Request routing and URL rewriting
* A/B testing and personalization logic
* Authentication and token validation
* Cache key customization
* Conditional origin selection

The programming model for most EdgeWorkers events is tightly scoped to Akamai's edge platform APIs. The `onClientRequest`, `onOriginRequest`, `onOriginResponse`, and `onClientResponse` events run within Akamai CDN metadata stages. This tight coupling makes EdgeWorkers extremely fast and low-latency, and makes EdgeWorkers well-suited for building functionality to enhance CDN delivery. It also means the runtime is intentionally constrained. CPU, memory, and execution time limits are low to ensure that heavy workloads can’t cause contention at small CDN regions. The environment is optimized for traffic orchestration rather than general-purpose computation.

With the `responseProvider` event, EdgeWorkers can also act as the origin to the CDN.  Latency is still minimal with `responseProvider`, as it runs on the same edge server as the CDN delivery and security. The limits for `responseProvider` are a bit higher than other EdgeWorkers events. You can use them to perform lightweight general-purpose computation such as modifying small request and response bodies or orchestrating multiple small API calls. It's still fundamentally limited by the compute power available in small regions.

# About Akamai Functions

Akamai Functions is a fully managed serverless compute platform built on WebAssembly, powered by [Spin](https://spinframework.dev/), an open source developer tool. Unlike EdgeWorkers, Akamai Functions is designed for general-purpose application workloads that need to run close to users without managing infrastructure. These applications workloads include microservices, APIs, AI inference endpoints, and backend logic.

The Akamai Functions platform automatically routes execution based on the user's location. This ensures low latency without any manual configuration. Because it's built on Spin (which leverages Wasmtime), developers can write functions in a variety of languages such as Rust, Go, Python, JavaScript. This makes it highly accessible across engineering teams.  

## Akamai Functions key features

* **Fully managed**. No infrastructure to provision, scale, or maintain.
* **Wasm-based runtime**. Language-agnostic, fast cold starts, strong security sandboxing.
* **Auto-routing**. Requests are automatically directed to the nearest of region.
* **Longer execution**. Suitable for more complex compute tasks than CDN-layer edge execution.
* **Spin framework**. Leverages the growing Akamai Functions/Wasm ecosystem for building components.

## Data Access in Akamai Functions

One of the most significant benefits of Akamai Functions is the breadth of data access available. Where EdgeWorkers is largely limited to EdgeKV and Akamized HTTP endpoints, Akamai Functions supports a richer set of persistence and data options suited to real application workloads.

### Supported Data Stores

**Functions KV** (platform managed). A key-value store native to the Akamai Functions platform, similar in concept to EdgeKV but with access from the compute layer rather than the CDN layer.

**MySQL** (customer managed). Full relational database support via the MySQL protocol. Compatible with Akamai's Linode DBaaS MySQL offering, making it straightforward to provision a managed database and connect directly from a Function.

**PostgreSQL** (customer managed). PostgreSQL protocol support is available, though it is not yet compatible with Linode DBaaS. Teams can connect to self-managed PostgreSQL instances or third-party hosted PostgreSQL services in the interim.

**Redis** (customer managed). Redis protocol support is available for caching, session storage, pub/sub, and other Redis use cases. Akamai does not currently offer a managed Redis service, so teams need to bring their own Redis instance, whether self-managed on Linode or via a third-party provider.

**Outbound HTTP**. Akamai Functions can make outbound HTTP requests to any hostname, not just Akamized endpoints. This opens up easier integration with third-party APIs, internal services, and any HTTP-accessible data source, without needing to create a CDN property to act as proxy to the 3rd-party endpoint.

The availability of MySQL and PostgreSQL support is particularly significant. It means Akamai Functions can serve as a genuine application backend, not just a stateless compute layer. Functions that need to read or write structured data, perform joins, enforce referential integrity, or run complex queries can do so directly against a relational database. These are patterns that would be impractical or impossible in EdgeWorkers.

Redis support enables a class of workloads that benefit from in-memory speed: session caches, rate limit counters, real-time leaderboards, pub/sub messaging, and distributed locks. These are common patterns in microservice architectures that Akamai Functions can now support natively.

> 📘
>
> MySQL with Linode DBaaS is the smoothest path today for teams wanting a fully managed Akamai-native persistence layer in a single region. Extra effort would be needed to build out a multi-region MySQL cluster. PostgreSQL and Redis integrations require bringing your own infrastructure for now, though the platform roadmap indicates managed options are coming.

# Sub pages

* [Use cases](https://techdocs.akamai.com/akamai-functions/docs/use-cases.md)

# Sibling pages

* [Welcome to Akamai Functions (Limited availability)](https://techdocs.akamai.com/akamai-functions/docs/welcome.md)
* [Quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart.md)
* [Manage  accounts](https://techdocs.akamai.com/akamai-functions/docs/manage-accounts.md)
* [Tutorials](https://techdocs.akamai.com/akamai-functions/docs/tutorials.md)