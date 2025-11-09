from concurrent import futures
import grpc, pipeline_pb2, pipeline_pb2_grpc
import time

class MasterServicer(pipeline_pb2_grpc.MasterServiceServicer):
    def RunPipeline(self, request, context):
        
        # --- START: Added for clear output ---
        print("=" * 60)
        print("🚀 gRPC MASTER SERVICE ACTIVITY 🚀")
        print("=" * 60)
        
        start = time.time()
        data_size = request.data_size
        
        print(f"[{time.strftime('%H:%M:%S')}] MASTER: Received pipeline request with data_size = {data_size}...")
        
        try:
            # Connect to each service
            data_stub = pipeline_pb2_grpc.DataGenServiceStub(grpc.insecure_channel('localhost:50051'))
            pre_stub = pipeline_pb2_grpc.PreprocessServiceStub(grpc.insecure_channel('localhost:50052'))
            feat_stub = pipeline_pb2_grpc.FeatureServiceStub(grpc.insecure_channel('localhost:50053'))
            ana_stub = pipeline_pb2_grpc.AnalysisServiceStub(grpc.insecure_channel('localhost:50054'))
            
            # --- Step-by-step logging ---
            print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 1 (DataGen)... ", end="")
            data = data_stub.GenerateData(pipeline_pb2.DataRequest(size=data_size))
            print("-> SUCCESS")

            print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 2 (Preprocess)... ", end="")
            cleaned = pre_stub.CleanData(data)
            print("-> SUCCESS")

            print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 3 (Feature)... ", end="")
            features = feat_stub.ExtractFeatures(cleaned)
            print("-> SUCCESS")

            print(f"[{time.strftime('%H:%M:%S')}] MASTER: Calling Worker 4 (Analysis)... ", end="")
            result = ana_stub.AnalyzeData(features)
            print("-> SUCCESS")
            
            total_time = time.time() - start
            summary = f"Cluster={result.cluster_result}, Corr={result.correlation:.3f}, Dist={result.avg_distance:.3f}"
            
            # --- Detailed completion output ---
            print("-" * 25)
            print("✅ PIPELINE COMPLETE")
            print("-" * 25)
            print(f"📊 Final Summary (Prepared for client): {summary}")
            print(f"⏱️ Total orchestration time: {total_time:.4f} seconds")
            print("=" * 60)

            return pipeline_pb2.PipelineResponse(total_time=total_time, summary=summary)

        except Exception as e:
            print(f"\nERROR: An error occurred during pipeline orchestration: {e}")
            # You can also return an error to the gRPC client here if needed
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Pipeline failed: {e}')
            return pipeline_pb2.PipelineResponse()


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
pipeline_pb2_grpc.add_MasterServiceServicer_to_server(MasterServicer(), server)
server.add_insecure_port('[::]:50055')
server.start()
print("MasterService running on port 50055")
server.wait_for_termination()