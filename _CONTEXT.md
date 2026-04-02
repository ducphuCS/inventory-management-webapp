# A prototype for developing a web application with Streamlit and FastAPI

**Status:** 🟢 Active
**Objective:** A proof of concept (POC) about web application development using Streamlit and FastAPI. This POC demonstrates a "frontend-api-microservice" architecture where a Streamlit UI communicates with a FastAPI bridge, which in turn orchestrates data from a Go-based inventory service.

## Engineer Decisions:
- **Python environment:** Use `uv` for dependency management and environment management.
- **Frontend:** Streamlit for rapid dashboard development and state-persistent UI.
- **Backend Bridge:** FastAPI to provide a consistent internal API and handle communication with downstream microservices.
- **State Management:** Use `st.session_state` to maintain UI consistency during complex interaction (e.g., toggling analytical views).
- **Dockerization:** Fully containerized with a shared network for microservice discovery.

## 🎯 Next Actions:
- [x] Initialize FastAPI backend and Streamlit frontend
- [x] Configure Docker networking (`prototype-webapp-service`)
- [x] Implement bridging logic to `PROTOTYPE-GinServices`
- [x] Standardize Item mapping between services
- [x] Add persistent state management for item analysis
- [x] Finalize deployment documentation

## 📂 Directory Structure

```text
PROTOTYPE-WebApp/
├── app/
│   ├── backend/      # FastAPI proxy service
│   └── frontend/     # Streamlit UI
├── Dockerfile        # Combined/Single definition
├── docker-compose.yml # Orchestration with GinServices
└── ...
```

## 🔗 Connectivity
- **Upstream:** End User (Browser access on Port 8501)
- **Downstream:** `PROTOTYPE-GinServices` (Inventory and Analysis Engine)
- **Shared Network:** `prototype-webapp-service`

## 🏷️ Semantic Hooks
#streamlit #fastapi #python #webapp #fastpace #development #poc #docker #microservices