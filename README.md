# 🚀 Prototype Web Dashboard (Streamlit + FastAPI)

A modern, fast-paced web application prototype demonstrating a **Streamlit** frontend and a **FastAPI** backend, integrated with a separate Go-based microservice for inventory management.

## 🛠️ Features
- **Rapid UI Development**: Built with Streamlit for a responsive and lightweight developer experience.
- **Backend Orchestration**: FastAPI handles internal API routing and bridges requests to downstream services.
- **Microservices Integration**: Communicates seamlessly with the **GinServices** inventory system via a shared Docker network.
- **Interactive Analysis**: On-demand triggering of product analytical engine with dynamic results display.
- **State Persistence**: Uses session state to prevent UI loss during service cross-calls.

## 🚀 Getting Started

### Using Docker (Recommended)
This approach automatically sets up the communication bridge with the inventory service.
1. Ensure `PROTOTYPE-GinServices` is running to initialize the shared network.
2. Build and start the dashboard:
   ```bash
   docker compose up -d --build
   ```
3. Access the Streamlit UI at `http://localhost:8501`.

### Local Development (Direct Run)
1. Install [uv](https://github.com/astral-sh/uv).
2. Sync the project environment:
   ```bash
   uv sync
   ```
3. Start the application using `main.py` (which handles both FastAPI and Streamlit processes):
   ```bash
   uv run python main.py
   ```

## 📡 API Proxy Structure
The WebApp backend proxies these requests for the frontend:
- `GET /items/` -> Fetches all items from GinServices.
- `POST /items/` -> Adds a new item to the global inventory.
- `GET /items/{id}/analyze` -> Specifically triggers the Python-based analytical engine in GinServices.

## 🏗️ Project Architecture
```text
PROTOTYPE-WebApp/
├── app/
│   ├── backend/      # FastAPI (Handles logic & bridging)
│   └── frontend/     # Streamlit (Interactive Dashboard)
├── main.py           # Combined local execution script
└── pyproject.toml    # Modern Python dependency management (uv)
```

## 🏷️ Tags
#streamlit #fastapi #python #docker #microservices #uv #poc
