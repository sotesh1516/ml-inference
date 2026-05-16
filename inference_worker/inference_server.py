import grpc
import asyncio
import uuid
from typing import AsyncGenerator
from concurrent import futures
from protobuf_generated.inference import inference_pb2_grpc, inference_pb2
from .model_server import model_predict
from .task_queue import TaskQueue
from ..models.schemas.inference_request import InferenceRequest


class InferenceProducerServicer(inference_pb2_grpc.InferenceProducerServicer):
    """
    request: actual input data for ml inference
    context: information about RPC environment and control its lifecycle. It represents the life of a single RPC call, one client, one call, one context.
    """

    def __init__(self, task_queue: TaskQueue):
        super().__init__()
        self.task_queue = task_queue

    async def Predict(
        self, request: inference_pb2.PredictRequest, context: grpc.aio.ServicerContext
    ) -> inference_pb2.PredictResponse:
        image_bytes = request.image

        # creat an inference request object and add it to the task queue for processing by the worker
        task_future = asyncio.Future()
        id = str(uuid.uuid4())
        inference_request = InferenceRequest(
            image=image_bytes, future=task_future, uuid=id
        )
        self.task_queue.add_task(inference_request)

        prediction = await task_future
        # prediction = model_predict(image_bytes)
        print(
            f"Prediction from model: {prediction[:5]}..."
        )  # Print first 5 values for brevity
        response = inference_pb2.PredictResponse(output=prediction)
        return response


class InferenceConsumerServicer(inference_pb2_grpc.InferenceConsumerServicer):
    def __init__(self, task_queue: TaskQueue):
        super().__init__()
        self.task_queue = task_queue
        self.task_mapping = {}  # quick lookup for task_id to future mapping

    async def GetTaskFromQueue(
        self, context: grpc.aio.ServicerContext
    ) -> AsyncGenerator[inference_pb2.InferenceTask, None]: #ensures the yield inside the loop is the return mechanism
        while True:

            if context.cancelled():
                print("Client cancelled the request.")
                break

            if not self.task_queue.is_empty():
                inference_request = self.task_queue.get_task()
                task_id = inference_request.uuid
                self.task_mapping[task_id] = (
                    inference_request.future
                )  # Store the future in the mapping
                inference_task = inference_pb2.InferenceTask(
                    task_id=task_id, image=inference_request.image
                )
                yield inference_task


"""
start up a gRPC server for clients to use the service

gRPC.server takes in futures.ThreadPoolExecutor, a high-level interface for asyncly executing functions using threads
"""


def serve():
    queue = TaskQueue()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inference_pb2_grpc.add_InferenceProducerServicer_to_server(
        InferenceProducerServicer(queue), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
