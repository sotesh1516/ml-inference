from fastapi import FastAPI, File, UploadFile

from models.schemas.gateway_input_data import InputData
from gateway.inference_client import InferenceClient

app = FastAPI()

#tcp handshake is expensive, so we create the client once and reuse it for all requests
grpc_client = InferenceClient()

@app.get("/")
def run_server():
    return {"message": "Hello world!"}

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    contents = await image.read()
    prediction_index = await grpc_client.predict(contents)
    return {"prediction_index": prediction_index}