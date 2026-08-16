# Source: https://techdocs.akamai.com/akamai-functions/docs/link-an-application
Date: 2026-08-16T10:56:44.578806
Model: gpt-oss:120b-cloud
## Supported APIs and Syntax

- `spin aka link` — Links the current workspace to an Akamai Functions application (prompts for selection).  
- `spin aka app link --app-name <app-name>` — Directly links the workspace to the specified application.  
- `spin aka app unlink` — Unlinks the current workspace from its associated application.  
- `spin aka info` — Displays authentication info, workspace root directory, and any linked application.  
- `spin aka deploy` — Deploys the workspace’s Spin application; on first run it also creates the link automatically.  
- `spin aka logs` — Retrieves logs for the linked application (or the one specified with `--app-name`).  

---

## Required Patterns

**Link a workspace (interactive)**  
```shell
spin aka link
```

**Link a workspace (direct)**  
```shell
spin aka app link --app-name <app-name>
```

**Verify linkage**  
```shell
spin aka info
# Example output shows:
# Workspace Info
#   Root dir: /path/to/workspace
#   Linked app: <app-name>
```

**Unlink a workspace**  
```shell
spin aka app unlink
```

**Deploy (automatically links on first run)**  
```shell
spin aka deploy
```

**Access logs (uses linked app by default)**  
```shell
spin aka logs
```

---

## Common Mistakes and Gotchas

- Unlike many CLI tools that require you to specify the target application on every command, **Akamai Functions will automatically use the linked application** after you run `spin aka link` (or after the first `spin aka deploy`).  
- Forgetting to run `spin aka info` after linking/unlinking may lead you to assume the workspace is still linked; always verify with `spin aka info`.  