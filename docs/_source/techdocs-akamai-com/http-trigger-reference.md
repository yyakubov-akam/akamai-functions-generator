---
updatedAt: 2026-03-26T14:47:40.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further.

# HTTP trigger reference

Akamai Functions currently supports the `http` [trigger type](https://spinframework.dev/v3/http-trigger) for Spin applications.

```
[[trigger.http]]
route = "/..."                # the route that the trigger matches
component = "my-application"  # the name of the component to handle this route
```

# HTTP Requests

Learn about the inbound HTTP request received by an application or a specific component when running on Akamai Functions.

## Request Headers

In addition to any headers passed by the client making the request to an application, several Spin-related headers are included in the request passed to your component.

[block:parameters]
{
  "data": {
    "h-0": "Header",
    "h-1": "Description",
    "0-0": "[`spin-full-url`](https://spinframework.dev/v3/http-trigger#additional-request-information-spin-full-url)",
    "0-1": "The full URL of the request. This includes full host and scheme information.",
    "1-0": "[`spin-path-info`](https://spinframework.dev/v3/http-trigger#additional-request-information-spin-path-info)",
    "1-1": "The request path relative to the component route.",
    "2-0": "[`spin-path-match-n`](https://spinframework.dev/v3/http-trigger#additional-request-information-spin-path-match-n)",
    "2-1": "(Conditionally included) Where n is the pattern for a single-segment wildcard value.  \nFor example, `spin-path-match-userid` will access the value in a URL containing a route that includes `userid`.",
    "3-0": "[`spin-matched-route`](https://spinframework.dev/v3/http-trigger#additional-request-information-spin-matched-route)",
    "3-1": "The part of the trigger route that was matched by the route, including the wildcard indicator if present.",
    "4-0": "[`spin-raw-component-route`](https://spinframework.dev/v3/http-trigger#additional-request-information-spin-raw-component-route)",
    "4-1": "The component route pattern matched, including the wildcard indicator if present.",
    "5-0": "",
    "5-1": ""
  },
  "cols": 2,
  "rows": 6,
  "align": [
    "left",
    "left"
  ]
}
[/block]

The triggered component can also use the `true-client-ip` header. It returns the IP of the client sending the request. For example, `151.49.93.60`

# Sibling pages

* [aka command reference](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference.md)
* [WebAssembly language support matrix](https://techdocs.akamai.com/akamai-functions/docs/webassembly-language-support-matrix.md)
* [WebAssembly standards](https://techdocs.akamai.com/akamai-functions/docs/related-standards.md)
* [FAQ](https://techdocs.akamai.com/akamai-functions/docs/faq.md)