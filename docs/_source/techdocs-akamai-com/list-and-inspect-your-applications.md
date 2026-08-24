---
updatedAt: 2026-07-23T22:20:42.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# List and inspect your applications

You can list and inspect Spin applications deployed to your Akamai Functions account using the `spin aka` plugin.

# List your applications

To list all Spin applications deployed to your Akamai Functions account, use the [`spin aka app list` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-app-list).

```shell
spin aka app list
```

Depending on which apps you have deployed to your Akamai Functions account, the actual output will differ from the output shown here.

```shell
hello-akamai-functions  
validate-jwt-tokens  
query-external-database
```

By default, `spin aka app list` will print the name of each Spin application deployed to your Akamai Functions account as plain text. Alternatively, you can add the `--format` flag and change the output format to JSON.

```shell
spin aka app list --format json
```

This time, you’ll receive the list of Spin applications as a JSON array.

```shell
[  
  "hello-akamai-functions",  
  "validate-jwt-tokens",  
  "query-external-database"  
]
```

You can also use the `--verbose` flag to learn more about your apps. Below, you’ll see the spin app names alongside their respective app ids.

```shell
spin aka app list --verbose  
```

```shell
hello-akamai-functions (25a5fd1e-d476-40fd-bc54-6cee0e846540)  
validate-jwt-tokens (8d8ffd7d-57fe-4c0e-b982-251542db8792)  
query-external-database (b6cc1427-392c-4f96-859d-bb4d0adc216c)
```

<br />

# Inspect an application

Use the [`spin aka app status` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-app-status), to gather fundamental information about a Spin application deployed to your Akamai Functions account. This command provides the status of the application your workspace is [linked](https://techdocs.akamai.com/akamai-functions/docs/link-an-application) to. Alternatively, you can specify an app using the `--app-name` flag.

```shell
spin aka app status
```

```shell
Name: hello-akamai-functions  
ID: ec8a19d8-6d10-4056-bb69-cc864306b489  
URL: <https://ec8a19d8-6d10-4056-bb69-cc864306b489.fwf.app>  
Created at: 2025-05-23 16:11:49 UTC  
Invocations: 229 in the past 7 days
```

As you can see, you’ll also receive the public origin, that can be used to access the Spin application. Similar to the `spin aka app list` command, you can add the `--format json` flag to make the command return fundamental information about a particular application as a  `JSON` object.

```shell
spin aka app status --app-name hello-akamai-functions --format json
```

```shell
{  
  "id": "ec8a19d8-6d10-4056-bb69-cc864306b489",  
  "name": "hello-akamai-functions",  
  "urls": [  
    "https://ec8a19d8-6d10-4056-bb69-cc864306b489.fwf.app"  
  ],  
  "created_at": "2025-05-23 16:11:49 UTC",  
  "invocations": "229 in the past 7 days"  
}
```

# Sibling pages

* [Link an application](https://techdocs.akamai.com/akamai-functions/docs/link-an-application.md)
* [Update an application](https://techdocs.akamai.com/akamai-functions/docs/update-an-application.md)
* [Delete an application](https://techdocs.akamai.com/akamai-functions/docs/delete-an-application.md)
* [Deploy and specify application variables](https://techdocs.akamai.com/akamai-functions/docs/deploy-app-variables.md)
* [Deploy using GitHub actions](https://techdocs.akamai.com/akamai-functions/docs/deploy-using-github-actions.md)