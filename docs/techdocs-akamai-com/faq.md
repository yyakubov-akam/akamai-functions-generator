# Source: https://techdocs.akamai.com/akamai-functions/docs/faq
Date: 2026-07-22T11:14:51.141625
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not assume a login session remains active indefinitely; an idle session expires after **30 days** of inactivity.

## Supported APIs and Syntax
- `spin aka login` — command‑line operation that creates a user account and starts an authentication session for Akamai Functions.

## Common Mistakes and Gotchas
- Unlike typical web applications where a login may persist until explicit logout, **Akamai Functions** sessions **expire after 30 days of inactivity**.  

---