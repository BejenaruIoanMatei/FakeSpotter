# fake_spotter_utils.py - Versiunea simplificată

import torch
import numpy as np
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os

# === CONFIGURARE ===
MODEL_PATH = '../classifier/models/inception_fake_spotter_binary.pth'

class_labels = {
    0: "Real",
    1: "Fake"
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === ÎNCĂRCARE MODEL ===
def load_inception_model():
    inception = models.inception_v3(weights=None, aux_logits=False)
    inception.fc = nn.Linear(inception.fc.in_features, 2)
    
    state_dict = torch.load(MODEL_PATH, map_location=device)
    # Filtrează weights-urile auxiliare dacă există
    filtered_state_dict = {k: v for k, v in state_dict.items() if 'AuxLogits' not in k}
    
    inception.load_state_dict(filtered_state_dict, strict=False)
    inception = inception.to(device)
    inception.eval()
    return inception

# Încarcă modelul o singură dată
model = load_inception_model()

# === TRANSFORMARE IMAGINE ===
transform = transforms.Compose([
    transforms.Resize((299, 299)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# === CLASIFICARE IMAGINE ===
def classify_image(img_path):
    try:
        # Încarcă imaginea
        image_pil = Image.open(img_path).convert("RGB")
        input_tensor = transform(image_pil).unsqueeze(0).to(device)
        
        # Predicție
        with torch.no_grad():
            outputs = model(input_tensor)
            if isinstance(outputs, tuple):
                outputs = outputs[0]
        
        # Calculează probabilitățile
        probs = torch.nn.functional.softmax(outputs, dim=1)
        predicted_index = torch.argmax(probs, dim=1).item()
        label = class_labels[predicted_index]
        confidence = float(probs[0][predicted_index])
        
        return label, confidence
        
    except Exception as e:
        print(f"Error: {e}")
        return "error", 0.0