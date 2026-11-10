---
updatedAt: 2026-11-08T16:04:08.000Z
agentTools:
  siteIndex: https://techdocs.akamai.com/llms.txt
  projectIndex: https://techdocs.akamai.com/akamai-functions/llms.txt
---

# Manage  accounts

Akamai Functions uses its own account system, which is not directly controlled by Akamai Control Center (ACC) or Cloud Manager identity and access management. It does, however, use ACC as an identity provider to let you log in with your Akamai credentials and link you to the correct Akamai Functions accounts. For more information, see [Sign up for Akamai Functions](https://techdocs.akamai.com/akamai-functions/docs/sign-up-for-akamai-functions).

There are two Akamai Functions account types:

* **Personal accounts**: One personal account is available per user. Use personal accounts for experimentation and testing. These accounts support lower limits and fewer requests per month.
* **Team accounts**: Multiple team accounts are available per contract. Use team accounts for collaboration and production deployments. These accounts support access to the [full limits](https://techdocs.akamai.com/akamai-functions/docs/quotas-and-limits) and request counts specified in your contract.

When you [log in for the first time](https://techdocs.akamai.com/akamai-functions/docs/quickstart#log-in-to-akamai-functions) using `spin aka login`, the system automatically creates a personal account named after your Akamai Control Center username. The system also adds you to one or more default team accounts. One default team account is created for each linked Akamai Control Center contract that has Akamai Functions enabled.

In the example below, username <info@example.com> has an account associated with contract **X-ABC-DEF**. Akamai is Functions enabled under the [Extended plan](https://techdocs.akamai.com/akamai-functions/docs/quotas-and-limits#resource-tier-limits). When the user runs`spin aka info` the following output will appear.

```shell
Auth Info  
  Accounts:  
    - info-example-com (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)  
    - X-ABC-DEF-extended-default (id: yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyy)
```

# Manage user account access

Your personal account is visible and accessible only to you. You can create, update, remove, and even deploy applications within this account, but it should not be used for production workloads.

Team accounts are visible and accessible to all team members. The “default” contract team account includes all users of your company with an Akamai Control Center account tied to that contract.

> 🚧
>
> At the moment, Akamai Functions does not support the identity and access management system used in Akamai Control Center, or any other Role-Based Access Control (RBAC) system. This means that all users in a team account currently have full administrative access. Every team member can create, update, permanently remove, and deploy an application.

In a future update, the [Spin aka plugin](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference) will let you directly create new Team Accounts and manage membership. Until then, you can request a new team account tied to your contract by filling out this [short form](https://fibsu0jcu2g.typeform.com/to/coitknMl?typeform-source=developer.fermyon.com). You’ll need to provide a name for the team account and a list of active Akamai Functions usernames (the personal account names, info-example-com in the example above) that can access the account.

Akamai Functions takes each user profile and adds it to the team account that you provided. Any users you want to add to a team account need to have [logged in successfully at least once via `spin aka login`](https://techdocs.akamai.com/akamai-functions/docs/quickstart#log-in-to-akamai-functions) to create their personal account. To add or remove individuals, use the same form and select “Modify existing account” on question two. Note that this form is currently manually processed, so allow up to 48 hours to complete your request.

Once you have received email confirmation that the team account has been created or modified, any member of the team can run the [`spin aka info` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-info). As long as you're logged in with the user profile with membership to the team, you can access that team account.

Below you can see an example of the output of `spin aka info` after requesting the creation of a new team account called "dev-team-2":

```shell
Auth Info  
  Accounts:  
    - info-example-com (id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)  
    - X-ABC-DEF-extended-default (id: yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyy)
    - X-ABC-DEF-dev-team-2 (id: zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzz)
```

Akamai Functions does not currently limit the number of team accounts or users per team account you can have.

# Manage applications in team accounts

By default, all spin commands run on your personal account. If you would like to deploy, upgrade, or delete an application running in a team account, you need to provide the account ID or name to the spin commands. This can be done in two ways:

1. Either use the `--account-id` or `--account-name` argument with each command.
2. Or set the `SPIN_AKA_ACCOUNT_ID` or `SPIN_AKA_ACCOUNT_NAME` environment variables, which are automatically picked up by spin. To use this option you need spin aka plugin v0.7.8 or higher.

For example, see the different outputs of `spin aka app list` depending on which account you are observing.

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
spin aka app list --account-name X-ABC-DEF-extended-default
```

```shell
graphql 
pw_checker
```

This also applies if you would like to [deploy](https://techdocs.akamai.com/akamai-functions/docs/quickstart#deploy-the-application), [update](https://techdocs.akamai.com/akamai-functions/docs/update-an-application), or [delete](https://techdocs.akamai.com/akamai-functions/docs/delete-an-application) an application running in a team account. For example, to delete the application named graphql from the team account, you would use:

```shell
# Delete an app from a team account
spin aka delete app --app-name graphql --account-name X-ABC-DEF-extended-default
```

Finally, to link an application named pw\_checker in a local workspace to a team account instead of your personal account, you would use:

```shell
spin aka app link --app-name pw_checker --account-id yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyy
```

# Automation with personal access tokens

As described in [Deploy using GitHub actions](https://techdocs.akamai.com/akamai-functions/docs/deploy-using-github-actions), you can automate Akamai Functions operations using a Personal Access Token (PAT).

These PATs impersonate the user that created them using the `spin aka login --token {YOUR-PAT}` command. PATs can also manage applications in all team accounts that this user has access to (though they cannot delete them). See [Quotas and Limits](https://techdocs.akamai.com/akamai-functions/docs/quotas-and-limits) for more information about PAT restrictions.

# Sibling pages

* [Welcome to Akamai Functions](https://techdocs.akamai.com/akamai-functions/docs/welcome.md)
* [Quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart.md)
* [Akamai Functions & EdgeWorkers comparison](https://techdocs.akamai.com/akamai-functions/docs/akamai-functions-and-edgeworkers-comparison.md)
* [Tutorials](https://techdocs.akamai.com/akamai-functions/docs/tutorials.md)