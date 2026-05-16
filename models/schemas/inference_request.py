import asyncio
from pydantic import BaseModel

class InferenceRequest(BaseModel):
    image: bytes
    future: asyncio.Future
    uuid: str = None
