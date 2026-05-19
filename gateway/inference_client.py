import asyncio
import grpc
from concurrent import futures
from protobuf_generated.inference import inference_pb2_grpc, inference_pb2

"""
stub is another name for client, it provides the methods defined in the gRPC service

The Stub is a fully functional object that already knows how to translate your function 
calls into binary network packets. Just use it.
"""
class InferenceClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.aio.insecure_channel(f"{host}:{port}")
        self.stub = inference_pb2_grpc.InferenceProducerStub(self.channel)

    async def predict(self, input_data: bytes):
        request = inference_pb2.PredictRequest(image=input_data)
        rpc_response = await self.stub.Predict(request)
        response_list = list(rpc_response.output)
        prediction_index = response_list.index(max(response_list))
        print(prediction_index)
        return prediction_index


if __name__ == "__main__":
    client = InferenceClient()
    # Example input data, replace with actual data as needed
    input_data = '../car.jpg'  # Placeholder for image bytes

    with open(input_data, 'rb') as f:
        image_bytes = f.read()

    prediction = asyncio.run(client.predict(image_bytes))