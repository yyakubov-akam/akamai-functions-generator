---
updatedAt: 2026-11-05T20:44:45.000Z
agentTools:
  siteIndex: https://techdocs.akamai.com/llms.txt
  projectIndex: https://techdocs.akamai.com/akamai-functions/llms.txt
---

# Application logs and usage

You can review the Akamai Functions [usage](https://techdocs.akamai.com/akamai-functions/docs/application-logs#usage) metrics to see how often your application is invoked. You can also check the application [logs](https://techdocs.akamai.com/akamai-functions/docs/application-logs#logs) to help you understand runtime behavior and gather insights.

# Usage

The [`spin aka app status` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-app-status) provides basic information about the application, including the number of invocations over a specific time period.

> 📘
>
> By default, this command provides information for the application [linked](https://techdocs.akamai.com/akamai-functions/docs/link-an-application) to your workspace. If your workspace isn’t linked to an application, you can specify the application name using the `--app-name` and `--account-name` flags or run `spin aka link` to link your workspace to an application running on Akamai Functions.

You can use the `--usage-since` argument to specify the time period for the usage metrics. The `--usage-since` argument supports a maximum of 7 days (`7d`), a minimum of 5 minutes (`5m`), and defaults to 7 days (`7d`).

```shell
spin aka app status --app-name hello-akamai-functions -–usage-since 3d
```

The `spin aka app status` command prints all log messages to `stdout`.

```shell
Name: hello-akamai-functions  
ID: 11077e3b-d632-4df3-921f-f7ebefb9aaca  
URLs:  
  https://11077e3b-d632-4df3-921f-f7ebefb9aaca.fwf.app  
Created at: 2026-03-30 14:49:15 UTC  
Invocations: 86502 in the last 3 days
```

Upon request, full usage information can be made available in [Akamai Control Center Billing](https://techdocs.akamai.com/billing-app/docs/welcome-billing) so you can track usage across more than seven days. Contact your Akamai representative for more information.

# Logs

Spin application logs help you to understand runtime behavior and gather insights.

Use the [`spin aka logs` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-logs) to retrieve logs for your Spin applications deployed to Akamai Functions.

> 👍
>
> By default, this command provides logs for the application [linked](https://techdocs.akamai.com/akamai-functions/docs/link-an-application) to your workspace. If your workspace is not linked to an application, you can specify the application name using the `--app-name` and `--account-name` flags, or run `spin aka link` to link your workspace to an application running on Akamai Functions.

```shell
spin aka logs --app-name hello-akamai-functions
```

The `spin aka logs` command prints all log messages to `stdout`.

```shell
2025-01-16 13:31:46 [hello-akamai-functions]  2025/01/16 13:31:36 INFO GET https://11077e3b-d632-4df3-921f-f7ebefb9aaca.fwf.app/hello: Handled by handle_hello func
2025-01-16 13:31:48 [hello-akamai-functions]  2025/01/16 13:31:47 INFO POST https://11077e3b-d632-4df3-921f-f7ebefb9aaca.fwf.app/greet: Handled by handle_greet func
2025-01-16 13:31:48 [hello-akamai-functions]  2025/01/16 13:31:47 WARN Greet invoked with invalid payload. Will respond with HTTP 400
2025-01-16 13:32:04 [hello-akamai-functions]  2025/01/16 13:31:56 INFO POST https://11077e3b-d632-4df3-921f-f7ebefb9aaca.fwf.app/greet: Handled by handle_greet func
```

The log messages above were generated using the [`log/slog` package](https://go.dev/blog/slog) by a Spin application written in Go. Everything your Spin application writes to `stdout` and `stderr` (for example, via JavaScript’s `console.log`) is captured by Akamai Functions and made accessible via the `spin aka logs` command.

By default, the logs print to `stdout` in Akamai Functions. To enable verbose Spin error messages, you need add the `--verbose` flag. To see applications logs when running your function locally with `spin up`,  see the [observability guide for Spin](https://spinframework.dev/observing-apps#application-logs).

> 📘
>
> As described on the [Quotas and limits](https://techdocs.akamai.com/akamai-functions/docs/quotas-and-limits) page, you should only use Akamai Functions logging for debugging at low traffic levels. It does not provide full large scale observability.