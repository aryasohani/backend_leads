from dotenv import load_dotenv
load_dotenv()   # this loads variables from .env file

import os
import openai
import json

openai.api_key = os.getenv('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')

def classify_with_ai(offer: dict, lead: dict):
    prompt = f"""
    You are a lead qualification assistant.
    Offer:
    Name: {offer['name']}
    Value props: {offer['value_props']}
    Ideal use cases: {offer['ideal_use_cases']}

    Prospect:
    Name: {lead['name']}
    Role: {lead['role']}
    Company: {lead['company']}
    Industry: {lead['industry']}
    Location: {lead['location']}
    LinkedIn bio: {lead['linkedin_bio']}

    Task:
    1) Classify the buying intent as "High", "Medium", or "Low".
    2) Provide 1-2 sentence reasoning.

    Return ONLY a JSON object with keys intent and reason.
    """

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"You are a helpful assistant."},
                  {"role":"user","content":prompt}],
        temperature=0.0,
        max_tokens=200
    )

    text = resp['choices'][0]['message']['content'].strip()
    try:
        data = json.loads(text)
        return data.get("intent","Low"), data.get("reason","")
    except:
        # fallback
        if "High" in text: return "High", text
        if "Medium" in text: return "Medium", text
        return "Low", text
