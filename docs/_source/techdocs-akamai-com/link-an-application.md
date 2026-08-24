---
updatedAt: 2026-04-16T15:03:29.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Link an application

You can link your local workspace to an application running in Akamai Functions so you don’t always have to specify the `--app-name` when running commands.

A workspace is a directory on your local machine that contains the Spin application code and the manifest file, `spin.toml`. It's where you develop and test your application before deploying it to Akamai Functions. Any child directory where the Spin manifest is located is also considered part of the workspace.

> 👍
>
> Linking is useful if your local workspace wasn't automatically linked on first deploy. For example, if you cloned an existing repo, switched machines, or joined a team working on an established application. Once linked, commands like `spin aka deploy` and `spin aka logs` will automatically target the correct application without needing to pass `--app-name` each time.

# Inspect your workspace

To see information about the current workspace, navigate to the directory where your Spin application is located and run this command.

```shell
spin aka info
```

The [`spin aka info` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-info) will also tell if your workspace is linked to an application on Akamai Functions and if so, which one.

```shell
Auth Info  
  Accounts: your-account  
Workspace Info  
  Root dir: /Users/user/src/hello-spin  
  Linked app: hello-spin
```

> 👍
>
> When you run `spin aka deploy `for the first time, it automatically links your workspace to the application you just deployed.

# Link your workspace

If your workspace is not linked to an application, you can link it by running the following command.

```shell
spin aka link
```

The [`spin aka app link` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-app-link) will prompt you to select an application to link to. You can also specify the application name directly.

```shell
spin aka app link --app-name <app-name>
```

This will link your workspace to the specified application. You can verify that the workspace is linked by running the `spin aka info` command again.

Now anytime you run a command in this workspace Akamai Functions will automatically assume that you want to run it against the linked application. For example, if you run `spin aka deploy` it will upgrade that application. If you run `spin aka logs`, it will show the logs for that application and so on.

# Unlink your workspace

To unlink your workspace from the currently linked application, run the [`spin aka app unlink` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-app-unlink).

```shell
spin aka app unlink
```

You can run the [`spin aka info`command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-info) again to verify that the workspace is no longer linked to an application.

> 👍
>
> Unlinking your workspace does not delete the application on Akamai Functions. It simply removes the link between your local workspace and the application.

# Sibling pages

* [List and inspect your applications](https://techdocs.akamai.com/akamai-functions/docs/list-and-inspect-your-applications.md)
* [Update an application](https://techdocs.akamai.com/akamai-functions/docs/update-an-application.md)
* [Delete an application](https://techdocs.akamai.com/akamai-functions/docs/delete-an-application.md)
* [Deploy and specify application variables](https://techdocs.akamai.com/akamai-functions/docs/deploy-app-variables.md)
* [Deploy using GitHub actions](https://techdocs.akamai.com/akamai-functions/docs/deploy-using-github-actions.md)