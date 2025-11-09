# --- START OF FILE client_xmlrpc.py (Modified for Docker with Clear Output) ---
import xmlrpc.client
import time

def run_pipeline_client(data_size):
    """
    Calls the XML-RPC master service running in Docker and prints a detailed summary.
    """
    print("=" * 60)
    print("🚀 STARTING DOCKER XML-RPC CLIENT 🚀")
    print("=" * 60)

    try:
        # Connect to the master service's port exposed by Docker
        master = xmlrpc.client.ServerProxy("http://localhost:8005")
        
        print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Initiating pipeline with data_size = {data_size}...")
        
        # Make the remote procedure call
        resp = master.run_pipeline(data_size)
        
        print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Received final response from the master server.")
        print("-" * 25)
        print("✅ PIPELINE COMPLETE")
        print("-" * 25)

        # --- Parse the summary string from the response to display structured results ---
        summary_parts = {}
        if "summary" in resp:
            try:
                parts = resp["summary"].split(', ')
                for part in parts:
                    key, value = part.split('=')
                    summary_parts[key.strip()] = value.strip()
            except Exception as e:
                print(f"Warning: Could not parse summary string '{resp['summary']}'. Error: {e}")
                summary_parts = {}

        print("📊 Final Summary:")
        print(f"     - Cluster Result:   {summary_parts.get('Cluster', 'N/A')}")
        print(f"     - Correlation:      {float(summary_parts.get('Corr', 0.0)):.4f}")
        print(f"     - Average Distance: {float(summary_parts.get('Dist', 0.0)):.4f}")
        
        print(f"\n⏱️ Total Execution Time: {resp.get('total_time', 0.0):.4f} seconds")
        print("=" * 60)

    except Exception as e:
        print("\n" + "="*60)
        print("❌ ERROR: Could not connect to the XML-RPC Master Service in Docker.")
        print(f"   Please ensure the docker-compose services are running.")
        print(f"   Details: {e}")
        print("="*60)


if __name__ == '__main__':
    # Define the size of the data for the pipeline.
    matrix_size = 300
    run_pipeline_client(matrix_size)
# --- END OF FILE client_xmlrpc.py (Modified for Docker with Clear Output) ---