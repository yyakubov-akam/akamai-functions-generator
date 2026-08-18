# Source: https://techdocs.akamai.com/akamai-functions/docs/delete-an-application
Date: 2026-08-17T09:27:14.266122
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Deleting an application is permanent and cannot be undone
- No role-based access control (RBAC) is supported; any team account member can delete any application

## Supported APIs and Syntax

`spin aka app list` — Retrieves a list of all Spin applications deployed to the Akamai Functions account

`spin aka app delete --app-name <name>` — Deletes a specific Spin application from the account

`spin aka app delete` — Deletes a Spin application from the account (interactive mode)

## Required Patterns

```shell
spin aka app delete --app-name validate-jwt-tokens
```

## Common Mistakes and Gotchas

Unlike standard RBAC implementations, Akamai Functions does not support role-based access control (RBAC); any member of a team account can permanently delete any application within that account

## Version and Compatibility Notes

N/A