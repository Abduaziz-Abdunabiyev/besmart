
import os
import tempfile
import subprocess
import torch
from PIL import Image
import whisper
from transformers import pipeline, CLIPProcessor, CLIPModel, AutoTokenizer

# Load models
whisper_model = whisper.load_model("medium")

# Text classifiers
educational_model = "typeform/distilbert-base-uncased-mnli"  # Can simulate intent (e.g., is this educational?)
educational_tokenizer = AutoTokenizer.from_pretrained(educational_model)
educational_classifier = pipeline("text-classification", model=educational_model, tokenizer=educational_tokenizer)

# Image model (CLIP)
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Concepts to match for visuals
educational_concepts = ["science", "education", "lecture", "classroom", "coding", "learning", "technology"]

# Extract keyframes (1 frame every 5 seconds)
def extract_keyframes(video_path, output_folder, interval=5):
    os.makedirs(output_folder, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-i", video_path,
        "-vf", f"fps=1/{interval}",
        os.path.join(output_folder, "frame_%04d.jpg"),
        "-hide_banner", "-loglevel", "error"
    ], check=True)

def analyze_images(folder_path):
    results = []
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.lower().endswith(".jpg"):
            image_path = os.path.join(folder_path, file_name)
            image = Image.open(image_path)
            inputs = clip_processor(text=educational_concepts, images=image, return_tensors="pt", padding=True)
            outputs = clip_model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            top_score, top_idx = torch.max(probs, dim=1)
            matched_concept = educational_concepts[top_idx.item()]
            results.append((file_name, matched_concept, top_score.item()))
    return results

def is_educational_text(text):
    results = educational_classifier(text)
    top = max(results, key=lambda x: x["score"])
    return top["label"], top["score"]

def is_video_appropriate(video_path):
    tmp_audio_path = None
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_audio_path = os.path.join(tmpdir, "audio.wav")
        tmp_frames_dir = os.path.join(tmpdir, "frames")
        
        # Step 1: Extract audio
        subprocess.run([
            "ffmpeg", "-i", video_path,
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
            tmp_audio_path, "-y"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Step 2: Transcribe
        result = whisper_model.transcribe(tmp_audio_path, language="en")
        transcript = result.get("text", "").strip()
        if not transcript:
            return False, "Transcript is empty", ""

        # Step 3: Analyze text
        label, score = is_educational_text(transcript)
        educational_pass = ("entailment" in label.lower()) and score > 0.75

        # Step 4: Extract keyframes
        extract_keyframes(video_path, tmp_frames_dir)

        # Step 5: Analyze images
        image_results = analyze_images(tmp_frames_dir)
        top_images = [r for r in image_results if r[2] > 0.5]

        # Decide
        if educational_pass and top_images:
            return True, f"✅ Passed. Educational content detected in text and visuals.\nTranscript intent: {label} ({score:.2f})\nVisual match: {top_images[:2]}", transcript
        else:
            return False, f"🚫 Rejected.\nTranscript intent: {label} ({score:.2f})\nVisual evidence insufficient.", transcript

# CLI
if __name__ == "__main__":
    path = input("Enter video path: ").strip()
    if not os.path.exists(path):
        print("❌ File not found.")
    else:
        ok, msg, text = is_video_appropriate(path)
        print("\n🔎 Result:", msg)
        print("\n📝 Transcript:", text)
