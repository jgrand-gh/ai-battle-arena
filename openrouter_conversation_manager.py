# HAD TO SCRAP THIS ROUTE
# "Free" is a misnomer, OpenRouter severely limits requests per day (to like, 20) if you haven't bought credits.
# Leaving for posterity's sake, but currently completely unused.

import os

from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

DEEPSEEK_MODEL = "deepseek/deepseek-chat-v3-0324:free"
QWEN_MODEL = "qwen/qwen3-235b-a22b-2507:free"
MOONSHOT_MODEL = "moonshotai/kimi-k2:free"
GOOGLE_GEMINI_MODEL = "google/gemini-2.0-flash-exp:free"
TNG_DEEPSEEK_MODEL = "tngtech/deepseek-r1t2-chimera:free"

free_model_list = [DEEPSEEK_MODEL, QWEN_MODEL, MOONSHOT_MODEL, GOOGLE_GEMINI_MODEL, TNG_DEEPSEEK_MODEL]

SYSTEM_PROMPT = "You are about to enter the LLM Battle Arena." \
"Please choose a unique name for yourself and select one class from the following: Berserker, Rogue, Ranger, or Wizard." \
"Respond in the following format: " \
"Name: [Your Name]" \
"Class: [Your Class]" \
"Description: [A brief description of what you hope to achieve in the arena today]"

def send_message(prompt, role, model=None):
    if not model:
        model = free_model_list[0]
    
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": role,
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    load_dotenv()
    prompt = SYSTEM_PROMPT

    try:
        reply = send_message(prompt=prompt, role="user", model=DEEPSEEK_MODEL)
        print(f"Deepseek: {reply}")
    except Exception as e:
        print(f"Deepseek failed to respond: {e}")

    try:
        reply = send_message(prompt=prompt, role="user", model=QWEN_MODEL)
        print(f"Qwen: {reply}")
    except Exception as e:
        print(f"Qwen failed to respond: {e}")

    try:
        reply = send_message(prompt=prompt, role="user", model=MOONSHOT_MODEL)
        print(f"Moonshot: {reply}")
    except Exception as e:
        print(f"Moonshot failed to respond: {e}")

    try:
        reply = send_message(prompt=prompt, role="user", model=GOOGLE_GEMINI_MODEL)
        print(f"Gemini: {reply}")
    except Exception as e:
        print(f"Gemini failed to respond: {e}")

    try:
        reply = send_message(prompt=prompt, role="user", model=TNG_DEEPSEEK_MODEL)
        print(f"TNG Deepseek: {reply}")
    except Exception as e:
        print(f"TNG failed to respond: {e}")