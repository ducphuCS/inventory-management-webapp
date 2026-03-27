import subprocess
import sys
import time
import os

def main():
    print("Welcome to the Prototype WebApp!")
    print("Starting FastAPI backend...")
    
    # Start FastAPI backend
    backend_process = subprocess.Popen(
        ["uv", "run", "fastapi", "dev", "app/backend/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2) # Wait a bit for backend to start up
    print("Starting Streamlit frontend...")
    
    # Start Streamlit frontend
    env = os.environ.copy()
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    env["STREAMLIT_server_headless"] = "true"
    
    frontend_process = subprocess.Popen(
        ["uv", "run", "streamlit", "run", "app/frontend/app.py"],
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=env
    )

    try:
        # Keep the main process running
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("Services stopped.")

if __name__ == "__main__":
    main()
