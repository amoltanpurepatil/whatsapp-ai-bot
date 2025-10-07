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
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    full_prompt = f"{PERSONA_PROMPT}\n\nUser: {user_message}\nPriya:"
    response = model.generate_content(full_prompt)
    return response.text.strip()
  except Exception as e:
    return f"Sorry, kuch problem ho gayi: {e}"

# --- Step 3: Create the Flask server ---
app = Flask(__name__)

# --- Step 4: Create the webhook that receives messages from Twilio ---
@app.route('/webhook', methods=['POST'])
def webhook():
  incoming_msg = request.values.get('Body', '').strip()
  bot_reply = get_bot_reply(incoming_msg)
  resp = MessagingResponse()
  resp.message(bot_reply)
  return str(resp)

# The final 'if __name__ == "__main__"' block is removed for deployment.
# Gunicorn runs the 'app' object directly.
