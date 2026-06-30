# Source: https://techdocs.akamai.com/akamai-functions/docs/faq
Date: 2026-06-30T09:40:31.472947
Model: gpt-oss:120b-cloud
## Supported APIs and Syntax
- `spin aka login` — initiates a user login session; creates a token that remains valid for 30 days of inactivity.  

## Required Patterns
**Login before any Spin application operation**

```bash
# Acquire a login token (valid for 30 days without activity)
spin aka login

# Subsequent Spin commands (e.g., deploy, view) can now be run
# spin deploy my-app
# spin status my-app
```

**Account‑scoped application management**

```bash
# Personal account – applications are isolated to the logged‑in user
spin app create my-personal-app   # belongs only to your account

# Team account – applications are shared among team members
spin app create my-team-app       # requires a team account context
```

## Common Mistakes and Gotchas
- **Unlike typical short‑lived session tokens, Akamai Functions login sessions persist for 30 days without activity.** Forgetting this may lead developers to assume they need to re‑login more frequently.  
- **Unlike many multi‑tenant platforms where resources are globally visible, Akamai Functions isolates Spin applications to the owning account.** Attempting to access another user’s application without a team account will fail.  
- **Unlike generic CLI tools, the `spin aka login` command is the only supported way to obtain authentication for all subsequent Spin commands.** Using alternative authentication methods will not work.  