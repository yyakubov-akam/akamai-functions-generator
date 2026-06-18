# Source: https://techdocs.akamai.com/akamai-functions/docs/welcome
Date: 2026-06-05T08:47:57.308399
Model: gpt-oss:120b-cloud
## Supported APIs and Syntax
- `spin aka deploy` — Deploy a Spin application to Akamai Functions using the `spin aka` plugin.  
- `spin` — General Spin CLI command for building, testing, and running Spin applications locally before deployment.  

## Required Patterns
**Deployment pattern**
```bash
# Build (if needed) and deploy the Spin application to Akamai Functions
spin aka deploy
```
*Use the `spin aka deploy` command as the sole step for publishing a Spin‑based function to the Akamai Functions platform.*

## Version and Compatibility Notes
- Akamai Functions is currently **limited‑availability (public preview)**; access requires completion of the onboarding form.  
- The platform runs **Spin applications compiled to WebAssembly**, supporting SDKs for **Rust, Go, JavaScript, and Python**.  
- Documentation was **last updated 2 months ago**; features may change as the preview progresses.