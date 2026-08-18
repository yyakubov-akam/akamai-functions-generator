# Source: https://techdocs.akamai.com/akamai-functions/docs/deploy-app-variables
Date: 2026-08-17T09:27:52.973433
Model: glm-4.7-flash:q8_0
## Runtime Constraints

*   No specific runtime constraints (CPU, memory, module restrictions) are defined in this source document.

## Supported APIs and Syntax

*   `spin aka deploy` — Deploys the application to Akamai Functions.
*   `spin.toml` — Configuration file for defining application variables.

## Required Patterns

### Define Variables in Configuration
Declare variables within the `[variables]` section of the `spin.toml` file.

```toml
[variables]
compression_level = { default = "1" }
```

### Deploy with Variable Overrides
Use the `--variable` flag with `spin aka deploy` to override variable values without modifying the application code.

```shell
spin aka deploy --variable compression_level=3
```

## Common Mistakes and Gotchas

*   Unlike standard deployments where configuration changes might be hot-swapped, Akamai Functions propagates variable changes as a new deployment, incrementing the version number.
*   Unlike standard secrets, Akamai Functions encrypts application variables at rest and in transit by default.
*   Unlike standard PCI compliance, the underlying cryptographic implementations for application variables have not been assessed for PCI compliance.

## Version and Compatibility Notes

*   Requires Spin v3.
*   Last updated: 2026-08-05