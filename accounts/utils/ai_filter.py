


import ollama

def is_content_meaningful(text: str) -> bool:
    prompt = f"""
You are an assistant moderating content for an intellectual platform like BeSmart.

Determine if the following content is meaningful, educational, or valuable for users seeking knowledge. 
Respond ONLY with "yes" or "no".

Content: {text}
"""
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        result = response['message']['content'].strip().lower()
        return result.startswith("yes")
    except Exception as e:
        print("Ollama Filter Error:", e)
        return False

def generate_tags(text: str) -> str:
    prompt = f"""
Generate 3-5 relevant, short tags for this educational content, separated by commas.

Content: {text}

Example Output: science, AI, future, innovation
"""
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return response['message']['content'].strip()
    except Exception as e:
        print("Ollama Tag Error:", e)
        return ""
