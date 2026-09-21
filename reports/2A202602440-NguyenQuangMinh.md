# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Quang Minh
- Mã học viên: 2A202602440
- Nhóm: Ainoob
- Vai trò: Nhóm trưởng
- Repository/branch: `quangminh141005/K4-L3A-RAG-Pipeline` / `main`

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 1 — Thu thập tài liệu chính sách/quy định | Chọn 3 tài liệu công khai chính thức về IELTS Writing, cấu hình URL nguồn và xây dựng hàm tải file theo luồng; kiểm tra phần mở rộng, HTTP status, file rỗng và dọn file `.part` khi tải lỗi. | `src/task1_collect_legal_docs.py`, `data/landing/legal/`; commits `1b67e32`, `e6c8d6f`, `4cbdba1` | Done |
| Task 2 — Crawl bài viết/thông báo | Chọn 6 bài viết IELTS Writing, triển khai crawl bất đồng bộ bằng Crawl4AI và lưu riêng từng bài dưới dạng JSON với đủ `url`, `title`, `date_crawled`, `content_markdown`; xử lý lỗi độc lập theo từng URL. | `src/task2_crawl_news.py`, `data/landing/news/article_01.json` đến `article_06.json` | Done |
| Điều phối và tích hợp nhóm | Phân chia các task theo pipeline, thống nhất chủ đề IELTS Writing và cấu trúc dữ liệu đầu vào; theo dõi việc ghép các module convert → retrieval → generation/UI trên nhánh `main`, rà soát sản phẩm theo README và acceptance criteria. | `README.md`, `tests/test_acceptance.py`, `group_project/evaluation/RESULT.md`, branch `main` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Dùng tài liệu từ trang IELTS chính thức cho nhóm dữ liệu chính sách và các bài hướng dẫn IELTS Writing công khai từ IELTS Liz cho nhóm bài viết.  
   **Lý do/evidence:** Ba URL trong `DOCUMENT_SOURCES` cung cấp tiêu chí chấm, đề mẫu và band descriptors; sáu URL trong `ARTICLE_URLS` bổ sung bài học, câu hỏi và bài mẫu cho Task 1/Task 2. Hai nhóm nguồn cùng chủ đề nhưng khác loại nội dung, phù hợp cho hybrid retrieval.  
   **Trade-off:** Corpus tập trung tốt vào IELTS Writing nhưng còn nhỏ và phụ thuộc vào khả năng truy cập của website nguồn; nội dung crawl từ trang web có thể chứa menu, bình luận hoặc phần điều hướng gây nhiễu.

2. **Quyết định:** Chuẩn hoá ngay dữ liệu crawl thành một JSON cho mỗi bài và giữ metadata nguồn thay vì chỉ lưu phần văn bản.  
   **Lý do/evidence:** Các trường `url`, `title`, `date_crawled`, `content_markdown` đáp ứng contract trong `tests/test_acceptance.py`, đồng thời giúp bước chuyển Markdown và generation giữ được nguồn để tạo citation.  
   **Trade-off:** File JSON lớn hơn và nội dung Markdown thô cần được làm sạch ở bước chuẩn hoá; bù lại dữ liệu có thể truy vết và crawl lại dễ dàng.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Chạy hai module bằng `python -m src.task1_collect_legal_docs` và `python -m src.task2_crawl_news`; đối chiếu điều kiện trong `tests/test_acceptance.py` cho dữ liệu đầu vào.
- Kết quả trước/sau nếu có: Hoàn thành 3/3 tài liệu PDF hợp lệ trong `data/landing/legal/` và 6/6 bài viết JSON trong `data/landing/news/` (vượt yêu cầu tối thiểu 5 bài); tất cả JSON đều có đủ bốn trường metadata bắt buộc và nội dung không rỗng.
- Lỗi đã phát hiện và cách xử lý: Quá trình tải có thể tạo file dở dang hoặc một URL crawl bị lỗi làm gián đoạn toàn bộ batch. Task 1 tải vào file `.part`, chỉ đổi tên sau khi thành công và xoá file tạm khi lỗi; Task 2 bọc từng URL trong `try/except` để các bài còn lại vẫn được lưu.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Nội dung Crawl4AI hiện vẫn có thể chứa navigation, comment và boilerplate; Task 1 mới kiểm tra kích thước file, chưa xác thực chặt `Content-Type` hoặc chữ ký định dạng PDF/DOCX.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Thêm bước lọc boilerplate và kiểm thử tự động cho crawler/downloader bằng mock HTTP/Crawl4AI, đồng thời bổ sung retry với exponential backoff và kiểm tra MIME type.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 21/09/2026
- Tên thành viên: Nguyễn Quang Minh
