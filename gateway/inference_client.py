import grpc
from concurrent import futures
from ..protobuf_generated import inference_pb2_grpc, inference_pb2

"""
stub is another name for client, it is provides the methods defined in the gRPC service
"""
channel = grpc.insecure_channel("localhost:50051")
stub = inference_pb2_grpc.InferenceStub(channel)

