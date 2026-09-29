import uuid
import streamlit as st

from langchain_core.messages import (AIMessage, HumanMessage,ToolMessage)
from langraph_rag_backend import (chatbot, ingest_pdf, retrieve_all_threads,thread_document_metadata)

def generate_thread_id():
    return uuid.uuid4()

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

if "ingested_docs" not in st.session_state:
    st.session_state["ingested_docs"] = {}
add_thread(st.session_state["thread_id"])
thread_id = str(st.session_state["thread_id"])
thread_docs = st.session_state["ingested_docs"].setdefault(thread_id, {})

st.sidebar.title("LangGraph PDF Chatbot")
st.sidebar.write(f"Thread: `{thread_id}`")

if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()

uploaded_pdf = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

if uploaded_pdf:
    if uploaded_pdf.name not in thread_docs:
        with st.sidebar.status("Indexing PDF..."):
            summary = ingest_pdf(uploaded_pdf.getvalue(), thread_id, uploaded_pdf.name)
            thread_docs[uploaded_pdf.name] = summary
        st.sidebar.success("PDF indexed successfully")

if thread_docs:
    latest = list(thread_docs.values())[-1]
    st.sidebar.info(
        f"{latest['filename']} | "
        f"{latest['chunks']} chunks"
    )

st.sidebar.subheader("Past Conversations")
for old_thread in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(old_thread), key=f"old-{old_thread}"):
        st.session_state["thread_id"] = old_thread
        messages = load_conversation(old_thread)
        st.session_state["message_history"] = [{"role": "user"
                if isinstance(msg, HumanMessage)
                else "assistant",
                "content": msg.content
            }
            for msg in messages
        ]
        st.rerun()

st.title("Multi Utility RAG Chatbot")
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask about your PDF...")
if user_input:
    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    config = {"configurable": {"thread_id": thread_id}}
    with st.chat_message("assistant"):
        def response_stream():
            for chunk, _ in chatbot.stream(
                {
                    "messages": [HumanMessage(content=user_input)]
                },
                config=config,
                stream_mode="messages"
            ):

                if isinstance(chunk, AIMessage):
                    yield chunk.content

        answer = st.write_stream(response_stream())
    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    metadata = thread_document_metadata(thread_id)
    if metadata:
        st.caption(
            f"Document: "
            f"{metadata.get('filename')} | "
            f"Pages: "
            f"{metadata.get('documents')} | "
            f"Chunks: "
            f"{metadata.get('chunks')}"
        )