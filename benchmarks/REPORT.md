# TechDocs summarizer benchmark

Date: 2026-08-17

## Setup

- Prompt: `CODEGEN_REFERENCE_PROMPT.md`
- Frozen articles: Welcome, Quickstart, Key Value store, Quotas and limits
- Temperature: 0.3
- Cloud model: `gpt-oss:120b-cloud` through Ollama
- Local model: `mlx-community/gemma-4-26b-a4b-it-4bit` through MLX on a
  MacBook Pro M4 with 24 GB unified memory
- Remote model: `glm-4.7-flash:q8_0` (29.9B, Q8_0) through Ollama
- Remote model: `muse-glimmer:latest` (27.9B, Q4_K_M) through Ollama
- Remote Ollama maximum generation: 4,096 tokens per article

The remote run reused the exact source files from `results/20260816-112158`;
all four files are byte-for-byte identical. The older gpt-oss run did not have
an explicit generation ceiling, but its longest result was 2,367 tokens, so the
new 4,096-token ceiling would not have changed it.

Remote timing measures the Ollama VM as a complete service. Its hardware and
other workload were not controlled, so it is directly useful for this project's
observed latency but is not a hardware-normalized comparison of model
architectures.

## Speed

The inference column excludes model load where the backend reported it. Total
elapsed includes load.

| Variant | Four-article inference | Mean/article | Load | Total elapsed | Peak local memory |
|---|---:|---:|---:|---:|---:|
| gpt-oss cloud, thinking | 68.73 s | 17.18 s | Hosted | 68.73 s | Not local |
| Gemma MLX, thinking | 162.54 s | 40.63 s | 5.28 s | 167.82 s | 15.96 GB |
| Gemma MLX, no thinking, temp 0.3 | 52.75 s | 13.19 s | 5.48 s | 58.23 s | 15.96 GB |
| Gemma MLX, no thinking, temp 0 | 45.85 s | 11.46 s | 5.11 s | 50.96 s | 15.96 GB |
| GLM 4.7 Flash Q8, thinking | 177.72 s | 44.43 s | 22.34 s | 200.06 s | Remote, not measured |
| GLM 4.7 Flash Q8, no thinking | 66.30 s | 16.58 s | 1.00 s | 67.30 s | Remote, not measured |
| Muse Glimmer Q4, thinking | 512.10 s | 128.03 s | 15.23 s | 527.33 s | Remote, not measured |

In the primary four-article run, GLM was 2.91 times slower end-to-end than
gpt-oss cloud and 1.19 times slower than local Gemma with thinking, including
their respective load times. Muse was 2.64 times slower than GLM and 3.14 times
slower than local Gemma with thinking.

GLM's remote throughput was unstable. Its primary Quotas request took 41.17
seconds at about 60 generated tokens/second, while an identical repeat took
245.47 seconds at about 11.6 generated tokens/second. Both ended naturally
below the token ceiling. An earlier uncapped Quotas request also failed to
return after approximately nine minutes and was manually interrupted. This
points to remote service/runtime variability, not simply longer output.

Muse was consistently around 18.5 generated tokens/second. Its repeated Key
Value Store request took 179.72 seconds instead of 141.42 seconds mainly because
it generated 3,327 rather than 2,592 tokens.

With GLM alone on the server, disabling thinking reduced total time from 200.06
to 67.30 seconds, a 66.4% reduction or 2.97 times speedup. Generated tokens fell
from 10,143 to 2,456 because the reasoning channel was empty, while visible
output actually increased from 1,175 to 1,474 words.

## Quality audit

| Variant | Grounding | Coverage | Format adherence | Main issue |
|---|---|---|---|---|
| gpt-oss cloud | Mixed | Highest | Strong | Invented APIs and code not present in sources |
| Gemma, thinking | Strongest | Moderate | Strong | Omits some secondary details and reasons excessively |
| Gemma, no thinking | Generally strong | Moderate | Unreliable | Corrupted words/headings and occasional unsupported additions |
| GLM 4.7 Flash Q8 | Generally strong | Moderate | Mostly strong | Promoted a recommendation to a requirement; sparse output and unstable latency |
| GLM 4.7 Flash Q8, no thinking | Weak | High | Strong | Invented runtime restrictions, version requirements, and code |
| Muse Glimmer Q4 | Mixed | Moderate | Mixed | Very slow; one run emitted broken code and inferred pseudo-signatures |

### gpt-oss cloud

The model produced the most comprehensive references, especially for tutorial
articles. However, it repeatedly converted feature names into fictional APIs.
On two independent Quotas and limits runs it invented signatures and examples
including `variables.set`, `kv.delete`, `spin.service.chain`, and imports from
`spin-sdk`. The source contains only a feature-support table and provides none
of those signatures or code patterns. This is unsafe for a coding reference.

It also promoted recommendations to hard constraints, such as treating Node.js
22 as mandatory when the source says it is recommended, and added unsupported
Quickstart material such as `router.post` and Node built-in restrictions.

### Gemma with thinking

This was the most conservative and source-grounded original variant. It avoided
inventing detailed APIs for the Quotas article and produced clean expected
headings. Its main weakness was under-extraction: it omitted some secondary
details such as query-rate notes and limited-access features.

The reasoning channel was disproportionate to the task. Across four articles
it generated 9,200 tokens while the visible results totaled only 891 words,
making it 2.37 times slower than the cloud model.

### Gemma without thinking

Disabling thinking made Gemma the speed winner. Temperature zero reduced its
four-article generation time to 45.85 seconds, or 50.96 seconds including model
load. However, both tested temperatures produced corrupted words such as
`Gotwas`, `Gotaks`, and `Akaks`. The model also occasionally added unsupported
details such as `router.post` to the Quickstart reference.

### GLM 4.7 Flash Q8

GLM handled the most important safety case well. Both completed Quotas outputs
kept feature-support entries as features and did not invent API signatures. Its
Quickstart and Key Value Store code was usable and closely followed source code.
It produced more visible coverage than Gemma with thinking without the word
corruption seen in Gemma's no-thinking mode.

Its main factual error was promoting the source's recommendation of Node.js 22
or newer into a hard runtime requirement. The Welcome output was only 55 words,
included empty sections that the prompt says to omit, and surfaced the YAML
`updatedAt` value as a compatibility note. GLM is therefore grounded but not
consistently precise about rule severity or extraction depth.

### GLM 4.7 Flash Q8 without thinking

The speed improvement came with an unacceptable grounding regression. For the
Welcome article, GLM invented restrictions on Node modules (`fs`, `path`, and
`http`), browser APIs (`window`, `document`, and `localStorage`), and blocking
operations. None appears in the source. It also invented an `export default`
JavaScript handler pattern rather than extracting a documented example.

Quickstart repeated those unsupported restrictions for `fs`, `Buffer`, native
`require`, and CommonJS. It invented unspecified CPU, memory, and "few MB"
application-size limits, and promoted a Windows download link for Spin v3.6.2
into a platform-wide minimum-version requirement. The output was longer and
looked polished, but it was materially less trustworthy for a coding agent.

Key Value Store and Quotas were closer to their sources and their code was
usable. That is not enough to offset fabricated hard constraints in two of the
four articles.

### Muse Glimmer Q4

Muse also avoided the fictional APIs that made gpt-oss unsafe on Quotas. Its
best outputs were detailed and largely source-grounded, but categorization was
inconsistent: the Welcome article placed every extracted fact under Version
and Compatibility Notes, including runtime and deployment facts.

The first Key Value Store run emitted a `handleSetValue` example that called
`store.setJson(key, payload)` without defining `payload`, making the required
pattern unusable. An identical repeat produced the correct parsing code, which
shows stochastic code-integrity risk. The Quickstart output also inferred
pseudo-signatures such as `ResponseBuilder.status(code)` from chained Rust
example code even though those signatures were not documented in that form.

## Recommendation

Of the two new remote models, GLM 4.7 Flash Q8 is the clear candidate. It is
substantially faster and more reliable than Muse, and it avoided gpt-oss's most
dangerous behavior. Keep the 4,096-token ceiling and add request timeouts/retry
handling if it is used for unattended ingestion because the remote service
showed severe latency variance.

Do not switch production summarization to Muse Glimmer. It was the slowest
variant by a wide margin and did not provide a quality advantage that justifies
the latency or stochastic broken-code risk.

GLM is not yet a decisive replacement for Gemma with thinking. It offers better
coverage at roughly similar warm latency, but Gemma remains the most
conservative result and its local performance is predictable. The next useful
test is GLM at temperature zero with a stricter prompt that prohibits promoting
recommendations to requirements and prohibits inventing signatures from code
examples. Validate generated code blocks before changing the thinking default.

Keep thinking enabled for GLM with the current prompt. The 3-times latency
improvement from disabling it does not justify feeding fabricated constraints
and code to the downstream coding agent. The production thinking behavior was
not changed by this benchmark.

## Raw results

- `results/20260816-112158`: gpt-oss cloud and Gemma with thinking, temperature 0.3
- `results/20260816-112725`: Gemma without thinking, temperature 0.3
- `results/20260816-112936`: Gemma without thinking, temperature 0
- `results/20260816-113113`: repeated gpt-oss Quotas case
- `results/20260817-072755`: interrupted uncapped GLM diagnostic; partial outputs only
- `results/20260817-074053`: primary GLM and Muse four-article run, temperature 0.3
- `results/20260817-075453`: repeated bounded GLM Quotas case
- `results/20260817-075920`: repeated bounded Muse Key Value Store case
- `results/20260817-091428`: discarded no-thinking run with GLM and Muse resident concurrently
- `results/20260817-092247`: valid GLM no-thinking run with GLM alone
