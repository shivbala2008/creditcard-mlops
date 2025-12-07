import subprocess
import time
import requests

def test_api_health():
    # Start server
    proc = subprocess.Popen(
        ["uvicorn", "service.app:app", "--host", "127.0.0.1", "--port", "8001"]
    )
    time.sleep(3)  # give server time to start

    try:
        r = requests.get("http://127.0.0.1:8001/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"
    finally:
        proc.terminate()
