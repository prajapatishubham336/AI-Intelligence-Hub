import uuid
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph_backend import chatbot as chat_bot
from langgraph_tool_backend import chatbot as tool_bot
from langraph_rag_backend import chatbot as rag_bot
from langgraph_mcp_backend import chatbot as mcp_bot

load_dotenv()

st.set_page_config(page_title="AI Intelligence Hub", page_icon="🤖", layout="wide")

if "thread_id" not in st.session_state: st.session_state["thread_id"] = str(uuid.uuid4())
if "messages" not in st.session_state: st.session_state["messages"] = []
if "chat_threads" not in st.session_state: st.session_state["chat_threads"] = []
if "chat_titles" not in st.session_state: st.session_state["chat_titles"] = {}

router_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)


def route_query(query):
    prompt = f"""
You are an AI routing system.

CHAT = normal/general questions
TOOLS = calculator, web search, latest information, news, stocks
RAG = uploaded PDF/document questions
MCP = MCP tools or expense operations

User question:
{query}

Return only CHAT, TOOLS, RAG or MCP.
"""

    result = router_llm.invoke([HumanMessage(content=prompt)])
    route = result.content.strip().upper()

    if "TOOLS" in route: return "TOOLS"
    if "RAG" in route: return "RAG"
    if "MCP" in route: return "MCP"
    return "CHAT"


def run_backend(route, query):
    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    message = HumanMessage(content=query)

    if route == "TOOLS": chatbot = tool_bot
    elif route == "RAG": chatbot = rag_bot
    elif route == "MCP": chatbot = mcp_bot
    else: chatbot = chat_bot

    result = chatbot.invoke({"messages": [message]}, config=config)
    return result["messages"][-1].content


# ---------------- SIDEBAR ----------------

st.sidebar.title("🤖 AI Intelligence Hub")

if st.sidebar.button("＋ New Chat", use_container_width=True):
    st.session_state["thread_id"] = str(uuid.uuid4())
    st.session_state["messages"] = []
    st.rerun()

st.sidebar.divider()
st.sidebar.subheader("💬 My Conversations")

for thread in reversed(st.session_state["chat_threads"]):
    title = st.session_state["chat_titles"].get(thread, "New Conversation")

    if st.sidebar.button(title, key=f"thread_{thread}", use_container_width=True):
        st.session_state["thread_id"] = thread
        st.rerun()

st.sidebar.divider()
st.sidebar.caption(f"Thread: {st.session_state['thread_id']}")
st.sidebar.success("🟢 Groq Connected")


# ---------------- MAIN UI ----------------

st.title("🤖 AI Intelligence Hub")
st.caption("LangGraph + Groq • Automatic AI Routing")
st.divider()

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- USER INPUT ----------------

user_input = st.chat_input("Ask anything...")

if user_input:

    thread_id = st.session_state["thread_id"]

    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)
        st.session_state["chat_titles"][thread_id] = user_input[:45]

    st.session_state["messages"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                route = route_query(user_input)
                answer = run_backend(route, user_input)
            except Exception as e:
                answer = f"**Error:** `{str(e)}`"

            st.markdown(answer)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": answer
    })