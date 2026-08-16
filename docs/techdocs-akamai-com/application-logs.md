# Source: https://techdocs.akamai.com/akamai-functions/docs/application-logs
Date: 2026-07-31T09:06:09.665033
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not write log output to files; only `stdout` and `stderr` are captured by Akamai Functions.  
- The `spin aka logs` command must be invoked with `--app-name <app>` when the workspace is not linked, otherwise it defaults to the linked application.  

## Supported APIs and Syntax
- `spin aka logs --app-name <app>` — Retrieves logs for the specified Akamai Functions application.  
- `spin aka link` — Links the current workspace to an Akamai Functions application for future `spin aka logs` calls without `--app-name`.  
- `spin aka logs --verbose` — Enables verbose Spin error messages in the log output.  

## Required Patterns
```js
// Minimal logging pattern for an Akamai Functions handler (Node.js)
export async function handler(event) {
  // Standard informational log
  console.log('INFO', new Date().toISOString(), 'Handling request', event);

  // Warning or error log
  console.error('WARN', new Date().toISOString(), 'Invalid payload received');

  // Return a response as usual
  return new Response('OK', { status: 200 });
}
```

## Common Mistakes and Gotchas
- Unlike typical Node.js environments where logs may be written to files or external services, Akamai Functions **only captures** output written to `stdout` and `stderr`.  
- Unlike generic CLI tools, the `spin aka logs` command **does not automatically include** verbose Spin error messages; you must add the `--verbose` flag.  

## Version and Compatibility Notes
*No specific version or feature‑flag information is provided in the source document.*