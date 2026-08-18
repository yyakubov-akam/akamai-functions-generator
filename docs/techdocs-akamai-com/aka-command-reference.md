# Source: https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference
Date: 2026-08-17T08:53:27.731246
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Spin compatibility: >=v3.0.0
- Cron job management commands are marked UNSTABLE/Tech Preview and may change behavior
- Token expiration is limited to a maximum of 90 days
- Usage time range for status/logs is enforced between a minimum of 5 minutes and a maximum of 7 days

## Supported APIs and Syntax

`spin aka app deploy [OPTIONS]` — Deploy an app to Akamai Functions
`spin aka app cron create [OPTIONS] --schedule <SCHEDULE>` — Create a cron job for the current app
`spin aka app cron delete [OPTIONS] <NAME>` — Delete a cron job from the current app
`spin aka app cron list [OPTIONS]` — List cron jobs for the current app
`spin aka app delete [OPTIONS]` — Delete an app
`spin aka app history [OPTIONS]` — Lists past events for an app
`spin aka app link [OPTIONS]` — Link your local workspace to an existing Akamai Functions app
`spin aka app list [OPTIONS]` — List apps
`spin aka app logs [OPTIONS]` — Fetch the logs for an app
`spin aka app status [OPTIONS]` — Display information about an app
`spin aka app unlink [OPTIONS]` — Unlink your local workspace from an existing Akamai Functions app
`spin aka auth login [OPTIONS]` — Log into Akamai Functions
`spin aka auth token create [OPTIONS] --name <NAME>` — Create a new personal access token
`spin aka auth token delete [OPTIONS] --id <ID>` — Delete a personal access token
`spin aka auth token list [OPTIONS]` — List personal access tokens for the current user
`spin aka auth token regenerate [OPTIONS] --id <ID>` — Regenerate a personal access token
`spin aka cron create [OPTIONS] --schedule <SCHEDULE>` — Create a cron job for the current app
`spin aka cron delete [OPTIONS] <NAME>` — Delete a cron job from the current app
`spin aka cron list [OPTIONS]` — List cron jobs for the current app
`spin aka deploy [OPTIONS]` — Deploy an app to Akamai Functions
`spin aka info [OPTIONS]` — Print out user and workspace information
`spin aka logs [OPTIONS]` — Fetch the logs for an app
`spin aka send-feedback` — Send us your feedback!

## Required Patterns

**Variable Passing**
Pass variables to the app during deployment using the `--variable` flag. Values can be key-value pairs or file paths.
```bash
spin aka app deploy --variable key=value --variable @config.json
```

**Account Context Specification**
Specify the account using either `--account-id` or `--account-name`. If neither is provided, the current account context is used.
```bash
spin aka app deploy --account-id <ACCOUNT_ID>
spin aka app deploy --account-name <ACCOUNT_NAME>
```

**App Inference**
Specify the app using either `--app-id` or `--app-name`. If neither is provided, the app is inferred from the workspace config (`./spin.toml`).
```bash
spin aka app deploy
```

**Time Specification**
Specify time ranges using RFC3339 timestamps, Unix epoch timestamps, or duration strings (e.g., "30m", "7d").
```bash
spin aka app logs --since 7d
spin aka app status --usage-since 30m
```

## Common Mistakes and Gotchas

Unlike standard CLI tools, Akamai Functions commands default to the current account context if neither `--account-id` nor `--account-name` is provided.

Unlike standard CLI tools, Akamai Functions commands default to the workspace config for app identification if neither `--app-id` nor `--app-name` is provided.

Unlike standard CLI tools, the `--variable` flag allows multiple repetitions; if the same key is specified multiple times, the last value will be used.

Unlike standard CLI tools, the `--from` flag defaults to `./spin.toml` if omitted.

## Version and Compatibility Notes

- Spin compatibility: >=v3.0.0
- Plugin versions documented: v0.4.0 and v0.7.0
- Cron job features are currently marked UNSTABLE/Tech Preview
- Plugin versions show evolution between 2025-05-22 and 2026-03-20