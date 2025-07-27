# HAD TO SCRAP THIS ROUTE
# "Free" is a misnomer, OpenRouter severely limits requests per day (to like, 20) if you haven't bought credits.
# Leaving for posterity's sake, but currently completely unused.

import os

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

DEEPSEEK_MODEL = "deepseek/deepseek-chat-v3-0324:free"
QWEN_MODEL = "qwen/qwen3-235b-a22b-2507:free"
MOONSHOT_MODEL = "moonshotai/kimi-k2:free"
GOOGLE_GEMINI_MODEL = "google/gemini-2.0-flash-exp:free"
TNG_DEEPSEEK_MODEL = "tngtech/deepseek-r1t2-chimera:free"

free_model_list = [DEEPSEEK_MODEL, QWEN_MODEL, MOONSHOT_MODEL, GOOGLE_GEMINI_MODEL, TNG_DEEPSEEK_MODEL]

def generate_response_with_fallback(prompt, system_prompt=None, response_schema=None, is_streamed=False):
    models = free_model_list
    response_func = generate_streamed_response if is_streamed else generate_response

    for model in models:
        try:
            response = response_func(
                prompt=prompt,
                model=model,
                system_prompt=system_prompt,
                response_schema=response_schema,
            )
            return response
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue
    raise RuntimeError("All models failed to generate a response.")

def generate_response(prompt, model, system_prompt=None, response_schema=None):
    if response_schema:
        return client.responses.parse(
            model=model,
            instructions=system_prompt,
            input=prompt,
            text_format=response_schema,
        )
    return client.responses.create(
        model=model,
        instructions=system_prompt,
        input=prompt,
    )

def generate_streamed_response(prompt, model, system_prompt=None, response_schema=None):
    if response_schema:
        return client.responses.parse(
            model=model,
            instructions=system_prompt,
            input=prompt,
            text_format=response_schema,
            stream=True,
        )
    return client.responses.create(
        model=model,
        instructions=system_prompt,
        input=prompt,
        stream=True,
    )