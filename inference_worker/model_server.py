import torch
import threading
from torchvision.models import mobilenet_v3_large, MobileNet_V3_Large_Weights
from torchvision import transforms
from PIL import Image
from typing import List

class ModelSingleton: 
    #need to consider locks and handling a single instance
    def __new__(cls):
        pass

    def _load_model():
        pass

    def _infer():
        pass

model = mobilenet_v3_large(weights=MobileNet_V3_Large_Weights.IMAGENET1K_V2)
model.eval()

def model_predict(image: bytes) -> List[float]:
    #standard imagenet transform
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0) # Add batch dimension (1, 3, 224, 224)

    with torch.no_grad():
        output = model(input_batch)

    output.detach().cpu().numpy().flatten().tolist() #convert to a regular python list

    return output