import uuid
import streamlit as st
from langchain_core.messages import (HumanMessage, AIMessage)
from langgraph_tool_backend import chatbot

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

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []
add_thread(st.session_state["thread_id"])

st.sidebar.title("LangGraph Tool Chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("Conversations")
for thread_id in st.session_state["chat_threads"][::-1]:
    st.sidebar.write(str(thread_id))

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type here...")

if user_input:
    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    config = {
        "configurable": {
            "thread_id":
                st.session_state["thread_id"]
        }
    }

    with st.chat_message("assistant"):
        def ai_stream():
            for chunk, _ in chatbot.stream(
                {
                    "messages": [HumanMessage(content=user_input)]
                },
                config=config,
                stream_mode="messages"
            ):

                if isinstance(chunk, AIMessage):
                    yield chunk.content
        answer = st.write_stream(ai_stream())

    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": answer
        }
    )