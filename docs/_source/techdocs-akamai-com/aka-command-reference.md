---
updatedAt: 2026-03-31T19:48:19.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further. Append .md to any documentation page URL to get its markdown version.

# aka command reference

The `spin aka` plugin lets you interact with the Akamai Functions platform. Use this plugin to log in, deploy, and inspect applications running on Akamai Functions.

> 👍
>
> For instruction on how to install the plugin, go to [Install the aka plugin for Spin](https://techdocs.akamai.com/akamai-functions/docs/quickstart#install-the-aka-plugin-for-spin) in this guide.

# spin aka

Spin compatibility: >=v3.0.0

```Text v.0.7.0
$ spin aka --help
spin-aka 0.7.0 (887b0b3 2026-03-20)
Spin plugin for Akamai Functions

USAGE:
    spin aka <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    app              Manage apps deployed to Akamai Functions
    auth             Manage user authentication
    cron             UNSTABLE: Manage cron jobs for an app
    deploy           Deploy an app to Akamai Functions
    help             Print this message or the help of the given subcommand(s)
    info             Print out user and workspace information
    login            Log into Akamai Functions
    logs             Fetch the logs for an app
    send-feedback    Send us your feedback!
```
```text v0.4.0
$ spin aka --help

spin-aka 0.4.0 (d0e9cc8 2025-05-22)
Spin plugin for Akamai Functions

USAGE:
    spin aka <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    app              Manage apps deployed to Akamai Functions
    auth             Manage user authentication
    cron             UNSTABLE: Manage cron jobs for an app
    deploy           Deploy an app to Akamai Functions
    help             Print this message or the help of the given subcommand(s)
    info             Print out user and workspace information
    login            Log into Akamai Functions
    logs             Fetch the logs for an app
    send-feedback    Send us your feedback!

```

# spin aka app

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app --help
spin-aka-app 0.7.0 (887b0b3 2026-03-20)
Manage apps deployed to Akamai Functions

USAGE:
    spin aka app <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    cron       UNSTABLE: Manage cron jobs for an app
    delete     Delete an app
    deploy     Deploy an app to Akamai Functions
    help       Print this message or the help of the given subcommand(s)
    history    Lists past events for an app
    link       Link your local workspace to an existing Akamai Functions app
    list       List apps
    logs       Fetch the logs for an app
    status     Display information about an app
    unlink     Unlink your local workspace from an existing Akamai Functions app
```
```Text v0.4.0
$ spin aka app --help

spin-aka-app 0.4.0 (d0e9cc8 2025-05-22)
Manage apps deployed to Akamai Function

USAGE:
    spin aka app <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    cron       UNSTABLE: Manage cron jobs for an app
    delete     Delete an app
    deploy     Deploy an app to Akamai Functions
    help       Print this message or the help of the given subcommand(s)
    history    Lists past events for an app
    link       Link your local workspace to an existing Akamai Functions app
    list       List apps
    logs       Fetch the logs for an app
    status     Display information about an app
    unlink     Unlink your local workspace from an existing Akamai Functions app

```

# spin aka app cron (Tech Preview)

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app cron --help
spin-aka-app-cron 0.7.0 (887b0b3 2026-03-20)
UNSTABLE: Manage cron jobs for an app

USAGE:
    spin aka app cron <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    create    Create a cron job for the current app
    delete    Delete a cron job from the current app
    help      Print this message or the help of the given subcommand(s)
    list      List cron jobs for the current app
```

# spin aka app cron create

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app cron create --help
spin-aka-app-cron-create 0.7.0 (887b0b3 2026-03-20)
Create a cron job for the current app

USAGE:
    spin aka app cron create [OPTIONS] --schedule <SCHEDULE>

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

        --name <NAME>
            Optional name of the cron job
            
            Will default to an auto-generated name.

    -p, --path-and-query <PATH_AND_QUERY>
            The path and query of the request to make to the app
            
            e.g., "/api/cron?foo=bar".

    -s, --schedule <SCHEDULE>
            The cron schedule configuration
            
            e.g., "0 0 * * *" for every day at midnight.

    -V, --version
            Print version information
```

# spin aka app cron delete

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app cron delete --help
spin-aka-app-cron-delete 0.7.0 (887b0b3 2026-03-20)
Delete a cron job from the current app

USAGE:
    spin aka app cron delete [OPTIONS] <NAME>

ARGS:
    <NAME>
            The name of the cron job to delete

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -V, --version
            Print version information
```

# spin aka app cron list

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app cron list --help
spin-aka-app-cron-list 0.7.0 (887b0b3 2026-03-20)
List cron jobs for the current app

USAGE:
    spin aka app cron list [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -V, --version
            Print version information
```

# spin aka app delete

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app delete --help
spin-aka-app-delete 0.7.0 (887b0b3 2026-03-20)
Delete an app

USAGE:
    spin aka app delete [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

        --no-confirm
            Skip the delete confirmation prompt

    -V, --version
            Print version information
```

# spin aka app deploy

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app deploy --help
spin-aka-app-deploy 0.7.0 (887b0b3 2026-03-20)
Deploy an app to Akamai Functions

USAGE:
    spin aka app deploy [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app to deploy to
            
            If `app-id` is not provided, the app will be inferred from the workspace config. If no
            app is inferred a new app will be created.

        --build
            For local apps, specifies to perform `spin build` before deploying the app
            
            This is ignored on remote apps, as they are already built.
            
            [env: SPIN_ALWAYS_BUILD=]

        --cache-dir <CACHE_DIR>
            Cache directory for downloaded components and assets

        --create-name <NEW_APP_NAME>
            Name of the new app that will be created
            
            This is only valid when you are deploying to an app that does not exist yet.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

        --no-confirm
            Skip the deploy confirmation prompt

        --skip-readiness-check
            Skip readiness check after deployment

    -V, --version
            Print version information

        --variable <KEY=VALUE | @FILE.json | @FILE.toml>...
            Variable(s) to be passed to the app
            
            A single key-value pair can be passed as `key=value`. Alternatively, the path to a JSON
            or TOML file may be given as `@file.json` or `@file.toml`.
            
            This option may be repeated. If the same key is specified multiple times the last value
            will be used.
```

# spin aka app create

Spin compatibility: >=v3.0.0

```Text v0.4.0
$ spin aka app delete --help

spin-aka-app-delete 0.4.0 (d0e9cc8 2025-05-22)
Delete an app

USAGE:
    spin aka app delete [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

        --app-id <APP_ID>
            ID of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app

            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.

            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

        --no-confirm
            Skip the delete confirmation prompt

    -V, --version
            Print version information
```

# spin aka app help

Spin compatibility: >=v3.0.0

```Text v0.4.0
$ spin aka app help --help
```

# spin aka app history

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app history --help
spin-aka-app-history 0.7.0 (887b0b3 2026-03-20)
Lists past events for an app

USAGE:
    spin aka app history [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

        --format <FORMAT>
            Desired output format
            
            [default: plain]
            [possible values: plain, json]

    -h, --help
            Print help information

    -V, --version
            Print version information
```
```Text v0.4.0
$ spin aka app history --help
spin-aka-app-history 0.4.1 (486ad84 2025-07-04)
Lists past events for an app

USAGE:
    spin aka app history [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

        --app-id <APP_ID>
            ID of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app

            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.

            If omitted, it defaults to "./spin.toml".

        --format <FORMAT>
            Desired output format

            [default: plain]
            [possible values: plain, json]

    -h, --help
            Print help information

    -V, --version
            Print version information
```

# spin aka app link

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app link --help
spin-aka-app-link 0.7.0 (887b0b3 2026-03-20)
Link your local workspace to an existing Akamai Functions app

USAGE:
    spin aka app link [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app to link to.
            
            If neither `app-id` nor `app-name` is provided, the app will be selected from an
            interactive prompt.

        --app-name <APP_NAME>
            Name of the app to link to.
            
            If neither `app-id` nor `app-name` is provided, the app will be selected from an
            interactive prompt.

    -f, --from <PATH>
            A path to the workspace you want to link.
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -V, --version
            Print version information
```
```Text v0.4.0
$ spin aka app link --help

spin-aka-app-link 0.4.0 (d0e9cc8 2025-05-22)
Link your local workspace to an existing Akamai Functions app

USAGE:
    spin aka app link [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

        --app-id <APP_ID>
            ID of the app to link to.

            If neither `app-id` nor `app-name` is provided, the app will be selected from an
            interactive prompt.

        --app-name <APP_NAME>
            Name of the app to link to.

            If neither `app-id` nor `app-name` is provided, the app will be selected from an
            interactive prompt.

    -f, --from <PATH>
            A path to the workspace you want to link.

            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.

            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -V, --version
            Print version information

```

# spin aka app list

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app list --help
spin-aka-app-list 0.7.0 (887b0b3 2026-03-20)
List apps

USAGE:
    spin aka app list [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --format <FORMAT>
            Desired output format
            
            [default: plain]
            [possible values: plain, json]

    -h, --help
            Print help information

    -V, --version
            Print version information

        --verbose
            Show more detailed information
```
```Text v0.4.0
$ spin aka app list --help

spin-aka-app-list 0.4.0 (d0e9cc8 2025-05-22)
List apps

USAGE:
    spin aka app list [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

        --format <FORMAT>
            Desired output format

            [default: plain]
            [possible values: plain, json]

    -h, --help
            Print help information

    -V, --version
            Print version information

        --verbose
            Show more detailed information
```

# spin aka app logs

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app logs --help
spin-aka-app-logs 0.7.0 (887b0b3 2026-03-20)
Fetch the logs for an app

USAGE:
    spin aka app logs [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --component-id <COMPONENT_ID>
            Only return logs for the given component ID
            
            If this is omitted, logs from all components will be returned.

        --deployment-version <DEPLOYMENT_VERSION>
            Only return logs for the given deployment version
            
            If this is omitted, logs from the latest deployment version will be returned.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -n, --max-lines <MAX_LINES>
            Number of lines to show from the end of the logs
            
            [default: 10]

        --region <REGION>
            Only return logs for the given region
            
            If this is omitted, logs from all regions will be returned.

        --since <SINCE>
            Only return logs since the given time
            
            The time can be specified as an RFC3339 timestamp, Unix epoch timestamp in seconds, or
            as a duration from the present. The duration is specified as a number followed by a
            unit: 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days (e.g. "30m" for
            30 minutes ago). The default is 7 days.
            
            [default: 7d]

    -v, --verbose
            Verbose output

    -V, --version
            Print version information
```

# spin aka app status

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app status --help
spin-aka-app-status 0.7.0 (887b0b3 2026-03-20)
Display information about an app

USAGE:
    spin aka app status [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

        --format <FORMAT>
            Desired output format
            
            [default: plain]
            [possible values: plain, json]

    -h, --help
            Print help information

        --usage-since <USAGE_SINCE>
            Only show app usage since the given time.
            
            The time can be specified as an RFC3339 timestamp, Unix epoch timestamp in seconds, or
            as a duration from the present. The duration is specified as a number followed by a
            unit: 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days (e.g. "30m" for
            30 minutes ago). The default is 7 days. A maximum of 7 days and minimum of 5 minutes is
            enforced.
            
            [default: 7d]

    -V, --version
            Print version information
```
```Text v0.4.0
$ spin aka app status --help

spin-aka-app-status 0.4.0 (d0e9cc8 2025-05-22)
Display information about an app

USAGE:
    spin aka app status [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

        --app-id <APP_ID>
            ID of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app

            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.

            If omitted, it defaults to "./spin.toml".

        --format <FORMAT>
            Desired output format

            [default: plain]
            [possible values: plain, json]

    -h, --help
            Print help information

    --usage-since <USAGE_SINCE>
        Only show app usage since the given time.

        The time can be specified as an RFC3339 timestamp, Unix epoch timestamp in seconds, or
        as a duration from the present. The duration is specified as a number followed by a
        unit: 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days (e.g. "30m" for
        30 minutes ago). The default is 7 days. A maximum of 7 days and minimum of 5 minutes is
        enforced.

        [default: 7d]

    -V, --version
            Print version information
```

# spin aka app unlink

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka app unlink --help
spin-aka-app-unlink 0.7.0 (887b0b3 2026-03-20)
Unlink your local workspace from an existing Akamai Functions app

USAGE:
    spin aka app unlink [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

    -f, --from <PATH>
            A path to the workspace you want to unlink.
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -V, --version
            Print version information
```
```Text v0.4.0
$ spin aka app unlink --help

spin-aka-app-unlink 0.4.0 (d0e9cc8 2025-05-22)
Unlink your local workspace from an existing Akamai Functions app

USAGE:
    spin aka app unlink [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

    -f, --from <PATH>
            A path to the workspace you want to unlink.

            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.

            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -V, --version
            Print version information
```

# spin aka auth

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka auth --help
spin-aka-auth 0.7.0 (887b0b3 2026-03-20)
Manage user authentication

USAGE:
    spin aka auth <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    help     Print this message or the help of the given subcommand(s)
    login    Log into Akamai Functions
    token    Manage personal access tokens
```
```Text v0.4.0
$ spin aka auth --help

spin-aka-auth 0.4.0 (d0e9cc8 2025-05-22)
Manage user authentication

USAGE:
    spin aka auth <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    help     Print this message or the help of the given subcommand(s)
    login    Log into Akamai Functions
    token    Manage personal access tokens

```

# spin aka auth help

Spin compatibility: >=v3.0.0

```Text v0.4.0
$ spin aka auth help --help

```

# spin aka auth login

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka auth login --help
spin-aka-auth-login 0.7.0 (887b0b3 2026-03-20)
Log into Akamai Functions

USAGE:
    spin aka auth login [OPTIONS]

OPTIONS:
    -h, --help             Print help information
        --token <TOKEN>    A personal access token to use for authentication [env:
                           SPIN_AKA_ACCESS_TOKEN=]
    -V, --version          Print version information
```

# spin aka auth token

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka auth token --help
spin-aka-auth-token 0.7.0 (887b0b3 2026-03-20)
Manage personal access tokens

USAGE:
    spin aka auth token <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    create        Create a new personal access token
    delete        Delete a personal access token
    help          Print this message or the help of the given subcommand(s)
    list          List personal access tokens for the current user
    regenerate    Regenerate a personal access token
```
```Text v0.4.0
$ spin aka auth token --help

spin-aka-auth-token 0.4.0 (d0e9cc8 2025-05-22)
Manage personal access tokens

USAGE:
    spin aka auth token <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    create        Create a new personal access token
    delete        Delete a personal access token
    help          Print this message or the help of the given subcommand(s)
    list          List personal access tokens for the current user
    regenerate    Regenerate a personal access token

```

# spin aka auth token create

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka auth token create --help
spin-aka-auth-token-create 0.7.0 (887b0b3 2026-03-20)
Create a new personal access token

USAGE:
    spin aka auth token create [OPTIONS] --name <NAME>

OPTIONS:
    -d, --description <DESCRIPTION>
            Description of the token

    -e, --expiration-days <EXPIRATION_DAYS>
            How many days before the token expires [max: 90] [default: 30]

        --format <FORMAT>
            Desired output format [default: plain] [possible values: plain, table, json, yaml]

    -h, --help
            Print help information

    -n, --name <NAME>
            Name of the token

    -s, --short
            Show only the token, without additional information

    -V, --version
            Print version information
```
```Text v0.4.0
$ spin aka auth token create --help

spin-aka-auth-token-create 0.4.0 (d0e9cc8 2025-05-22)
Create a new personal access token

USAGE:
    spin aka auth token create [OPTIONS] --name <NAME>

OPTIONS:
    -d, --description <DESCRIPTION>
            Description of the token

    -e, --expiration-days <EXPIRATION_DAYS>
            How many days before the token expires [default: 30]

        --format <FORMAT>
            Desired output format [default: plain] [possible values: plain, table, json, yaml]

    -h, --help
            Print help information

    -n, --name <NAME>
            Name of the token

    -s, --short
            Show only the token, without additional information

    -V, --version
            Print version information

```

# spin aka auth token delete

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka auth token delete --help
spin-aka-auth-token-delete 0.7.0 (887b0b3 2026-03-20)
Delete a personal access token

USAGE:
    spin aka auth token delete [OPTIONS] --id <ID>

OPTIONS:
    -h, --help          Print help information
    -i, --id <ID>       ID of the personal access token to delete
        --no-confirm    Skip the delete confirmation prompt
    -V, --version       Print version information
```
```Text v0.4.0
$ spin aka auth token delete --help

spin-aka-auth-token-delete 0.4.0 (d0e9cc8 2025-05-22)
Delete a personal access token

USAGE:
    spin aka auth token delete [OPTIONS] --id <ID>

OPTIONS:
    -h, --help          Print help information
    -i, --id <ID>       ID of the personal access token to delete
        --no-confirm    Skip the delete confirmation prompt
    -V, --version       Print version information

```

# spin aka auth token help

Spin compatibility: >=v3.0.0

```Text v0.4.0
$ spin aka auth token help --help
```

# spin aka auth token list

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka auth token list --help
spin-aka-auth-token-list 0.7.0 (887b0b3 2026-03-20)
List personal access tokens for the current user

USAGE:
    spin aka auth token list [OPTIONS]

OPTIONS:
        --format <FORMAT>    Desired output format [default: table] [possible values: plain, table,
                             json, yaml]
    -h, --help               Print help information
    -V, --version            Print version information
        --verbose            Show more detailed information
```
```Text v0.4.0
$ spin aka auth token list --help

spin-aka-auth-token-list 0.4.0 (d0e9cc8 2025-05-22)
List personal access tokens for the current user

USAGE:
    spin aka auth token list [OPTIONS]

OPTIONS:
        --format <FORMAT>    Desired output format [default: table] [possible values: plain, table,
                             json, yaml]
    -h, --help               Print help information
    -V, --version            Print version information
        --verbose            Show more detailed information
```

# spin aka auth token regenerate

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka auth token regenerate --help
spin-aka-auth-token-regenerate 0.7.0 (887b0b3 2026-03-20)
Regenerate a personal access token

USAGE:
    spin aka auth token regenerate --id <ID>

OPTIONS:
    -h, --help       Print help information
    -i, --id <ID>    ID of the personal access token to regenerate
    -V, --version    Print version information
```
```Text v0.4.0
$ spin aka auth token regenerate --help

spin-aka-auth-token-regenerate 0.4.0 (d0e9cc8 2025-05-22)
Regenerate a personal access token

USAGE:
    spin aka auth token regenerate --id <ID>

OPTIONS:
    -h, --help       Print help information
    -i, --id <ID>    ID of the personal access token to regenerate
    -V, --version    Print version information

```

# spin aka cron (Tech Preview)

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka cron --help
spin-aka-cron 0.7.0 (887b0b3 2026-03-20)
UNSTABLE: Manage cron jobs for an app

USAGE:
    spin aka cron <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    create    Create a cron job for the current app
    delete    Delete a cron job from the current app
    help      Print this message or the help of the given subcommand(s)
    list      List cron jobs for the current app
```
```Text v0.4.0
$ spin aka cron --help

spin-aka-cron 0.4.0 (d0e9cc8 2025-05-22)
UNSTABLE: Manage cron jobs for an app

USAGE:
    spin aka cron <SUBCOMMAND>

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

SUBCOMMANDS:
    create    Create a cron job for the current app
    delete    Delete a cron job from the current app
    help      Print this message or the help of the given subcommand(s)
    list      List cron jobs for the current app


```

# spin aka cron create

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka cron create --help
spin-aka-cron-create 0.7.0 (887b0b3 2026-03-20)
Create a cron job for the current app

USAGE:
    spin aka cron create [OPTIONS] --schedule <SCHEDULE>

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

        --name <NAME>
            Optional name of the cron job
            
            Will default to an auto-generated name.

    -p, --path-and-query <PATH_AND_QUERY>
            The path and query of the request to make to the app
            
            e.g., "/api/cron?foo=bar".

    -s, --schedule <SCHEDULE>
            The cron schedule configuration
            
            e.g., "0 0 * * *" for every day at midnight.

    -V, --version
            Print version information
```
```Text v0.4.0
$ spin aka cron create --help

spin-aka-cron-create 0.4.0 (d0e9cc8 2025-05-22)
Create a cron job for the current app

USAGE:
    spin aka cron create [OPTIONS] --schedule <SCHEDULE>

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

        --app-id <APP_ID>
            ID of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app

            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.

            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

        --name <NAME>
            Optional name of the cron job

            Will default to an auto-generated name.

    -p, --path-and-query <PATH_AND_QUERY>
            The path and query of the request to make to the app

            e.g., "/api/cron?foo=bar".

    -s, --schedule <SCHEDULE>
            The cron schedule configuration

            e.g., "0 0 * * *" for every day at midnight.

    -V, --version
            Print version information


```

# spin aka cron delete

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka cron delete --help
spin-aka-cron-delete 0.7.0 (887b0b3 2026-03-20)
Delete a cron job from the current app

USAGE:
    spin aka cron delete [OPTIONS] <NAME>

ARGS:
    <NAME>
            The name of the cron job to delete

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -V, --version
            Print version information
```
```Text v0.4.0
$ spin aka cron delete --help

spin-aka-cron-delete 0.4.0 (d0e9cc8 2025-05-22)
Delete a cron job from the current app

USAGE:
    spin aka cron delete [OPTIONS] <NAME>

ARGS:
    <NAME>
            The name of the cron job to delete

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

        --app-id <APP_ID>
            ID of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app

            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.

            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -V, --version
            Print version information

```

# spin aka cron help

Spin compatibility: >=v3.0.0

```Text v0.4.0
$ spin aka cron help --help

```

# spin aka cron list

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka cron list --help
spin-aka-cron-list 0.7.0 (887b0b3 2026-03-20)
List cron jobs for the current app

USAGE:
    spin aka cron list [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -V, --version
            Print version information
```
```Text v0.4.0
$ spin aka cron list --help

spin-aka-cron-list 0.4.0 (d0e9cc8 2025-05-22)
List cron jobs for the current app

USAGE:
    spin aka cron list [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

        --app-id <APP_ID>
            ID of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app

            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.

            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -V, --version
            Print version information

```

# spin aka deploy

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka deploy --help
spin-aka-deploy 0.7.0 (887b0b3 2026-03-20)
Deploy an app to Akamai Functions

USAGE:
    spin aka deploy [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app to deploy to
            
            If `app-id` is not provided, the app will be inferred from the workspace config. If no
            app is inferred a new app will be created.

        --build
            For local apps, specifies to perform `spin build` before deploying the app
            
            This is ignored on remote apps, as they are already built.
            
            [env: SPIN_ALWAYS_BUILD=]

        --cache-dir <CACHE_DIR>
            Cache directory for downloaded components and assets

        --create-name <NEW_APP_NAME>
            Name of the new app that will be created
            
            This is only valid when you are deploying to an app that does not exist yet.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

        --no-confirm
            Skip the deploy confirmation prompt

        --skip-readiness-check
            Skip readiness check after deployment

    -V, --version
            Print version information

        --variable <KEY=VALUE | @FILE.json | @FILE.toml>...
            Variable(s) to be passed to the app
            
            A single key-value pair can be passed as `key=value`. Alternatively, the path to a JSON
            or TOML file may be given as `@file.json` or `@file.toml`.
            
            This option may be repeated. If the same key is specified multiple times the last value
            will be used.
```
```Text v0.4.0
$ spin aka deploy --help

spin-aka-deploy 0.4.0 (d0e9cc8 2025-05-22)
Deploy an app to Akamai Functions

USAGE:
    spin aka deploy [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

        --app-id <APP_ID>
            ID of the app to deploy to

            If `app-id` is not provided, the app will be inferred from the workspace config. If no
            app is inferred a new app will be created.

        --build
            For local apps, specifies to perform `spin build` before deploying the app

            This is ignored on remote apps, as they are already built.

            [env: SPIN_ALWAYS_BUILD=]

        --cache-dir <CACHE_DIR>
            Cache directory for downloaded components and assets

        --create-name <NEW_APP_NAME>
            Name of the new app that will be created

            This is only valid when you are deploying to an app that does not exist yet.

    -f, --from <PATH>
            A path to the app

            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.

            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

        --no-confirm
            Skip the deploy confirmation prompt

    -V, --version
            Print version information

        --variable <KEY=VALUE | @FILE.json | @FILE.toml>...
            Variable(s) to be passed to the app

            A single key-value pair can be passed as `key=value`. Alternatively, the path to a JSON
            or TOML file may be given as `@file.json` or `@file.toml`.

            This option may be repeated. If the same key is specified multiple times the last value
            will be used.


```

# spin aka help

Spin compatibility: >=v3.0.0

```Text v0.4.0
$ spin aka help --help
```

# spin aka info

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka info --help
spin-aka-info 0.7.0 (887b0b3 2026-03-20)
Print out user and workspace information

USAGE:
    spin aka info [OPTIONS]

OPTIONS:
        --format <FORMAT>    Desired output format [default: plain] [possible values: plain, json]
    -h, --help               Print help information
    -V, --version            Print version information
```
```Text v0.4.0
$ spin aka info --help

spin-aka-info 0.4.0 (d0e9cc8 2025-05-22)
Print out user and workspace information

USAGE:
    spin aka info

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

```

# spin aka login

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka login --help
spin-aka-login 0.7.0 (887b0b3 2026-03-20)
Log into Akamai Functions

USAGE:
    spin aka login [OPTIONS]

OPTIONS:
    -h, --help             Print help information
        --token <TOKEN>    A personal access token to use for authentication [env:
                           SPIN_AKA_ACCESS_TOKEN=]
    -V, --version          Print version information
```
```Text v0.4.0
$ spin aka login --help

spin-aka-login 0.4.0 (d0e9cc8 2025-05-22)
Log into Akamai Functions

USAGE:
    spin aka login [OPTIONS]

OPTIONS:
    -h, --help             Print help information
        --token <TOKEN>    A personal access token to use for authentication [env:
                           SPIN_AKA_ACCESS_TOKEN=]
    -V, --version          Print version information

```

# spin aka logs

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka logs --help
spin-aka-logs 0.7.0 (887b0b3 2026-03-20)
Fetch the logs for an app

USAGE:
    spin aka logs [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in
            
            If neither `--account-id` nor `--account-name` is provided, defaults to the current
            account context.

        --account-name <ACCOUNT_NAME>
            The account name to perform the operation in.
            
            If neither `--account-name` nor `--account-id` is provided, defaults to the current
            account context.

        --app-id <APP_ID>
            ID of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app
            
            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --component-id <COMPONENT_ID>
            Only return logs for the given component ID
            
            If this is omitted, logs from all components will be returned.

        --deployment-version <DEPLOYMENT_VERSION>
            Only return logs for the given deployment version
            
            If this is omitted, logs from the latest deployment version will be returned.

    -f, --from <PATH>
            A path to the app
            
            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.
            
            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

    -n, --max-lines <MAX_LINES>
            Number of lines to show from the end of the logs
            
            [default: 10]

        --region <REGION>
            Only return logs for the given region
            
            If this is omitted, logs from all regions will be returned.

        --since <SINCE>
            Only return logs since the given time
            
            The time can be specified as an RFC3339 timestamp, Unix epoch timestamp in seconds, or
            as a duration from the present. The duration is specified as a number followed by a
            unit: 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days (e.g. "30m" for
            30 minutes ago). The default is 7 days.
            
            [default: 7d]

    -v, --verbose
            Verbose output

    -V, --version
            Print version information
```
```Text v0.4.0
$ spin aka logs --help

spin-aka-logs 0.4.0 (d0e9cc8 2025-05-22)
Fetch the logs for an app

USAGE:
    spin aka logs [OPTIONS]

OPTIONS:
        --account-id <ACCOUNT_ID>
            The account to perform the operation in

            Defaults to the current account context.

        --app-id <APP_ID>
            ID of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

        --app-name <APP_NAME>
            Name of the app

            If neither `app-id` nor `app-name` is provided, the app will be inferred from the
            workspace config.

    -f, --from <PATH>
            A path to the app

            This may be a manifest (spin.toml) file or a directory containing a spin.toml file.

            If omitted, it defaults to "./spin.toml".

    -h, --help
            Print help information

        --since <since>
            Only return logs since the given time

            The time can be specified as an RFC3339 timestamp, Unix epoch timestamp in seconds, or
            as a duration from the present. The duration is specified as a number followed by a
            unit: 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days (e.g. "30m" for
            30 minutes ago). The default is 7 days.

            [default: 7d]

        --tail <tail>
            Number of lines to show from the end of the logs

            [default: 10]

    -v, --verbose
            Verbose output

    -V, --version
            Print version information

```

# spin aka send-feedback

Spin compatibility: >=v3.0.0

```Text v0.7.0
$ spin aka send-feedback --help
spin-aka-send-feedback 0.7.0 (887b0b3 2026-03-20)
Send us your feedback!

USAGE:
    spin aka send-feedback

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information
```
```Text v0.4.0
$ spin aka send-feedback --help

spin-aka-send-feedback 0.4.0 (d0e9cc8 2025-05-22)
Send us your feedback!

USAGE:
    spin aka send-feedback

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information

```

# Sibling pages

* [WebAssembly language support matrix](https://techdocs.akamai.com/akamai-functions/docs/webassembly-language-support-matrix.md)
* [HTTP trigger reference](https://techdocs.akamai.com/akamai-functions/docs/http-trigger-reference.md)
* [WebAssembly standards](https://techdocs.akamai.com/akamai-functions/docs/related-standards.md)
* [FAQ](https://techdocs.akamai.com/akamai-functions/docs/faq.md)