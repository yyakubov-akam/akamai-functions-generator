# Source: https://techdocs.akamai.com/akamai-functions/docs/deploy-using-github-actions
Date: 2026-08-16T10:57:36.579148
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not use a Personal Access Token (PAT) older than its expiration date (default 30 days, maximum 90 days).  
- Do not exceed the maximum PAT expiration of 90 days (`--expiration-days` ≤ 90).  
- Do not attempt to deploy without first running `spin build`.  
- Do not run `spin aka deploy` without authenticating first (`spin aka login --token …`).  
- Do not omit the `--variable` flag when you need to set or override application variables at deploy time.  
- Do not reference a secret name that does not exist in the GitHub repository’s **Secrets and Variables → Actions** store.  
- Do not install Spin on a runner that is not a Linux environment supporting `bash` (the provided workflow uses `ubuntu‑latest`).  

## Supported APIs and Syntax
- `spin aka login --token <PAT>` — Authenticates the CLI session with the supplied Personal Access Token.  
- `spin aka auth token create --name <name>` — Generates a new PAT that expires in 30 days.  
- `spin aka auth token create --name <name> --expiration-days <days>` — Generates a new PAT with a custom expiration (1 ≤ days ≤ 90).  
- `spin build` — Compiles the Spin application into a WebAssembly artifact.  
- `spin aka deploy` — Deploys the built Spin application to Akamai Functions using the currently logged‑in account.  
- `spin aka deploy --variable <key>=<value>` — Deploys while overriding a single application variable.  
- `rustup target add wasm32-wasip1` — Installs the Rust WASM target needed for Rust‑based Spin apps.  
- `curl -fsSL https://wasm-functions.fermyon.app/downloads/install.sh | bash` — Installs the latest Spin binary.  

## Required Patterns  

**PAT creation (CLI)**
```bash
spin aka login
spin aka auth token create --name mytoken   # expires in 30 days
# or with custom expiration
spin aka auth token create --name mytoken --expiration-days 90
```

**GitHub Actions workflow (minimal)**
```yaml
name: Deploy to Akamai Functions
on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Spin
        run: |
          curl -fsSL https://wasm-functions.fermyon.app/downloads/install.sh | bash
          mv spin /usr/local/bin/spin

      - name: Build
        run: spin build

      - name: Login to Akamai Functions
        run: spin aka login --token ${{ secrets.SPIN_AKA_ACCESS_TOKEN }}

      - name: Deploy to Akamai Functions
        run: spin aka deploy
```

**Adding language‑specific build tools (example for Rust)**
```yaml
- name: Add build dependencies
  run: rustup target add wasm32-wasip1
```

**Deploy with application variable**
```yaml
- name: Deploy to Akamai Functions
  run: spin aka deploy --variable compression_level=${{ secrets.COMPRESSION_LEVEL }}
```

**Token rotation workflow**
```bash
# Create new token (optional longer expiry)
spin aka auth token create --name mynewtoken --expiration-days 90
# Update GitHub secret with the new token value
gh secret set SPIN_AKA_ACCESS_TOKEN < new_token.txt
```

## Common Mistakes and Gotchas
- Unlike a typical long‑lived API key, Akamai Functions PATs **expire** (30 days by default, up to 90 days max).  
- Unlike generic CI scripts, the workflow **must** run `spin aka login` **before** any `spin aka deploy`.  
- Unlike a local development environment, the GitHub Actions runner **does not** have Spin pre‑installed; you must install it via the provided `curl … install.sh` step.  
- Unlike a plain `spin deploy`, using `spin aka deploy --variable …` is required to set or override variables at deploy time.  
- Unlike standard secret handling, the PAT is shown **only once** when created; failing to copy it immediately results in loss of the token.  

## Version and Compatibility Notes
- The install script (`https://wasm-functions.fermyon.app/downloads/install.sh`) always fetches the **latest stable Spin release**; ensure the runner has network access to this URL.  
- PAT expiration can be set up to **90 days** via `--expiration-days`; any value above 90 will be rejected.  
- The reference workflow targets **Ubuntu‑latest** runners; other OS images may require adjustments to the installation commands.  