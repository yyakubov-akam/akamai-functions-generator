# Source: https://techdocs.akamai.com/akamai-functions/docs/list-and-inspect-your-applications
Date: 2026-08-17T09:26:14.116480
Model: glm-4.7-flash:q8_0
## Required Patterns

List applications in JSON format
```shell
spin aka app list --format json
```

List applications with verbose details (includes App IDs)
```shell
spin aka app list --verbose
```

Inspect application status in JSON format
```shell
spin aka app status --app-name <app_name> --format json
```

## Common Mistakes and Gotchas

Unlike standard command-line behavior where `spin aka app list` might output detailed metadata by default, this command prints the name of each Spin application as plain text unless the `--verbose` flag is used.

Unlike standard command-line behavior where `spin aka app status` might default to the current context, this command provides the status of the application your workspace is linked to unless the `--app-name` flag is specified.