import json

from config import GEMINI_NARRATIVE_MODEL
from src import llm

NARRATIVE_PROMPT = llm.load_prompt("narrative")


def generate_narrative(analyses: list[dict], output_path) -> None:
    summaries = json.dumps(analyses, indent=2)
    narrative = llm.generate_text(NARRATIVE_PROMPT + summaries, GEMINI_NARRATIVE_MODEL)

    header = "# Survey Narrative Synthesis\n\n"
    output_path.write_text(header + narrative, encoding="utf-8")
