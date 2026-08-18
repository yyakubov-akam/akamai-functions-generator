# Source: https://techdocs.akamai.com/akamai-functions/docs/application-logs
Date: 2026-08-17T09:09:48.173129
Model: glm-4.7-flash:q8_0
## Runtime Constraints

*   (No relevant content in source)

## Supported APIs and Syntax

*   `log/slog` package — Used by Spin applications to generate log messages

## Required Patterns

*   (No relevant content in source)

## Common Mistakes and Gotchas

*   Unlike standard behavior where logs are local, Akamai Functions captures everything written to `stdout` and `stderr`.
*   Unlike standard behavior where the CLI might auto-detect, the `spin aka logs` command defaults to the application linked to your workspace; use `--app-name` to target a specific application if not linked.

## Version and Compatibility Notes

*   Spin applications must be written in Go.
*   Compatible with Spin framework v3.