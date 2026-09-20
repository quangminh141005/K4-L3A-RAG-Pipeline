# RAG evaluation results

## Run information

| Field                              | Value |
| ---------------------------------- | ----- |
| Evaluation date                    | 20/09/2026 |
| Framework and version              | Ragas 0.4.3 |
| Evaluator model                    | ministral-3b-2512 |
| Generator model                    | ministral-3b-2512 |
| Embedding model                    | mistral-embed-2312 |
| Corpus version/commit              | main |
| Golden dataset size                | 15 questions (Synthetic) |
| `top_k`                            | 5 |
| Fallback threshold and calibration | 0.3 |

## Configurations

- **Config A — dense-only:** Tìm kiếm thuần Vector (Cosine similarity) trên ChromaDB.
- **Config B — hybrid + RRF:** Tìm kiếm kết hợp Vector (Dense) + BM25L (Lexical) và rerank bằng Reciprocal Rank Fusion (k=60).

Hai config phải dùng cùng golden dataset, generator, evaluator, prompt và `top_k`; chỉ thay retrieval strategy.

## Overall scores

| Metric            | Config A | Config B | Delta B−A |
| ----------------- | -------: | -------: | --------: |
| Faithfulness      |     0.82 |     0.88 |     +0.06 |
| Answer relevance  |     0.85 |     0.89 |     +0.04 |
| Context recall    |     0.75 |     0.91 |     +0.16 |
| Context precision |     0.80 |     0.83 |     +0.03 |
| **Average**       |     0.805|     0.877|    +0.072 |

## A/B comparison

- Cấu hình tốt hơn: **Config B (Hybrid + RRF)**
- Evidence: Context recall tăng vọt (+0.16) vì BM25L giúp bắt chính xác các keyword hiếm (như mã môn học, tên riêng) mà Dense search hay bỏ sót. Faithfulness cũng tăng nhờ context đưa vào chuẩn xác hơn.
- Trade-off về latency/cost: Config B tốn thêm thời gian query BM25L và tính toán RRF (~30-50ms) so với Config A, nhưng chất lượng kết quả vượt trội, hoàn toàn xứng đáng với mức đánh đổi.

## Worst performers

|   # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage             | Root cause |
| --: | -------- | ------ | -----------: | --------: | -----: | --------: | ------------------------- | ---------- |
|   1 | IELTS writing task 1 band 9 tips | A |         0.40 |      0.50 |   0.20 |      0.30 | retrieval | Dense model không phân biệt được các từ khóa nhỏ (band 9 vs band 8) |
|   2 | What is tuition fee for international? | A |         0.50 |      0.60 |   0.40 |      0.40 | retrieval | Dùng sai keyword "tuition" thay vì từ vựng trong văn bản |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| -------: | ------ | ------------------------------ | --------------- | ------------- |
|        1 | Bật Hybrid Search mặc định | Config B vượt trội Config A ở mọi mặt | Giảm 80% câu trả lời sai do thiếu context | So sánh tỉ lệ hallucination |
|        2 | Thay đổi Chunking Size | Một số chunks bị cắt ngang ý quan trọng | Tăng Context Precision | Đánh giá lại Context Precision |
|        3 | Implement PageIndex Fallback | Threshold thi thoảng dưới 0.3 | Đảm bảo hệ thống không bao寄 trả kết quả rỗng | Test các query out-of-domain |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| ---------- | -------- | -----------: | -----------------: | ---------- |
| Thay đổi k=60 thành k=20 trong RRF | RRF k=60 |         -0.02|                 0 | k=60 vẫn hoạt động ổn định nhất với phân phối score hiện tại. |
