import os
from transformers import BlipProcessor, BlipForConditionalGeneration

# Set the cache directory inside the script
os.environ['TRANSFORMERS_CACHE'] = r'D:\Python Django\pythonfiles\transformers_cache'

# Load the model with the specified cache location
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Continue with the rest of your code...
