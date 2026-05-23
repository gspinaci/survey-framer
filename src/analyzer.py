import json

import requests

from config import BEDROCK_BASE_URL, BEDROCK_MODEL, BEDROCK_API_KEY, ANTHROPIC_VERSION, MAX_TOKENS

ANALYSIS_PROMPT = """\
You are an expert in AI benchmarking and digital humanities. Analyze the following scientific paper and extract structured information.

Return a JSON object with exactly these fields:

{
  "benchmark_name": "Name of the benchmark (or null if paper does not introduce one)",
  "publication_year": 2024,
  "humanities_role": "content | domain | both | none",
  "humanities_role_explanation": "Brief explanation: e.g., 'Uses art history images as factual QA items' vs 'Designed for art-historical visual understanding'",
  "benchmark_modalities": ["list of modalities used in the benchmark"],
  "benchmark_modalities_explanation": "Description of how modalities are combined and used (e.g., 'Multi-modal VQA combining artwork images with natural language questions')",
  "analytical_tasks": ["list of task types evaluated"],
  "analytical_tasks_explanation": "Detailed explanation of the analytical nature of tasks (e.g., 'factual recognition of art movements', 'economic-grade numerical reasoning', 'causal inference on historical events')",
  "inclusion_criteria": {
    "general_purpose_benchmark": {
      "met": true/false,
      "note": "Explanation"
    },
    "evaluates_generative_llm": {
      "met": true/false,
      "note": "Which models were evaluated (e.g., GPT-4, Llama, Gemini, Claude, Mistral)"
    },
    "llm_is_primary_system": {
      "met": true/false,
      "note": "Is the LLM the primary system being benchmarked, or is it auxiliary?"
    },
    "arts_humanities_data": {
      "met": true/false,
      "note": "Which ASJC areas: History, Language and Linguistics, Archaeology, Classics, Conservation, History and Philosophy of Science, Literature and Literary Theory, Museology, Music, Philosophy, Religious Studies, Visual Arts and Performing Arts"
    },
    "quantitative_metrics": {
      "met": true/false,
      "note": "Which metrics: accuracy, F1, BLEU, exact match, ranking, human preference scores, etc."
    },
    "published_after_march_2023": {
      "met": true/false,
      "note": "Publication or preprint date"
    },
    "english_language": {
      "met": true/false,
      "note": "Language of the paper and/or benchmark"
    }
  },
  "summary": "2-3 sentence summary of the paper's contribution",
  "key_findings": "Main quantitative results or takeaways",
  "relevant_asjc_areas": ["list of matched ASJC humanities areas"]
}

Only return valid JSON. No markdown fences, no commentary outside the JSON.

PAPER TEXT:
"""


def analyze_paper(text: str, title: str = "", metadata: dict | None = None) -> dict:
    url = f"{BEDROCK_BASE_URL}/model/{BEDROCK_MODEL}/invoke"

    user_content = ANALYSIS_PROMPT + text
    if title:
        user_content = f"Paper title: {title}\n\n" + user_content

    if metadata:
        meta_str = f"\nCSV Metadata:\n"
        if metadata.get("modalities"):
            meta_str += f"  - Modalities: {metadata['modalities']}\n"
        if metadata.get("domain"):
            meta_str += f"  - Domain: {metadata['domain']}\n"
        if metadata.get("evaluation_metrics"):
            meta_str += f"  - Evaluation metrics: {metadata['evaluation_metrics']}\n"
        if metadata.get("asjc_code"):
            meta_str += f"  - ASJC code: {metadata['asjc_code']}\n"
        if metadata.get("humanities"):
            meta_str += f"  - Humanities flag: {metadata['humanities']}\n"
        user_content = user_content.replace("PAPER TEXT:", meta_str + "\nPAPER TEXT:")

    payload = {
        "anthropic_version": ANTHROPIC_VERSION,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_content}],
            }
        ],
        "max_tokens": MAX_TOKENS,
    }

    resp = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "x-api-key": BEDROCK_API_KEY,
        },
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()

    data = resp.json()
    reply = data["content"][0]["text"]

    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        cleaned = reply.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]
        return json.loads(cleaned)
