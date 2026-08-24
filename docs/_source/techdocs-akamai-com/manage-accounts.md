---
updatedAt: 2026-04-20T13:57:25.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# Manage  accounts

When you  [sign up](https://fibsu0jcu2g.typeform.com/fwf-preview?typeform-source=developer.fermyon.com) for Akamai Functions, you’re automatically assigned a personal account. All actions run in the context of your personal account unless you create a team account for collaboration with other Akamai Functions users. With a personal account, you’re the only one who can view and interact with your Spin applications running on Akamai Functions.

> 🚧
>
> Proceed with caution when sharing access to team accounts. Akamai Functions does not support Role-Based Access Control (RBAC). Everyone has the same level of permissions and any member can permanently delete any application in the account.

> 👍
>
> Follow the instructions in the Quickstart to [Login to Akamai Functions](https://techdocs.akamai.com/akamai-functions/docs/quickstart#login-to-akamai-functions) using the [`spin aka login` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-login).

# View your personal account information

Your personal account name matches the username you used to sign up for Akamai Functions. To view your account ID and account name, run the [`spin aka info` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-info) using plugin version v0.4 or higher.

```shell
# returns account_name (id: account_id)
spin aka info
```

```shell
Auth Info
  Accounts:
    - my_username (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
```

# Request a team account

To collaborate on Spin applications with other Akamai Functions users, create a team account by filling out this [short form](https://fibsu0jcu2g.typeform.com/to/coitknMl?typeform-source=developer.fermyon.com). You’ll need to provide a name for the team account and  a complete list of usernames that can access the account. Akamai Functions takes each user profile, which is the same as the personal account name, and adds it to the team account that you provided. To add or remove individuals later, use the same form and select, **Modify existing account** on question two.

There is currently no limit to the number of team accounts or users per team account you can have on Akamai Functions.

Once you have received email confirmation that the team account has been created or modified, any member of the team run the [`spin aka info` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-info). As long as you're logged in with the uses profile that was added to the team, you can access that team account.

```shell
# returns account_name (id: account_id)
spin aka info
```

```shell
Auth Info
  Accounts:
    - my_username (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
    - dev_team_1 (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
    - dev_team_2 (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
```

# View applications in team accounts

To see which applications are running within a given account, provide the `--account-id` or `account-name` flag. Otherwise the default will be your personal account.

```shell
# Personal account apps
spin aka app list 
```

```shell
my-test-app 
hello-kv-store 
```

```shell
# Team account apps
spin aka app list --account-name dev_team_1
```

```shell
graphql 
pw_checker 
```

# Run create, upgrade, and delete operations on team accounts

If you would like to deploy, upgrade, or delete an application running in a team account, you need to provide the account-id or account-name, otherwise the default will be your personal account.

```shell
# Deploy into a team account
spin aka deploy --account-name dev_team_1
```

```shell
# Delete an app from a team account
spin aka delete app --app-name graphql --account-name dev_team_1
```

To upgrade your application, follow the steps in [Update an application](https://techdocs.akamai.com/akamai-functions/docs/update-an-application) and pass along the `account-name` or `account-id` on the final spin aka deploy step to target a specific account.

# Sibling pages

* [Welcome to Akamai Functions (Limited availability)](https://techdocs.akamai.com/akamai-functions/docs/welcome.md)
* [Quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart.md)
* [Akamai Functions & EdgeWorkers comparison](https://techdocs.akamai.com/akamai-functions/docs/akamai-functions-and-edgeworkers-comparison.md)
* [Tutorials](https://techdocs.akamai.com/akamai-functions/docs/tutorials.md)