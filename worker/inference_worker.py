import torch
import numpy
import threading
from torchvision.models import mobilenet_v3_large, MobileNet_V3_Large_Weights
from torchvision import transforms
from PIL import Image
from io import BytesIO
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

    try:
        img = Image.open(BytesIO(image)).convert('RGB') # decode bytes -> RGB PIL image
        input_tensor = preprocess(img) # tensor shape (3, H, W)
        input_batch = input_tensor.unsqueeze(0) # Add batch dimension (1, 3, 224, 224)

        with torch.no_grad():
            output = model(input_batch)

        prediction_list =output.detach().cpu().numpy().flatten().tolist() #convert to a regular python list

        return prediction_list
    except Exception as e:
        print("Reaching model prediction error handling")
        print(f"Error during model prediction: {e}")
        return []   