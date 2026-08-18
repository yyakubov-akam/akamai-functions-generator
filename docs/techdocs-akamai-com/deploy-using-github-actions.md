# Source: https://techdocs.akamai.com/akamai-functions/docs/deploy-using-github-actions
Date: 2026-08-17T09:28:33.574228
Model: glm-4.7-flash:q8_0
## Runtime Constraints

*   Omitted (No relevant content in source).

## Supported APIs and Syntax

*   `spin aka login` — Authenticates the Spin CLI with Akamai Functions.
*   `spin aka auth token create` — Generates a Personal Access Token (PAT).
*   `spin aka auth token create --name <name>` — Creates a PAT with a specific name.
*   `spin aka auth token create --expiration-days <days>` — Creates a PAT with a custom expiration (maximum 90 days).
*   `spin aka deploy` — Deploys the current application to Akamai Functions.
*   `spin aka deploy --variable <key>=<value>` — Deploys the application with specific variable overrides.
*   `gh secret set <name>` — Sets a GitHub repository secret via the GitHub CLI.

## Required Patterns

### GitHub Actions Workflow Structure

```yaml
name: Deploy to Akamai Functions

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Clone repository
      uses: actions/checkout@v4

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

### Token Rotation Sequence

```shell
# 1. Create a new token
spin aka auth token create --name mynewtoken --expiration-days 90

# 2. Copy the token output immediately
# 3. Update the GitHub repository secret
gh secret set SPIN_AKA_ACCESS_TOKEN
```

## Common Mistakes and Gotchas

*   Unlike standard CI/CD workflows, Akamai Functions Personal Access Tokens (PATs) expire by default after 30 days and must be rotated before expiration.
*   Tokens are only displayed once upon creation; ensure the token is saved securely immediately.
*   Unlike standard environment variable assignment, Akamai Functions deployment variables must use the `--variable key=value` format.
*   The Spin installation script redirects `spin` to `/usr/local/bin/spin` to ensure it is available in the PATH.

## Version and Compatibility Notes

*   **GitHub Action:** Use `actions/checkout@v4` for repository cloning.
*   **Spin Installation:** Use the script at `https://wasm-functions.fermyon.app/downloads/install.sh`.
*   **Token Expiration:** Maximum supported expiration is 90 days.