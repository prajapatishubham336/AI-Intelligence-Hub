import uuid
import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph_database_backend import (chatbot, retrieve_all_threads)

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
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id }})
    return state.values.get("messages", [])

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_thread(st.session_state["thread_id"])
st.sidebar.title("LangGraph Chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")
for thread_id in st.session_state["chat_threads"][::-1]:

    if st.sidebar.button(
        str(thread_id),
        key=f"thread-{thread_id}"):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id)
        st.session_state["message_history"] = [
            {
                "role": "user"
                if isinstance(msg, HumanMessage)
                else "assistant",
                "content": msg.content
            }
            for msg in messages
        ]


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

    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    with st.chat_message("assistant"):
        response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
        answer = response["messages"][-1].content
        st.write(answer)

    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": answer
        }
    )