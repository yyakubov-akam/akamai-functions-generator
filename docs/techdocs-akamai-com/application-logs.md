# Source: https://techdocs.akamai.com/akamai-functions/docs/application-logs
Date: 2026-07-22T11:15:02.804684
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not rely on log files; Akamai Functions captures **only** data written to `stdout` and `stderr`.
- Log output is streamed to `stdout` by default; there is no separate log storage mechanism.
- Verbose spin error messages are **not** emitted unless the `--verbose` flag is supplied to the `spin aka logs` command.

## Supported APIs and Syntax
- `spin aka logs` — Retrieves logs for the Spin application linked to the current workspace.  
- `spin aka logs --app-name <app-name>` — Retrieves logs for the specified application (one‑time connection).  
- `spin aka logs --verbose` — Enables verbose spin error messages in the log output.  
- `spin aka link` — Links the current workspace to an application running on Akamai Functions.  
- `log/slog` (Go) — Standard Go logging package used by Spin applications; any output from this package ends up on `stdout`/`stderr` and is captured by Akamai Functions.

## Required Patterns
**Pattern: Emit logs via standard output streams**  
```js
// JavaScript (Node.js) example
console.log('INFO GET /hello: Handled by handle_hello func');
console.error('WARN Greet invoked with invalid payload. Will respond with HTTP 400');
```

```go
// Go example (using log/slog)
import "log/slog"

slog.Info("GET https://example.com/hello: Handled by handle_hello func")
slog.Warn("Greet invoked with invalid payload. Will respond with HTTP 400")
```
*All messages written to `stdout` or `stderr` are automatically captured and displayed by `spin aka logs`.*

## Common Mistakes and Gotchas
- **Unlike typical server environments**, Akamai Functions does **not** write logs to files; only `stdout`/`stderr` output is captured.  
- **Unlike default CLI behavior**, verbose spin error messages are **not** shown unless the `--verbose` flag is added to `spin aka logs`.  

## Version and Compatibility Notes
*No version‑specific flags or rollout limitations are mentioned in the source document.*