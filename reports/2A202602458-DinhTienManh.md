# Individual contribution report

## Thông tin

- Họ và tên: Đinh Tiến Mạnh
- Mã học viên: 2A202602458
- Nhóm: Ainoob
- Repository/branch: `quangminh141005/K4-L3A-RAG-Pipeline` / `main`

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 5 — Semantic search | Dùng chung `embed_texts()` với Task 4 để embed query, truy vấn ChromaDB, chuyển cosine distance thành similarity và trả `SearchResult` theo điểm giảm dần. | `src/task5_semantic_search.py`; commit `9418add` | Done |
| Task 6 — Lexical search | Xây dựng BM25L trên cùng corpus chunks, token hóa nội dung/query, lọc kết quả có điểm dương và trả đúng metadata cùng schema `SearchResult`. | `src/task6_lexical_search.py`; commit `9418add` | Done |
| Task 7 — Reranking | Cài đặt Reciprocal Rank Fusion cho nhiều ranked lists, đánh rank từ 1, khử trùng theo `id`, giới hạn `top_k` và đánh dấu kết quả là `hybrid`. | `src/task7_reranking.py`; commit `9418add` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Task 5 sử dụng chính hàm embedding và collection của Task 4, đồng thời chuyển distance thành `max(0, 1 - distance)`.  
   **Lý do/evidence:** `docs/MODULE_CONTRACTS.md` yêu cầu Task 4 và Task 5 dùng chung model/dimension; Chroma collection được cấu hình cosine distance. Cách chuyển này tạo score similarity để sort và dùng cho fallback.  
   **Trade-off:** Phụ thuộc Mistral Embedding API và ChromaDB; đổi model hoặc distance space phải cập nhật đồng bộ cả index và truy vấn.

2. **Quyết định:** Dùng BM25L cho lexical search và RRF để hợp nhất dense với BM25 theo thứ hạng, không cộng trực tiếp hai loại score.  
   **Lý do/evidence:** BM25L phù hợp với keyword, mã tài liệu và tên riêng; RRF theo đúng công thức `sum(1 / (k + rank))` giúp hai nguồn có thang điểm khác nhau vẫn được kết hợp ổn định.  
   **Trade-off:** Mỗi query phải tính thêm BM25 và RRF; BM25L hiện xây index từ corpus trong bộ nhớ nên chưa tối ưu cho corpus lớn.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Đối chiếu interface với `docs/MODULE_CONTRACTS.md` và các test contract cho semantic search, lexical search, RRF; query thử nghiệm dùng trong nhóm: `What is the IELTS writing test about?`.
- Kết quả trước/sau nếu có: Dense search trả kết quả theo cosine similarity; BM25L bắt được keyword chính xác; RRF hợp nhất hai danh sách, khử trùng ID và trả `retrieval_method="hybrid"`. Báo cáo evaluation ghi nhận cấu hình Hybrid + RRF đạt average `0.877`, cao hơn dense-only `0.805`.
- Lỗi đã phát hiện và cách xử lý: BM25 cần dùng cùng corpus chunks với dense nên Task 6 có `_ensure_corpus()` để nạp corpus khi cần. RRF không dùng cosine/BM25 score trực tiếp mà chỉ tính theo rank, phù hợp contract. Môi trường hiện tại chưa cài `pytest`, vì vậy chưa chạy lại được bộ test trong phiên làm việc này.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: BM25 index được tạo lại ở mỗi lần gọi `lexical_search`, và phép tách token hiện chỉ dùng `lower().split()` nên chưa xử lý tốt dấu câu, biến thể từ hoặc từ đồng nghĩa.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Cache BM25 index theo phiên và bổ sung tokenizer/normalizer phù hợp với corpus IELTS, sau đó đánh giá lại top-k và latency trên golden dataset.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 21/09/2026
- Tên thành viên: Đinh Tiến Mạnh