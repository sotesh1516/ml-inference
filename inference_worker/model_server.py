import torch
import threading
from torchvision.models import MobileNetV3
from PIL import image

class ModelSingleton: 

    def __new__(cls):
        pass

    def _load_model():
        pass

    def _infer():
        pass