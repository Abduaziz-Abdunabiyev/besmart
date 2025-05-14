
# import os
# import tempfile
# import subprocess
# import whisper
# import torch
# import re
# from transformers import pipeline, AutoTokenizer

# # Load Whisper model for transcription
# whisper_model = whisper.load_model("medium")

# # Load Offensive Language Detection Model
# offensive_model = "cardiffnlp/twitter-roberta-base-offensive"
# offensive_tokenizer = AutoTokenizer.from_pretrained(offensive_model)
# offensive_classifier = pipeline("text-classification", model=offensive_model, tokenizer=offensive_tokenizer, return_all_scores=True)

# # Load Toxicity Detection Model
# toxic_model = "unitary/toxic-bert"
# toxic_tokenizer = AutoTokenizer.from_pretrained(toxic_model)
# toxic_classifier = pipeline("text-classification", model=toxic_model, tokenizer=toxic_tokenizer, return_all_scores=True)

# # Load Hate Speech Detection Model
# hate_model = "Hate-speech-CNERG/bert-base-uncased-hatexplain"
# hate_tokenizer = AutoTokenizer.from_pretrained(hate_model)
# hate_classifier = pipeline("text-classification", model=hate_model, tokenizer=hate_tokenizer, return_all_scores=True)

# # Load Emotion Detection Model
# emotion_model = "j-hartmann/emotion-english-distilroberta-base"
# emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model)
# emotion_classifier = pipeline("text-classification", model=emotion_model, tokenizer=emotion_tokenizer, return_all_scores=True)

# # Define disallowed keywords and phrases
# disallowed_keywords = {
#     'hate', 'violence', 'sexual', 'nudity', 'drugs', 'terrorism', 'racism', 'murder',
#     'bomb', 'suicide', 'onlyfans', 'strip', 'nude', 'kill', 'sex', 'porn', 'abuse',
#     'weapon', 'knife', 'gun', 'rape', 'blood', 'dead', 'death', 'extremist', 'hostage',
#     'explosion', 'torture', 'erotic', 'orgasm', 'xxx', 'slut', 'fetish', 'shooting',
#     'molest', 'masturbation', 'genocide', 'incest', 'cocaine', 'meth', 'anal', 'bdsm',
#     'rape scene', 'uncensored', 'snuff', 'scream', 'isis', 'behead', 'decapitate'
# }

# semantic_phrases = {
#     "i hate", "i will kill", "let's bomb", "doing drugs", "committing suicide",
#     "showing body", "show my body", "start onlyfans", "join isis", "get naked",
#     "hardcore porn", "rape scene", "i’m naked", "selling nudes", "porn site"
# }

# # Function to analyze emotions
# def analyze_emotion(text):
#     results = emotion_classifier(text)
#     top = max(results[0], key=lambda x: x["score"])
#     return top["label"], top["score"]

# # Main function to evaluate video content
# def is_video_appropriate(video_path):
#     tmp_audio_path = None
#     try:
#         # Extract audio from video
#         with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
#             tmp_audio_path = tmp_audio.name
#         subprocess.run([
#             "ffmpeg", "-i", video_path,
#             "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
#             tmp_audio_path, "-y"
#         ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

#         # Transcribe audio
#         result = whisper_model.transcribe(tmp_audio_path, language="en")
#         transcript = result.get("text", "").strip()
#         if not transcript:
#             return False, "⚠️ Empty transcript.", ""

#         transcript_lower = transcript.lower()

#         # Analyze with offensive language model
#         offensive_results = offensive_classifier(transcript)
#         offensive_label = max(offensive_results[0], key=lambda x: x["score"])
#         offensive_issue = offensive_label["label"].lower() != "not-offensive" and offensive_label["score"] > 0.6

#         # Analyze with toxicity model
#         toxic_results = toxic_classifier(transcript)
#         toxic_label = max(toxic_results[0], key=lambda x: x["score"])
#         toxic_issue = toxic_label["label"].lower() != "non-toxic" and toxic_label["score"] > 0.6

#         # Analyze with hate speech model
#         hate_results = hate_classifier(transcript)
#         hate_label = max(hate_results[0], key=lambda x: x["score"])
#         hate_issue = hate_label["label"].lower() != "normal" and hate_label["score"] > 0.6

#         # Analyze emotions
#         emotion_label, emotion_score = analyze_emotion(transcript)
#         emotion_issue = emotion_label.lower() in {"anger", "disgust", "fear"} and emotion_score > 0.6

#         # Check for disallowed keywords and phrases
#         keyword_violations = [kw for kw in disallowed_keywords if kw in transcript_lower]
#         phrase_violations = [ph for ph in semantic_phrases if ph in transcript_lower]

#         # Compile issues
#         issues = []
#         if offensive_issue:
#             issues.append(f"Offensive Language Detected: {offensive_label['label']} ({offensive_label['score']:.2f})")
#         if toxic_issue:
#             issues.append(f"Toxic Content Detected: {toxic_label['label']} ({toxic_label['score']:.2f})")
#         if hate_issue:
#             issues.append(f"Hate Speech Detected: {hate_label['label']} ({hate_label['score']:.2f})")
#         if emotion_issue:
#             issues.append(f"Negative Emotion Detected: {emotion_label} ({emotion_score:.2f})")
#         if keyword_violations:
#             issues.append(f"Disallowed Keywords Found: {', '.join(keyword_violations)}")
#         if phrase_violations:
#             issues.append(f"Disallowed Phrases Found: {', '.join(phrase_violations)}")

#         if issues:
#             return False, "🚫 Violations Detected:\n- " + "\n- ".join(issues), transcript

#         return True, "✅ Content is clean by all models.", transcript

#     except Exception as e:
#         return False, f"❌ Error: {e}", ""

#     finally:
#         if tmp_audio_path and os.path.exists(tmp_audio_path):
#             os.remove(tmp_audio_path)

# # CLI for testing
# if __name__ == "__main__":
#     video_path = input("🎬 Enter path to your video file: ").strip()
#     ok, msg, text = is_video_appropriate(video_path)
#     print("\n📝 Transcript:\n", text)
#     print("\n🔎 Result:\n", msg)

#===================================================================

# import os
# import tempfile
# import subprocess
# import whisper
# import torch
# from transformers import pipeline, AutoTokenizer

# # Use GPU if available
# device = 0 if torch.cuda.is_available() else -1

# # Load Whisper model on GPU if available
# whisper_model = whisper.load_model("medium").to("cuda" if torch.cuda.is_available() else "cpu")

# # Load Offensive Language Detection Model
# offensive_model = "cardiffnlp/twitter-roberta-base-offensive"
# offensive_tokenizer = AutoTokenizer.from_pretrained(offensive_model)
# offensive_classifier = pipeline(
#     "text-classification",
#     model=offensive_model,
#     tokenizer=offensive_tokenizer,
#     return_all_scores=True,
#     device=device
# )

# # Load Toxicity Detection Model
# toxic_model = "unitary/toxic-bert"
# toxic_tokenizer = AutoTokenizer.from_pretrained(toxic_model)
# toxic_classifier = pipeline(
#     "text-classification",
#     model=toxic_model,
#     tokenizer=toxic_tokenizer,
#     return_all_scores=True,
#     device=device
# )

# # Load Hate Speech Detection Model
# hate_model = "Hate-speech-CNERG/bert-base-uncased-hatexplain"
# hate_tokenizer = AutoTokenizer.from_pretrained(hate_model)
# hate_classifier = pipeline(
#     "text-classification",
#     model=hate_model,
#     tokenizer=hate_tokenizer,
#     return_all_scores=True,
#     device=device
# )

# # Load Emotion Detection Model
# emotion_model = "j-hartmann/emotion-english-distilroberta-base"
# emotion_tokenizer = AutoTokenizer.from_pretrained(emotion_model)
# emotion_classifier = pipeline(
#     "text-classification",
#     model=emotion_model,
#     tokenizer=emotion_tokenizer,
#     return_all_scores=True,
#     device=device
# )

# # Define disallowed keywords and phrases
# disallowed_keywords = {
#     'hate', 'violence', 'sexual', 'nudity', 'drugs', 'terrorism', 'racism', 'murder',
#     'bomb', 'suicide', 'onlyfans', 'strip', 'nude', 'kill', 'sex', 'porn', 'abuse',
#     'weapon', 'knife', 'gun', 'rape', 'blood', 'dead', 'death', 'extremist', 'hostage',
#     'explosion', 'torture', 'erotic', 'orgasm', 'xxx', 'slut', 'fetish', 'shooting',
#     'molest', 'masturbation', 'genocide', 'incest', 'cocaine', 'meth', 'anal', 'bdsm',
#     'rape scene', 'uncensored', 'snuff', 'scream', 'isis', 'behead', 'decapitate'
# }

# semantic_phrases = {
#     "i hate", "i will kill", "let's bomb", "doing drugs", "committing suicide",
#     "showing body", "show my body", "start onlyfans", "join isis", "get naked",
#     "hardcore porn", "rape scene", "i’m naked", "selling nudes", "porn site"
# }

# # Function to analyze emotions
# def analyze_emotion(text):
#     results = emotion_classifier(text)
#     top = max(results[0], key=lambda x: x["score"])
#     return top["label"], top["score"]

# # Main function to evaluate video content
# def is_video_appropriate(video_path, cartoon_mode=False):
#     tmp_audio_path = None
#     try:
#         # Extract audio from video
#         with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
#             tmp_audio_path = tmp_audio.name
#         subprocess.run([
#             "ffmpeg", "-i", video_path,
#             "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
#             tmp_audio_path, "-y"
#         ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

#         # Transcribe audio
#         result = whisper_model.transcribe(tmp_audio_path, language="en")
#         transcript = result.get("text", "").strip()
#         if not transcript:
#             return False, "⚠️ Empty transcript.", ""

#         transcript_lower = transcript.lower()
#         threshold = 0.7 if cartoon_mode else 0.6

#         # Analyze with offensive language model
#         offensive_results = offensive_classifier(transcript)
#         offensive_label = max(offensive_results[0], key=lambda x: x["score"])
#         offensive_issue = offensive_label["label"].lower() != "not-offensive" and offensive_label["score"] > threshold

#         # Analyze with toxicity model
#         toxic_results = toxic_classifier(transcript)
#         toxic_label = max(toxic_results[0], key=lambda x: x["score"])
#         toxic_issue = toxic_label["label"].lower() != "non-toxic" and toxic_label["score"] > threshold

#         # Analyze with hate speech model
#         hate_results = hate_classifier(transcript)
#         hate_label = max(hate_results[0], key=lambda x: x["score"])
#         hate_issue = hate_label["label"].lower() != "normal" and hate_label["score"] > threshold

#         # Analyze emotions
#         emotion_label, emotion_score = analyze_emotion(transcript)
#         emotion_issue = emotion_label.lower() in {"anger", "disgust", "fear"} and emotion_score > (0.8 if cartoon_mode else 0.6)

#         # Check for disallowed keywords and phrases
#         keyword_violations = []
#         phrase_violations = []

#         if not cartoon_mode:
#             keyword_violations = [kw for kw in disallowed_keywords if kw in transcript_lower]
#             phrase_violations = [ph for ph in semantic_phrases if ph in transcript_lower]

#         # Compile issues
#         issues = []
#         if offensive_issue:
#             issues.append(f"Offensive Language Detected: {offensive_label['label']} ({offensive_label['score']:.2f})")
#         if toxic_issue:
#             issues.append(f"Toxic Content Detected: {toxic_label['label']} ({toxic_label['score']:.2f})")
#         if hate_issue:
#             issues.append(f"Hate Speech Detected: {hate_label['label']} ({hate_label['score']:.2f})")
#         if emotion_issue:
#             issues.append(f"Negative Emotion Detected: {emotion_label} ({emotion_score:.2f})")
#         if keyword_violations:
#             issues.append(f"Disallowed Keywords Found: {', '.join(keyword_violations)}")
#         if phrase_violations:
#             issues.append(f"Disallowed Phrases Found: {', '.join(phrase_violations)}")

#         if issues:
#             return False, "🚫 Violations Detected:\n- " + "\n- ".join(issues), transcript

#         return True, "✅ Content is clean by all models.", transcript

#     except Exception as e:
#         return False, f"❌ Error: {e}", ""

#     finally:
#         if tmp_audio_path and os.path.exists(tmp_audio_path):
#             os.remove(tmp_audio_path)

# # CLI for testing
# if __name__ == "__main__":
#     video_path = input("🎬 Enter path to your video file: ").strip()
#     is_cartoon = input("🎨 Is this a cartoon/animated video? (y/n): ").strip().lower() == "y"
#     ok, msg, text = is_video_appropriate(video_path, cartoon_mode=is_cartoon)
#     print("\n📝 Transcript:\n", text)
#     print("\n🔎 Result:\n", msg)

#===================================================================

# import os
# import subprocess
# import tempfile
# import cv2
# from PIL import Image
# import torch
# from transformers import CLIPProcessor, CLIPModel
# import whisper

# # Device setup
# device = "cuda" if torch.cuda.is_available() else "cpu"

# # Load Whisper and CLIP
# whisper_model = whisper.load_model("small").to(device)
# clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
# clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# # Labels and keywords
# labels = ["educational content", "science", "technology", "meme", "random photo", "offensive", "irrelevant", "clickbait"]
# approved_labels = {"educational content", "science", "technology"}
# keywords = {"education", "learning", "university", "science", "technology", "ai", "physics", "biology", "robot", "research"}

# def extract_middle_frame(video_path):
#     cap = cv2.VideoCapture(video_path)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     if total_frames == 0:
#         return None
#     target_frame = total_frames // 2
#     cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
#     success, frame = cap.read()
#     cap.release()
#     if success:
#         tmp_path = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
#         cv2.imwrite(tmp_path, frame)
#         return tmp_path
#     return None

# def classify_frame_with_clip(image_path):
#     try:
#         image = Image.open(image_path).convert("RGB")
#         inputs = clip_processor(text=labels, images=image, return_tensors="pt", padding=True).to(device)
#         outputs = clip_model(**inputs)
#         probs = outputs.logits_per_image.softmax(dim=1).detach().cpu().numpy()[0]
#         best_label = labels[probs.argmax()]
#         confidence = probs.max() * 100
#         print(f"🖼️ Image label: {best_label} ({confidence:.1f}%)")
#         return best_label in approved_labels
#     except Exception as e:
#         print("⚠️ CLIP error:", e)
#         return False

# def is_video_appropriate(video_path):
#     audio_temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
#     transcript = ""
#     try:
#         # 1. Extract audio
#         subprocess.run([
#             "ffmpeg", "-i", video_path,
#             "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
#             audio_temp, "-y"
#         ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

#         # 2. Transcribe
#         result = whisper_model.transcribe(audio_temp, language="en")
#         transcript = result.get("text", "").lower().strip()

#         print("📝 Transcription:", transcript[:150], "..." if len(transcript) > 150 else "")

#         # 3. Check keywords
#         found_keywords = {word for word in keywords if word in transcript}
#         audio_ok = len(found_keywords) >= 2  # stricter threshold
#         print(f"🔑 Keywords found: {found_keywords}")

#         # 4. Check frame
#         frame_path = extract_middle_frame(video_path)
#         image_ok = classify_frame_with_clip(frame_path) if frame_path else False
#         if frame_path:
#             os.remove(frame_path)

#         # 5. Final decision
#         if audio_ok and image_ok:
#             return True, "✅ Approved: Educational content.", transcript
#         return False, "🚫 Rejected: Not clearly educational.", transcript

#     except Exception as e:
#         return False, f"❌ Error: {e}", transcript

#     finally:
#         if os.path.exists(audio_temp):
#             os.remove(audio_temp)

# # CLI test
# if __name__ == "__main__":
#     path = input("🎬 Enter video path: ").strip()
#     ok, msg, _ = is_video_appropriate(path)
#     print("\n🔍 Result:", msg)


#================================



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


# ==============================================================


# import os
# import tempfile
# import subprocess
# import torch
# from PIL import Image
# import whisper
# from transformers import pipeline, CLIPProcessor, CLIPModel, AutoTokenizer

# # Load models
# whisper_model = whisper.load_model("medium")

# # Text classifiers
# educational_model = "typeform/distilbert-base-uncased-mnli"  # Can simulate intent (e.g., is this educational?)
# educational_tokenizer = AutoTokenizer.from_pretrained(educational_model)
# educational_classifier = pipeline("text-classification", model=educational_model, tokenizer=educational_tokenizer)

# # Image model (CLIP)
# clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
# clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# # Expanded Concepts to match for visuals and text classification
# sport_concepts = [
#     "football", "basketball", "soccer", "tennis", "sports", "athlete", "competition", 
#     "Olympics", "world cup", "baseball", "rugby", "volleyball", "swimming", "boxing", 
#     "track and field", "golf", "cricket", "fitness", "workout", "sportsmanship", 
#     "sports event", "team", "championship", "coach", "stadium", "tournament"
# ]
# news_concepts = [
#     "news", "headline", "report", "current events", "journalism", "broadcast", "press", 
#     "media", "breaking news", "headline news", "investigation", "news report", "coverage", 
#     "story", "correspondent", "interview", "editorial", "press release", "press conference", 
#     "news outlet", "politics", "economy", "government", "world news", "local news"
# ]
# education_concepts = [
#     "science", "education", "lecture", "classroom", "coding", "learning", "technology", 
#     "math", "history", "biology", "physics", "geography", "literature", "chemistry", 
#     "research", "education system", "homework", "assignment", "studying", "college", "university", 
#     "degree", "online learning", "curriculum", "academic", "student", "teacher", "lesson"
# ]
# useful_content_concepts = [
#     "how-to", "tutorial", "guide", "tips", "life hacks", "useful information", "DIY", 
#     "step-by-step", "life tips", "productivity", "self-improvement", "organization", 
#     "time management", "money-saving", "career advice", "health tips", "work from home", 
#     "personal finance", "hobby", "tech tips", "fitness", "recipe", "meal prep", "gardening", 
#     "home improvement"
# ]
# cartoon_concepts = [
#     "cartoon", "animation", "kids", "children", "fun", "comedy", "cartoon series", 
#     "funny", "animated movie", "superhero", "cartoon character", "family-friendly", 
#     "animation series", "adventure", "children's show", "animated film", "comic", 
#     "animated TV show", "cartoon network", "cartoonist", "cartoon drawing", "animation movie"
# ]

# technology_concepts = [
#     "technology", "innovation", "AI", "machine learning", "robotics", "future", "gadget", 
#     "automation", "data science", "blockchain", "internet of things", "5G", "cybersecurity", 
#     "tech news", "smartphone", "wearable technology", "software", "hardware", "programming", 
#     "app development", "virtual reality", "augmented reality", "cloud computing"
# ]

# health_wellness_concepts = [
#     "health", "fitness", "wellness", "nutrition", "exercise", "mental health", "workout", 
#     "yoga", "meditation", "healthy eating", "diet", "weight loss", "stress management", 
#     "self-care", "personal growth", "mindfulness", "sleep", "bodybuilding", "mental well-being", 
#     "hydration", "fitness routine", "health tips"
# ]

# business_finance_concepts = [
#     "business", "finance", "entrepreneur", "investment", "startup", "marketing", "economy", 
#     "stock market", "management", "leadership", "profit", "company", "corporate", "strategy", 
#     "growth", "economics", "business ideas", "financial advice", "business plan", "funding", 
#     "mergers and acquisitions", "business news"
# ]

# # Define educational keywords
# educational_keywords = [
#     "course", "lesson", "tutorial", "neural networks", "machine learning", "deep learning", 
#     "artificial intelligence", "education", "study", "lecture", "classroom", "homework", 
#     "assignment", "quiz", "exam", "syllabus", "curriculum", "university", "college", 
#     "school", "student", "teacher", "professor", "research", "thesis", "academic", 
#     "science", "mathematics", "physics", "chemistry", "biology", "engineering", "statistics", 
#     "data science", "algebra", "geometry", "calculus", "computer science", "programming", 
#     "coding", "python", "java", "C++", "html", "css", "javascript", "blockchain", 
#     "cybersecurity", "cloud computing", "networking", "database", "SQL", "data structures", 
#     "algorithms", "problem solving", "critical thinking", "MOOC", "edtech", "learning platform", 
#     "Udemy", "Coursera", "edX", "Khan Academy", "academic writing", "research paper", 
#     "knowledge", "skills", "training", "instructional", "workshop", "seminar", 
#     "webinar", "tutorial video", "open courseware", "e-learning", "online education", 
#     "professional development", "intellectual", "brainstorm", "case study", "self-paced learning", 
#     "learning objective", "exam preparation", "test prep", "STEM", "peer review", 
#     "educational content", "interactive learning", "project-based learning", "mentorship", 
#     "higher education", "scholar", "scholarship", "academic discipline", "educator"
# ]

# # Extract keyframes (1 frame every 5 seconds)
# def extract_keyframes(video_path, output_folder, interval=5):
#     os.makedirs(output_folder, exist_ok=True)
#     subprocess.run([  
#         "ffmpeg", "-i", video_path,
#         "-vf", f"fps=1/{interval}",
#         os.path.join(output_folder, "frame_%04d.jpg"),
#         "-hide_banner", "-loglevel", "error"
#     ], check=True)

# def analyze_images(folder_path, category_concepts):
#     results = []
#     for file_name in sorted(os.listdir(folder_path)):
#         if file_name.lower().endswith(".jpg"):
#             image_path = os.path.join(folder_path, file_name)
#             image = Image.open(image_path)
#             inputs = clip_processor(text=category_concepts, images=image, return_tensors="pt", padding=True)
#             outputs = clip_model(**inputs)
#             logits_per_image = outputs.logits_per_image
#             probs = logits_per_image.softmax(dim=1)
#             top_score, top_idx = torch.max(probs, dim=1)
#             matched_concept = category_concepts[top_idx.item()]
#             results.append((file_name, matched_concept, top_score.item()))
#     return results

# def is_educational_text(text):
#     max_chunk_size = 500  # Max chunk size for model processing
#     step = max_chunk_size
#     chunks = [text[i:i+step] for i in range(0, len(text), step)]
    
#     total_score = 0
#     educational_votes = 0
#     keyword_votes = 0

#     for chunk in chunks:
#         # Classify text chunk using the educational classifier
#         result = educational_classifier(chunk[:512])[0]  # Limit each chunk to 512 tokens
#         label = result['label']
#         score = result['score']
        
#         total_score += score
#         if label == 'LABEL_1':  # Assuming 'LABEL_1' corresponds to educational content
#             educational_votes += 1

#         # Additional check for the presence of educational keywords
#         if any(keyword in chunk.lower() for keyword in educational_keywords):
#             keyword_votes += 1

#     avg_score = total_score / len(chunks)
    
#     # If majority of chunks are classified as educational or contain educational keywords
#     if educational_votes > len(chunks) / 2 or keyword_votes > len(chunks) / 2:
#         final_label = 'LABEL_1'  # Educational content
#     else:
#         final_label = 'LABEL_0'  # Non-educational content

#     return final_label, avg_score

# def is_video_appropriate(video_path, category="education"):
#     tmp_audio_path = None
#     with tempfile.TemporaryDirectory() as tmpdir:
#         tmp_audio_path = os.path.join(tmpdir, "audio.wav")
#         tmp_frames_dir = os.path.join(tmpdir, "frames")
        
#         # Step 1: Extract audio
#         subprocess.run([  
#             "ffmpeg", "-i", video_path,
#             "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
#             tmp_audio_path, "-y"
#         ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

#         # Step 2: Transcribe
#         result = whisper_model.transcribe(tmp_audio_path, language="en")
#         transcript = result.get("text", "").strip()
#         if not transcript:
#             return False, "Transcript is empty", ""

#         # Step 3: Analyze text
#         label, score = is_educational_text(transcript)
#         educational_pass = (label == 'LABEL_1') and score > 0.75

#         # Step 4: Extract keyframes
#         extract_keyframes(video_path, tmp_frames_dir)

#         # Step 5: Analyze images
#         if category == "sports":
#             category_concepts = sport_concepts
#         elif category == "news":
#             category_concepts = news_concepts
#         elif category == "education":
#             category_concepts = education_concepts
#         elif category == "useful":
#             category_concepts = useful_content_concepts
#         elif category == "cartoon":
#             category_concepts = cartoon_concepts
#         elif category == "technology":
#             category_concepts = technology_concepts
#         elif category == "health":
#             category_concepts = health_wellness_concepts
#         elif category == "business":
#             category_concepts = business_finance_concepts
#         else:
#             category_concepts = education_concepts  # Default to education if unknown

#         image_results = analyze_images(tmp_frames_dir, category_concepts)
#         top_images = [r for r in image_results if r[2] > 0.5]

#         # Decide
#         if educational_pass and top_images:
#             return True, f"✅ Passed. {category.capitalize()} content detected in text and visuals.\nTranscript intent: {label} ({score:.2f})\nVisual match: {top_images[:2]}", transcript
#         else:
#             return False, f"🚫 Rejected.\nTranscript intent: {label} ({score:.2f})\nVisual evidence insufficient.", transcript

# # CLI
# if __name__ == "__main__":
#     path = input("Enter video path: ").strip()
#     category = input("Enter content category (sports, news, education, useful, cartoon): ").strip().lower()

#     if not os.path.exists(path):
#         print("❌ File not found.")
#     else:
#         ok, msg, text = is_video_appropriate(path, category)
#         print("\n🔎 Result:", msg)
#         print("\n📝 Transcript:", text)
