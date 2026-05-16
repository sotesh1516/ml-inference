import asyncio

from .schemas.inference_request import InferenceRequest

'''
TaskQueue is a simple wrapper around asyncio.Queue to manage inference tasks in the Inference Worker.
It facilitates communication between concurrent coroutines(async functions that can pause and resume easily) that produce and consume inference tasks.
'''
class TaskQueue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def add_task(self, task: InferenceRequest):
        await self.queue.put(task)

    async def get_task(self):
        return await self.queue.get()
    
    def is_empty(self):
        return self.queue.empty()
    
    def size(self):
        return self.queue.qsize()