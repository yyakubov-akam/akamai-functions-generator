---
updatedAt: 2026-04-16T15:02:17.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further.

# Application logs

Spin application logs help you to understand runtime behavior and gather insights.

Use the [`spin aka logs` command](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference#spin-aka-logs) to retrieve logs for your Spin applications deployed to Akamai Functions.

> 👍
>
> By default, this command provides logs for the application [linked](https://techdocs.akamai.com/akamai-functions/docs/link-an-application) to your workspace. If your workspace isn’t linked to an application, you can either specify the application name using the `--app-name` flag for a one-time connection or run `spin aka link` to link your workspace to an application running on Akamai Functions.

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

The log messages above were generated using the [`log/slog` package](https://go.dev/blog/slog) by a Spin application written in Go. Everything your Spin application writes to `stdout` and `stderr` is captured by Akamai Functions and made accessible via the `spin aka logs` command.

By default, the logs print to `stdout` on Akamai Functions. To enable verbose spin error messages, you need to run add the `--verbose` flag. To see applications logs when running your function locally with `spin up`, please go the [observability guide for Spin](https://spinframework.dev/v3/observing-apps#application-logs) for more information.