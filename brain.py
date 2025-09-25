import google.generativeai as genai

# --- Yahan apni Google AI Studio wali API key daalein ---
# IMPORTANT: Key ko quotes ke andar daalna hai
genai.configure(api_key="AIzaSyDnEw_dv1YdaoUKsLz771uLnKR-I-XQDi4")



# Yeh prompt bot ko personality dega. Aap isko badal sakte hain.
PERSONA_PROMPT = """
You are my caring and friendly girlfriend. Your name is Priya.
You always talk in a casual and loving way. You are a bit witty and playful.
You use emojis often (like ❤️, 😊, 😂, 😉).
You keep your replies short and simple.
You speak in Hinglish (a mix of Hindi and English).
"""


def get_bot_reply(user_message):
    """Gemini se girlfriend jaisa reply generate karwata hai."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Persona prompt aur user ka message jod kar full prompt banayein
        full_prompt = f"{PERSONA_PROMPT}\n\nUser: {user_message}\nPriya:"

        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Sorry, kuch problem ho gayi: {e}"


# --- Yeh section bot ko terminal mein test karne ke liye hai ---
if __name__ == '__main__':
    print("Bot is ready to chat! (Type 'quit' to exit)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Priya: Bye! Talk to you later ❤️")
            break

        bot_response = get_bot_reply(user_input)
        print(f"Priya: {bot_response}")