from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import google.generativeai as genai

# Configure Gemini API

genai.configure(
    api_key="YOUR_API_KEY"
)

# Create Model

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

# FastAPI App

app = FastAPI()

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model

class Symptom(BaseModel):
    symptom: str

# Home Route

@app.get("/")
def home():

    return {
        "message": "AI Medical Assistant Backend Running Successfully"
    }

# Chat Route

@app.post("/chat")
def chat(data: Symptom):

    prompt = f"""
    You are an AI Medical Assistant.

    User symptoms:
    {data.symptom}

    Give:
    - possible condition
    - precautions
    - simple advice

    Keep response short and easy to understand.
    """

    try:

        # AI Response

        response = model.generate_content(prompt)

        return {
            "response": response.text
        }

    except Exception as e:

        print("Gemini Error:", e)

    # Fallback Local Responses

    symptom_text = data.symptom.lower()

    if "fever" in symptom_text:

        ai_text = """
⚠️ Medium Risk

Possible viral fever.

✅ Drink plenty of water
✅ Take proper rest
✅ Monitor body temperature

Consult a doctor if fever increases.
"""

    elif "cough" in symptom_text:

        ai_text = """
⚠️ Mild Risk

Possible common cold or throat infection.

✅ Drink warm water
✅ Avoid cold foods
✅ Take enough rest
"""

    elif "headache" in symptom_text:

        ai_text = """
⚠️ Low Risk

Possible stress or migraine.

✅ Stay hydrated
✅ Sleep properly
✅ Reduce screen time
"""

    elif "blood vomit" in symptom_text:

        ai_text = """
🚨 High Risk

Possible internal bleeding or serious stomach condition.

❗ Seek immediate medical attention.
❗ Visit nearest hospital immediately.
"""

    elif "chest pain" in symptom_text:

        ai_text = """
🚨 High Risk

Possible heart-related emergency.

❗ Consult emergency medical services immediately.
"""

    else:

        ai_text = """
⚠️ General Advice

Symptoms are unclear.

✅ Monitor symptoms
✅ Stay hydrated
✅ Consult a doctor if condition worsens
"""

    return {
        "response": ai_text
    }