# Summarizer benchmark

Date: 2026-08-16T11:22:01.978329

Temperature: 0.3

| Backend | Article | Wall time | Prompt tokens | Output tokens | Wall tok/s | Words |
|---|---|---:|---:|---:|---:|---:|
| ollama | welcome | 4.74s | 1286 | 436 | 92.04 | 63 |
| ollama | quickstart | 23.31s | 4648 | 2022 | 86.73 | 753 |
| ollama | key-value-store | 13.93s | 3456 | 1385 | 99.43 | 564 |
| ollama | quotas-and-limits | 26.75s | 1428 | 2367 | 88.49 | 995 |
| mlx | welcome | 42.60s | 1417 | 2372 | 55.68 | 38 |
| mlx | quickstart | 46.69s | 5115 | 2518 | 53.93 | 333 |
| mlx | key-value-store | 34.32s | 3887 | 1878 | 54.73 | 274 |
| mlx | quotas-and-limits | 38.93s | 1636 | 2432 | 62.47 | 246 |

MLX model load time: 5.28s
