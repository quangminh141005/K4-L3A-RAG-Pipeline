"""
Task 2 — Crawl bài viết/thông báo.

Hướng dẫn:
    1. Điền tối thiểu 5 URL công khai vào ARTICLE_URLS.
    2. Crawl từng URL bằng Crawl4AI.
    3. Lưu mỗi bài thành một JSON trong data/landing/news/.
    4. Giữ đủ url, title, date_crawled và content_markdown.

Cài browser trước khi chạy:
    python -m playwright install chromium
    
-> Dùng Firecrawl or bất cứ công cụ nào bạn quen    
"""

from datetime import datetime
import asyncio
import json
from pathlib import Path
from crawl4ai import AsyncWebCrawler


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"

ARTICLE_URLS = [
    "https://ieltsliz.com/ielts-writing-task-1-lessons-and-tips/",
    "https://ieltsliz.com/ielts-writing-task-2/",
    "https://ieltsliz.com/100-ielts-essay-questions/",
    "https://ieltsliz.com/ielts-model-essay-score-9/",
    "https://ieltsliz.com/ielts-writing-task-1-bar-chart-model-score-9/",
    "https://ieltsliz.com/ielts-discussion-essay-model-answer/",
]


async def crawl_article(url: str, crawler: AsyncWebCrawler | None = None) -> dict:
    """Crawl một bài viết từ URL sử dụng Crawl4AI."""
    if crawler is not None:
        result = await crawler.arun(url=url)
    else:
        async with AsyncWebCrawler() as default_crawler:
            result = await default_crawler.arun(url=url)

    title = result.metadata.get("title") or "Unknown"
    return {
        "url": url,
        "title": title.strip(),
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": result.markdown or "",
    }


async def crawl_all() -> None:
    """Crawl và lưu từng bài thành một file JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    async with AsyncWebCrawler() as crawler:
        for index, url in enumerate(ARTICLE_URLS, 1):
            try:
                article = await crawl_article(url, crawler=crawler)
                output = DATA_DIR / f"article_{index:02d}.json"
                output.write_text(
                    json.dumps(article, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                print(f"Saved: {output}")
            except Exception as error:
                print(f"Failed: {url} — {error}")


if __name__ == "__main__":
    asyncio.run(crawl_all())

