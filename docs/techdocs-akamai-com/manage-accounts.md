# Source: https://techdocs.akamai.com/akamai-functions/docs/manage-accounts
Date: 2026-08-16T10:55:16.365202
Model: gpt-oss:120b-cloud
## Supported APIs and Syntax
| Command | Description |
|---|---|
| `spin aka info` | Returns the current account name and its UUID. Requires plugin version **v0.4** or higher. |
| `spin aka app list` | Lists applications in the default (personal) account. |
| `spin aka app list --account-name <account_name>` | Lists applications in the specified team account. |
| `spin aka app list --account-id <account_id>` | Lists applications in the specified team account (using the UUID). |
| `spin aka deploy --account-name <account_name>` | Deploys the current Spin application into the specified team account. |
| `spin aka deploy --account-id <account_id>` | Deploys the current Spin application into the specified team account (using the UUID). |
| `spin aka delete app --app-name <app_name> --account-name <account_name>` | Deletes the named application from the specified team account. |
| `spin aka delete app --app-name <app_name> --account-id <account_id>` | Deletes the named application from the specified team account (using the UUID). |

---

## Required Patterns
**Targeting a specific team account**

```bash
# Deploy to a team account
spin aka deploy --account-name dev_team_1

# List apps in a team account
spin aka app list --account-name dev_team_1

# Delete an app from a team account
spin aka delete app --app-name graphql --account-name dev_team_1
```

*Always include either `--account-name` or `--account-id` when operating on a team account; otherwise the command defaults to the personal account.*

---

## Common Mistakes and Gotchas
- **Unlike platforms with Role‑Based Access Control (RBAC), Akamai Functions does not support RBAC.** Every member of a team account has full permissions and can permanently delete any application in that account.  
- **Omitting the `--account-name`/`--account-id` flag** runs the command against the personal account, which may lead to unintended deployments or deletions.  

---

## Version and Compatibility Notes
- The `spin aka info` command is only available with **plugin version v0.4** or higher.  
- There is **no limit** on the number of team accounts or the number of users per team account.  