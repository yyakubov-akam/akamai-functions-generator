---
updatedAt: 2026-07-23T22:20:42.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further.

# Schedule tasks with cron jobs in Spin (Tech Preview)

This tutorial shows you how to schedule HTTP requests in a Spin application running on Akamai Functions using cron jobs. The [`spin aka cron` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-cron) allows applications to receive scheduled HTTP triggers without relying on external services.

> 👍
>
> Support for Cron jobs currently in Tech Preview.

# Prerequisites

Before you start this tutorial, make sure you have the following prerequisites. You can also follow the steps in the [Quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart) guide to get up and running with Akamai Functions in less than two minutes.

* Sign up for the public preview so you can [login](https://techdocs.akamai.com/akamai-functions/docs/quickstart#login-to-akamai-functions) to Akamai Functions. If you haven’t already requested access, please complete the [Onboarding form](https://fibsu0jcu2g.typeform.com/fwf-preview?typeform-source=developer.fermyon.com).
* [Install Spin](https://techdocs.akamai.com/akamai-functions/docs/quickstart#install-spin) and the [aka Plugin for Spin](https://techdocs.akamai.com/akamai-functions/docs/quickstart#install-the-aka-plugin-for-spin).

# Introduction to cron jobs

Cron jobs are scheduled tasks that run at specified intervals. They are commonly used for automating repetitive tasks such as data processing, report generation, and background maintenance. Other potential use cases include:

* Automated data backups
* Periodic API polling
* Log file rotation
* Scheduled notifications

# Create a Spin application

You need a Spin application deployed to Akamai Functions to associate a cron job.

1. Create a new Spin application using the `http-js` template.

```shell
spin new -E akamai-functions -t http-js --accept-defaults hello-world

cd hello-world

npm install
```

2. Update the event handler to confirm that our Spin application runs at the expected interval.

To keep things simple, the code sample below also includes a log statement that prints the time the application is triggered. This will help to verify that the cron job is working correctly. In a real-world scenario, you might query a database for stale records, call an API to sync data, or trigger a more complex workflow like sending a report or cleaning up expired sessions.

To apply the simple log changes, navigate to the `hello-world` directory, open `src/index.js`, and add the following code snippet.

```javascript
// For AutoRouter documentation refer to https://itty.dev/itty-router/routers/autorouter
import { AutoRouter } from 'itty-router';

// Initialize the router
let router = AutoRouter();

// Define a route that responds to GET requests 
router.get("/", (request) => {
    // Parse the request URL to access query parameters
    const url = new URL(request.url);

    // Capture the current timestamp
    const now = new Date().toISOString();

    // Log every time the route is triggered, including the message (if any)
    console.log(`Cron job triggered at ${now}"`);

    // Return a generic success response
    return new Response("Cron job executed", {
        status: 200,
    });
});

// Attach the router to the fetch event
addEventListener('fetch', (event) => {
    event.respondWith(router.fetch(event.request));
});
```

3. To build and run the application locally, run the following command.

```shell
spin build --up
```

4. Use this curl command on the application’s endpoint to test if it is working as expected.

```curl
curl localhost:3000
```

You should see the following output in response.

```shell
Cron job executed
```

# Deploy a Spin application to Akamai Functions

Before scheduling our cron job, we need to deploy our Spin application to the Akamai Functions platform.

1. Use the [`spin aka deploy` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-deploy) to deploy the application.

```shell
spin aka deploy
```

Here's an example of a successful deployment.

```shell
Name of new app: hello-world
Creating new app hello-world in account your-account
Note: If you would instead like to deploy to an existing app, cancel this deploy and link this workspace to the app with `spin aka app link`
OK to continue? yes
Workspace linked to app hello-world
Waiting for app to be ready... ready

App Routes:
- hello-world: https://ec8a19d8-6d10-4056-bb69-cc864306b489.aka.fermyon.tech (wildcard)
```

2. Use the domain name provided to you by Akamai Functions to test that the Spin application is working as expected by curling the new endpoint.

```curl
curl https://af30f3b0-ed52-4c5b-b2dd-b261945ff696.aka.fermyon.tech/
```

3. You should receive the same message as you did during local testing.

```shell
Cron job executed
```

# Schedule a cron job for your Spin application

You can use the [`spin aka cron` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-cron) to invoke the Spin application’s HTTP endpoint on a scheduled basis. The schedule uses standard crontab syntax.

> 👍
>
> `spin aka cron` supports multiple digits in each cron field, as well as intervals in any position, for example `* */12 * * *` to run every 12 hours). You can also use comma-separated lists and ranges. If your schedule includes a specific time of day, be sure to use UTC—you may need to [convert your local time to UTC](https://www.worldtimebuddy.com/?pl=1\&lid=100\&h=100\&hf=1) to ensure correct execution.

1. Create a cron job that triggers your Spin application every 5 minutes using the `spin aka cron create` subcommand. The cron job you generate with this subcommand will be associated with the Spin application in your current working directory that you deployed to Akamai Functions. The `spin aka cron create` subcommand takes three arguments:

* **Schedule**. How often the job runs, in standard cron syntax.
* **Path and query**. The HTTP path and (optional) query parameters to invoke.
* **Name**. A name for your cron job.

> 📘
>
> You can have multiple cron jobs per Spin application as long as the combination of **schedule** and **path and query\*** is unique. You might want multiple cron jobs in a single Spin application when different tasks need to run on separate schedules or require different logic. For example, you may want your Spin application to fetch different types of data, perform distinct maintenance routines, or sync with multiple external services independently.

2. Schedule a job to hit the `/*` path with a msg query parameter set to “fwf” every 5 minutes, for a Spin app named hello-world.

```shell
spin aka cron create "*/5 * * * *" "/" "cron-job-1"
```

3. You should see output similar to this example.

```shell
Created cron which will next run at 2025-04-02 04:00:00 UTC
```

4. You can wait 5 minutes and check the application logs with the `spin aka logs` subcommand. In this example the  cron job invoked the application every five minutes as expected.

```shell
spin aka logs --app-name hello-world  
2025-04-02 04:00:00 [hello-world]  Cron job triggered at 2025-04-12T04:00:00Z
```

# Manage cron jobs

You can view all of your running cron jobs using the [`spin aka cron list` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-cron-list).

```shell
spin aka cron list
```

```shell
+----------------+--------------+-------------------------+
| Name           | Schedule     | Next Run                |
+=========================================================+
| cron-job-1     |  */5 * * * * | 2025-04-02 04:00:00 UTC |
+----------------+--------------+-------------------------+
```

# Delete a cron job

To delete a cron job, use the [`spin aka cron delete` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-cron-delete).

```shell
spin aka cron delete cron-job-1
```

```shell
Deleted cron job 'cron-job-1' with schedule '_/5 _ \* \* \*'
```

Your application will persist unless you explicitly run the `spin aka app delete` command.

# Sibling pages

* [Integrate with Property Manager](https://techdocs.akamai.com/akamai-functions/docs/integrate-with-property-manager.md)
* [Stream data from Linode Object Store](https://techdocs.akamai.com/akamai-functions/docs/stream-data-from-linode-object-store.md)
* [Query relational databases: MySQL](https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-mysql.md)
* [Query relational databases: PostgreSQL](https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-postgresql.md)
* [Build a Supabase cache proxy](https://techdocs.akamai.com/akamai-functions/docs/build-a-supabase-cache-proxy.md)
* [Use the Key Value store](https://techdocs.akamai.com/akamai-functions/docs/use-the-key-value-store.md)