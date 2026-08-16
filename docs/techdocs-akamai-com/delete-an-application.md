# Source: https://techdocs.akamai.com/akamai-functions/docs/delete-an-application
Date: 2026-08-16T10:57:08.452799
Model: gpt-oss:120b-cloud
## Supported APIs and Syntax
- `spin aka app list` — Retrieves a list of all Spin applications deployed to the current Akamai Functions account.  
- `spin aka app delete --app-name <appName>` — Deletes the specified Spin application; the command will prompt for confirmation before permanently removing the app.

## Required Patterns
**Pattern: List applications**
```shell
spin aka app list
```

**Pattern: Delete an application**
```shell
spin aka app delete --app-name <appName>
# Example:
spin aka app delete --app-name validate-jwt-tokens
# When prompted, type "yes" to confirm deletion
```