# --- START OF FILE master_xmlrpc.py (Modified for Clear Output) ---
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import time

def run_pipeline(data_size):
    print("=" * 60)
    print("🚀 XML-RPC MASTER SERVICE ACTIVITY 🚀")
    print("=" * 60)
    
    start = time.time()
    
    print(f"[{time.strftime('%H:%M:%S')}] MASTER: Received pipeline request with data_size = {data_size}...")

    try:
        # Connect to each worker service
        data_s = xmlrpc.client.ServerProxy("http://localhost:8001")
        pre_s = xmlrpc.client.ServerProxy("http://localhost:8002")
        feat_s = xmlrpc.client.ServerProxy("http://localhost:8003")
        ana_s = xmlrpc.client.ServerProxy("http://localhost:8004")

        # Step-by-step logging
        print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 1 (DataGen)... ", end="")
        data = data_s.generate_data(data_size)
        print("-> SUCCESS")

        print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 2 (Preprocess)... ", end="")
        cleaned = pre_s.clean_data(data)
        print("-> SUCCESS")

        print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 3 (Feature)... ", end="")
        features = feat_s.extract_features(cleaned)
        print("-> SUCCESS")

        print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 4 (Analysis)... ", end="")
        result = ana_s.analyze_data(features)
        print("-> SUCCESS")

        total_time = time.time() - start
        summary = f"Cluster={result['cluster']}, Corr={result['correlation']:.3f}, Dist={result['avg_distance']:.3f}"
        
        # --- Detailed completion output ---
        print("-" * 25)
        print("✅ PIPELINE COMPLETE")
        print("-" * 25)
        print(f"📊 Final Summary (Prepared for client): {summary}")
        print(f"⏱️ Total orchestration time: {total_time:.4f} seconds")
        print("=" * 60)

        return {"total_time": total_time, "summary": summary}

    except Exception as e:
        print(f"\nERROR: An error occurred during pipeline orchestration: {e}")
        # In XML-RPC, errors are raised as exceptions to the client
        raise e

server = SimpleXMLRPCServer(("localhost", 8005), allow_none=True)
server.register_function(run_pipeline, "run_pipeline")
print("MasterService (XML-RPC) running on port 8005")
server.serve_forever()
# --- END OF FILE master_xmlrpc.py (Modified for Clear Output) ---