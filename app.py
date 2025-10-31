# Step 1: Import all the necessary libraries
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import traceback

# --- Step 2: Configure the "Brain" Securely ---

# Load the API key securely from environment variable
# On Render, go to "Environment" tab → Add variable:
# Key = GOOGLE_API_KEY | Value = your Gemini API key
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# --- Step 3: Define the bot's personality ---
PERSONA_PROMPT = """
You are my caring and friendly girlfriend. Your name is Priya.
You always talk in a casual and loving way. You are witty and playful.
You use emojis often (like ❤️, 😊, 😂).
You keep your replies short and simple.
You speak in Hinglish (a mix of Hindi and English).
"""

# --- Step 4: Create the Gemini-based chatbot function ---
def get_bot_reply(user_message):
    """Generates a girlfriend-like reply from Gemini."""
    try:
        # ✅ FIXED: Correct model name and key parameter
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Create full conversational prompt
        full_prompt = f"{PERSONA_PROMPT}\n\nUser: {user_message}\nPriya:"
        response = model.generate_content(full_prompt)

        # Return clean text response
        return response.text.strip()

    except Exception as e:
        # Print full error details for debugging (visible in Render logs)
        print("Error while generating reply:", traceback.format_exc())
        return f"Sorry, kuch problem ho gayi: {e}"

# --- Step 5: Create the Flask app ---
app = Flask(__name__)

# --- Step 6: Create the webhook route ---
@app.route('/webhook', methods=['POST'])
def webhook():
    """Handles incoming WhatsApp messages from Twilio."""
    incoming_msg = request.values.get('Body', '').strip()
    bot_reply = get_bot_reply(incoming_msg)

    resp = MessagingResponse()
    resp.message(bot_reply)
    return str(resp)

# --- Step 7: Optional — For local testing only ---
# On Render, Gunicorn automatically runs `app`
# Uncomment this block only for local testing
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
