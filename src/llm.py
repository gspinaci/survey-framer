"""Shared Gemini call helpers and prompt loading."""

import json

import google.genai as genai

from config import GEMINI_API_KEY, PROMPTS_DIR


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")


def _parse_json_reply(reply: str) -> dict:
    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        pass
    cleaned = reply.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0]
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Model appended extra content after the JSON — take the first object
        start = cleaned.index("{")
        obj, _ = json.JSONDecoder().raw_decode(cleaned[start:])
        return obj


def generate_json(prompt: str, model: str) -> dict:
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )
    return _parse_json_reply(response.text)


def generate_text(prompt: str, model: str) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text
