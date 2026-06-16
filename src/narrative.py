import json
from pathlib import Path

import requests
import google.genai as genai

from config import (
    BEDROCK_BASE_URL, BEDROCK_MODEL, BEDROCK_API_KEY, ANTHROPIC_VERSION, MAX_TOKENS,
    MODEL, GEMINI_API_KEY, GEMINI_MODEL, GEMINI_NARRATIVE_MODEL
)

_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
NARRATIVE_PROMPT = (_PROMPTS_DIR / "narrative.txt").read_text(encoding="utf-8")


def generate_narrative(analyses: list[dict], output_path) -> None:
    # Framer always uses Gemini 3.1 Pro regardless of MODEL setting
    narrative = _generate_narrative_with_gemini(analyses)

    header = "# Survey Narrative Synthesis\n\n"
    output_path.write_text(header + narrative, encoding="utf-8")


def _generate_narrative_with_bedrock(analyses: list[dict]) -> str:
    """Generate narrative using Harvard Bedrock API."""
    summaries = json.dumps(analyses, indent=2)
    user_content = NARRATIVE_PROMPT + summaries

    url = f"{BEDROCK_BASE_URL}/model/{BEDROCK_MODEL}/invoke"
    payload = {
        "anthropic_version": ANTHROPIC_VERSION,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_content}],
            }
        ],
        "max_tokens": MAX_TOKENS * 2,
    }

    resp = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "x-api-key": BEDROCK_API_KEY,
        },
        json=payload,
        timeout=180,
    )
    resp.raise_for_status()

    data = resp.json()
    narrative = data["content"][0]["text"]
    return narrative


def _generate_narrative_with_gemini(analyses: list[dict]) -> str:
    """Generate narrative using Google Gemini API."""
    client = genai.Client(api_key=GEMINI_API_KEY)

    summaries = json.dumps(analyses, indent=2)
    user_content = NARRATIVE_PROMPT + summaries

    response = client.models.generate_content(
        model=GEMINI_NARRATIVE_MODEL,
        contents=user_content
    )
    narrative = response.text
    return narrative
