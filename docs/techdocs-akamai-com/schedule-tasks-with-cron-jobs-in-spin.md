# Source: https://techdocs.akamai.com/akamai-functions/docs/schedule-tasks-with-cron-jobs-in-spin
Date: 2026-08-16T10:56:35.061883
Model: gpt-oss:120b-cloud
## Runtime Constraints
- Do not rely on external services for scheduling; use `spin aka cron` to create scheduled HTTP triggers.  
- Cron schedules are interpreted in **UTC**; convert local times accordingly.  
- The cron feature is **Tech Preview** – it may change or be limited in availability.  

## Supported APIs and Syntax
| API / Construct | Signature | Description |
|-----------------|-----------|-------------|
| `AutoRouter()` | `AutoRouter()` | Creates a new router instance (itty‑router). |
| `router.get()` | `router.get(path: string, handler: (request: Request) => Response | Promise<Response>)` | Registers a GET route. |
| `new Response()` | `new Response(body?: BodyInit, init?: ResponseInit)` | Returns an HTTP response. |
| `addEventListener()` | `addEventListener('fetch', (event: FetchEvent) => void)` | Attaches a listener for the `fetch` event. |
| `console.log()` | `console.log(...data: any[])` | Writes a message to the function’s logs. |
| `new Date().toISOString()` | `new Date().toISOString(): string` | Returns the current timestamp in ISO‑8601 format. |
| `URL()` | `new URL(input: string, base?: string)` | Parses a URL string. |
| `spin new` | `spin new -E akamai-functions -t http-js --accept-defaults <app-name>` | Creates a new Spin application from the `http-js` template. |
| `spin build` | `spin build --up` | Builds the app and runs a local development server. |
| `spin aka deploy` | `spin aka deploy` | Deploys the current workspace to Akamai Functions. |
| `spin aka cron create` | `spin aka cron create "<schedule>" "<path>" "<name>"` | Creates a cron job that issues an HTTP request to the given path on the deployed app. |
| `spin aka cron list` | `spin aka cron list` | Lists all cron jobs for the current app. |
| `spin aka cron delete` | `spin aka cron delete <name>` | Deletes the specified cron job. |
| `spin aka logs` | `spin aka logs --app-name <app>` | Streams the logs of the specified deployed app. |

## Required Patterns
### 1. Basic HTTP handler with logging (Spin + Akamai Functions)
```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

router.get("/", (request) => {
  const now = new Date().toISOString();
  console.log(`Cron job triggered at ${now}`);
  return new Response("Cron job executed", { status: 200 });
});

addEventListener('fetch', (event) => {
  event.respondWith(router.fetch(event.request));
});
```

### 2. Creating a cron job that hits the app every 5 minutes
```bash
# Inside the workspace that contains the deployed Spin app
spin aka cron create "*/5 * * * *" "/" "cron-job-1"
```

### 3. Viewing and deleting cron jobs
```bash
# List all cron jobs
spin aka cron list

# Delete a specific job
spin aka cron delete cron-job-1
```

## Common Mistakes and Gotchas
- **Unlike standard cron implementations, Akamai Functions cron schedules are interpreted in UTC** – you must convert any local time to UTC before specifying the schedule.  
- **Unlike typical Node.js environments, you cannot use external schedulers**; the only supported way to run scheduled tasks is via `spin aka cron`.  
- **Unlike generic cron services, the combination of *schedule* and *path & query* must be unique per app** – attempting to create a duplicate will be rejected.  

## Version and Compatibility Notes
- The cron job feature is **Tech Preview**; it may be subject to change and is not yet GA.  
- `spin aka cron` supports:
  - Multiple digits per field (e.g., `*/12` for every 12 hours).  
  - Intervals in any position (`* */12 * * *`).  
  - Comma‑separated lists and ranges (e.g., `0,15,30,45`).  
- All cron syntax follows standard *crontab* conventions, but remember the UTC requirement.  