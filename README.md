\# ⚖️ LexBridge



\### Agentic AI-Powered Legal Intake, Research \& Case Triage



LexBridge is an \*\*agentic AI backend for legal assistance\*\* that transforms an unstructured legal problem into a structured, research-backed case.



It uses a \*\*multi-agent LangGraph workflow\*\* to collect case information, classify legal issues, retrieve relevant legal information using RAG, assess case priority, and generate structured case briefs for human legal professionals.



\---



\## 🚨 The Problem



People facing legal problems often struggle to:



\* Understand what area of law applies to their situation

\* Identify what information is relevant to their case

\* Find applicable legal resources

\* Prepare a structured case for a lawyer

\* Access legal assistance quickly



At the same time, legal professionals and legal-aid organizations have limited time to process large numbers of cases.



\*\*LexBridge automates the initial intake, research, and triage process while keeping humans involved in important legal decisions.\*\*



\---



\## 💡 How It Works



```text

User Case

&#x20;  │

&#x20;  ▼

┌─────────────────┐

│  Intake Agent   │

│                 │

│ Collect facts   │

│ \& ask questions │

└────────┬────────┘

&#x20;        │

&#x20;        ▼

┌──────────────────────┐

│ Classification Agent │

│                      │

│ Identify legal issue │

│ \& jurisdiction       │

└──────────┬───────────┘

&#x20;          │

&#x20;          ▼

┌─────────────────┐

│ Research Agent  │

│                 │

│ RAG + Vector    │

│ Legal Search    │

└────────┬────────┘

&#x20;        │

&#x20;        ▼

┌─────────────────┐

│  Triage Agent   │

│                 │

│ Priority \&      │

│ Case Routing    │

└────────┬────────┘

&#x20;        │

&#x20;        ▼

┌───────────────────┐

│ Case Brief Agent  │

│                   │

│ Structured Legal  │

│ Case Brief        │

└─────────┬─────────┘

&#x20;         │

&#x20;         ▼

&#x20;   Human Review

```



\---



\## 🤖 Multi-Agent Architecture



LexBridge uses \*\*LangGraph\*\* to orchestrate multiple specialized agents.



\### 🗣️ Intake Agent



Conducts an adaptive conversation to collect important case information such as:



\* Facts

\* Timeline

\* Jurisdiction

\* Parties involved

\* Legal concerns

\* Missing information



\### 🧩 Classification Agent



Processes the collected information and identifies:



\* Legal issue

\* Area of law

\* Jurisdiction

\* Case category



\### 🔎 Research Agent



Uses \*\*Retrieval-Augmented Generation (RAG)\*\* to search a curated legal knowledge base.



It:



\* Generates semantic search queries

\* Retrieves relevant legal documents

\* Identifies relevant sections

\* Extracts supporting information

\* Tracks sources

\* Identifies unresolved questions



The agent is instructed to ground its findings in retrieved information rather than inventing legal authorities.



\### 🚦 Triage Agent



Analyzes the structured case and determines relevant triage information such as:



\* Priority

\* Urgency

\* Case category

\* Routing requirements

\* Missing information



\### 📄 Case Brief Agent



Generates a structured case brief containing:



\* Case summary

\* Relevant facts

\* Legal issue

\* Research findings

\* Relevant legal sections

\* Sources

\* Priority

\* Unresolved questions



The generated brief is intended for \*\*human legal review\*\*.



\---



\## 🧠 RAG Architecture



LexBridge uses PostgreSQL and \*\*pgvector\*\* for semantic legal-document retrieval.



```text

Legal Documents

&#x20;     │

&#x20;     ▼

Text Extraction

&#x20;     │

&#x20;     ▼

Chunking

&#x20;     │

&#x20;     ▼

Embeddings

&#x20;     │

&#x20;     ▼

PostgreSQL + pgvector

&#x20;     │

&#x20;     │

&#x20;     │ Case Query

&#x20;     ▼

Vector Search

&#x20;     │

&#x20;     ▼

Relevant Legal Chunks

&#x20;     │

&#x20;     ▼

Research Agent

&#x20;     │

&#x20;     ▼

Grounded Legal Findings

```



\---



\## 🏗️ Technology Stack



\### Backend



\* \*\*Python\*\*

\* \*\*FastAPI\*\*

\* \*\*LangGraph\*\*

\* \*\*PostgreSQL\*\*

\* \*\*pgvector\*\*

\* \*\*SQLAlchemy\*\*

\* \*\*PyJWT\*\*

\* \*\*Ollama\*\*



\### AI



\* Agentic AI

\* Multi-agent workflows

\* Retrieval-Augmented Generation

\* Embeddings

\* Vector similarity search

\* Structured LLM outputs

\* Human-in-the-loop workflows



\---



\## 🔐 Authentication



LexBridge uses JWT-based authentication.



```text

Login

&#x20; ↓

Credential Verification

&#x20; ↓

JWT Generation

&#x20; ↓

Bearer Token

&#x20; ↓

Protected API Endpoint

&#x20; ↓

JWT Verification

&#x20; ↓

Authenticated User

```



\---



\## 📁 Project Structure



```text

LexBridge/

│

├── backend/

│   ├── agents/

│   │   ├── intake\_agent.py

│   │   ├── classification\_agent.py

│   │   ├── research\_agent.py

│   │   ├── triage\_agent.py

│   │   └── case\_brief\_agent.py

│   │

│   ├── knowledge/

│   │   ├── case\_state.py

│   │   ├── llm.py

│   │   └── retriever.py

│   │

│   ├── models/

│   ├── schemas/

│   ├── auth.py

│   ├── database.py

│   ├── app.py

│   └── requirements.txt

│

├── .gitignore

└── README.md

```



\---



\## ⚙️ Getting Started



\### 1. Clone the repository



```bash

git clone https://github.com/gitman66-coder/lexbridge.git

cd lexbridge

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



Activate it on Windows:



```powershell

.venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

cd backend

pip install -r requirements.txt

```



\### 4. Configure environment variables



Create a `.env` file inside `backend/`:



```env

DATABASE\_URL=postgresql://username:password@localhost:5432/lexbridge



SECRET\_KEY=your-secret-key



OLLAMA\_BASE\_URL=http://localhost:11434

OLLAMA\_MODEL=your-model

```



\*\*Never commit your `.env` file to GitHub.\*\*



\### 5. Start the API



From the `backend` directory:



```bash

uvicorn app:app --reload

```



The API will be available at:



```text

http://127.0.0.1:8000

```



Interactive API documentation:



```text

http://127.0.0.1:8000/docs

```



\---



\## 🗄️ Data Persistence



LexBridge uses PostgreSQL to persist the application's important state.



Core entities include:



```text

Users

Cases

Case Briefs

Legal Documents

Legal Chunks

```



Case workflow information is persisted in the database rather than relying solely on temporary LangGraph state.



\---



\## 🔄 Case Lifecycle



```text

Case Created

&#x20;    ↓

AI Intake

&#x20;    ↓

Information Extraction

&#x20;    ↓

Legal Classification

&#x20;    ↓

RAG-Based Research

&#x20;    ↓

Case Triage

&#x20;    ↓

Case Brief Generation

&#x20;    ↓

Human Legal Review

```



\---



\## 🎯 Project Goal



LexBridge is designed to reduce the initial workload involved in legal case intake and preparation while making legal assistance more accessible.



It does \*\*not replace a lawyer\*\*. Instead, it acts as an intelligent pipeline that helps transform raw case information into structured, research-supported material that can be reviewed by a qualified legal professional.



\---



\## 🛠️ Future Improvements



\* React-based client application

\* Lawyer dashboard

\* Document upload from the client

\* Automated case routing

\* More comprehensive legal knowledge bases

\* Persistent LangGraph checkpoints

\* Human-in-the-loop approval nodes

\* Role-based access control

\* Production deployment

\* Audit logging



\---



\## 👨‍💻 Built For



\*\*Avinya Hackathon 2026\*\*



LexBridge explores how \*\*Agentic AI + RAG + workflow orchestration\*\* can be applied to real-world access-to-justice problems.



