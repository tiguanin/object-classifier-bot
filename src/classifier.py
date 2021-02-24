import json

import torch
from PIL import Image
from efficientnet_pytorch import EfficientNet
from torchvision import transforms

MODEL_NAME = 'efficientnet-b7'
image_size = EfficientNet.get_image_size(MODEL_NAME)  # 224

img = Image.open('../panda.jpg')

# Preprocess image
tfms = transforms.Compose([transforms.Resize(image_size), transforms.CenterCrop(image_size),
                           transforms.ToTensor(),
                           transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]), ])
img = tfms(img).unsqueeze(0)

# Load class names
labels_map = json.load(open('../labels_map.txt'))
labels_map = [labels_map[str(i)] for i in range(1000)]

# Classify with EfficientNet
# WEIGHTS_PATH = '../efficientnet-b7-dcc49843.pth'

model = EfficientNet.from_pretrained(MODEL_NAME)

model.eval()
with torch.no_grad():
    logits = model(img)
preds = torch.topk(logits, k=5).indices.squeeze(0).tolist()

print('-----')
for idx in preds:
    label = labels_map[idx]
    prob = torch.softmax(logits, dim=1)[0, idx].item()
    print('{:<75} ({:.2f}%)'.format(label, prob * 100))

