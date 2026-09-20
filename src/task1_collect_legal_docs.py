"""
Task 1 — Thu thập tài liệu chính sách/quy định.

Hướng dẫn:
    1. Chọn chủ đề của nhóm.
    2. Tìm tối thiểu 3 tài liệu PDF/DOCX từ nguồn công khai.
    3. Lưu file gốc vào data/landing/legal/.
    4. Đặt tên không dấu và thể hiện đúng nội dung.

Ví dụ tài liệu: học phí, học bổng, ký túc xá, quy trình đăng ký.
Nếu website chặn crawler, hãy chọn nguồn công khai khác; không vượt WAF.
"""

from pathlib import Path

import requests


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"

# Điền URL công khai tương ứng vào đây. Có thể đổi tên file cho phù hợp với
# nội dung tài liệu, nhưng nên giữ phần mở rộng là .pdf, .doc hoặc .docx.
DOCUMENT_SOURCES = {
    "chinh_sach_01.pdf": "https://assets.ctfassets.net/unrdeg6se4ke/3eT3ue2RV5egjS34QqXdVt/ce0e178707e2021111f943ebbd9a0a8d/Writing-Band-descriptors-Task-1.pdf",
    "chinh_sach_02.pdf": "https://assets.ctfassets.net/unrdeg6se4ke/4AqjlJ7Tp1wLiY1j6DzpOg/39561e03e8d48ddc7648b479b903c701/Writing-Band-descriptors-Task-2.pdf",
    "chinh_sach_03.pdf": "",
}

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}


def setup_directory() -> None:
    """Tạo thư mục lưu tài liệu gốc."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def download_documents() -> None:
    """Tải ít nhất 3 PDF/DOCX từ nguồn công khai."""
    setup_directory()

    configured_sources = {
        filename: url.strip()
        for filename, url in DOCUMENT_SOURCES.items()
        if url.strip()
    }
    if not configured_sources:
        print("No URLs configured. Add URLs to DOCUMENT_SOURCES and run again.")
        return

    headers = {"User-Agent": "Mozilla/5.0 (legal-document-collector/1.0)"}
    with requests.Session() as session:
        session.headers.update(headers)

        for filename, url in configured_sources.items():
            destination = DATA_DIR / filename
            temporary_file = destination.with_suffix(destination.suffix + ".part")

            try:
                if destination.suffix.lower() not in ALLOWED_EXTENSIONS:
                    raise ValueError(
                        f"Unsupported extension for {filename}; use PDF, DOC, or DOCX"
                    )

                with session.get(url, timeout=30, stream=True) as response:
                    response.raise_for_status()
                    with temporary_file.open("wb") as file:
                        for chunk in response.iter_content(chunk_size=64 * 1024):
                            if chunk:
                                file.write(chunk)

                if temporary_file.stat().st_size == 0:
                    raise ValueError("Downloaded file is empty")

                temporary_file.replace(destination)
                print(f"Saved: {destination}")
            except (OSError, ValueError, requests.RequestException) as error:
                temporary_file.unlink(missing_ok=True)
                print(f"Failed: {url} — {error}")


if __name__ == "__main__":
    download_documents()
