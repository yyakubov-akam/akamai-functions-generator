# Source: https://techdocs.akamai.com/akamai-functions/docs/welcome
Date: 2026-07-22T11:11:20.095341
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use languages that cannot be compiled to WebAssembly; only **Rust**, **Go**, **JavaScript**, and **Python** are supported for Akamai Functions.

## Supported APIs and Syntax
- `spin aka deploy` — Deploy a Spin application (compiled to WebAssembly) to Akamai Functions with a single command.

## Required Patterns
**Pattern: Deploying a Spin application to Akamai Functions**

```bash
# Build the Spin application (example for JavaScript/TypeScript)
spin build

# Deploy the built WebAssembly module to Akamai Functions
spin aka deploy
```

## Version and Compatibility Notes
- Akamai Functions is currently in **public preview** (limited availability). Features and limits may change before general availability.