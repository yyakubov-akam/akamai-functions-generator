# Source: https://techdocs.akamai.com/akamai-functions/docs/manage-accounts
Date: 2026-08-17T09:12:10.778036
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- RBAC is not supported; all members have the same permissions.
- `spin aka info` command requires plugin version v0.4 or higher.

## Supported APIs and Syntax

- `spin aka login` — Authenticates user to Akamai Functions.
- `spin aka info` — Displays account name and ID.
- `spin aka app list` — Lists applications in the current or specified account.
- `spin aka deploy` — Deploys application to the current or specified account.
- `spin aka delete app` — Removes an application from the specified account.

## Required Patterns

- **View Team Applications**
  ```shell
  spin aka app list --account-name <team_name>
  ```

- **Deploy to Team Account**
  ```shell
  spin aka deploy --account-name <team_name>
  ```

- **Delete Application from Team Account**
  ```shell
  spin aka delete app --app-name <app_name> --account-name <team_name>
  ```

## Common Mistakes and Gotchas

- Unlike standard cloud environments, Akamai Functions does not support Role-Based Access Control (RBAC); any member can permanently delete any application.
- Unlike standard deployments, default actions run in the personal account context; team accounts require explicit `--account-name` or `--account-id` flags.
- All actions run in the context of the personal account unless a team account is specified.

## Version and Compatibility Notes

- Plugin version v0.4 or higher is required for `spin aka info`.
- Limited availability status is noted in sibling pages.