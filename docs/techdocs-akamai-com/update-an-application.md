# Source: https://techdocs.akamai.com/akamai-functions/docs/update-an-application
Date: 2026-08-17T09:26:39.142562
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Do not rely on built-in support for running multiple versions simultaneously (e.g., canary or blue-green deployments).
- In-flight requests are gracefully completed by the previous version; no simultaneous version routing is available.

## Supported APIs and Syntax

- `spin aka deploy` — Deploys the application to Akamai Functions.
- `version` (in `spin.toml`) — Specifies the application version string.

## Required Patterns

### Update Application Version
Edit the `spin.toml` file to increment the version number before deployment.

```toml
version = "0.1.1"
```

### Deploy Application
Run the deployment command to push changes.

```shell
spin aka deploy
```

### Deploy with Variables
Specify application variables during deployment.

```shell
spin aka deploy --variable <key>=<value>
```

## Common Mistakes and Gotchas

- Unlike standard deployment workflows that might support instant zero-downtime updates via multiple versions, Akamai Functions does not support running multiple versions simultaneously.

## Version and Compatibility Notes

- When upgrading a Spin application, remember to specify application variables explicitly using the `--variable` flag, as they are not automatically retained if not re-specified.