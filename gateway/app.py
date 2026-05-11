from fastapi import FastAPI

from models.schemas.input_data import InputData
from gateway.inference_client import InferenceClient

app = FastAPI()

#tcp handshake is expensive, so we create the client once and reuse it for all requests
grpc_client = InferenceClient()

@app.get("/")
def run_server():
    return {"message": "Hello world!"}

@app.post("/predict")
def predict(input_data: InputData):
    prediction_index = grpc_client.predict(input_data.image)
    return {"prediction_index": prediction_index}