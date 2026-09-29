# AI-Intelligence-Hub
AI Intelligence Hub — A LangGraph + Groq powered multi-agent chatbot that automatically routes user queries to Chat, Tools, RAG, or MCP backends through a unified Streamlit interface.

# 🤖 AI Intelligence Hub

> **A unified AI chatbot platform built with LangGraph and Groq that automatically routes user queries to the appropriate AI capability such as General Chat, Tools, RAG, or MCP.**

---

## 📌 Project Description

**AI Intelligence Hub** is an advanced AI chatbot application built using **LangGraph, Groq, LangChain, and Streamlit**.

The main goal of this project is to provide a **single intelligent chat interface** where users do not need to manually select which AI capability they want to use.

The user simply enters a question, and the application automatically analyzes the query and routes it to the appropriate backend.

For example:

- General questions → **Chat Backend**
- Calculations and web search → **Tools Backend**
- PDF/document questions → **RAG Backend**
- MCP-related operations → **MCP Backend**

This creates a unified AI experience where multiple AI capabilities work together behind a single interface.

---

## 🎯 Problem Statement

Traditional AI applications often require users to manually select different modes such as:

- Chat
- Web Search
- Calculator
- RAG
- MCP
- Document Q&A

This makes the application less convenient because users need to understand which tool or mode should be selected.

**AI Intelligence Hub solves this problem by introducing automatic query routing.**

The user only provides the question.

The AI Router determines which backend should handle the request.

---

# 🚀 Key Features

## 🧠 Automatic AI Query Routing

The application uses a Groq-powered router to analyze the user's question and automatically select the appropriate backend.

Supported routes:

```text
CHAT
TOOLS
RAG
MCP
```

---
### 💬 General AI Chat

The Chat backend handles:

- General questions
- Concept explanations
- Programming questions
- Normal conversations
- Knowledge-based queries

Example:

> What is LangGraph and why is it used?

Flow:

```text
User Query
    ↓
AI Router
    ↓
CHAT
    ↓
LangGraph Chat Backend
    ↓
Groq
    ↓
Answer
```

---

### 🛠️ AI Tools

The Tools backend provides additional AI capabilities such as:

- 🌐 Web Search
- 🧮 Calculator
- 📈 Stock Information

The AI automatically identifies when a tool is required and routes the query to the appropriate tool.

### 🌐 Web Search

The application can perform web searches when the user's query requires external or recent information.

### 🧮 Calculator Tool

The project includes a calculator tool for performing basic arithmetic operations:

- Addition
- Subtraction
- Multiplication
- Division

### 📈 Stock Price Tool

The Tools backend supports stock information through the configured stock-price service.

The AI can identify stock-related queries and route them to the appropriate tool.

### 📚 RAG-Based Document Question Answering

The project includes a **Retrieval-Augmented Generation (RAG)** backend for answering questions from PDF documents.

The RAG pipeline works as follows:

```text
PDF
 ↓
Document Loader
 ↓
Text Splitting
 ↓
Embeddings
 ↓
FAISS Vector Store
 ↓
Similarity Search
 ↓
Relevant Context
 ↓
Groq LLM
 ↓
Final Answer
```

---

### 🔌 MCP Integration

The project supports **Model Context Protocol (MCP)** for connecting external tools and servers with the AI workflow.

The MCP backend can dynamically load available MCP tools and make them available to the AI model.

```text
User Query
    ↓
MCP Backend
    ↓
MCP Server
    ↓
MCP Tool
    ↓
Groq LLM
    ↓
Final Answer
```

---
### 💬 Unified Chat Interface

The project provides a single Streamlit interface for all AI capabilities.

The user only needs to enter a question in the chat input:

```text
Ask anything...
```

---

### 🗂️ Conversation History

The application provides a conversation sidebar containing previous conversations.

Instead of displaying internal UUIDs as conversation names, the sidebar displays the user's first question.

```text
My Conversations

What is LangGraph?
Calculate 1250 × 48
```
---

### 📝 Markdown Support

AI responses are rendered using Markdown and can display:

```text
Headings
Bold text
Bullet points
Numbered lists
Tables
Code blocks
Structured responses
```
---

### 🏗️ System Architecture
```text
                    ┌─────────────────┐
                    │      USER       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Streamlit UI   │
                    │     app.py      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    AI Router    │
                    │      Groq       │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
     ┌─────────┐        ┌─────────┐        ┌─────────┐
     │  CHAT   │        │  TOOLS  │        │   RAG   │
     └────┬────┘        └────┬────┘        └────┬────┘
          │                  │                  │
          ▼                  ▼                  ▼
     Chat Backend       Tool Backend       RAG Backend
                             │                  │
                       ┌─────┼─────┐            │
                       ▼     ▼     ▼            ▼
                    Search Calc Stock         FAISS
                                                │
                                                ▼
                                           Documents

                             │
                             ▼
                       ┌───────────┐
                       │    MCP    │
                       │  Backend  │
                       └─────┬─────┘
                             │
                             ▼
                        MCP Servers
```
---

### 🔄 Query Routing Workflow
```text
User enters a question
        ↓
Streamlit receives the query
        ↓
Groq AI Router analyzes the query
        ↓
┌───────────────┬───────────────┬───────────────┬───────────────┐
│     CHAT      │     TOOLS     │      RAG      │      MCP      │
└───────┬───────┴───────┬───────┴───────┬───────┴───────┬───────┘
        │               │               │               │
        ▼               ▼               ▼               ▼
   Chat Backend    Tool Backend    RAG Backend    MCP Backend
        │               │               │               │
        └───────────────┴───────────────┴───────────────┘
                                │
                                ▼
                           Final Answer
                                │
                                ▼
                         Streamlit UI
```
---

## 🛠️ Technology Stack

### Programming Language

- Python 3.10+

### AI / LLM

- Groq
- `openai/gpt-oss-120b`

### AI Frameworks

- LangChain
- LangGraph
- LangChain Community
- LangChain Groq

### Frontend

- Streamlit

### RAG

- PyPDF
- FAISS
- Hugging Face Sentence Transformers
- Hugging Face Embeddings

### Tools

- DuckDuckGo Search
- Calculator
- Alpha Vantage

### MCP

- LangChain MCP Adapters
- MCP Servers

### Database / Persistence

- SQLite
- LangGraph SQLite Checkpoint

### Environment

- Python dotenv
- Conda / Virtual Environment

---

## 📁 Project Structure

```text
chatbot-in-langgraph/
│
├── app.py
│
├── langgraph_backend.py
├── langgraph_database_backend.py
├── langgraph_tool_backend.py
├── langraph_rag_backend.py
├── langgraph_mcp_backend.py
│
├── streamlit_frontend.py
├── streamlit_frontend_database.py
├── streamlit_frontend_tool.py
├── streamlit_frontend_mcp.py
├── streamlit_frontend_streaming.py
├── streamlit_frontend_threading.py
├── streamlit_rag_frontend.py
│
├── requirements.txt
├── .env.example
├── README.md
│
└── chatbot.db
```

---

## 📄 Important Files

| File | Purpose |
|---|---|
| `app.py` | Main unified UI and automatic query router |
| `langgraph_backend.py` | Normal AI chatbot |
| `langgraph_database_backend.py` | SQLite-backed LangGraph chatbot |
| `langgraph_tool_backend.py` | Tools-enabled chatbot |
| `langraph_rag_backend.py` | PDF/RAG chatbot |
| `langgraph_mcp_backend.py` | MCP-enabled chatbot |
| `streamlit_frontend.py` | Basic chatbot interface |
| `streamlit_frontend_database.py` | Database/thread chatbot interface |
| `streamlit_frontend_tool.py` | Tool chatbot interface |
| `streamlit_frontend_mcp.py` | MCP chatbot interface |
| `streamlit_rag_frontend.py` | RAG/PDF interface |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment configuration template |

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/prajapatishubham336/chatbot-in-langgraph.git
cd chatbot-in-langgraph
```

### 2. Create the Environment

```bash
conda create -n llmapp python=3.10
conda activate llmapp
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```text
Create a .env file using .env.example and add the required configuration values.
```
---

## ▶️ Run the Application

Run the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Testing

You can test the application with different types of queries.

### 💬 General Chat

```text
What is LangGraph?
```

### 🛠️ Tools

```text
Calculate 1250 × 48
```

```text
Search the web for the latest developments in Generative AI.
```

### 📚 RAG

Upload a PDF document and ask:

```text
According to my PDF, explain the main topic in simple language.
```

### 🔌 MCP

```text
Use the MCP expense tool to check my expense information.
```

The system automatically identifies the appropriate backend and processes the query.

---

## 🔐 Security

- Environment variables are used for sensitive configuration.
- API credentials should not be hard-coded in source files.
- `.env` files should not be committed to GitHub.
- External tools and MCP services should be configured carefully.
- User data and conversation history should be handled securely.

---

## 📊 Advantages

- Unified AI chatbot interface
- Automatic query routing
- Multiple LangGraph backends in one application
- Groq-powered LLM responses
- Web search capabilities
- Calculator and stock price tools
- PDF-based RAG question answering
- MCP tool integration
- Conversation history support
- Streamlit-based interactive UI
- Modular and extensible architecture
- Easy to add new AI capabilities

---

## 🔮 Future Scope

### 🧠 Advanced Query Planning

Implement advanced query planning so the system can break complex user requests into multiple steps and select the required tools or backends automatically.

### 🗂️ Persistent Conversation History

Improve conversation history so previous conversations can be permanently stored and restored from the database.

### 🔐 User Authentication

Add user authentication and authorization so each user can have a separate account and private conversation history.

### 🔌 More MCP Integrations

Add more MCP servers and tools for:

- File management
- Database operations
- Email
- Calendar
- Cloud services
- Business applications
- External APIs

---

## 🎓 Learning Outcomes

This project provides practical experience with:

- Generative AI
- Large Language Models
- LangChain
- LangGraph
- Groq
- AI Agents
- Tool Calling
- RAG
- Vector Databases
- FAISS
- MCP
- Streamlit
- Prompt Engineering
- Query Routing
- Conversation Memory
- AI Application Development

---

## 🚀 Why This Project?

This project demonstrates how multiple modern Generative AI concepts can be combined into a single practical application.

Instead of building separate applications for chat, tools, RAG, and MCP, the system provides a unified interface that automatically routes user queries to the appropriate AI backend.

It demonstrates practical knowledge of building modular, tool-enabled and extensible LLM applications using LangGraph and Groq.

---

## 👨‍💻 Author

**Shubham Prajapati**

AI/ML  and  Generative AI 

---

## 📌 Project Status

**Status:** Completed

The current version includes:

- General AI Chat
- Automatic Query Routing
- AI Tools
- Web Search
- Calculator
- Stock Price Tool
- RAG-Based Document Question Answering
- MCP Integration
- Unified Streamlit Interface
- Conversation History
- Groq LLM Integration

Future improvements can extend the platform with authentication, advanced query planning, persistent conversations and additional MCP integrations.

---

## ⭐ Conclusion

**AI Intelligence Hub** demonstrates a complete Generative AI application built using **LangGraph, Groq, Tools, RAG, MCP and Streamlit**.

The project combines multiple AI capabilities into a single intelligent interface and provides a practical foundation for developing advanced enterprise-level AI applications.

---
