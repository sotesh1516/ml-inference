import grpc
import asyncio
import uuid
from typing import AsyncGenerator
from concurrent import futures
from protobuf_generated.inference import inference_pb2_grpc, inference_pb2
from .model_server import model_predict
from .task_queue import TaskQueue
from models.schemas.inference_request import InferenceRequest


class InferenceProducerServicer(inference_pb2_grpc.InferenceProducerServicer):
    """
    request: actual input data for ml inference
    context: information about RPC environment and control its lifecycle. It represents the life of a single RPC call, one client, one call, one context.
    """

    def __init__(self, task_queue: TaskQueue, task_mapping: dict):
        super().__init__()
        self.task_queue = task_queue
        self.task_mapping = task_mapping  

    async def Predict(
        self, request: inference_pb2.PredictRequest, context: grpc.aio.ServicerContext
    ) -> inference_pb2.PredictResponse:
        image_bytes = request.image

        # creat an inference request object and add it to the task queue for processing by the worker
        task_future = asyncio.Future()
        id = str(uuid.uuid4())
        self.task_mapping[id] = task_future
        inference_request = InferenceRequest(
            image=image_bytes, uuid=id
        )
        await self.task_queue.add_task(inference_request)
        print(f"Added task with id {id} to the queue. Queue size is now {self.task_queue.size()}.")
        single_task = await self.task_queue.get_task()
        print(single_task.uuid)
        prediction = await task_future
        # prediction = model_predict(image_bytes)
        print(
            f"Prediction from model: {prediction[:5]}..."
        )  # Print first 5 values for brevity
        response = inference_pb2.PredictResponse(output=prediction)
        return response


class InferenceConsumerServicer(inference_pb2_grpc.InferenceConsumerServicer):
    def __init__(self, task_queue: TaskQueue, task_mapping: dict):
        super().__init__()
        self.task_queue = task_queue
        self.task_mapping = task_mapping

    """
    Maintain a long lived http/2 connection with api gateway
    """
    async def GetTaskFromQueue(
        self, context: grpc.aio.ServicerContext
    ) -> AsyncGenerator[
        inference_pb2.InferenceTask, None
    ]:  # ensures the yield inside the loop is the return mechanism
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
    Inference worker(ml model) makes a post request to this endpoint with the inference result
    """
    async def ReturnTask(
        self, request: inference_pb2.InferenceResult, context: grpc.aio.ServicerContext
    ):
        task_id = request.task_id
        prediction = request.output
        if task_id in self.task_mapping:
            future = self.task_mapping[task_id]
            future.set_result(prediction)  
            del self.task_mapping[task_id] 
        else:
            print(f"Received result for unknown task_id: {task_id}")





"""
start up a gRPC server for clients to use the service

gRPC.server takes in futures.ThreadPoolExecutor, a high-level interface for asyncly executing functions using threads
"""


async def serve():
    queue = TaskQueue()
    task_mapping = {} 
    server = grpc.aio.server()
    inference_pb2_grpc.add_InferenceProducerServicer_to_server(
        InferenceProducerServicer(queue, task_mapping), server
    )
    inference_pb2_grpc.add_InferenceConsumerServicer_to_server(
        InferenceConsumerServicer(queue, task_mapping), server
    )
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("Server started on port 50051...")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
