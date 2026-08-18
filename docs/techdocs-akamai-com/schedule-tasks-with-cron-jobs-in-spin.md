# Source: https://techdocs.akamai.com/akamai-functions/docs/schedule-tasks-with-cron-jobs-in-spin
Date: 2026-08-17T09:23:04.920741
Model: glm-4.7-flash:q8_0
## Runtime Constraints

- Cron job support is currently in Tech Preview.
- Applications must use the `http-js` template.
- All cron schedules must be specified in UTC.

## Supported APIs and Syntax

`spin new -E akamai-functions -t http-js --accept-defaults <app-name>` — Create a new Spin application for Akamai Functions.

`spin aka deploy` — Deploy the current workspace to Akamai Functions.

`spin aka cron create "<schedule>" "<path>" "<name>"` — Create a cron job associated with the deployed application.

`spin aka cron list` — List all running cron jobs for the application.

`spin aka cron delete "<name>"` — Delete a specific cron job.

`addEventListener('fetch', handler)` — Attach the router to the fetch event.

`AutoRouter` — Initialize the router (imported from `itty-router`).

`router.get(path, handler)` — Define a route that responds to GET requests.

`new URL(request.url)` — Parse the request URL to access query parameters.

`new Date().toISOString()` — Capture the current timestamp.

`console.log(message)` — Log messages to the application logs.

`new Response(body, options)` — Return a generic success response.

## Required Patterns

### Basic HTTP Handler Pattern
Initialize `AutoRouter`, define a route, and attach it to the fetch event.

```javascript
import { AutoRouter } from 'itty-router';

let router = AutoRouter();

router.get("/", (request) => {
    const url = new URL(request.url);
    const now = new Date().toISOString();
    console.log(`Cron job triggered at ${now}"`);
    return new Response("Cron job executed", { status: 200 });
});

addEventListener('fetch', (event) => {
    event.respondWith(router.fetch(event.request));
});
```

### Cron Job Creation Pattern
Use standard crontab syntax for the schedule argument.

```shell
spin aka cron create "*/5 * * * *" "/" "cron-job-1"
```

## Common Mistakes and Gotchas

- Unlike standard local cron implementations, Akamai Functions cron jobs must be created and managed using the `spin aka cron` CLI commands.
- Unlike standard local execution, cron schedules must use UTC time. If a specific time of day is required, convert local time to UTC.
- Unlike standard Node.js environments, Akamai Functions requires the `http-js` template and uses `itty-router` for routing.
- You can have multiple cron jobs per Spin application, but the combination of **schedule** and **path and query** must be unique.

## Version and Compatibility Notes

- Support for Cron jobs is currently in Tech Preview.
- The `http-js` template is required for cron job functionality.