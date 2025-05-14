
from PIL import Image
import torch
from torchvision import transforms
from transformers import CLIPProcessor, CLIPModel
import os

# Load model once (expensive, so do it globally)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Define labels you want to detect
labels = ["educational content", "science", "technology", "meme", "random photo", "offensive", "irrelevant", "clickbait"]
positive_labels = {"educational content", "science", "technology"}

def is_image_meaningful(image_path: str) -> bool:
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1).detach().cpu().numpy()[0]
        
        best_match = labels[probs.argmax()]
        print(f"CLIP detected: {best_match} ({probs.max()*100:.2f}%)")
        return best_match in positive_labels
    except Exception as e:
        print("Image filtering error:", e)
        return False
