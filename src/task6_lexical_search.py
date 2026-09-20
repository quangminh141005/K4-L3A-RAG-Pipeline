"""
Task 6 — Lexical search bằng BM25.

Dùng cùng corpus chunks với Task 5. BM25 phù hợp với từ khóa chính xác, mã tài
liệu và tên riêng. Output phải theo SearchResult và sort score giảm dần.
"""


CORPUS: list[dict] = []


def _ensure_corpus() -> None:
    """Load corpus từ Task 4 nếu chưa có."""
    if not CORPUS:
        from .task4_chunking_indexing import load_documents, chunk_documents
        documents = load_documents()
        chunks = chunk_documents(documents)
        CORPUS.extend(chunks)


def build_bm25_index(corpus: list[dict]):
    """Tạo BM25 index từ cùng corpus chunks của Task 4."""
    from rank_bm25 import BM25L
    tokenized = [item["content"].lower().split() for item in corpus]
    return BM25L(tokenized)


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """Trả về BM25 SearchResult theo score giảm dần."""
    import numpy as np
    _ensure_corpus()
    bm25 = build_bm25_index(CORPUS)
    scores = bm25.get_scores(query.lower().split())
    indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for index in indices:
        if scores[index] <= 0:
            continue
        item = CORPUS[index]
        results.append({
            "id": item["id"],
            "content": item["content"],
            "score": float(scores[index]),
            "metadata": item["metadata"],
            "retrieval_method": "bm25",
        })
    return results


if __name__ == "__main__":
    for result in lexical_search("test query", top_k=3):
        print(result)
