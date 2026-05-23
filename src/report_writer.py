import re
from pathlib import Path


def _safe_filename(paper_id: str) -> str:
    return re.sub(r"[^\w\-]", "_", paper_id) + ".md"


def _criteria_icon(met: bool) -> str:
    return "YES" if met else "NO"


def write_paper_report(paper: dict, analysis: dict, output_dir: Path) -> Path:
    filename = _safe_filename(paper["id"])
    dest = output_dir / filename

    criteria = analysis.get("inclusion_criteria", {})

    title = analysis.get('benchmark_name') or paper.get('name', paper['id'])
    lines = [
        f"# {title}",
        "",
        f"**Paper name:** {paper.get('name', 'N/A')}",
        f"**DOI:** {paper.get('doi', 'N/A')}",
        f"**arXiv ID:** {paper.get('arxiv_id', 'N/A')}",
        f"**Year:** {paper.get('year', 'N/A')}",
        f"**Article URL:** {paper.get('article_url', 'N/A')}",
        f"**Publication year (from analysis):** {analysis.get('publication_year', 'N/A')}",
        "",
        "## Humanities Role",
        "",
        f"**Classification:** {analysis.get('humanities_role', 'N/A')}",
        f"**Explanation:** {analysis.get('humanities_role_explanation', 'N/A')}",
        f"**Relevant ASJC areas:** {', '.join(analysis.get('relevant_asjc_areas', []))}",
        f"**CSV Humanities?:** {paper.get('humanities', 'N/A')}",
        f"**CSV ASJC code:** {paper.get('asjc_code', 'N/A')}",
        "",
        "## Inclusion Criteria",
        "",
        "| Criterion | Met? | Note |",
        "|-----------|------|------|",
    ]

    labels = {
        "general_purpose_benchmark": "General-purpose benchmark",
        "evaluates_generative_llm": "Evaluates generative LLM",
        "llm_is_primary_system": "LLM is primary evaluated system",
        "arts_humanities_data": "Arts & Humanities data/tasks",
        "quantitative_metrics": "Quantitative performance metrics",
        "published_after_march_2023": "Published after Mar 2023",
        "english_language": "English language",
    }

    for key, label in labels.items():
        c = criteria.get(key, {})
        met = _criteria_icon(c.get("met", False))
        note = c.get("note", "")
        lines.append(f"| {label} | {met} | {note} |")

    lines += [
        "",
        "## Benchmark Modalities",
        "",
        f"**Modality Types:** {', '.join(analysis.get('benchmark_modalities', []))}",
        "",
        f"**Description:** {analysis.get('benchmark_modalities_explanation', 'N/A')}",
        "",
        "## Analytical Tasks",
        "",
        f"**Task Types:** {', '.join(analysis.get('analytical_tasks', []))}",
        "",
        f"**Detailed Description:** {analysis.get('analytical_tasks_explanation', 'N/A')}",
        "",
        "## Summary",
        "",
        analysis.get("summary", "N/A"),
        "",
        "## Key Findings",
        "",
        analysis.get("key_findings", "N/A"),
        "",
    ]

    dest.write_text("\n".join(lines), encoding="utf-8")
    return dest


def append_exclusion_note(paper_id: str, failed_criteria: list[tuple[str, str]], output_dir: Path) -> None:
    """Append an exclusion section to an existing paper report."""
    filename = _safe_filename(paper_id)
    dest = output_dir / filename
    if not dest.exists():
        return

    labels = {
        "general_purpose_benchmark": "General-purpose benchmark",
        "evaluates_generative_llm": "Evaluates generative LLM",
        "llm_is_primary_system": "LLM is primary evaluated system",
        "arts_humanities_data": "Arts & Humanities data/tasks",
        "quantitative_metrics": "Quantitative performance metrics",
        "published_after_march_2023": "Published after Mar 2023",
        "english_language": "English language",
    }

    lines = [
        "",
        "---",
        "",
        "## Exclusion Note",
        "",
        "This paper **does not meet all inclusion criteria** and will be excluded from the narrative synthesis.",
        "",
        "| Failed Criterion | Reason |",
        "|------------------|--------|",
    ]
    for key, note in failed_criteria:
        label = labels.get(key, key)
        lines.append(f"| {label} | {note} |")

    existing = dest.read_text(encoding="utf-8")
    dest.write_text(existing + "\n".join(lines) + "\n", encoding="utf-8")
