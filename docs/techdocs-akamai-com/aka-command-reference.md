# Source: https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference
Date: 2026-06-05T09:06:01.367238
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not omit the required `--schedule <SCHEDULE>` option when creating a cron job.  
- Do not set token expiration‑days greater than **90** (`--expiration-days <DAYS>`).  
- Do not request `--usage-since` outside the range **5 minutes** – **7 days** (inclusive).  
- Do not use the `cron` sub‑commands in production; they are marked **UNSTABLE** and may change.  
- Do not omit required arguments (e.g., `<NAME>` for `cron delete`).  
- Do not pass both `--account-id` and `--account-name` simultaneously; they are mutually exclusive alternatives.  
- Do not exceed the default `--max-lines` of **10** when using `logs` without specifying a larger value.  

## Supported APIs and Syntax
```
SpinAka.app.delete(options)                     — Delete an app
SpinAka.app.deploy(options)                     — Deploy an app to Akamai Functions
SpinAka.app.link(options)                       — Link a local workspace to an existing app
SpinAka.app.list(options)                       — List apps
SpinAka.app.logs(options)                        — Fetch logs for an app
SpinAka.app.status(options)                     — Display information about an app
SpinAka.app.unlink(options)                      — Unlink a local workspace from an app
SpinAka.app.history(options)                    — List past events for an app
SpinAka.app.cron.create(options)                — Create a cron job for the current app
SpinAka.app.cron.delete(name, options)          — Delete a cron job from the current app
SpinAka.app.cron.list(options)                  — List cron jobs for the current app
SpinAka.auth.login(options)                     — Log into Akamai Functions
SpinAka.auth.token.create(options)              — Create a new personal access token
SpinAka.auth.token.delete(options)              — Delete a personal access token
SpinAka.auth.token.list(options)                 — List personal access tokens for the current user
SpinAka.auth.token.regenerate(options)          — Regenerate a personal access token
SpinAka.cron.create(options)                    — Create a cron job for the current app (top‑level)
SpinAka.cron.delete(name, options)              — Delete a cron job from the current app (top‑level)
SpinAka.cron.list(options)                      — List cron jobs for the current app (top‑level)
SpinAka.deploy(options)                           — Deploy an app (alias of `app deploy`)
SpinAka.info(options)                            — Print user and workspace information
SpinAka.login(options)                           — Log into Akamai Functions (alias of `auth login`)
SpinAka.logs(options)                            — Fetch logs for an app (alias of `app logs`)
SpinAka.sendFeedback()                           — Send feedback
```

*All `options` correspond to the flags shown in the help output (e.g., `--account-id <ACCOUNT_ID>`, `--from <PATH>`, `--variable <KEY=VALUE|@FILE.json|@FILE.toml>`, etc.).*  

## Required Patterns
**Pattern 1 – Variable Passing**  
```bash
spin aka app deploy ... --variable key1=value1 --variable @config.json --variable @settings.toml
```
*Repeat `--variable` for each key/value or file; later keys override earlier ones.*

**Pattern 2 – Path Specification**  
```bash
-f, --from <PATH>        # defaults to "./spin.toml" if omitted
```
*Always provide a path when the manifest is not in the current directory.*

**Pattern 3 – Time/Duration Syntax**  
```bash
--since <DURATION>       # e.g., "30m", "2h", "1d", "2023-04-01T12:00:00Z"
--usage-since <DURATION> # same format, limited to 5m–7d
```
*Units: `s` (seconds), `m` (minutes), `h` (hours), `d` (days).*

**Pattern 4 – Cron Creation**  
```bash
spin aka app cron create \
  --schedule "0 0 * * *" \
  --name my-cron \
  --path-and-query "/api/cron?foo=bar"
```
*`--schedule` is mandatory; `--name` and `--path-and-query` are optional.*

**Pattern 5 – Token Creation**  
```bash
spin aka auth token create \
  --name my-token \
  --description "CI token" \
  --expiration-days 30 \
  --short
```
*`--name` is required; `--expiration-days` defaults to 30, max 90.*

## Common Mistakes and Gotchas
- Unlike many CLIs, **`--account-id` and `--account-name` are mutually exclusive**; providing both is ignored and the command falls back to the current context.  
- Unlike generic token tools, **`--expiration-days` cannot exceed 90**; the CLI will reject larger values.  
- Unlike typical log commands, **the default `--since` period is 7 days**, not “all time”.  
- Unlike stable commands, **`cron` sub‑commands are marked UNSTABLE** and may change without notice.  
- Unlike some CLI frameworks, **the `--from` flag defaults to `./spin.toml`**; omitting it does *not* search the current directory for other manifests.  
- Unlike standard `--max-lines` behavior, the `logs` command defaults to **10 lines** if `--max-lines` is not supplied.  

## Version and Compatibility Notes
- All commands require **Spin >= v3.0.0**.  
- The CLI version shown in help (`0.7.0` as of 2026‑03‑20) adds several flags not present in older `0.4.x` releases (e.g., `--account-name`, `--skip-readiness-check`).  
- Features introduced in **0.7.0** (e.g., `--account-name`, `--skip-readiness-check`, `--usage-since` limits) may be unavailable in environments still using **0.4.x**.  
- The `cron` family (`spin aka cron …` and `spin aka app cron …`) is labeled **UNSTABLE / Tech Preview** and should be treated as experimental.  
- The `--expiration-days` flag in `auth token create` added a **max = 90** constraint in version 0.7.0; earlier versions allowed any positive integer.  
- The `--no-confirm` flag for destructive actions (`delete`, `token delete`) is present in both versions but may have differing default prompts.  