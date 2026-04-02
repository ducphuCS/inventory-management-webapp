# 🚀 Inventory Management WebApp (Dashboard POC)

A modern, fast-paced web application prototype demonstrating a **Streamlit** frontend and a **FastAPI** backend, integrated with a separate Go-based microservice for inventory management.

> [!NOTE]
> **Disclaimer**: This project is a personal **prototype developed for learning and experimentation purposes**. It is intended as a proof-of-concept (POC) to explore bridging various technologies (Streamlit, FastAPI, Golang, and Docker) into a cohesive microservice architecture.

## 🚀 Key Features
- **Rapid UI Development**: Built with [Streamlit](https://streamlit.io/) for a responsive and lightweight developer experience.
- **Backend Orchestration**: [FastAPI](https://fastapi.tiangolo.com/) handles internal API routing and bridges requests to downstream services.
- **Microservices Integration**: Communicates seamlessly with the **GinServices** inventory system via a shared Docker network.
- **Interactive Analysis**: On-demand triggering of product analytical engine with dynamic results display.
- **State Persistence**: Uses session state to prevent UI loss during service cross-calls.

## 🛠️ Technology Stack
- **Frontend**: Streamlit
- **API Bridge**: FastAPI (Python 3.13)
- **Dependency Management**: [uv](https://github.com/astral-sh/uv)
- **Orchestration**: Docker Compose

---

## 🏃 Getting Started

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

---

## 📡 API Proxy Structure
The WebApp backend proxies these requests for the frontend:
- `GET /items/` -> Fetches all items from GinServices.
- `POST /items/` -> Adds a new item to the global inventory.
- `GET /items/{id}/analyze` -> Specifically triggers the Python-based analytical engine in GinServices.

---

## 🏗️ Project Structure
```text
PROTOTYPE-WebApp/
├── app/
│   ├── backend/      # FastAPI (Handles logic & bridging)
│   └── frontend/     # Streamlit (Interactive Dashboard)
├── main.py           # Combined local execution script
├── Dockerfile        # Container definition
├── docker-compose.yml # Orchestration with GinServices
├── pyproject.toml    # Python dependency management (uv)
└── README.md         # This file!
```

## 🏷️ Tags
#streamlit #fastapi #python #docker #microservices #uv #poc

---

## 📜 License & Credits
- **Designed & Implemented with [Antigravity](https://google.com)**: A collaborative POC built with an AI-first coding assistant.
- This project is released under the [MIT License](LICENSE.md).
