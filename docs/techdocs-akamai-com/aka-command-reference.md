# Source: https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference
Date: 2026-07-22T11:14:29.568117
Model: gpt-oss:120b-cloud
## Runtime Constraints
- **Spin version** – All commands require **Spin ≥ v3.0.0**.  
- **Required flags** – `spin aka cron create` and `spin aka app cron create` **must** include `--schedule <SCHEDULE>`.  
- **Expiration limit** – `spin aka auth token create` accepts `--expiration-days` **max = 90** (hard limit).  
- **Usage‑since window** – `spin aka app status` enforces a **maximum of 7 days** and a **minimum of 5 minutes** for `--usage-since`.  
- **Variable precedence** – When `--variable` is supplied multiple times, **the last occurrence wins**.  
- **Build flag** – `--build` on `spin aka app deploy` (or `spin aka deploy`) is **ignored for remote apps**; only local apps trigger a `spin build`.  
- **Auto‑generated names** – Omit `--name` on any `cron create` command to let the platform generate a unique name.  
- **Confirmation prompts** – `--no-confirm` may be used on destructive commands (`delete`, `unlink`) to bypass interactive confirmation.  
- **Path default** – `-f, --from <PATH>` defaults to `./spin.toml` if omitted.  
- **Account context** – If neither `--account-id` nor `--account-name` is supplied, the **current account context** is used.  

---

## Supported APIs and Syntax
*(CLI commands are treated as callable APIs for the coding agent)*  

| Command (signature) | Description |
|----------------------|-------------|
| `spin aka auth login [--token <TOKEN>]` | Log into Akamai Functions using an optional personal access token. |
| `spin aka auth token create --name <NAME> [--description <DESCRIPTION>] [--expiration-days <DAYS>] [--format <FORMAT>] [--short]` | Create a new personal access token. |
| `spin aka auth token delete --id <ID> [--no-confirm]` | Delete a personal access token. |
| `spin aka auth token list [--format <FORMAT>] [--verbose]` | List tokens for the current user. |
| `spin aka auth token regenerate --id <ID>` | Regenerate an existing token. |
| `spin aka app list [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--format <FORMAT>] [--verbose]` | List all apps in the account. |
| `spin aka app link [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--from <PATH>]` | Link the local workspace to an existing app. |
| `spin aka app unlink [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--from <PATH>]` | Unlink the local workspace from its app. |
| `spin aka app deploy [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--build] [--cache-dir <CACHE_DIR>] [--create-name <NEW_APP_NAME>] [--from <PATH>] [--no-confirm] [--skip-readiness-check] [--variable <KEY=VALUE|@FILE.json|@FILE.toml>...]` | Deploy (or create) an app. |
| `spin aka app delete [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--from <PATH>] [--no-confirm]` | Delete an app. |
| `spin aka app status [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--from <PATH>] [--format <FORMAT>] [--usage-since <USAGE_SINCE>]` | Show app details and usage statistics. |
| `spin aka app logs [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--component-id <COMPONENT_ID>] [--deployment-version <DEPLOYMENT_VERSION>] [--from <PATH>] [--max-lines <MAX_LINES>] [--region <REGION>] [--since <SINCE>] [--verbose]` | Retrieve logs for an app (or component). |
| `spin aka app cron create --schedule <SCHEDULE> [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--from <PATH>] [--name <NAME>] [--path-and-query <PATH_AND_QUERY>]` | Create a cron job for the current app. |
| `spin aka app cron delete <NAME> [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--from <PATH>]` | Delete a specific cron job. |
| `spin aka app cron list [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--from <PATH>]` | List all cron jobs for the current app. |
| `spin aka cron create --schedule <SCHEDULE> [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--from <PATH>] [--name <NAME>] [--path-and-query <PATH_AND_QUERY>]` | (Tech‑preview) Create a cron job (same flags as `app cron create`). |
| `spin aka cron delete <NAME> [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--from <PATH>]` | (Tech‑preview) Delete a cron job. |
| `spin aka cron list [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--from <PATH>]` | (Tech‑preview) List cron jobs. |
| `spin aka info [--format <FORMAT>]` | Print user and workspace information. |
| `spin aka logs [--account-id <ACCOUNT_ID>] [--account-name <ACCOUNT_NAME>] [--app-id <APP_ID>] [--app-name <APP_NAME>] [--component-id <COMPONENT_ID>] [--deployment-version <DEPLOYMENT_VERSION>] [--from <PATH>] [--max-lines <MAX_LINES>] [--region <REGION>] [--since <SINCE>] [--verbose]` | Fetch logs for an app (global shortcut). |
| `spin aka send-feedback` | Open a feedback submission (no options). |

---

## Required Patterns
> **Pattern 1 – Authenticate before any other command**  
```bash
spin aka auth login --token $MY_AKAMAI_TOKEN
```

> **Pattern 2 – Deploy a local app with environment variables**  
```bash
spin aka app deploy \
  --from ./my-app \
  --build \
  --variable DB_HOST=prod.db.example.com \
  --variable @secrets.json
```

> **Pattern 3 – Create a cron job with a custom request path**  
```bash
spin aka app cron create \
  --schedule "0 2 * * *" \
  --name nightly-cleanup \
  --path-and-query "/maintenance/cleanup?force=true"
```

> **Pattern 4 – List apps in JSON for machine‑readable output**  
```bash
spin aka app list --format json
```

> **Pattern 5 – Delete an app without interactive confirmation**  
```bash
spin aka app delete --app-name my-old-app --no-confirm
```

> **Pattern 6 – Retrieve the last 20 log lines for a specific component**  
```bash
spin aka logs \
  --app-name my-app \
  --component-id comp-12345 \
  --max-lines 20 \
  --verbose
```

> **Pattern 7 – Generate a short‑lived personal access token**  
```bash
spin aka auth token create \
  --name "ci-runner" \
  --expiration-days 7 \
  --short
```

---

## Common Mistakes and Gotchas
- **Unlike standard CLI tools, Akamai Functions** does **not** assume a default account when `--account-id`/`--account-name` are omitted; it **uses the current account context** instead.  
- **Unlike many CLI utilities, Akamai Functions** treats `-f/--from` **as optional**; if omitted it **defaults to `./spin.toml`**.  
- **Unlike generic `spin` commands, Akamai Functions** will **ignore `--build` for remote apps**; the flag only triggers a local `spin build`.  
- **Unlike typical token creation, Akamai Functions** caps `--expiration-days` at **90 days**; values above are rejected.  
- **Unlike some APIs, the `--variable` flag** can be **repeated**, but **the last value for a duplicate key wins**.  
- **Unlike older versions, the `--no-confirm` flag** must be **explicitly added** to skip prompts on destructive actions.  
- **Unlike generic `spin` output, the default format for many list commands** is **plain text**, not JSON; specify `--format json` when machine‑readable data is required.  

---

## Version and Compatibility Notes
- **All documented commands require Spin ≥ v3.0.0**.  
- The **0.7.0** release (dated 2026‑03‑20) adds **UNSTABLE/Tech‑Preview** cron sub‑commands and expands flag sets (e.g., `--account-name`, `--no-confirm`, `--skip-readiness-check`).  
- The **0.4.x** releases (2025‑05‑22 / 2025‑07‑04) lack some newer flags (`--account-name`, `--no-confirm`, `--skip-readiness-check`) and default to older behavior.  
- **Cron management commands** (`spin aka cron …` and `spin aka app cron …`) are marked **UNSTABLE**; they may change in future releases.  
- **`spin aka auth token create`**: `--expiration-days` default = 30, max = 90 (enforced in 0.7.0).  
- **`spin aka app status`**: `--usage-since` default = 7d, enforced range **5 min – 7 d** (0.7.0).  
- **Environment variable** `SPIN_ALWAYS_BUILD` can be used to force a build even when `--build` is omitted.  

*The agent should target the latest 0.7.0 command signatures and respect the constraints above.*