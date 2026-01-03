import os
import gradio as gr
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

def chat(message, history):
    try:
        message = message.strip()

        # Handle date locally
        if message.lower() in ["what date is it", "what is the date today"]:
            return f"Today is {datetime.now().strftime('%d %B %Y')}"

        needs_web = any(word in message.lower() for word in [
            "today", "latest", "current", "population", "news", "price"
        ])

        if needs_web:
            web_data = web_search(message)

            if not web_data.strip():
                return "I couldn't find reliable live data for this question."

            prompt = f"""
WEB SEARCH RESULTS:
{web_data}

QUESTION:
{message}
"""
            system_prompt = WEB_SYSTEM_PROMPT
        else:
            prompt = message
            system_prompt = BASE_SYSTEM_PROMPT

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Internal error: {str(e)}"


demo = gr.ChatInterface(
    fn=chat,
    title="🤖 AI Chatbot (Web + Live Search)",
    description="Ask anything. Live data supported."
)

import os

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    show_error=True
)


