# Source: https://techdocs.akamai.com/akamai-functions/docs/application-logs
Date: 2026-06-30T09:40:41.938098
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not write log data to files; only `stdout` and `stderr` are captured by Akamai Functions.
- Do not rely on any logging library that writes to locations other than `stdout`/`stderr`.
- The `spin aka logs` command must be used to retrieve logs; there is no programmatic API for log retrieval inside the function.

## Supported APIs and Syntax
- `spin aka logs` — CLI command that streams all `stdout`/`stderr` output from the linked application to the terminal.  
- `spin aka logs --app-name <app>` — Retrieves logs for a specific application without linking the workspace.  
- `spin aka logs --verbose` — Enables verbose Spin error messages in the log stream.  

## Required Patterns
**Pattern: Write logs to stdout/stderr**  
```js
// Example using console (writes to stdout)
console.log('INFO GET /hello: Handled by handle_hello');

// Example using console.error (writes to stderr)
console.error('WARN Greet invoked with invalid payload. Will respond with HTTP 400');
```

**Pattern: Retrieve logs via CLI**  
```bash
# Default: logs for linked application
spin aka logs

# One‑time fetch for a specific app
spin aka logs --app-name hello-akamai-functions

# Verbose error output
spin aka logs --verbose
```

## Common Mistakes and Gotchas
- Unlike typical Node.js environments where you might use file‑based loggers, Akamai Functions **only captures** output written to `stdout` and `stderr`.
- Unlike some platforms that provide a logging SDK, Akamai Functions **does not expose** a programmatic logging API; you must rely on standard console streams.
- Unlike local development where logs appear in the terminal, **logs are not automatically displayed** when running `spin up`; you must consult the observability guide or use the `spin aka logs` command after deployment.

## Version and Compatibility Notes
- No feature flags or version constraints are mentioned for log capture; the behavior is consistent across current Akamai Functions releases.