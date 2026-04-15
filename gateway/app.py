from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def run_server():
    return {"message": "Hello world!"}