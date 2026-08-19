---
updatedAt: 2026-04-16T15:09:31.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further.

# Delete an application

You can delete a Spin application from Akamai Functions using the `aka` plugin for `spin` CLI.

Any member of a [team account](https://techdocs.akamai.com/akamai-functions/docs/manage-accounts#request-a-team-account) can delete any application within that account. Akamai Functions does not currently support role-based access control (RBAC) or per-application permissions. Use caution when sharing team account access, as any member can permanently delete any application in the account.

# Find the application you want to delete

You can use the [`spin aka app list` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-app-list) to retrieve a list of all Spin applications deployed to your Akamai Functions account.

```shell
spin aka app list
```

```shell
hello-akamai-functions  
validate-jwt-tokens  
query-external-database
```

# Delete your application

Use the [`spin aka app delete` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-app-delete) to delete a Spin application from your Akamai Functions account.

> 🚧 Before you proceed
>
> Deleting an application is permanent and cannot be undone.

```shell
spin aka app delete --app-name validate-jwt-tokens
```

The `spin aka app delete` command, will ask you to confirm that you want to delete the app. Once confirmed, the application will be removed from your Akamai Functions account.

```shell
Are you sure you want to delete the app 'validate-jwt-tokens' (21077e3b-d632-4df3-921f-f7ebefb9aaca)? yes
Deleted app successfully.
```

# Sibling pages

* [Link an application](https://techdocs.akamai.com/akamai-functions/docs/link-an-application.md)
* [List and inspect your applications](https://techdocs.akamai.com/akamai-functions/docs/list-and-inspect-your-applications.md)
* [Update an application](https://techdocs.akamai.com/akamai-functions/docs/update-an-application.md)
* [Deploy and specify application variables](https://techdocs.akamai.com/akamai-functions/docs/deploy-app-variables.md)
* [Deploy using GitHub actions](https://techdocs.akamai.com/akamai-functions/docs/deploy-using-github-actions.md)