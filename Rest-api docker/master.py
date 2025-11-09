# --- START OF FILE master.py (Modified for Clear Output) ---
from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# Define the service URLs using the container names from docker-compose
WORKER1_URL = "http://worker1:5001/process"
WORKER2_URL = "http://worker2:5002/process"
WORKER3_URL = "http://worker3:5003/process"
WORKER4_URL = "http://worker4:5004/process"

@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    print("=" * 60)
    print("🚀 REST API MASTER SERVICE ACTIVITY 🚀")
    print("=" * 60)
    
    start_time = time.time()
    data_size = request.json.get("data_size", 100)
    
    print(f"[{time.strftime('%H:%M:%S')}] MASTER: Received pipeline request with data_size = {data_size}...")
    
    try:
        # Step 1: Call Worker 1
        print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 1 (DataGen)... ", end="")
        resp1 = requests.post(WORKER1_URL, json={"data_size": data_size})
        resp1.raise_for_status()
        data_from_w1 = resp1.json()
        print("-> SUCCESS")
        
        # Step 2: Call Worker 2
        print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 2 (Preprocess)... ", end="")
        resp2 = requests.post(WORKER2_URL, json=data_from_w1)
        resp2.raise_for_status()
        data_from_w2 = resp2.json()
        print("-> SUCCESS")
        
        # Step 3: Call Worker 3
        print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 3 (Feature)... ", end="")
        resp3 = requests.post(WORKER3_URL, json=data_from_w2)
        resp3.raise_for_status()
        data_from_w3 = resp3.json()
        print("-> SUCCESS")
        
        # Step 4: Call Worker 4
        print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 4 (Analysis)... ", end="")
        resp4 = requests.post(WORKER4_URL, json=data_from_w3)
        resp4.raise_for_status()
        final_result = resp4.json()
        print("-> SUCCESS")

        total_time = time.time() - start_time
        
        print("-" * 25)
        print("✅ PIPELINE COMPLETE")
        print("-" * 25)
        
        # This is the data that will be sent back to the client
        final_payload = {
            "total_time": f"{total_time:.4f}",
            "summary": {
                "final_analysis": final_result.get("analysis", "N/A"),
                "features": data_from_w3.get("features", {}),
            }
        }

        print("Returning final summary to the client.")
        print("=" * 60)
        
        return jsonify(final_payload)

    except requests.exceptions.RequestException as e:
        print(f"\nERROR: Pipeline failed. Details: {e}")
        return jsonify({"error": "Failed to process pipeline", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)