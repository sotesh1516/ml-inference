import grpc
from concurrent import futures
from protobuf_generated.inference import inference_pb2_grpc, inference_pb2
from .model_server import model_predict


class InferenceServicer(inference_pb2_grpc.InferenceServicer):
    """
    request: actual input data for ml inference
    context: information about RPC environment and control its lifecycle
    """

    def Predict(
        self, request: inference_pb2.PredictRequest, context: grpc.ServicerContext
    ) -> inference_pb2.PredictResponse:
        image_bytes = request.image
        prediction = model_predict(image_bytes)
        print(f"Prediction from model: {prediction[:5]}...")  # Print first 5 values for brevity
        response = inference_pb2.PredictResponse(output=prediction)
        # response.output.extend(prediction)  # since PredictResponse is a pre-allocated C based structure
        return response


"""
start up a gRPC server for clients to use the service

gRPC.server takes in futures.ThreadPoolExecutor, a high-level interface for asyncly executing functions using threads
"""


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inference_pb2_grpc.add_InferenceServicer_to_server(InferenceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
