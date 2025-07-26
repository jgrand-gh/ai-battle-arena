import os

from google import genai
from google.genai import types

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client()

def generate_response_with_fallback(prompt, system_prompt=None, response_schema=None, is_streamed=False):
    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-pro"]
    response_func = generate_streamed_response if is_streamed else generate_response

    for model in models:
        try:
            response = response_func(
                prompt=prompt,
                model=model,
                system_prompt=system_prompt,
                response_schema=response_schema)
            return response
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue

def generate_response(prompt, model, system_prompt=None, response_schema=None):
    config = types.GenerateContentConfig(system_instruction=system_prompt)
    if response_schema:
        config.response_mime_type = "application/json"
        config.response_schema = response_schema
    return client.models.generate_content(
        model=model,
        config=config,
        contents=prompt,
    )

def generate_streamed_response(prompt, model, system_prompt=None, response_schema=None):
    config = types.GenerateContentConfig(system_instruction=system_prompt)
    if response_schema:
        config.response_mime_type = "application/json"
        config.response_schema = response_schema
    return client.models.generate_content_stream(
        model=model,
        config=config,
        contents=prompt,
    )