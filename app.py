from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import os

app = Flask(__name__)

# ✅ Configure Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Load Gemini model correctly
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

@app.route("/")
def home():
    return "WhatsApp AI Bot is running!"

@app.route("/bot", methods=["POST"])
def bot():
    user_message = request.form.get("Body")
    sender = request.form.get("From")

    print(f"Message from {sender}: {user_message}")

    try:
        # ✅ Generate AI reply
        response = model.generate_content(user_message)
        ai_reply = response.text.strip()
    except Exception as e:
        print("Error:", e)
        ai_reply = "Sorry, I had trouble processing that. Please try again."

    # ✅ Send reply via Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(ai_reply)

    return str(twilio_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
