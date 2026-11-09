"""Extraction rounds: where agent outputs live, who made them, what is left to do.

    output/rounds/<round>/round.json                 frozen protocol (written once)
    output/rounds/<round>/papers/<paper>/<agent>.json one file per agent per paper

One file per (paper, agent) is what makes distributed work merge cleanly: two
operators running different agents never touch the same file, so `git pull`
needs no conflict resolution. Running the same agent on the same paper twice
is a coordination error, and git reports it as a conflict — as it should.

All state is derived from these files; there is no database to keep in sync.
"""

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from config import BASE_DIR, OUTPUT_DIR
from src.protocol import PER_PAPER_ROLES, REQUIRES, Protocol

ROUNDS_DIR = OUTPUT_DIR / "rounds"


def safe(paper_id: str) -> str:
    return re.sub(r"[^\w\-.]", "_", paper_id)


def round_dir(round_id: str) -> Path:
    return ROUNDS_DIR / round_id


def artifact_path(round_id: str, paper_id: str, agent_id: str) -> Path:
    return round_dir(round_id) / "papers" / safe(paper_id) / f"{agent_id}.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def operator() -> str:
    """Who is running this step: CENSUS_OPERATOR (initials, set in .env), else git user.name."""
    name = os.getenv("CENSUS_OPERATOR", "").strip()
    if not name:
        name = subprocess.run(["git", "config", "user.name"], capture_output=True,
                              text=True, cwd=BASE_DIR).stdout.strip()
    if not name:
        raise RuntimeError("set CENSUS_OPERATOR in .env (e.g. CENSUS_OPERATOR=RG)")
    return name


# --- round ---------------------------------------------------------------------

# What makes an artifact belong to a round: same model, same prompt file, same
# rendered scaffold (prompt + schema + vocabularies + research questions + rules).
FROZEN_KEYS = ("model", "prompt_sha256", "scaffold_sha256")


def _snapshot(protocol: Protocol, scaffolds: dict[str, str]) -> dict:
    snap = protocol.snapshot()
    for aid, agent in snap["agents"].items():
        agent["scaffold_sha256"] = scaffolds.get(aid)
    return snap


def init_round(protocol: Protocol, scaffolds: dict[str, str]) -> Path:
    """scaffolds: agent id -> sha256 of its prompt minus the paper (see src/stages)."""
    path = round_dir(protocol.round) / "round.json"
    if path.exists():
        raise FileExistsError(f"round {protocol.round} already initialised ({path})")
    snap = _snapshot(protocol, scaffolds)
    missing = [aid for aid, a in snap["agents"].items() if a["prompt"] and not a["prompt_sha256"]]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "round": protocol.round,
        "created": now(),
        "created_by": operator(),
        "note": "Frozen protocol. Artifacts whose agent model or prompt hash differ "
                "from this snapshot are refused. To change prompts or models, start a new round.",
        "prompts_not_yet_written": missing,
        **snap,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


# Rounds whose protocol may still change: prompts are being tuned there. A real
# round is frozen for good; to change its prompts, open a new round.
SCRATCH_PREFIXES = ("test-", "pilot-")


def refresh_round(protocol: Protocol, scaffolds: dict[str, str]) -> list[str]:
    """Re-snapshot a scratch round after editing prompts. Returns the agents whose
    model or prompt changed; their existing artifacts become `stale`, everything
    else stays valid — so a pilot can iterate on one stage without redoing the others."""
    if not protocol.round.startswith(SCRATCH_PREFIXES):
        raise RuntimeError(f"round {protocol.round} is frozen; only {'/'.join(SCRATCH_PREFIXES)}* "
                           f"rounds can be refreshed — open a new round instead")
    path = round_dir(protocol.round) / "round.json"
    old = load_round(protocol.round)
    snap = _snapshot(protocol, scaffolds)
    changed = sorted(
        aid for aid in set(old["agents"]) | set(snap["agents"])
        if {k: old["agents"].get(aid, {}).get(k) for k in FROZEN_KEYS}
        != {k: snap["agents"].get(aid, {}).get(k) for k in FROZEN_KEYS}
    )
    data = {**old, **snap}
    data["prompts_not_yet_written"] = [a for a, v in snap["agents"].items() if v["prompt"] and not v["prompt_sha256"]]
    data.setdefault("refreshes", []).append({"on": now(), "by": operator(), "changed": changed})
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def load_round(round_id: str) -> dict:
    path = round_dir(round_id) / "round.json"
    if not path.exists():
        raise FileNotFoundError(
            f"round {round_id} is not initialised: run `python census.py round init` once, "
            f"commit output/rounds/{round_id}/round.json, and share it before anyone runs agents")
    return json.loads(path.read_text(encoding="utf-8"))


def check_against_round(rnd: dict, protocol: Protocol, agent_id: str, scaffold_sha: str | None = None) -> list[str]:
    """Reasons this machine's protocol may not produce artifacts for the round."""
    frozen = rnd["agents"].get(agent_id)
    if frozen is None:
        return [f"agent {agent_id} is not part of round {rnd['round']}"]
    current = protocol.agent(agent_id)
    problems = []
    if current.model != frozen["model"]:
        problems.append(f"model {current.model} != round's {frozen['model']}")
    sha = current.prompt_sha256()
    if frozen["prompt_sha256"] and sha != frozen["prompt_sha256"]:
        problems.append(f"{current.prompt} differs from the version frozen in the round "
                        f"(pull the latest, or start a new round)")
    if frozen["prompt_sha256"] is None and current.prompt:
        problems.append(f"{current.prompt} did not exist when the round was frozen")
    if scaffold_sha and frozen.get("scaffold_sha256") and scaffold_sha != frozen["scaffold_sha256"]:
        problems.append("the rendered prompt differs from the round's (schema, extra_fields.json, "
                        "vocabularies, research questions or evidence rules changed)")
    return problems


# --- artifacts -------------------------------------------------------------------

def read_artifact(round_id: str, paper_id: str, agent_id: str) -> dict | None:
    path = artifact_path(round_id, paper_id, agent_id)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def write_artifact(round_id: str, paper_id: str, agent_id: str, data: dict) -> Path:
    path = artifact_path(round_id, paper_id, agent_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def archive_artifact(round_id: str, paper_id: str, agent_id: str) -> Path | None:
    """Move an existing artifact aside before it is redone (--force): nothing a
    colleague produced is ever silently overwritten."""
    path = artifact_path(round_id, paper_id, agent_id)
    if not path.exists():
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    dest = path.parent / "archive" / f"{agent_id}.{stamp}.json"
    dest.parent.mkdir(exist_ok=True)
    path.rename(dest)
    return dest


def paper_state(protocol: Protocol, rnd: dict, paper_id: str) -> dict[str, str]:
    """agent id -> done | missing | blocked | stale, for every per-paper agent."""
    state: dict[str, str] = {}
    done_roles: dict[str, bool] = {}
    for agent in (a for a in protocol.agents if a.role in PER_PAPER_ROLES):
        art = read_artifact(protocol.round, paper_id, agent.id)
        if art is not None:
            stamp = art.get("extraction", {})
            frozen = rnd["agents"].get(agent.id, {})
            stale = any(frozen.get(k) and stamp.get(k) != frozen.get(k) for k in FROZEN_KEYS)
            state[agent.id] = "stale" if stale else "done"
        else:
            ready = all(done_roles.get(r, False) for r in REQUIRES.get(agent.role, ()))
            state[agent.id] = "missing" if ready else "blocked"
        role_done = state[agent.id] == "done"
        done_roles[agent.role] = done_roles.get(agent.role, True) and role_done
    return state


def input_consistency(protocol: Protocol, paper_id: str) -> str | None:
    """Readers of the same paper must have read the same PDF bytes. arXiv serves
    the latest version, so two operators fetching weeks apart can get different
    files; this is where that surfaces."""
    shas = {}
    for agent in protocol.by_role("reader"):
        art = read_artifact(protocol.round, paper_id, agent.id)
        if art:
            shas[agent.id] = art.get("extraction", {}).get("input", {}).get("pdf_sha256")
    if len(set(shas.values())) > 1:
        return "readers read different PDFs: " + ", ".join(f"{k}={v[:8]}" for k, v in shas.items())
    return None
