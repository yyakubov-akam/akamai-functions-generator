---
updatedAt: 2026-06-12T01:14:42.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further.

# Integrate with Property Manager

This tutorial integrates a Spin application - deployed to your Akamai Functions account - with an existing Akamai Property to route requests through your property to the Spin application.

The goal of this tutorial is to route a specific path on your existing property, for example, `<https://www.mydomain.com/hello>` to your Spin application deployed to Akamai Functions.

> 👍
>
> As this guide does not provide an introduction to Akamai Properties you may want to consult the [Akamai Property Manager](https://techdocs.akamai.com/property-mgr/docs/welcome-prop-manager) documentation.

# Prerequisites

Before you start this tutorial, make sure you have the following prerequisites. You can also follow the steps in the [Quickstart](https://techdocs.akamai.com/akamai-functions/docs/quickstart) guide to get up and running with Akamai Functions in less than two minutes.

* [Create and configure a Property](https://techdocs.akamai.com/property-mgr/docs/workflow-ov) in Akamai Control Center.
* Sign up for the public preview so you can [login](https://techdocs.akamai.com/akamai-functions/docs/quickstart#login-to-akamai-functions) to Akamai Functions. If you haven’t already requested access, please complete the [Onboarding form](https://fibsu0jcu2g.typeform.com/fwf-preview?typeform-source=developer.fermyon.com).
* [Install Spin](https://techdocs.akamai.com/akamai-functions/docs/quickstart#install-spin) and the [aka Plugin for Spin](https://techdocs.akamai.com/akamai-functions/docs/quickstart#install-the-aka-plugin-for-spin).

# Build and deploy the Spin app

We'll use a  simple Spin application as part of this tutorial.

1. Use the `spin` CLI to create a new application using the `http-js` template and move it into the application directory.

```shell
spin new -E akamai-functions -t http-js -a hello-akamai-functions

cd hello-akamai-functions
```

2. To modify the implementation of the app, replace the contents of the `index.js` file with the following lines of JavaScript code.  The `index.js` file is located in the `src` directory of your application.

```javascript
Fimport { AutoRouter } from 'itty-router';

let router = AutoRouter();

router.get("/", () => new Response("Hello, Akamai Functions"));

addEventListener('fetch', async (event) => {  
    event.respondWith(router.fetch(event.request));  
});
```

3. Once you’ve updated the `src/index.js` file, use the `spin build` command to compile your source code to WebAssembly. Then use the [`spin aka deploy` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-deploy) to deploy the application to Akamai Functions.

```shell
spin build

spin aka deploy
```

> 👍
>
> You need to be authenticated to use the [`spin aka deploy` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-deploy). Use the [`spin aka login` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-login) to authenticate using your Akamai Control Center or GitHub account credentials.

4. The `spin aka deploy` command will generate an output similar to the one shown below.

```shell
Name of new app: hello-akamai-functions
Creating new app hello-akamai-functions in account your-account
Note: If you would instead like to deploy to an existing app, cancel this deploy and link this workspace to the app with `spin aka app link`
OK to continue? yes
Workspace linked to app hello-akamai-functions
Waiting for app to be ready... ready

App Routes:
- hello-akamai-functions: https://ec8a19d8-6d10-4056-bb69-cc864306b489.aka.akamai.tech (wildcard)
```

5. Copy the URL from the output in your terminal window, we’ll need it in a second to configure the Akamai Property.

# Route traffic to the Spin application through an Akamai property

Next, we have to update the Property in Akamai Control Center.

1. Navigate to [Akamai Control Center](https://control.akamai.com/apps/home-page/#/home) and find your Property.
2. Open its latest version, and press the **Edit New Version** button (located in the top right corner).
3. From the Property Configuration Settings click the **+ Rule** button, select the **Blank Rule Template** and provide a name for the new rule.

[block:image]
{
  "images": [
    {
      "image": [
        "https://techdocs.akamai.com/akamai-functions/img/functions-add-new-rule-v1.jpg",
        null,
        "Property Manager Blank Rule Template"
      ],
      "align": "center",
      "sizing": "900px",
      "border": true
    }
  ]
}
[/block]

4. Next, add a new match condition using the **+ Match** button from the **Criteria** panel and configure it for `Path` to `matches one of` and add `/hello/*` as  the value.

[block:image]
{
  "images": [
    {
      "image": [
        "https://techdocs.akamai.com/akamai-functions/img/functions- add-matchpath-v1.jpg",
        null,
        "Match condition for hello"
      ],
      "align": "center",
      "sizing": "900px",
      "border": true
    }
  ]
}
[/block]

With the match condition in place, we can add the custom behaviors using the Behaviors panel.

5. Add the [Origin Server](https://techdocs.akamai.com/property-mgr/docs/origin-server) behavior using the **Standard Property Behavior** button from within the **+ Behavior** drop-down button. We’ll leave the majority of properties  settings unchanged. However, ensure to update these fields.

[block:parameters]
{
  "data": {
    "h-0": "Field name",
    "h-1": "Desired value",
    "0-0": "Origin Server Hostname",
    "0-1": "`<origin*` of your Spin application.  \nYou can use the [`spin aka app status` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-app-status)  or [`spin aka deploy` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-deploy) to find the origin server host name of your Spin application.",
    "1-0": "Forward Host Header",
    "1-1": "Origin Hostname"
  },
  "cols": 2,
  "rows": 2,
  "align": [
    "left",
    "left"
  ]
}
[/block]

> 📘
>
> You can get the origin of your Spin Application by removing the `https://` prefix and the trailing slash (`/`) from the end of its URL.

6. Next, we'll prevent the Akamai Property from sending the routing criteria `(/hello/)` as a path to the Spin application running on Akamai Functions.

To do this, we'll add a [Modify Outgoing Request Path](https://techdocs.akamai.com/property-mgr/docs/modify-outgoing-req-path) behavior to our rule. Use the Standard Property Behavior button from within the **+ Behaviors** drop-down button. Update the following fields in the **Modify Outgoing Request Path** behavior.

| Field name                | Desired value                     |
| :------------------------ | :-------------------------------- |
| Action                    | Replace Part of the incoming path |
| Find what                 | `/hello/`                         |
| Replace with              | `/`                               |
| Occurrences               | First occurrence only             |
| Keep the query parameters | Yes                               |

Here are the behaviors configured for this tutorial.

[block:image]
{
  "images": [
    {
      "image": [
        "https://techdocs.akamai.com/akamai-functions/img/functions-add-origin-server-v1.jpg",
        null,
        "Origin Server behavior"
      ],
      "align": "center",
      "sizing": "900px",
      "border": true
    }
  ]
}
[/block]

[block:image]
{
  "images": [
    {
      "image": [
        "https://techdocs.akamai.com/akamai-functions/img/functions-modify-out-req-path-v1.jpg",
        null,
        "Modify Outgoing Request Path behavior"
      ],
      "align": "center",
      "sizing": "900px",
      "border": true
    }
  ]
}
[/block]

Click the **Save** button.

# Activate the new property version

At this point, the new rule isn’t active, yet! We have to activate the latest version of our Property in order for our changes to take effect. Activate the latest version of your Property using the **Activate** tab.

> 👍
>
> We highly recommend activating and testing the property modifications using the Staging environment instead of going straight to production.

# Call the Spin app through the Akamai property

To test the rule added as part of this tutorial, you can use a tool like `curl` to send a `GET` request to `https://engineerd.xyz/hello/` . Make sure you replace `https://engineerd.xyz` with the domain associated to your Property.

If the rule is configured correctly, we should see the same response being printed to `stdout` as if we would send a `GET` request to the root route of our Spin application deployed to Akamai Functions.

```curl
curl https://engineerd.xyz/hello/
```

You should see `Hello, Akamai Functions` printed to `stdout`. This means that you’ve successfully integrated a Spin application, running on Akamai Functions, with an existing Property.

# Sibling pages

* [Stream data from Linode Object Store](https://techdocs.akamai.com/akamai-functions/docs/stream-data-from-linode-object-store.md)
* [Query relational databases: MySQL](https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-mysql.md)
* [Query relational databases: PostgreSQL](https://techdocs.akamai.com/akamai-functions/docs/query-relational-databases-postgresql.md)
* [Build a Supabase cache proxy](https://techdocs.akamai.com/akamai-functions/docs/build-a-supabase-cache-proxy.md)
* [Schedule tasks with cron jobs in Spin (Tech Preview)](https://techdocs.akamai.com/akamai-functions/docs/schedule-tasks-with-cron-jobs-in-spin.md)
* [Use the Key Value store](https://techdocs.akamai.com/akamai-functions/docs/use-the-key-value-store.md)