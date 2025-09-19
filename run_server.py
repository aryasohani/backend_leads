# run_server.py
import threading
import time
import webbrowser
import urllib.request

def start_uvicorn():
    # NOTE: reload=False is important to avoid the auto-reloader spawning extra processes
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=False)

def wait_until_up(url, timeout=30.0, interval=0.5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(interval)
    return False

if __name__ == "__main__":
    # start server in a daemon thread (so the main thread can poll)
    t = threading.Thread(target=start_uvicorn, daemon=True)
    t.start()

    docs_url = "http://127.0.0.1:8001/docs"
    health_url = "http://127.0.0.1:8001/openapi.json"   # quick JSON endpoint to test readiness

    print("Waiting for server to start...", end="", flush=True)
    ok = wait_until_up(health_url, timeout=30.0)
    if ok:
        print(" started.")
        try:
            webbrowser.open(docs_url)
            print(f"Opened {docs_url} in your default browser.")
        except Exception as e:
            print("Could not open browser automatically:", e)
            print(f"Open the docs manually at: {docs_url}")
    else:
        print("\nServer did not respond within 30s. Check logs.")
        print(f"Try opening {docs_url} manually to see error details.")
    # Wait for the server thread (will run until you Ctrl+C)
    t.join()
