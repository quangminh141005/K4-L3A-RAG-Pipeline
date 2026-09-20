import streamlit as st
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("RAG Chatbot")
    st.caption("Thay mô tả theo đề tài của nhóm")
    top_k = st.slider("Số chunks", 3, 10, 5)

st.title("RAG Chatbot")
st.caption("Thay tiêu đề và hướng dẫn sử dụng")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander(f"Nguồn tham khảo (từ {message.get('retrieval_source', 'unknown')})"):
                for idx, src in enumerate(message["sources"], 1):
                    st.markdown(f"**{idx}. {src['metadata'].get('title', 'N/A')}** (Score: {src.get('score', 0):.2f})")
                    st.caption(src['content'][:200] + "...")

query = st.chat_input("Nhập câu hỏi...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        from src.task10_generation import generate_with_citation
        
        with st.spinner("Đang tìm kiếm và tạo câu trả lời..."):
            result = generate_with_citation(query, top_k=top_k)
            
        answer = result["answer"]
        sources = result["sources"]
        retrieval_source = result["retrieval_source"]
        
        st.markdown(answer)
        
        if sources:
            with st.expander(f"Nguồn tham khảo (từ {retrieval_source})"):
                for idx, src in enumerate(sources, 1):
                    st.markdown(f"**{idx}. {src['metadata'].get('title', 'N/A')}** (Score: {src.get('score', 0):.2f})")
                    st.caption(src['content'][:200] + "...")

    st.session_state.messages.append({
        "role": "assistant", 
        "content": answer,
        "sources": sources,
        "retrieval_source": retrieval_source
    })
