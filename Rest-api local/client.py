# --- START OF FILE client.py (for Local REST API) ---
import requests
import time

def run_pipeline_client(data_size):
    """
    Calls the local REST API master service and prints a detailed, formatted summary.
    """
    master_url = "http://localhost:5000/run_pipeline"
    payload = {"data_size": data_size}

    print("=" * 60)
    print("🚀 STARTING LOCAL REST API CLIENT 🚀")
    print("=" * 60)

    try:
        print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Initiating pipeline with data_size = {data_size}...")
        
        # Make the HTTP POST request to the local master server
        response = requests.post(master_url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (like 404 or 500)

        # Parse the JSON response from the server
        data = response.json()
        
        print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Received final response from the master server.")
        print("-" * 25)
        print("✅ PIPELINE COMPLETE")
        print("-" * 25)

        # --- Format the JSON data into the consistent output style ---
        summary = data.get("summary", {})
        features = summary.get("features", {})
        
        print("📊 Final Summary:")
        # Note: The metrics are different from gRPC's, but the *format* is the same.
        print(f"     - Final Analysis:   {summary.get('final_analysis', 'N/A')}")
        print(f"     - Calculated Mean:    {features.get('mean', 0.0):.4f}")
        print(f"     - Calculated Std Dev: {features.get('std', 0.0):.4f}")
        
        print(f"\n⏱️ Total Execution Time: {data.get('total_time', '0.0')} seconds")
        print("=" * 60)

    except requests.exceptions.RequestException as e:
        print("\n" + "="*60)
        print("❌ ERROR: Could not connect to the local REST API Master Service.")
        print(f"   Please ensure the master.py script is running on port 5000.")
        print(f"   Details: {e}")
        print("="*60)

if __name__ == "__main__":
    # Define the size of the data for the pipeline.
    matrix_size = 300
    run_pipeline_client(matrix_size)
# --- END OF FILE client.py (for Local REST API) ---