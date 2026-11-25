# 🤖 AutoFix: Autonomous GitHub Bug-Fixing AI Agent

An autonomous AI software engineering agent built with **LangGraph**, **Google Gemini**, and **Docker** that automatically investigates GitHub issues, writes patches in an isolated sandbox, verifies fixes using `pytest`, and opens a Pull Request.

## 🏗️ System Architecture

```text
GitHub Issue ──▶ LangGraph Agent (Gemini) ──▶ Isolated Docker Sandbox
                       ▲                              │
                       │ (Retry on Test Fail)         ▼
                GitHub Pull Request ◀── Pytest Verification Passed
```

## ✨ Key Features
- **Isolated Execution Sandbox:** Clones and executes untrusted code inside a memory-limited (`2GB`) custom Linux Docker container (`python:3.11-slim`).
- **Self-Correcting Agent Loop:** Uses **LangGraph** cyclic state machines (`Fix -> Test -> Retry`) to iteratively debug failures up to 3 attempts.
- **Structured Outputs:** Enforces strict **Pydantic** schemas for reliable file path identification and code generation.
- **End-to-End Git Automation:** Automatically creates a new branch, commits verified changes, and opens a detailed Pull Request via `PyGithub`.

## 🛠️ Tech Stack
- **Orchestration:** LangGraph, LangChain
- **LLM:** Google Gemini (`gemini-3.5-flash-lite`)
- **Sandboxing:** Docker SDK for Python, Linux (`ripgrep`, `git`, `pytest`)
- **Validation & Integration:** Pydantic, PyGithub, Python 3.11+

## 🚀 How to Run Locally

1. **Build the Docker Sandbox Image:**
   ```bash
   docker build -t autofix-sandbox:latest -f docker/Dockerfile.sandbox .
   ```

2. **Install Dependencies:**
   ```bash
   pip install langgraph langchain-google-genai docker pydantic PyGithub python-dotenv
   ```

3. **Configure Environment Variables (`.env`):**
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GITHUB_TOKEN=your_github_personal_access_token
   ```

4. **Run the Agent:**
   ```bash
   python run_agent.py
   ```
