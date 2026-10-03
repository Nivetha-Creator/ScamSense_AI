import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_scam(message, ml_result):

    prompt = f"""
You are ScamSense, an AI assistant that helps users identify
potentially fraudulent messages.

Analyze the following message:

MESSAGE:
{message}

Machine-learning result:
{ml_result}

Return your response using EXACTLY these four sections:

RISK ASSESSMENT:
Give a short assessment of the overall risk.

WHY IT MAY BE SUSPICIOUS:
Explain the specific reasons or patterns that could make the
message suspicious.

WARNING SIGNS:
List the important warning signs found in the message.
If there are no clear warning signs, say so.

SAFE NEXT STEPS:
Give practical safety advice for the user.

Important:
- Be concise and easy to understand.
- Do not claim that a message is definitely a scam solely because
  the machine-learning model classified it as one.
- Do not invent facts that are not present in the message.
- If the message appears normal, say that no obvious scam indicators
  were detected.
"""


    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )


    return response.output_text