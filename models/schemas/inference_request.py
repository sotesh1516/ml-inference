import asyncio
from pydantic import BaseModel

class InferenceRequest(BaseModel):
    image: bytes
    uuid: str = None
