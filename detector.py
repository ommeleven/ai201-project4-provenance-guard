import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def llm_detector(text):
    prompt = f"""
You are an AI content detector.

Given the text below, estimate the probability that it was written by AI.

Return ONLY valid JSON like this:

{{"score":0.82}}

Text:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        result = response.choices[0].message.content
        data = json.loads(result)

        return float(data["score"])

    except Exception as e:
        print(e)
        return 0.50