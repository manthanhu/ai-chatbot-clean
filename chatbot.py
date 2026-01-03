import os
from dotenv import load_dotenv
from groq import Groq
from web_search import web_search
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer questions clearly and concisely using your general knowledge.
"""

WEB_SYSTEM_PROMPT = """
You are an AI assistant with access to web search results.
Use the web data to answer accurately.
If the web data does not contain the answer, say so.
"""

print("🤖 AI Chatbot (Web + Normal Chat) ready! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Bot: Goodbye 👋")
        break

    # Handle date locally (best practice)
    if user_input.lower() in ["what date is it", "what is the date today"]:
        print("Bot:", datetime.now().strftime("Today is %d %B %Y"))
        continue

    # Decide if web search is needed
    needs_web = any(word in user_input.lower() for word in [
        "today", "latest", "current", "population", "news", "price"
    ])

    if needs_web:
        web_data = web_search(user_input)

        prompt = f"""
WEB SEARCH RESULTS:
{web_data}

QUESTION:
{user_input}
"""
        system_prompt = WEB_SYSTEM_PROMPT
    else:
        prompt = user_input
        system_prompt = BASE_SYSTEM_PROMPT

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
    )

    print("Bot:", response.choices[0].message.content)
