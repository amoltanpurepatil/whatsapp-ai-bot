# Step 1: Import all the necessary libraries
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# --- Step 2: Configure the "Brain" Securely ---
# The key is loaded from a secure Environment Variable on Render
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# This prompt gives the bot its personality
PERSONA_PROMPT = """
You are my caring and friendly girlfriend. Your name is Priya.
You always talk in a casual and loving way. You are a bit witty and playful.
You use emojis often (like ❤️, 😊, 😂, 😉).
You keep your replies short and simple.
You speak in Hinglish (a mix of Hindi and English).
"""

def get_bot_reply(user_message):
    """Generates a girlfriend-like reply from Gemini."""
    try:
        # ✅ Fixed model name (no -latest, correct version)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Combine the persona and user message
        full_prompt = f"{PERSONA_PROMPT}\n\nUser: {user_message}\nPriya:"

        # Generate response
        response = model.generate_content(full_prompt)

        # ✅ Safely extract text (for different SDK versions)
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return "Hmm... kuch samajh nahi aaya 😅"

    except Exception as e:
        # Return clean error message (shown in WhatsApp if API fails)
        return f"Sorry, kuch problem ho gayi: {e}"

# --- Step 3: Create the Flask server ---
app = Flask(__name__)

# --- Step 4: Create the webhook that receives messages from Twilio ---
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get message sent from user (via Twilio)
    incoming_msg = request.values.get('Body', '').strip()

    # Get AI-generated reply
    bot_reply = get_bot_reply(incoming_msg)

    # Prepare Twilio response
    resp = MessagingResponse()
    resp.message(bot_reply)
    return str(resp)

# --- Note ---
# No 'if __name__ == "__main__"' block is needed here.
# On Render, Gunicorn automatically runs the Flask 'app' object.
