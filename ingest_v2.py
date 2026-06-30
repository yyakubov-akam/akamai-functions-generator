import asyncio
import argparse
from html import parser
import os
import re
import json
import ollama
import trafilatura
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlparse
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from config import ARCHIVE_DIR, INDEX_FILE, MODEL, MIN_CONTENT_LENGTH, DEFAULT_SCRAPING_ORDER, SITE_SCRAPING_OVERRIDES
import hashlib


os.makedirs(ARCHIVE_DIR, exist_ok=True)
PROMPT_FILE = os.path.join(os.path.dirname(__file__), "CODEGEN_REFERENCE_PROMPT.md")
MAX_PROMPT_CONTENT_CHARS = 120000


async def check_all(force: bool = False):
    """
    Re-fetch every indexed URL using the same browser-based strategies as ingest
    (bypasses bot-protection that blocks plain HTTP requests), compare content
    hashes, and re-summarize only pages that have actually changed.
    """
    index = load_index()
    if not index:
        print("Index is empty — nothing to check.")
        return

    changed_count = 0
    unchanged_count = 0

    for url, entry in index.items():
        print(f"\n🔍 Checking: {url}")

        content, strategy = await get_article_content(url)

        if content is None:
            print(f"❌ Fetch failed ({strategy}) — skipping")
            continue

        new_hash = hashlib.sha256(content.encode()).hexdigest()
        old_hash = entry.get("content_hash")

        if not force and isinstance(old_hash, str) and new_hash == old_hash:
            print("✅ unchanged")
            unchanged_count += 1
            continue

        print("🔄 CHANGED — reingesting")
        changed_count += 1

        print("⚙️  Generating summary...\n")
        summary, source_was_truncated = summarize(content)

        if source_was_truncated:
            print(f"⚠️  Warning: Source exceeded {MAX_PROMPT_CONTENT_CHARS} chars and was truncated.")

        filepath = url_to_archive_path(url)
        _, word_count = save_to_disk(url, content, summary, strategy, filepath, source_was_truncated)

        index[url] = {
            **entry,
            "filepath": filepath,
            "strategy": strategy,
            "word_count": word_count,
            "last_fetched": datetime.now().isoformat(),
            "content_hash": new_hash,
            "etag": None,
            "last_modified": None,
        }
        save_index(index)
        print(f"💾 Archived to: {filepath}")

    print(f"\n📊 {changed_count} changed, {unchanged_count} unchanged")

# ─────────────────────────────────────────────
# URL → ARCHIVE PATH
# ─────────────────────────────────────────────
def url_to_archive_path(url: str) -> str:
    """
    Convert a URL to a deterministic archive filepath.

    Examples:
        https://aws.amazon.com/blogs/networking/.../adding-http-security-headers/
            → archives/aws-amazon-com/adding-http-security-headers.md

        https://blog.cloudflare.com/account-abuse-protection/
            → archives/blog-cloudflare-com/account-abuse-protection.md

        https://techdocs.akamai.com/cloud-computing/docs/block-storage
            → archives/techdocs-akamai-com/block-storage.md
    """
    parsed = urlparse(url)

    # Subfolder: hostname with dots replaced by hyphens
    subfolder = parsed.hostname.replace(".", "-")

    # Filename: last non-empty path segment, slugified
    path_parts = [p for p in parsed.path.split("/") if p]
    slug = path_parts[-1] if path_parts else "index"
    # Slugify: lowercase, replace non-alphanumeric with hyphens, collapse hyphens
    slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    if not slug:
        slug = "index"

    dirpath = os.path.join(ARCHIVE_DIR, subfolder)
    os.makedirs(dirpath, exist_ok=True)
    return os.path.join(dirpath, f"{slug}.md")


# ─────────────────────────────────────────────
# INDEX MANIFEST
# ─────────────────────────────────────────────
def load_index() -> dict:
    """Load index.json manifest. Returns dict keyed by URL."""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_index(index: dict):
    """Persist index.json manifest."""
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def update_index(url: str, filepath: str, strategy: str, word_count: int, content_hash: str | None = None):
    """Add or update an entry in the index manifest."""
    index = load_index()
    index[url] = {
        "filepath": filepath,
        "strategy": strategy,
        "word_count": word_count,
        "last_fetched": datetime.now().isoformat(),
        "etag": None,
        "last_modified": None,
        "content_hash": content_hash,
    }
    save_index(index)


# ─────────────────────────────────────────────
# TIER 1: crawl4ai with pruning
# ─────────────────────────────────────────────
async def fetch_crawl4ai_pruned(url: str) -> tuple[str | None, str | None]:
    try:
        prune_filter = PruningContentFilter(
            threshold=0.4, threshold_type="dynamic", min_word_threshold=5
        )
        md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)
        browser_cfg = BrowserConfig(headless=True)
        run_cfg = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            markdown_generator=md_generator,
            remove_overlay_elements=True,
            delay_before_return_html=1.0,
        )
        async with AsyncWebCrawler(config=browser_cfg) as crawler:
            result = await crawler.arun(url=url, config=run_cfg)
            if not result.success:
                return None, result.error_message
            content = (
                result.markdown.fit_markdown
                if len(result.markdown.fit_markdown) > MIN_CONTENT_LENGTH
                else result.markdown.raw_markdown
            )
            return (content, None) if content else (None, "Empty content after pruning")
    except Exception as e:
        return None, str(e)


# ─────────────────────────────────────────────
# TIER 2: crawl4ai without pruning
# ─────────────────────────────────────────────
async def fetch_crawl4ai_raw(url: str) -> tuple[str | None, str | None]:
    try:
        md_generator = DefaultMarkdownGenerator()
        browser_cfg = BrowserConfig(headless=True)
        run_cfg = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            markdown_generator=md_generator,
            remove_overlay_elements=True,
            delay_before_return_html=2.0,
        )
        async with AsyncWebCrawler(config=browser_cfg) as crawler:
            result = await crawler.arun(url=url, config=run_cfg)
            if not result.success:
                return None, result.error_message
            content = result.markdown.raw_markdown
            return (content, None) if content else (None, "Empty raw markdown")
    except Exception as e:
        return None, str(e)


# ─────────────────────────────────────────────
# TIER 3: trafilatura
# ─────────────────────────────────────────────
def fetch_trafilatura(url: str) -> tuple[str | None, str | None]:
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None, "trafilatura: failed to download page"
        content = trafilatura.extract(
            downloaded,
            output_format="markdown",
            include_comments=False,
            include_tables=True,
            favor_recall=True,
        )
        return (content, None) if content else (None, "trafilatura: no content extracted")
    except Exception as e:
        return None, str(e)


# ─────────────────────────────────────────────
# CONTENT CLEANING
# ─────────────────────────────────────────────
def clean_content(text: str) -> str:
    boilerplate_patterns = [
        r"(?i)accept(ing)? (all )?cookies?.*",
        r"(?i)subscribe to (our )?newsletter.*",
        r"(?i)share (this )?(article|post|page).*",
        r"(?i)follow us on.*",
        r"(?i)related (articles?|posts?).*",
        r"(?i)you (may )?also like.*",
        r"(?i)advertisement.*",
        r"\[!\[.*?\]\(.*?\)\]\(.*?\)",
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip()


def is_content_good(content: str) -> bool:
    if not content or len(content) < MIN_CONTENT_LENGTH:
        return False
    word_count = len(content.split())
    link_count = content.count("](")
    if link_count > word_count * 0.4:
        return False
    return True


# ─────────────────────────────────────────────
# STRATEGY ROUTING
# ─────────────────────────────────────────────
_STRATEGY_MAP = {
    "crawl4ai/pruned": lambda url: fetch_crawl4ai_pruned(url),
    "crawl4ai/raw":    lambda url: fetch_crawl4ai_raw(url),
    "trafilatura":     lambda url: fetch_trafilatura(url),
}

_STRATEGY_LABELS = {
    "crawl4ai/pruned": "crawl4ai (with pruning)",
    "crawl4ai/raw":    "crawl4ai (no pruning)",
    "trafilatura":     "trafilatura (HTTP fallback)",
}


def get_strategy_order(url: str) -> list[str]:
    domain = urlparse(url).netloc
    return SITE_SCRAPING_OVERRIDES.get(domain, DEFAULT_SCRAPING_ORDER)


# ─────────────────────────────────────────────
# ORCHESTRATOR: tiered fallback
# ─────────────────────────────────────────────
async def get_article_content(url: str) -> tuple[str | None, str]:
    strategies = get_strategy_order(url)
    for i, strategy in enumerate(strategies, 1):
        label = _STRATEGY_LABELS[strategy]
        print(f"🔍 Tier {i}: {label}...", end=" ", flush=True)
        fetcher = _STRATEGY_MAP[strategy]
        result = fetcher(url)
        # Await coroutines from async fetchers
        if asyncio.iscoroutine(result):
            content, err = await result
        else:
            content, err = result
        if content and is_content_good(content):
            print("✅")
            return clean_content(content), strategy
        print(f"❌ ({err or 'content too short/noisy'})")

    return None, "All fetch strategies failed"


# ─────────────────────────────────────────────
# SUMMARIZATION
# ─────────────────────────────────────────────
def load_summary_prompt() -> str:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()

def summarize(content: str) -> tuple[str, bool]:
    prompt_template = load_summary_prompt()
    source_was_truncated = len(content) > MAX_PROMPT_CONTENT_CHARS
    prompt = prompt_template.format(content=content[:MAX_PROMPT_CONTENT_CHARS])
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.3},
    )
    return response["message"]["content"], source_was_truncated


# ─────────────────────────────────────────────
# ARCHIVE
# ─────────────────────────────────────────────
def save_to_disk(
    url: str,
    content: str,
    summary: str,
    strategy: str,
    filepath: str,
    source_was_truncated: bool = False,
) -> str:
    word_count = len(content.split())
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Source: {url}\n")
        f.write(f"Date: {datetime.now().isoformat()}\n")
        f.write(f"Model: {MODEL}\n")
        if source_was_truncated:
            f.write(
                f"WARNING: Source article was truncated to first {MAX_PROMPT_CONTENT_CHARS} "
                "characters before summarization.\n\n"
            )
        f.write(summary)
    return filepath, word_count


# ─────────────────────────────────────────────
# SITEMAP
# ─────────────────────────────────────────────
def get_sitemap_urls(sitemap_url: str, prefix: str | None = None) -> List[str]:
    response = requests.get(sitemap_url, timeout=30)
    response.raise_for_status()
    root = ET.fromstring(response.content)

    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = root.findall(".//sm:loc", namespace)

    urls = [loc.text for loc in locs if loc.text]
    if prefix:
        return [
            url
            for url in urls
            if f"/{prefix}/" in url or url.endswith(f"/{prefix}")
        ]
    return urls


async def process_single_url(url: str):
    # Check if already archived
    index = load_index()
    if url in index:
        entry = index[url]
        print(f"\n📋 Already archived: {entry['filepath']}")
        print(f"   Last fetched: {entry['last_fetched']} | Words: {entry['word_count']} | Strategy: {entry['strategy']}")
        print("   Re-fetching and overwriting...\n")
    else:
        print(f"\n📰 Fetching: {url}\n")

    content, strategy = await get_article_content(url)

    if content is None:
        print(f"\n❌ Failed to extract content: {strategy}")
        print("   Possible reasons: bot protection, paywall, or empty page.")
        return

    print(f"\n✅ Content extracted ({len(content)} chars) via [{strategy}]")
    print("⚙️  Generating summary...\n")

    summary, source_was_truncated = summarize(content)

    if source_was_truncated:
        print(
            f"⚠️  Warning: Source article exceeded {MAX_PROMPT_CONTENT_CHARS} chars "
            "and was truncated before summarization."
        )

    filepath = url_to_archive_path(url)
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    _, word_count = save_to_disk(
        url,
        content,
        summary,
        strategy,
        filepath,
        source_was_truncated=source_was_truncated,
    )
    update_index(url, filepath, strategy, word_count, content_hash)

    print(f"\n💾 Archived to: {filepath}")


async def process_sitemap(sitemap_url: str, prefix: str | None = None):
    print(f"\n📡 Fetching sitemap: {sitemap_url}")
    try:
        urls = get_sitemap_urls(sitemap_url, prefix)
    except Exception as e:
        print(f"❌ Failed to fetch or parse sitemap: {e}")
        return

    if prefix:
        print(f"🎯 Found {len(urls)} URLs matching prefix '{prefix}'")
    else:
        print(f"🎯 Found {len(urls)} URLs (no prefix filter)")

    if not urls:
        return

    index = load_index()
    total = len(urls)

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{total}] {url}", end=" ", flush=True)

        if url in index:
            print("⏭️  Skipping (already indexed)")
            continue

        content, strategy = await get_article_content(url)
        if content:
            filepath = url_to_archive_path(url)
            placeholder_summary = "Crawled via sitemap mode. No LLM summary generated."
            _, word_count = save_to_disk(url, content, placeholder_summary, strategy, filepath)
            update_index(url, filepath, strategy, word_count)
            print("✅ Saved")
        else:
            print(f"❌ Failed ({strategy})")

        await asyncio.sleep(2)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
async def main():
    parser = argparse.ArgumentParser(description="Article ingester with optional sitemap crawl mode")
    parser.add_argument("url", nargs="?", help="Single article URL to fetch")
    parser.add_argument("--sitemap", help="Sitemap XML URL to crawl")
    parser.add_argument("--prefix", default=None, help="Optional URL path prefix filter for sitemap mode")
    
    parser.add_argument("--check", action="store_true",
                    help="Check all indexed URLs for changes and reingest if needed")
    parser.add_argument("--force", action="store_true",
                    help="With --check: reingest all URLs regardless of change detection")
    args = parser.parse_args()

    if args.sitemap:
        await process_sitemap(args.sitemap, args.prefix)
        return

    if args.url:
        await process_single_url(args.url)
        return

    if args.check:
        await check_all(force=args.force)
        return

    parser.print_help()
    print(f"\nModel: {MODEL}  (edit MODEL in config.py to change)")


if __name__ == "__main__":
    asyncio.run(main())