
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an expert HR Recruiter.

Analyze the following resume according to the job description.

Job Description:
{job_description}

Resume:
{resume_text}

Return the response in Markdown.

Include:

# Resume Score (/100)

# ATS Score (/100)

# Job Match (%)

# Strengths

# Weaknesses

# Missing Skills

# Suggestions
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content