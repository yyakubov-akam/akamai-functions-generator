# Source: https://techdocs.akamai.com/akamai-functions/docs/list-and-inspect-your-applications
Date: 2026-08-16T10:56:54.003302
Model: gpt-oss:120b-cloud
## Required Patterns

**List all applications (plain‑text)**
```shell
spin aka app list
```

**List all applications as JSON**
```shell
spin aka app list --format json
```

**List all applications with IDs (verbose)**
```shell
spin aka app list --verbose
```

**Inspect the linked application**
```shell
spin aka app status
```

**Inspect a specific application by name**
```shell
spin aka app status --app-name <app-name>
```

**Inspect a specific application and get JSON output**
```shell
spin aka app status --app-name <app-name> --format json
```

---

## Common Mistakes and Gotchas

- **Unlike generic CLI tools that default to JSON, Akamai Functions commands output plain‑text by default.**  
  *If you need machine‑readable data, you must add the `--format json` flag.*

- **Unlike some CLI utilities that combine `--verbose` with JSON output, Akamai Functions treats `--verbose` as a separate mode that prints names with IDs in plain‑text.**  
  *Do not expect `--verbose` to produce JSON; use `--format json` for that.*

---