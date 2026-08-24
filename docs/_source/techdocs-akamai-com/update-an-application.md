---
updatedAt: 2026-04-16T15:08:33.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Update an application

You can upgrade your application by re-deploying it after you’ve made changes to your code or its version. Your application's name and URL will remain the same after an update. Any existing integrations or links will also continue to work without interruption. When a new version is deployed, Akamai Functions automatically handles the transition, in-flight requests are gracefully completed by the previous version while all new traffic is routed to the updated version.

> 👍
>
> Built-in support for running multiple versions simultaneously, for example, canary or blue-green deployments is not available.

When upgrading a Spin application running in Akamai Functions, you can change the version of your application when making a code changes. You can either manually update the version in your application manifest along with your code changes, or accept the major version default upgrade prompted during the deployment process.

In this example we'll manually change the version number. This is an optional step.

1. Open the `spin.toml` file. In the file, you’ll find this line of code that indicates the version.

```shell
version = "0.1.0"
```

2. In this example, we’ll change the version from 0.1.0 to 0.1.1.

```shell
version = "0.1.1"
```

3. Whether you’ve just updated your application code or also bumped the version, you can now deploy the upgraded version of your application by running the [`spin aka deploy` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-deploy).

```shell
spin aka deploy
```

4. Remember to specify [your application’s variables](https://techdocs.akamai.com/akamai-functions/docs/deploy-app-variables) when upgrading the Spin application on Akamai Functions.

```shell
 spin aka deploy --variable <key>=<value>
```

# Sibling pages

* [Link an application](https://techdocs.akamai.com/akamai-functions/docs/link-an-application.md)
* [List and inspect your applications](https://techdocs.akamai.com/akamai-functions/docs/list-and-inspect-your-applications.md)
* [Delete an application](https://techdocs.akamai.com/akamai-functions/docs/delete-an-application.md)
* [Deploy and specify application variables](https://techdocs.akamai.com/akamai-functions/docs/deploy-app-variables.md)
* [Deploy using GitHub actions](https://techdocs.akamai.com/akamai-functions/docs/deploy-using-github-actions.md)