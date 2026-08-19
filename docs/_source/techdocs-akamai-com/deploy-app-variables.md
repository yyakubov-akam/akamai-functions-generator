---
updatedAt: 2026-08-05T21:52:57.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further.

# Deploy and specify application variables

Spin supports [application variables](https://spinframework.dev/v3/variables). Instead of being static, their values can be updated without modifying the application, creating a simpler experience for rotating secrets, updating API endpoints, and more.

> 👍
>
> If this is the first time you're deploying a Spin application or you don't want to specify application variables go to the [Quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart#deploy-the-application) guide. It'll walk you through the process of creating a new Spin application, using JavaScript, TypeScript, or Rust, and deploying it to Akamai Functions.

For example, consider a Spin application with the following variable declaration as part of the application manifest (`spin.toml`).

```shell
[variables]  
compression_level = { default = "1" }
```

When deploying the Spin application to Akamai Functions, you can set variables by providing `--variable flags` and passing the key and value using the `key=value` format. See the following [`spin aka deploy` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-deploy), which changes the value of the `compression_level` variable to `3`.

> 👍
>
> In this example `spin aka deploy` does not include any code changes. However, the changes are propagated as a new deployment, so you will see the version increment.

```shell
spin aka deploy --variable compression_level=3
```

```shell
Deploying updated version of app my-app in account your-account (version 1 → 2)
OK to continue? yes
Waiting for app to be ready... ready

App Routes:
- my-app: https://ec8a19d8-6d10-4056-bb69-cc864306b489.fwf.app (wildcard)
```

> 👍
>
> `spin aka deploy` can point to a `spin.toml` file by using the `--file` option.

Application variables can also be used to configure secrets as they are encrypted by default on the Akamai Functions platform. Once deployed, application variables are encrypted at rest and in transit for the entirety of the lifetime of the application.

> 🚧
>
> While application variables are encrypted, the underlying cryptographic implementations have not been assessed for PCI compliance.

# Sibling pages

* [Link an application](https://techdocs.akamai.com/akamai-functions/docs/link-an-application.md)
* [List and inspect your applications](https://techdocs.akamai.com/akamai-functions/docs/list-and-inspect-your-applications.md)
* [Update an application](https://techdocs.akamai.com/akamai-functions/docs/update-an-application.md)
* [Delete an application](https://techdocs.akamai.com/akamai-functions/docs/delete-an-application.md)
* [Deploy using GitHub actions](https://techdocs.akamai.com/akamai-functions/docs/deploy-using-github-actions.md)