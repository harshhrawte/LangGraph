import os
import json
import math
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini with API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def split_into_chunks(data, chunk_size=20):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def generate_report(data):
    full_report = ""

    for idx, chunk in enumerate(split_into_chunks(data, chunk_size=20)):
        prompt = f"""
You are a strategic B2B analyst. Analyze the customer data below and generate:
1. A summary of purchase and behavior patterns.
2. Top 3 cross-sell and upsell recommendations.
3. High-level insights and strategic recommendations.

Respond in markdown format with proper headings.

Data Chunk #{idx+1}:
{json.dumps(chunk, indent=2)}
        """

        response = model.generate_content(prompt)
        full_report += f"\n\n## Report Part {idx+1}\n{response.text}"

    return full_report.strip()
