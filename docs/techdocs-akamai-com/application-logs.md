# Source: https://techdocs.akamai.com/akamai-functions/docs/application-logs
Date: 2026-06-05T09:07:25.917169
Model: gpt-oss:120b-cloud
## Supported APIs and Syntax

- `spin aka logs` — Retrieves logs for the Spin application deployed to Akamai Functions; prints all log messages to `stdout`.
- `spin aka logs --app-name <application-name>` — Retrieves logs for the specified application, overriding the workspace‑linked application.
- `spin aka logs --verbose` — Enables verbose Spin error messages in the log output.
- `log/slog` (Go package) — Standard library package for structured logging; any output written to `stdout` or `stderr` via this package is captured by Akamai Functions.

## Required Patterns

**Pattern: Retrieving logs for the linked application**
```bash
spin aka logs
```

**Pattern: Retrieving logs for a specific application**
```bash
spin aka logs --app-name hello-akamai-functions
```

**Pattern: Enabling verbose Spin error messages**
```bash
spin aka logs --verbose
```

**Pattern: Emitting logs from a Go Spin function (captured by Akamai Functions)**
```go
import "log/slog"

func handle_hello(ctx context.Context, req Request) Response {
    slog.Info("GET /hello: Handled by handle_hello func")
    // ...function logic...
}
```

All data written to `stdout` or `stderr` (e.g., via `log/slog`) is automatically captured and made available through the `spin aka logs` command.

## Common Mistakes and Gotchas

- Unlike typical server environments where logs may be written to files, **Akamai Functions only captures output written to `stdout` and `stderr`.** Writing logs to a file will not appear in `spin aka logs`.
- Unlike local development where logs are displayed directly in the terminal, **the `spin aka logs` command prints logs to `stdout` on Akamai Functions**; you must use the `--verbose` flag to see detailed Spin error messages.
- If the workspace is not linked to an application, **the `spin aka logs` command will not know which logs to fetch** unless you provide `--app-name` or run `spin aka link` first.