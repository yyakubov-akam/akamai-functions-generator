# Summarizer benchmark

Date: 2026-08-17T07:40:53.337205

Temperature: 0.3

| Backend | Model | Article | Wall time | Load | Prompt tokens | Output tokens | Wall tok/s | Words |
|---|---|---|---:|---:|---:|---:|---:|---:|
| ollama | glm-4.7-flash:q8_0 | welcome | 68.59s | 21.59s | 1236 | 2779 | 40.51 | 55 |
| ollama | glm-4.7-flash:q8_0 | quickstart | 41.36s | 0.28s | 4624 | 2221 | 53.69 | 359 |
| ollama | glm-4.7-flash:q8_0 | key-value-store | 48.94s | 0.24s | 3417 | 2717 | 55.52 | 433 |
| ollama | glm-4.7-flash:q8_0 | quotas-and-limits | 41.17s | 0.24s | 1379 | 2426 | 58.93 | 328 |
| ollama | muse-glimmer:latest | welcome | 110.46s | 14.26s | 1275 | 1782 | 16.13 | 97 |
| ollama | muse-glimmer:latest | quickstart | 147.62s | 0.34s | 4558 | 2693 | 18.24 | 355 |
| ollama | muse-glimmer:latest | key-value-store | 141.42s | 0.32s | 3390 | 2592 | 18.33 | 452 |
| ollama | muse-glimmer:latest | quotas-and-limits | 127.82s | 0.32s | 1425 | 2365 | 18.50 | 371 |
