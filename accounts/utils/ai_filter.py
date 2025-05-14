# import openai
# import os

# # Set your OpenAI key
# openai.api_key = "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"

# def is_content_meaningful(text: str) -> bool:
#     prompt = (
#         f"Determine if the following content is meaningful, educational, or intellectually valuable. "
#         f"Respond only with 'Yes' or 'No'.\n\nContent: {text}"
#     )

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0
#         )
#         result = response['choices'][0]['message']['content'].strip().lower()
#         return result == 'yes'
#     except Exception as e:
#         print("OpenAI error:", e)
#         return False  # Fail-safe: block content if AI fails



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
