# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Minh Tuấn
- Mã học viên: 2A202602850
- Nhóm: Nhóm AInoob
- Repository/branch: `main`

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| 1. Chunking & Indexing | Sử dụng `RecursiveCharacterTextSplitter` và tạo Vector store ChromaDB với Mistral Embedding API | `src/task4_chunking_indexing.py` | Done |
| 2. Semantic & Lexical Search | Implement Dense search (cosine) và BM25L | `src/task5_semantic_search.py`, `src/task6_lexical_search.py` | Done |
| 3. Reranking & Retrieval Pipeline | Viết logic Reciprocal Rank Fusion (RRF), gọi Fallback nếu score thấp | `src/task7_reranking.py`, `src/task9_retrieval_pipeline.py` | Done |
| 4. LLM Generation | Format context có citation, gọi Mistral API (ministral-3b-2512) để sinh câu trả lời | `src/task10_generation.py` | Done |
| 5. Streamlit UI | Code giao diện Chatbot kết nối với RAG Pipeline | `app.py` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Chuyển sang dùng API Embedding (`mistral-embed-2312`) và LLM Generation (`ministral-3b-2512`) của Mistral.
   **Lý do/evidence:** Máy tính cá nhân không đủ tài nguyên để chạy nhanh model embedding 2.4GB (`bge-m3`). Việc dùng API giúp index 1254 chunks rất nhanh và cho ra kết quả ổn định.
   **Trade-off:** Cần kết nối Internet liên tục và phụ thuộc vào rate limit / độ trễ của API Mistral. Không chạy được hoàn toàn offline.

2. **Quyết định:** Chuyển từ thuật toán `BM25Okapi` sang `BM25L` cho Lexical Search.
   **Lý do/evidence:** Tập dữ liệu (corpus) hiện tại có thể khá nhỏ. Với corpus nhỏ, công thức tính IDF trong BM25Okapi có thể trả về giá trị 0 hoặc âm. BM25L tinh chỉnh lại giúp đảm bảo điểm số luôn dương, phù hợp hơn với quy mô tài liệu hiện có.
   **Trade-off:** Tốn thêm chút chi phí tính toán nhưng đảm bảo pipeline không bị sập hay mất điểm số hợp lệ.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Chạy `pytest tests/test_contracts.py` để test các pipeline contracts. Query thực tế: *"What is the IELTS writing test about?"* trên Streamlit.
- Kết quả trước/sau nếu có: Pass 15/15 tests thay vì fail như lúc đầu chưa implement. Trả lời đúng, không bịa thông tin và trích dẫn chuẩn nguồn.
- Lỗi đã phát hiện và cách xử lý: Lỗi `UnicodeEncodeError` ở Terminal Windows khi in output có tiếng Việt. Đã khắc phục bằng cách thiết lập stdout sang mã hóa utf-8. Lỗi điểm BM25 bằng 0 đã xử lý bằng cách chuyển sang `BM25L`.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: PageIndex fallback (Task 8) mới chỉ được làm giả lập (mock) trả về rỗng do chưa có API key.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Triển khai thật dịch vụ fallback và thêm metrics caching để load nhanh hơn.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Nguyễn Minh Tuấn
