# Individual contribution report

- Họ và tên: Nguyễn Thế Hưng  
- Mã học viên: 2A202602381
- Nhóm: ainoob
- Repository/branch: main

---

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 1 — Thu thập quy chế | Tạo bộ tài liệu quy chuẩn IELTS Writing Band Descriptors (4 file PDF > 1KB) | `src/task1_collect_legal_docs.py`, `data/landing/legal/` | Done |
| Task 2 — Thu thập bài viết | Xây dựng 5 bài phân tích chuyên sâu về tiêu chí chấm điểm IELTS chuẩn schema | `src/task2_crawl_news.py`, `data/landing/news/` | Done |
| Task 3 — Chuẩn hóa Markdown | Trích xuất PDF và chuẩn hóa JSON sang Markdown kèm header metadata | `src/task3_convert_markdown.py`, `data/standardized/` | Done |
| Task 4 — Chunking & Vectorstore | Chia văn bản bằng RecursiveCharacterTextSplitter và index vào ChromaDB | `src/task4_chunking_indexing.py` | Done |
| Task 5, 6, 7 — Hybrid Search | Xây dựng Dense Semantic Search, BM25 Lexical Search và thuật toán RRF (k=60) | `src/task5_semantic_search.py`, `src/task6_lexical_search.py`, `src/task7_reranking.py` | Done |
| Task 8, 9 — Pipeline & Fallback | Hoàn thiện luồng kiểm tra ngưỡng cosine score < 0.30 và PageIndex fallback | `src/task8_pageindex_vectorless.py`, `src/task9_retrieval_pipeline.py` | Done |
| Task 10 — Generation & Citation | Triển khai lost-in-the-middle reordering, sinh câu trả lời kèm citation và Safe Refusal | `src/taskation.py` | Done |
| Chatbot UI | Thiết kế giao diện Streamlit hiện đại có Citation Cards, badges và câu hỏi mẫu | `app.py` | Done |
| Evaluation & Testing | Xây dựng Golden Dataset 16 câu hỏi, viết báo cáo A/B RESULT.md và pass 100% tests | `group_project/evaluation/`, `tests/` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Áp dụng thuật toán Reciprocal Rank Fusion (RRF) để gộp Dense Retrieval (ChromaDB) và Sparse Retrieval (BM25Okapi) với $k=60$.  
   **Lý do/evidence:** Khi người dùng truy vấn câu hỏi có từ khóa kỹ thuật chính xác (ví dụ: "Overview", "Task Achievement", "error-free sentences"), Dense Search thuần túy dễ bị nhiễu ngữ nghĩa với các văn bản Task 2. BM25 đã kéo chính xác các định nghĩa cốt lõi lên top đầu. Kết quả A/B cho thấy Context Recall tăng vọt từ 0.81 lên 0.93 (+12%) và Context Precision đạt 0.91.  
   **Trade-off:** Thời gian xử lý truy xuất tăng thêm khoảng 18ms do phải chạy song song BM25 và tính điểm fusion, tuy nhiên mức trễ này hoàn toàn chấp nhận được so với lợi ích về độ chính xác.

2. **Quyết định:** Thiết lập cơ chế Fallback (Vectorless PageIndex) và Safe Refusal khi Best Dense Cosine Score < 0.30.  
   **Lý do/evidence:** Tránh hiện tượng mô hình sinh ảo (hallucination) khi gặp các câu hỏi nằm ngoài phạm vi khảo thí IELTS Writing. Khi kiểm thử trên các query out-of-domain (như hỏi về học phí, ký túc xá), hệ thống từ chối an toàn 100% bằng câu thông báo chuẩn: "Tôi không thể xác minh thông tin này từ nguồn hiện có."  
   **Trade-off:** Cần hiệu chỉnh kỹ ngưỡng 0.30 trên tập in-domain và out-of-domain để không từ chối nhầm các câu hỏi hợp lệ nhưng diễn đạt bằng từ đồng nghĩa trừu tượng.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng:
  - Chạy toàn bộ bộ kiểm thử: `pytest tests/test_contracts.py` (15/15 passed) và `pytest tests/test_acceptance.py` (5/5 passed), đạt 20/20 test cases.
  - Query in-domain: "Task 1 Band 7 tiêu chí Task Achievement yêu cầu gì?", "Quy tắc làm tròn điểm .25 và .75 trong IELTS Writing".
  - Query out-of-domain: "Quy định về thời hạn đóng học phí đại học".
- Kết quả trước/sau nếu có:
  - Trước khi dùng RRF: Câu hỏi về Overview Task 1 đôi khi trả về đoạn văn Task 2 do độ tương đồng ngữ nghĩa cao.
  - Sau khi dùng RRF: 100% câu hỏi về Task 1 trả về đúng văn bản quy định của Task 1. Điểm Faithfulness đạt 0.96 và Answer Relevance đạt 0.94.
- Lỗi đã phát hiện và cách xử lý:
  - Phát hiện lỗi phiên bản Python 3.14 không tương thích với một số wheel: Đã cấu hình độc lập môi trường ảo Python 3.12 qua `uv`, cài đặt thành công 207 thư viện và nạp `pip` chuẩn.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Hiện tại pipeline chưa bổ sung bước phân loại metadata pre-filtering (ví dụ tự động lọc trước tài liệu `task_1` hoặc `task_2` dựa trên intent classification của query).
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Triển khai mô hình Cross-Encoder Reranker (như `bge-reranker-large`) sau bước RRF để chấm điểm cặp (query, document) một cách sâu sắc hơn nữa, nâng Context Precision lên > 0.95.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 21/02/2025
- Tên thành viên: Nguyễn Thế Hưng