# 🧠 NeurRoute — Intelligent LLM Router

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_Pipeline-orange?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-0.x-green?style=for-the-badge)
![OpenRouter](https://img.shields.io/badge/OpenRouter-Multi--Model-purple?style=for-the-badge)
![Tavily](https://img.shields.io/badge/Tavily-Web_Search-red?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)
![Flask](https://img.shields.io/badge/Flask-REST_API-black?style=for-the-badge&logo=flask)

**A production-ready agentic system that intelligently classifies user queries, decides whether real-time web search is needed, and dynamically routes each query to the best-performing free LLM — all in a single automated pipeline.**

</div>

---

## 🚀 What Makes This Project Stand Out

Most LLM applications hardcode a single model for everything. **NeurRoute takes a different approach** — it treats model selection as a first-class problem. Instead of guessing which model to use, it *routes every query* to the model that objectively performs best for that task category.

This is not a tutorial project. It is a fully containerized, multi-service agentic system built with real engineering decisions:

- **Custom benchmark dataset** built by scraping live model performance data
- **Agentic graph pipeline** with conditional branching (not a simple chain)
- **Dynamic web search** injected into context when the query needs live data
- **REST API backend** serving a polished, animated frontend UI
- **Full Docker Compose deployment** — one command to run everything

---

## 🏗️ System Architecture

```
User Query
    │
    ▼
┌─────────────┐
│  CLASSIFY   │  → Categorizes query into one of 6 task types
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  DECIDE SEARCH  │  → LLM decides: does this need live web data?
└──────┬──────────┘
       │
   ┌───┴────┐
  YES       NO
   │         │
   ▼         │
┌────────┐   │
│  WEB   │   │    (Tavily Search — top 3 results injected as context)
│ SEARCH │   │
└───┬────┘   │
    └────┬───┘
         ▼
┌──────────────┐
│  PICK MODEL  │  → Selects highest-scoring model for this task category
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  RUN MODEL   │  → Calls the chosen model via OpenRouter API
└──────┬───────┘
       │
       ▼
  Final Response
```

---

## 📊 Benchmark-Driven Model Selection (The Core Innovation)

> **Model scores were gathered using a custom-built Ultimate Web Scraper** that extracted performance data from public LLM leaderboards and benchmark aggregators. This data was then structured into a scoring matrix used at runtime to select the best available free model per task.

Each model is scored across **6 task categories** on a scale of 1–10:

| Model | Global | Reasoning | Coding | Agentic Coding | Mathematics | Data Analysis |
|---|---|---|---|---|---|---|
| nvidia/nemotron-3-nano-30b-a3b | 7 | 8 | 7 | 7 | 8 | 7 |
| mistralai/mistral-small-3.1-24b | 7 | 7 | 8 | 7 | 7 | 7 |
| z-ai/glm-4.5-air | 7 | 7 | 7 | 6 | 7 | 7 |
| nvidia/nemotron-nano-12b-v2-vl | 6 | 6 | 6 | 5 | 6 | 7 |
| nvidia/nemotron-nano-9b-v2 | 6 | 6 | 6 | 5 | 7 | 6 |
| arcee-ai/trinity-mini | 6 | 6 | 7 | 7 | 6 | 6 |
| liquid/lfm-2.5-1.2b-thinking | 5 | 7 | 4 | 4 | 6 | 5 |
| stepfun/step-3.5-flash | 4 | 6 | 7 | 3 | 4 | 5 |
| liquid/lfm-2.5-1.2b-instruct | 4 | 4 | 4 | 3 | 4 | 4 |

At runtime, the system looks up the highest scorer for the detected task category and routes the query there — **no manual model selection needed, ever.**

---

## 🗂️ Task Classification Categories

| Category | Example Queries |
|---|---|
| **Global** | General knowledge, ambiguous questions |
| **Reasoning** | Logic puzzles, deductive analysis, comparisons |
| **Coding** | Algorithms, debugging, code generation |
| **Agentic Coding** | Tool use, multi-step automation, agent design |
| **Mathematics** | Equations, proofs, numerical analysis |
| **Data Analysis** | CSV interpretation, statistics, visualizations |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agentic Pipeline | LangGraph (StateGraph with conditional edges) |
| LLM Orchestration | LangChain + OpenRouter API |
| Web Search | Tavily Search API (top 3 results) |
| Backend | Flask + Flask-CORS (REST API) |
| Frontend | Vanilla HTML/CSS/JS (animated, dark UI) |
| Containerization | Docker + Docker Compose |
| Model Benchmarks | Custom scraper-built scoring matrix |

---

## 📁 Project Structure

```
neurroute/
├── backend/
│   ├── AgenticAiProject.py   # LangGraph pipeline (core logic)
│   ├── server.py             # Flask REST API server
│   ├── requirements.txt      # Python dependencies
│   ├── secret.env            # API keys (not committed)
│   └── Dockerfile
├── frontend/
│   ├── index.html            # Full animated UI
│   └── Dockerfile
└── docker-compose.yml        # One-command deployment
```

---

## ⚡ Quick Start

### Prerequisites
- Docker Desktop installed and running
- An [OpenRouter](https://openrouter.ai) API key (free tier works)
- A [Tavily](https://tavily.com) API key (free tier works)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/neurroute.git
cd neurroute
```

### 2. Set your API keys
Create `backend/secret.env`:
```env
web_search_key=tvly-your-tavily-key
Open_Ai_Key=sk-or-your-openrouter-key
```

### 3. Run with Docker
```bash
docker-compose up --build
```

### 4. Open the app
```
http://localhost:8080
```

That's it. The entire system — backend, frontend, and all dependencies — spins up in one command.

---

## 🖥️ UI Features

The frontend is a fully custom-built dark-themed interface with:

- **Live pipeline visualization** — watch each node (Classify → Search? → Web Search → Pick Model → Generate) animate in real time as your query is processed
- **Typewriter response effect** — responses stream character by character
- **Query history** — last 10 queries saved to localStorage
- **Result cards** — separate cards for query type, search status, selected model, and response
- **Source chips** — when web search is used, retrieved URLs are displayed

---

## 🔌 API Reference

The Flask backend exposes two endpoints:

### `POST /ask`
```json
// Request
{ "query": "What is the time complexity of quicksort?" }

// Response
{
  "classify":      "Reasoning",
  "needs_search":  "no",
  "search_result": "",
  "model":         "nvidia/nemotron-3-nano-30b-a3b:free",
  "response":      "The average time complexity of quicksort is O(n log n)..."
}
```

### `GET /health`
```json
{ "status": "ok" }
```

---

## 🔮 Future Improvements

- [ ] Add more models as free-tier availability expands on OpenRouter
- [ ] Re-run the web scraper periodically to keep benchmark scores up to date
- [ ] Add streaming responses via Server-Sent Events (SSE)
- [ ] Add authentication layer for multi-user deployments
- [ ] Build a model score dashboard with historical performance charts
- [ ] Replace LangChain deprecated classes with latest `langchain-openai` and `langchain-tavily` packages

---

## 👨‍💻 Author

Built by **Omar Ramy**

> This project was built as a demonstration of applied agentic AI engineering — combining benchmark-driven model selection, dynamic tool use, graph-based pipelines, and full-stack deployment into a single coherent system.

---

## 📄 License

MIT License — feel free to use, fork, and build on top of this.
