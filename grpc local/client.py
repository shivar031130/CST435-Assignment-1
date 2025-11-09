import grpc
import pipeline_pb2
import pipeline_pb2_grpc
import time

def run_pipeline_client(data_size):
    """
    Connects to the MasterService, initiates the pipeline, and prints a detailed summary.
    """
    print("=" * 60)
    print("🚀 STARTING gRPC PIPELINE CLIENT 🚀")
    print("=" * 60)
    
    try:
        # Establish a connection (channel) to the gRPC server.
        # For a local run, this is 'localhost:50055'.
        with grpc.insecure_channel('localhost:50055') as channel:
            # Create a client stub to perform RPCs.
            stub = pipeline_pb2_grpc.MasterServiceStub(channel)
            
            print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Initiating pipeline with data_size = {data_size}...")
            
            # Create the request message as defined in the .proto file.
            request = pipeline_pb2.PipelineRequest(data_size=data_size)
            
            # Make the remote procedure call to the RunPipeline method.
            response = stub.RunPipeline(request)
            
            print(f"[{time.strftime('%H:%M:%S')}] CLIENT: Received final response from the master server.")
            print("-" * 25)
            print("✅ PIPELINE COMPLETE")
            print("-" * 25)
            
            # --- Parse the summary string from the response to display structured results ---
            summary_parts = {}
            if response.summary:
                try:
                    parts = response.summary.split(', ')
                    for part in parts:
                        key, value = part.split('=')
                        summary_parts[key.strip()] = value.strip()
                except Exception as e:
                    print(f"Warning: Could not parse summary string '{response.summary}'. Error: {e}")
                    summary_parts = {}
            
            print("📊 Final Summary:")
            print(f"     - Cluster Result:   {summary_parts.get('Cluster', 'N/A')}")
            print(f"     - Correlation:      {float(summary_parts.get('Corr', 0.0)):.4f}")
            print(f"     - Average Distance: {float(summary_parts.get('Dist', 0.0)):.4f}")
            
            print(f"\n⏱️ Total Execution Time: {response.total_time:.4f} seconds")
            print("=" * 60)

    except grpc.RpcError as e:
        print("\n" + "="*60)
        print("❌ ERROR: Could not connect to the gRPC Master Service.")
        print(f"   Please ensure the master_server.py is running on localhost:50055.")
        print(f"   Details: {e.code()} - {e.details()}")
        print("="*60)


if __name__ == '__main__':
    # Define the size of the data matrix for the pipeline.
    matrix_size = 300 
    run_pipeline_client(matrix_size)