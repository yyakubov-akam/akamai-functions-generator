# Source: https://techdocs.akamai.com/akamai-functions/docs/deploy-app-variables
Date: 2026-08-16T10:57:18.827987
Model: gpt-oss:120b-cloud
## Supported APIs and Syntax

- `spin aka deploy --variable key=value` — Deploys a Spin application to Akamai Functions while overriding the value of an application variable defined in `spin.toml`.  
- `spin aka deploy --file path/to/spin.toml` — Specifies an alternate manifest file for the deployment.  
- `spin.toml` variable declaration syntax:  

  ```toml
  [variables]
  compression_level = { default = "1" }
  ```

  Defines an application variable named `compression_level` with a default value of `"1"`.

## Required Patterns

**Pattern: Declare an application variable in `spin.toml`**

```toml
[variables]
my_variable = { default = "default-value" }
```

**Pattern: Deploy with an overridden variable value**

```bash
spin aka deploy --variable my_variable=custom-value
```

**Pattern: Deploy using a custom manifest file**

```bash
spin aka deploy --file ./path/to/custom-spin.toml
```

**Pattern: Full deployment flow (example)**

```bash
# 1. Define variable in spin.toml
cat > spin.toml <<'EOF'
[variables]
compression_level = { default = "1" }
EOF

# 2. Deploy, overriding the variable
spin aka deploy --variable compression_level=3
```

## Common Mistakes and Gotchas

- **Unlike typical environment variables, Akamai Functions encrypts application variables at rest and in transit**, but the underlying cryptographic implementations have **not been assessed for PCI compliance**.  
- **Unlike a code change, updating an application variable still creates a new deployment version** (the version number is incremented). Forgetting this can lead to confusion when tracking releases.  

## Version and Compatibility Notes

- Application variables are **encrypted by default** on the Akamai Functions platform. No additional flags are required to enable encryption.  
- No explicit feature‑flag or bundle‑version requirements are documented for using application variables; they are available in all current releases of the Spin framework for Akamai Functions.  