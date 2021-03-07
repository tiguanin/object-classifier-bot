import json
import os

import torch
from PIL import Image
from efficientnet_pytorch import EfficientNet
from torchvision import transforms

import src


class EfficientClassifier:
    MODEL_NAME = 'efficientnet-b7'
    IMAGE_SIZE = EfficientNet.get_image_size(MODEL_NAME)  # 224
    model = None
    labels_map = None

    def __init__(self):
        self._initialize_model()

    def _initialize_model(self):
        path = os.path.dirname(src.__file__)
        labels_map = json.load(open(path + '/labels_map.txt'))
        self.labels_map = [labels_map[str(i)] for i in range(1000)]
        self.model = EfficientNet.from_pretrained(self.MODEL_NAME)
        self.model.eval()

    def _preprocess_image(self, image):
        tfms = transforms.Compose([transforms.Resize(self.IMAGE_SIZE), transforms.CenterCrop(self.IMAGE_SIZE),
                                   transforms.ToTensor(),
                                   transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]), ])
        image = tfms(image).unsqueeze(0)
        return image

    def predict(self, img_path):
        image = Image.open(img_path)
        preprocessed_image = self._preprocess_image(image)

        with torch.no_grad():
            logits = self.model(preprocessed_image)
        preds = torch.topk(logits, k=5).indices.squeeze(0).tolist()

        print('-----')
        for idx in preds:
            label = self.labels_map[idx]
            prob = torch.softmax(logits, dim=1)[0, idx].item()
            print('{:<75} ({:.2f}%)'.format(label, prob * 100))
