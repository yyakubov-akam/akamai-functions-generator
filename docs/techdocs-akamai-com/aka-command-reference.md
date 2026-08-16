# Source: https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference
Date: 2026-08-16T09:26:07.870011
Model: gpt-oss:120b-cloud
## Runtime Constraints
- **Spin compatibility** – All commands require the Spin CLI version **≥ v3.0.0**.  
- **Cron commands** – Marked **UNSTABLE / Tech Preview**; may be removed or change without notice.  
- **Personal access token expiration** – `--expiration-days` **max = 90**, default = 30.  
- **App usage‑since filter** – Accepts durations **≥ 5 minutes** and **≤ 7 days**; defaults to 7 days.  
- **Log retrieval “since” flag** – Accepts RFC3339 timestamps, Unix epoch seconds, or duration strings (`s`, `m`, `h`, `d`); default = 7 days.  
- **Log retrieval “max‑lines”** – Default **10** lines; no explicit upper bound documented, but the CLI will truncate output to the requested number.  
- **Variable option** – `--variable` may be repeated; later occurrences **override** earlier ones for the same key.  
- **Build flag** – `--build` is ignored for remote apps; only local apps trigger `spin build`.  
- **Environment variable** – `SPIN_ALWAYS_BUILD` can force a build when `--build` is supplied.  
- **Confirmation prompts** – `--no-confirm` **must** be used to skip interactive confirmation for destructive actions (`delete`, `deploy`).  

## Supported APIs and Syntax
```
spin aka app delete([OPTIONS])                     — Delete an app
spin aka app deploy([OPTIONS])                     — Deploy an app to Akamai Functions
spin aka app link([OPTIONS])                       — Link local workspace to an existing app
spin aka app list([OPTIONS])                      — List apps
spin aka app logs([OPTIONS])                       — Fetch logs for an app
spin aka app status([OPTIONS])                     — Display information about an app
spin aka app unlink([OPTIONS])                     — Unlink local workspace from an app
spin aka app history([OPTIONS])                   — List past events for an app
spin aka app cron create(--schedule <SCHEDULE>, [OPTIONS])   — Create a cron job
spin aka app cron delete(<NAME>, [OPTIONS])       — Delete a cron job
spin aka app cron list([OPTIONS])                 — List cron jobs
spin aka cron create(--schedule <SCHEDULE>, [OPTIONS])      — Create a cron job (top‑level)
spin aka cron delete(<NAME>, [OPTIONS])            — Delete a cron job (top‑level)
spin aka cron list([OPTIONS])                     — List cron jobs (top‑level)
spin aka auth login([--token <TOKEN>])             — Log in using a personal access token
spin aka auth token create(--name <NAME>, [OPTIONS]) — Create a personal access token
spin aka auth token delete(--id <ID>, [--no-confirm]) — Delete a personal access token
spin aka auth token list([OPTIONS])                — List personal access tokens
spin aka auth token regenerate(--id <ID>)         — Regenerate a personal access token
spin aka deploy([OPTIONS])                         — Deploy an app (alias of `app deploy`)
spin aka info([--format <FORMAT>])                — Print user/workspace information
spin aka logs([OPTIONS])                           — Fetch logs for an app
spin aka send-feedback()                           — Send feedback
```
*Options are exactly as documented (e.g., `--account-id <ACCOUNT_ID>`, `--app-id <APP_ID>`, `-f, --from <PATH>`, `--no-confirm`, `--verbose`, etc.).*  

## Required Patterns
### 1. Deploying an app (with variables and optional build)
```bash
spin aka app deploy \
  --account-id 12345 \
  --app-id my-app \
  --build \
  --variable KEY1=value1 \
  --variable @config.json \
  -f ./my-app
```
### 2. Creating a cron job (app‑scoped)
```bash
spin aka app cron create \
  --schedule "0 0 * * *" \
  --name nightly-job \
  --path-and-query "/api/cron?run=nightly" \
  --app-name my-app
```
### 3. Deleting a cron job (top‑level)
```bash
spin aka cron delete \
  old-job \
  --app-id 9876 \
  --no-confirm
```
### 4. Generating a short‑lived personal access token
```bash
spin aka auth token create \
  --name "ci-token" \
  --expiration-days 7 \
  --short
```
### 5. Fetching recent logs (default 10 lines, last 7 days)
```bash
spin aka logs \
  --app-name my-app \
  -n 50 \
  --since "2h"
```
### 6. Linking a workspace to an existing app (interactive selection)
```bash
spin aka app link \
  --from ./my-workspace
```
### 7. Listing apps in JSON format with verbose output
```bash
spin aka app list \
  --format json \
  --verbose
```

## Common Mistakes and Gotchas
- **Unlike typical CLI defaults,** omitting `--account-id` **or** `--account-name` **does NOT error** – the command silently uses the *current account context*.  
- **Unlike generic token creation,** Akamai Functions **enforces a maximum expiration of 90 days**; providing a larger value will be rejected.  
- **Unlike standard `spin build`,** the `--build` flag on `spin aka app deploy` **has no effect for remote apps**; the CLI will skip the build step.  
- **Unlike many CLIs,** the `--no-confirm` flag **must be supplied** to bypass interactive prompts for destructive actions; otherwise the command will pause for user input.  
- **Unlike generic duration parsers,** the `--since` and `--usage-since` flags **reject durations outside the 5 min–7 day window** for usage queries.  
- **Unlike a plain string,** the `--variable` option **overwrites duplicate keys**; the last occurrence wins.  
- **Unlike stable commands,** any `cron` sub‑command is **UNSTABLE/Tech Preview** and may change; scripts should avoid hard‑coding cron‑specific behavior.  

## Version and Compatibility Notes
- The reference reflects **plugin version 0.7.0** (commit 887b0b3, 2026‑03‑20). Earlier 0.4.x versions exist but share identical command signatures.  
- All commands require **Spin CLI ≥ v3.0.0**.  
- **Cron management** (`spin aka cron …` and `spin aka app cron …`) is marked **UNSTABLE** and **Tech Preview** – treat as experimental.  
- **Personal access token creation** supports output formats `plain`, `table`, `json`, `yaml`; default is `plain`.  
- **App status/usage‑since** enforces a **7‑day maximum** and **5‑minute minimum** window.  
- **Environment variable** `SPIN_ALWAYS_BUILD` can be set to force a build when `--build` is supplied.  
- **Variable input** can be supplied as `key=value` or as a file reference (`@file.json`, `@file.toml`). Repeating the flag merges values with later entries overriding earlier ones.  