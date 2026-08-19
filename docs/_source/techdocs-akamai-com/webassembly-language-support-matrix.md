---
updatedAt: 2026-06-22T13:18:15.000Z
---

Fetch the complete documentation index at: https://techdocs.akamai.com/akamai-functions/llms.txt. Use this file to discover all available pages before exploring further.

# WebAssembly language support matrix

This support matrix lists the programming languages that can be compiled to WebAssembly.

It also specifies if you can compile the language to run in the browser, in other non-browser environments, or in a [WASI](https://wasi.dev/) environment. Spin, SpinKube, and Akamai Functions require [WASI](https://wasi.dev/) support. Any language supported for WASI should be supported on the Akamai Functions. The Spin SDK indicates that there is additional libraries available for Spin.

> 👍
>
> For more information about technologies such as WASI, Wagi, and Spin go to the [Related standards](https://developer.fermyon.com/wasm-languages/standards) topic in this guide.

## Support details

Review the for descriptions for each of the language support categories.

* **Core**. An implementation of WebAssembly 1.0 is available.
* **Browser**.  At least one browser implementation is available.
* **WASI**. The language supports at least Preview 1 of the WASI proposal.
* **Spin SDK**. A Spin SDK is available for the language.
* Anything with WASI or Spin SDK support runs on Spin, and Akamai Functions.

> 👍
>
> We're often asked which languages are best for production-grade WebAssembly. We suggest [Rust](https://developer.fermyon.com/wasm-languages/rust), [JavaScript/TypeScript](https://developer.fermyon.com/wasm-languages/javascript), [Python](https://developer.fermyon.com/wasm-languages/python), and [Go](https://developer.fermyon.com/wasm-languages/go-lang).

# WebAssembly support for top 20 languages

Review the Wasm support for the top 20 programming languages as ranked by [RedMonk](https://redmonk.com/).

| Language                                                                | Core        | Browser     | WASI | Spin SDK    |
| :---------------------------------------------------------------------- | :---------- | :---------- | :--- | :---------- |
| [JavaScript](https://developer.fermyon.com/wasm-languages/javascript)   | ✓           | ✓           | ✓    | ✓           |
| [Python](https://developer.fermyon.com/wasm-languages/python)           | ✓           | In progress | ✓    | ✓           |
| [Java](https://developer.fermyon.com/wasm-languages/java)               | ✓           | ✓           | ✓    | In progress |
| [PHP](https://developer.fermyon.com/wasm-languages/php)                 | ✓           | ✓           | ✓    | ✗           |
| CSS                                                                     | N/A         | N/A         | N/A  | N/A         |
| [C# and .NET](https://developer.fermyon.com/wasm-languages/c-sharp)     | ✓           | ✓           | ✓    | ✓           |
| [C++](https://developer.fermyon.com/wasm-languages/cpp)                 | ✓           | ✓           | ✓    | ✗           |
| [TypeScript](https://developer.fermyon.com/wasm-languages/typescript)   | ✓           | In progress | ✗    | ✓           |
| [Ruby](https://developer.fermyon.com/wasm-languages/ruby)               | ✓           | ✓           | ✓    | ✗           |
| [C](https://developer.fermyon.com/wasm-languages/c-lang)                | ✓           | ✓           | ✓    | ✗           |
| [Swift](https://developer.fermyon.com/wasm-languages/swift)             | ✓           | ✓           | ✓    | In progress |
| [R](https://developer.fermyon.com/wasm-languages/r-lang)                | ✗           | ✓           | ✗    | ✗           |
| [Objective-C](https://developer.fermyon.com/wasm-languages/objective-c) | ?           | ✗           | ✗    | ✗           |
| Shell                                                                   | N/A         | N/A         | N/A  | N/A         |
| [Scala (JVM)](https://developer.fermyon.com/wasm-languages/scala)       | ✓           | ✓           | ✓    | In progress |
| [Scala (native)](https://developer.fermyon.com/wasm-languages/scala)    | In progress | ✗           | ✗    | ✗           |
| [Go](https://developer.fermyon.com/wasm-languages/go-lang)              | ✓           | ✓           | ✓    | ✓           |
| [PowerShell](https://developer.fermyon.com/wasm-languages/powershell)   | ✗           | ✗           | ✗    | ✗           |
| [Kotlin (JVM)](https://developer.fermyon.com/wasm-languages/kotlin)     | ✓           | ✓           | ✓    | In progress |
| [Kotlin (Wasm)](https://developer.fermyon.com/wasm-languages/kotlin)    | In progress | ✓           | ✓    | ✗           |
| [Rust](https://developer.fermyon.com/wasm-languages/rust)               | ✓           | ✓           | ✓    | ✓           |
| [Dart](https://developer.fermyon.com/wasm-languages/dart)               | ✓           | ✓           | ip   | ✗           |

# WebAssembly Specific Languages

| Language                                                                      | Browser | CLI | WASI | Spin SDK |
| :---------------------------------------------------------------------------- | :------ | :-- | :--- | :------- |
| [AssemblyScript](https://developer.fermyon.com/wasm-languages/assemblyscript) | ✓       | ✓   | ✓    | ✗        |
| [Grain](https://developer.fermyon.com/wasm-languages/grain)                   | ✓       | ✓   | ✓    | ✗        |
| [Motoko](https://developer.fermyon.com/wasm-languages/motoko)                 | ✓       | ✓   | ✓    | ✗        |

# Other notable languages

These languages, though not in the top 20, enjoy broad use and offer some degree of WebAssembly support.

| Language                                                                  | Browser     | CLI         | WASI        | Spin SDK    |
| :------------------------------------------------------------------------ | :---------- | :---------- | :---------- | :---------- |
| [Clojure](https://developer.fermyon.com/wasm-languages/clojure)           | ✓           | ✓           | ✓           | In progress |
| [COBOL](https://developer.fermyon.com/wasm-languages/cobol)               | In progress | ✓           | In progress | ✗           |
| [Erlang (BEAM)](https://developer.fermyon.com/wasm-languages/erlang-beam) | In progress | In progress | In progress | ✗           |
| [Haskell](https://developer.fermyon.com/wasm-languages/haskell)           | ✓           | ✓           | ✓           | ✗           |
| [Lisp](https://developer.fermyon.com/wasm-languages/lisp)                 | In progress | In progress | In progress | ✗           |
| [Lua](https://developer.fermyon.com/wasm-languages/lua)                   | ✓           | ✗           | ✗           | ✗           |
| [Perl](https://developer.fermyon.com/wasm-languages/perl)                 | ✓           | ✗           | ✗           | ✗           |
| [Prolog](https://developer.fermyon.com/wasm-languages/prolog)             | ✓           | ✗           | ✗           | ✓           |
| [Zig](https://developer.fermyon.com/wasm-languages/zig)                   | ✓           | ✓           | ✓           | ✗           |

<br />

> 📘
>
> The WebAssembly Language Guide is located in a [public GitHub project](https://github.com/fermyon/developer/tree/main/content/wasm-languages). If you find errors, want to make additions, or have further corrections for us, the [issue queue](https://github.com/fermyon/developer/issues) is a great place to discuss.

# Sibling pages

* [aka command reference](https://techdocs.akamai.com/akamai-functions/docs/aka-command-reference.md)
* [HTTP trigger reference](https://techdocs.akamai.com/akamai-functions/docs/http-trigger-reference.md)
* [WebAssembly standards](https://techdocs.akamai.com/akamai-functions/docs/related-standards.md)
* [FAQ](https://techdocs.akamai.com/akamai-functions/docs/faq.md)