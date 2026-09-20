"""
Task 3 — Chuẩn hóa dữ liệu sang Markdown.

Hướng dẫn:
    1. Dùng MarkItDown để convert PDF/DOCX.
    2. Đọc JSON và giữ metadata ở đầu file Markdown.
    3. Giữ cấu trúc thư mục legal/ và news/.
    4. Không tạo file rỗng hoặc file trùng khi chạy lại.

Cài đặt:
    Dependency MarkItDown đã được khai báo trong pyproject.toml.
    
-> Hoặc dùng công cụ nào bạn quen khác Markitdown
"""

from pathlib import Path


LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


import json
from markitdown import MarkItDown


def convert_legal_docs() -> None:
    """Convert PDF/DOCX trong landing/legal vào standardized/legal."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not legal_dir.exists():
        print(f"Directory not found: {legal_dir}")
        return

    converter = MarkItDown()
    for path in sorted(legal_dir.iterdir()):
        if path.suffix.lower() in {".pdf", ".doc", ".docx"}:
            try:
                result = converter.convert(str(path))
                content = (result.text_content or "").strip()
                if content:
                    output_file = output_dir / f"{path.stem}.md"
                    output_file.write_text(content, encoding="utf-8")
                    print(f"Converted legal: {output_file}")
                else:
                    print(f"Skipped empty content: {path.name}")
            except Exception as error:
                print(f"Failed to convert {path.name}: {error}")


def convert_news_articles() -> None:
    """Convert JSON trong landing/news vào standardized/news kèm header metadata."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not news_dir.exists():
        print(f"Directory not found: {news_dir}")
        return

    for path in sorted(news_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            content = (data.get("content_markdown") or "").strip()
            if not content:
                print(f"Skipped empty news: {path.name}")
                continue

            title = data.get("title") or "Unknown"
            url = data.get("url") or ""
            date_crawled = data.get("date_crawled") or ""

            header = (
                f"# {title}\n\n"
                f"**Source:** {url}\n\n"
                f"**Crawled:** {date_crawled}\n\n---\n\n"
            )
            output_file = output_dir / f"{path.stem}.md"
            output_file.write_text(header + content, encoding="utf-8")
            print(f"Converted news: {output_file}")
        except Exception as error:
            print(f"Failed to convert {path.name}: {error}")



def convert_all() -> None:
    """Convert toàn bộ dữ liệu landing."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    convert_legal_docs()
    convert_news_articles()
    print(f"Saved Markdown to: {OUTPUT_DIR}")


if __name__ == "__main__":
    convert_all()
