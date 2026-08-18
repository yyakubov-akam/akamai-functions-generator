#!/usr/bin/env python3
"""Benchmark the project's Ollama and MLX summarization backends."""

import argparse
import hashlib
import json
import re
import time
from datetime import datetime
from pathlib import Path

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = PROJECT_ROOT / "CODEGEN_REFERENCE_PROMPT.md"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "benchmarks" / "results"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
DEFAULT_OLLAMA_MODEL = "gpt-oss:120b-cloud"
DEFAULT_MLX_MODEL = "mlx-community/gemma-4-26b-a4b-it-4bit"
TEMPERATURE = 0.3
MAX_PROMPT_CONTENT_CHARS = 120000
MAX_OLLAMA_TOKENS = 4096
MAX_MLX_TOKENS = 4096

ARTICLES = {
    "welcome": {
        "url": "https://techdocs.akamai.com/akamai-functions/docs/welcome",
        "local_path": PROJECT_ROOT / "tests" / "welcome.md",
    },
    "quickstart": {
        "url": "https://techdocs.akamai.com/akamai-functions/docs/quickstart",
    },
    "key-value-store": {
        "url": (
            "https://techdocs.akamai.com/akamai-functions/docs/"
            "use-the-key-value-store"
        ),
    },
    "quotas-and-limits": {
        "url": (
            "https://techdocs.akamai.com/akamai-functions/docs/"
            "quotas-and-limits"
        ),
    },
}


def fetch_article(name: str, source_dir: Path | None = None) -> tuple[str, str]:
    article = ARTICLES[name]
    if source_dir is not None:
        frozen_path = source_dir / f"source-{name}.md"
        if not frozen_path.exists():
            raise FileNotFoundError(
                f"Frozen benchmark source is missing: {frozen_path}"
            )
        return frozen_path.read_text(encoding="utf-8"), str(frozen_path)

    local_path = article.get("local_path")
    if local_path and local_path.exists():
        return local_path.read_text(encoding="utf-8"), str(local_path)

    response = requests.get(
        article["url"],
        headers={"Accept": "text/markdown, text/html;q=0.9"},
        timeout=60,
    )
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "").lower()
    if not content_type.startswith("text/markdown"):
        raise RuntimeError(
            f"{article['url']} did not return Markdown: {content_type or 'missing'}"
        )
    return response.text, article["url"]


def build_prompt(source: str) -> str:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    return template.format(content=source[:MAX_PROMPT_CONTENT_CHARS])


def output_metrics(content: str) -> dict:
    allowed_headings = {
        "Runtime Constraints",
        "Supported APIs and Syntax",
        "Required Patterns",
        "Common Mistakes and Gotchas",
        "Version and Compatibility Notes",
    }
    headings = re.findall(r"(?m)^## (.+?)\s*$", content)
    return {
        "characters": len(content),
        "words": len(content.split()),
        "headings": headings,
        "unexpected_headings": [h for h in headings if h not in allowed_headings],
        "code_fences": content.count("```") // 2,
    }


def run_ollama(
    url: str,
    model: str,
    prompt: str,
    temperature: float,
    max_tokens: int,
    enable_thinking: bool,
) -> tuple[str, str, dict]:
    started = time.perf_counter()
    response = requests.post(
        url,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "think": enable_thinking,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        },
        timeout=1800,
    )
    response.raise_for_status()
    wall_seconds = time.perf_counter() - started
    data = response.json()
    message = data["message"]
    metrics = {
        "wall_seconds": wall_seconds,
        "provider_seconds": data.get("total_duration", 0) / 1_000_000_000,
        "load_seconds": data.get("load_duration", 0) / 1_000_000_000,
        "prompt_eval_seconds": (
            data.get("prompt_eval_duration", 0) / 1_000_000_000
        ),
        "generation_seconds": data.get("eval_duration", 0) / 1_000_000_000,
        "prompt_tokens": data.get("prompt_eval_count"),
        "generation_tokens": data.get("eval_count"),
        "done_reason": data.get("done_reason"),
    }
    generation_tokens = metrics["generation_tokens"] or 0
    metrics["wall_tokens_per_second"] = (
        generation_tokens / wall_seconds if wall_seconds else None
    )
    return message.get("content", ""), message.get("thinking", ""), metrics


def extract_gemma_response(raw: str) -> tuple[str, str]:
    thought_match = re.search(
        r"<\|channel>thought\s*(.*?)<channel\|>", raw, flags=re.DOTALL
    )
    final_match = re.search(
        r"<\|channel>final\s*(.*?)(?:<channel\|>|<turn\|>|$)",
        raw,
        flags=re.DOTALL,
    )
    thinking = thought_match.group(1).strip() if thought_match else ""
    if final_match:
        return final_match.group(1).strip(), thinking

    content = re.sub(
        r"<\|channel>thought\s*.*?<channel\|>", "", raw, flags=re.DOTALL
    )
    content = re.sub(r"<\|channel>(?:final)?", "", content)
    content = re.sub(r"<(?:channel|turn)\|>", "", content)
    return content.strip(), thinking


def load_mlx(model_name: str):
    from mlx_lm import load

    started = time.perf_counter()
    model, tokenizer = load(model_name)
    return model, tokenizer, time.perf_counter() - started


def run_mlx(
    model, tokenizer, prompt: str, enable_thinking: bool, temperature: float
) -> tuple[str, str, dict]:
    import mlx.core as mx
    from mlx_lm.generate import stream_generate
    from mlx_lm.sample_utils import make_sampler

    messages = [{"role": "user", "content": prompt}]
    prompt_tokens = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        enable_thinking=enable_thinking,
    )
    sampler = make_sampler(temp=temperature, top_p=0.95, top_k=64)
    mx.random.seed(42)

    started = time.perf_counter()
    first_token_seconds = None
    chunks = []
    last_response = None
    for generation in stream_generate(
        model,
        tokenizer,
        prompt_tokens,
        max_tokens=MAX_MLX_TOKENS,
        sampler=sampler,
    ):
        if first_token_seconds is None:
            first_token_seconds = time.perf_counter() - started
        chunks.append(generation.text)
        last_response = generation
    wall_seconds = time.perf_counter() - started

    if last_response is None:
        raise RuntimeError("MLX returned no generation response")

    raw = "".join(chunks)
    content, thinking = extract_gemma_response(raw)
    metrics = {
        "wall_seconds": wall_seconds,
        "first_token_seconds": first_token_seconds,
        "prompt_tokens": last_response.prompt_tokens,
        "prompt_tokens_per_second": last_response.prompt_tps,
        "generation_tokens": last_response.generation_tokens,
        "generation_tokens_per_second": last_response.generation_tps,
        "wall_tokens_per_second": (
            last_response.generation_tokens / wall_seconds if wall_seconds else None
        ),
        "peak_memory_gb": last_response.peak_memory,
        "done_reason": last_response.finish_reason,
    }
    return content, thinking, metrics


def write_markdown_summary(results: dict, destination: Path) -> None:
    lines = [
        "# Summarizer benchmark",
        "",
        f"Date: {results['created_at']}",
        "",
        f"Temperature: {results['temperature']}",
        "",
        "| Backend | Model | Article | Wall time | Load | Prompt tokens | "
        "Output tokens | Wall tok/s | Words |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for run in results["runs"]:
        metrics = run["timing"]
        lines.append(
            f"| {run['backend']} | {run['model']} | {run['article']} | "
            f"{metrics['wall_seconds']:.2f}s | "
            f"{metrics.get('load_seconds') or 0:.2f}s | "
            f"{metrics.get('prompt_tokens') or '-'} | "
            f"{metrics.get('generation_tokens') or '-'} | "
            f"{metrics.get('wall_tokens_per_second') or 0:.2f} | "
            f"{run['output_metrics']['words']} |"
        )

    if results.get("mlx_load_seconds") is not None:
        lines.extend(
            ["", f"MLX model load time: {results['mlx_load_seconds']:.2f}s"]
        )
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_results(results: dict, output_dir: Path) -> None:
    """Persist completed runs so an interrupted benchmark retains its data."""
    (output_dir / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_markdown_summary(results, output_dir / "summary.md")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--backend",
        choices=("all", "ollama", "mlx"),
        default="all",
    )
    parser.add_argument(
        "--articles",
        nargs="+",
        choices=tuple(ARTICLES),
        default=list(ARTICLES),
    )
    parser.add_argument(
        "--ollama-url",
        default=DEFAULT_OLLAMA_URL,
        help="Ollama chat endpoint URL",
    )
    parser.add_argument(
        "--ollama-model",
        action="append",
        dest="ollama_models",
        metavar="MODEL",
        help=(
            "Ollama model to benchmark; repeat for multiple models "
            f"(default: {DEFAULT_OLLAMA_MODEL})"
        ),
    )
    parser.add_argument(
        "--ollama-max-tokens",
        type=int,
        default=MAX_OLLAMA_TOKENS,
        help="Maximum generated tokens per Ollama request",
    )
    parser.add_argument(
        "--ollama-thinking",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable or disable the Ollama model's reasoning channel",
    )
    parser.add_argument("--mlx-model", default=DEFAULT_MLX_MODEL)
    parser.add_argument("--temperature", type=float, default=TEMPERATURE)
    parser.add_argument(
        "--mlx-thinking",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable or disable Gemma's reasoning channel",
    )
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument(
        "--source-dir",
        type=Path,
        help="Reuse source-<article>.md files from an earlier benchmark run",
    )
    args = parser.parse_args()
    ollama_models = args.ollama_models or [DEFAULT_OLLAMA_MODEL]

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = args.output_root / run_id
    output_dir.mkdir(parents=True, exist_ok=False)

    sources = {}
    source_origins = {}
    for article in args.articles:
        content, origin = fetch_article(article, args.source_dir)
        sources[article] = content
        source_origins[article] = origin
        (output_dir / f"source-{article}.md").write_text(content, encoding="utf-8")

    results = {
        "created_at": datetime.now().isoformat(),
        "temperature": args.temperature,
        "ollama_url": args.ollama_url,
        "ollama_models": ollama_models,
        "ollama_max_tokens": args.ollama_max_tokens,
        "ollama_thinking": args.ollama_thinking,
        "mlx_model": args.mlx_model,
        "mlx_thinking": args.mlx_thinking,
        "mlx_max_tokens": MAX_MLX_TOKENS,
        "articles": {
            name: {
                "origin": source_origins[name],
                "canonical_url": ARTICLES[name]["url"],
                "characters": len(source),
                "words": len(source.split()),
                "sha256": hashlib.sha256(source.encode()).hexdigest(),
            }
            for name, source in sources.items()
        },
        "runs": [],
        "mlx_load_seconds": None,
    }

    if args.backend in ("all", "ollama"):
        ollama_backend = (
            "ollama-thinking" if args.ollama_thinking else "ollama-no-thinking"
        )
        for ollama_model in ollama_models:
            model_slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", ollama_model)
            for article, source in sources.items():
                print(f"Ollama / {ollama_model} / {article}", flush=True)
                content, thinking, timing = run_ollama(
                    args.ollama_url,
                    ollama_model,
                    build_prompt(source),
                    args.temperature,
                    args.ollama_max_tokens,
                    args.ollama_thinking,
                )
                run = {
                    "backend": ollama_backend,
                    "model": ollama_model,
                    "article": article,
                    "content": content,
                    "thinking": thinking,
                    "timing": timing,
                    "output_metrics": output_metrics(content),
                }
                results["runs"].append(run)
                (
                    output_dir
                    / f"{ollama_backend}-{model_slug}-{article}.md"
                ).write_text(content, encoding="utf-8")
                write_results(results, output_dir)

    if args.backend in ("all", "mlx"):
        print(f"Loading MLX model: {args.mlx_model}", flush=True)
        model, tokenizer, load_seconds = load_mlx(args.mlx_model)
        results["mlx_load_seconds"] = load_seconds
        print(f"MLX model loaded in {load_seconds:.2f}s", flush=True)
        backend_name = "mlx-thinking" if args.mlx_thinking else "mlx-no-thinking"
        for article, source in sources.items():
            print(f"{backend_name} / {article}", flush=True)
            content, thinking, timing = run_mlx(
                model,
                tokenizer,
                build_prompt(source),
                enable_thinking=args.mlx_thinking,
                temperature=args.temperature,
            )
            run = {
                "backend": backend_name,
                "model": args.mlx_model,
                "article": article,
                "content": content,
                "thinking": thinking,
                "timing": timing,
                "output_metrics": output_metrics(content),
            }
            results["runs"].append(run)
            (output_dir / f"{backend_name}-{article}.md").write_text(
                content, encoding="utf-8"
            )
            write_results(results, output_dir)

    write_results(results, output_dir)
    print(f"Results: {output_dir}")


if __name__ == "__main__":
    main()
