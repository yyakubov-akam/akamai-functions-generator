# Source: https://techdocs.akamai.com/akamai-functions/docs/update-an-application
Date: 2026-08-16T10:57:03.054777
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not rely on built‑in support for running multiple versions simultaneously (e.g., canary or blue‑green deployments are **not** available).
- Do not omit the `--variable` flag when your application requires runtime variables; the deployment will fail without them.

## Supported APIs and Syntax
- `spin aka deploy` — Deploys the current Spin application to Akamai Functions.  
- `spin aka deploy --variable <key>=<value>` — Deploys the application while setting a single runtime variable. Multiple `--variable` flags may be used to pass several key/value pairs.

## Required Patterns
**Pattern: Bump application version in `spin.toml` before redeploy**
```toml
# spin.toml
version = "0.1.0"   # original version
# → change to the new version
version = "0.1.1"
```

**Pattern: Deploy (or redeploy) the application**
```shell
# Simple deployment
spin aka deploy

# Deployment with variables
spin aka deploy --variable API_KEY=abcd1234 --variable DEBUG=true
```

**Pattern: Full update workflow**
```shell
# 1️⃣ Edit spin.toml → bump version (optional but recommended)
# 2️⃣ Save changes
# 3️⃣ Deploy with any required variables
spin aka deploy --variable ENV=prod
```

## Common Mistakes and Gotchas
- **Unlike typical CI/CD pipelines**, Akamai Functions does **not** automatically provide canary or blue‑green deployment mechanisms; you must manage version roll‑outs manually.
- **Unlike a plain `spin deploy`**, omitting required `--variable` arguments will cause the deployment to error out or result in missing configuration at runtime.
- **Unlike some platforms that auto‑increment versions**, Akamai Functions will **not** change the `version` field for you; you must edit `spin.toml` yourself or accept the default major‑version upgrade prompted during deployment.

## Version and Compatibility Notes
- You may manually edit the `version` field in `spin.toml` (e.g., `0.1.0` → `0.1.1`). This step is optional; if omitted, the deployment process will prompt for a major‑version default upgrade.
- The `spin aka deploy` command works with the current Akamai Functions runtime; no additional feature flags are required.