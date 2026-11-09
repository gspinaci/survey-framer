"""The census protocol (census.toml): agents, backends, the current round.

Everything the engine needs to know about *this* survey comes from here, so the
engine itself stays generic: a different census is a different census.toml.
"""

import fnmatch
import hashlib
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from config import BASE_DIR

PROTOCOL_PATH = BASE_DIR / "census.toml"

# Roles in pipeline order. A role's prerequisites are the roles before it that
# work per paper; corpus-level roles (narrator, critic) come after every paper is
# reviewed. scout and intake sit before the table / before reading respectively.
ROLE_ORDER = ("scout", "intake", "reader", "supervisor", "reviewer", "narrator", "critic")
PER_PAPER_ROLES = ("intake", "reader", "supervisor", "reviewer")
REQUIRES = {
    "reader": (),
    "supervisor": ("reader",),
    "reviewer": ("reader", "supervisor"),
}
BACKEND_KINDS = ("claude-cli", "gemini", "mock")
# Which backend kinds can serve which model family. A round fixes the model; an
# operator may only run it through a backend that actually serves that model.
SERVES = {"claude-cli": ("claude-",), "gemini": ("gemini-",), "mock": ("",)}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class Agent:
    id: str
    role: str
    scope: str = ""
    model: str = ""
    backend: str = ""
    prompt: str = ""
    fields: list[str] | str = "all"
    options: dict = field(default_factory=dict)

    @property
    def prompt_path(self) -> Path:
        return BASE_DIR / self.prompt

    def prompt_sha256(self) -> str | None:
        return sha256_file(self.prompt_path) if self.prompt and self.prompt_path.exists() else None

    def select_fields(self, declared: dict[str, str]) -> dict[str, str]:
        """The subset of the declared schema this agent is scoped to."""
        if self.fields == "all":
            return dict(declared)
        patterns = list(self.fields)
        return {k: v for k, v in declared.items() if any(fnmatch.fnmatch(k, p) for p in patterns)}


@dataclass
class Protocol:
    path: Path
    name: str
    table: Path
    research_questions: Path
    round: str
    backends: dict[str, dict]
    agents: list[Agent]

    def agent(self, agent_id: str) -> Agent:
        for a in self.agents:
            if a.id == agent_id:
                return a
        raise KeyError(f"no agent {agent_id!r} in {self.path.name}; "
                       f"declared: {', '.join(a.id for a in self.agents)}")

    def by_role(self, role: str) -> list[Agent]:
        return [a for a in self.agents if a.role == role]

    def snapshot(self) -> dict:
        """What a round freezes: every agent's model, backend and prompt hash."""
        return {
            "protocol_sha256": sha256_file(self.path),
            "research_questions_sha256": sha256_file(self.research_questions)
            if self.research_questions.exists() else None,
            "agents": {
                a.id: {"role": a.role, "scope": a.scope, "model": a.model,
                       "backend": a.backend, "prompt": a.prompt,
                       "prompt_sha256": a.prompt_sha256(), "fields": a.fields}
                for a in self.agents
            },
        }


def load(path: Path = PROTOCOL_PATH) -> Protocol:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    census = data.get("census", {})
    defaults = data.get("defaults", {})
    backends = data.get("backends", {})
    for name, spec in backends.items():
        if spec.get("kind") not in BACKEND_KINDS:
            raise ValueError(f"backend {name!r}: kind must be one of {BACKEND_KINDS}")

    agents: list[Agent] = []
    for raw in data.get("agent", []):
        raw = dict(raw)
        role = raw.pop("role")
        if role not in ROLE_ORDER:
            raise ValueError(f"agent {raw.get('id')!r}: unknown role {role!r} (one of {ROLE_ORDER})")
        base_id = raw.pop("id")
        count = int(raw.pop("count", 1))
        known = {k: raw.pop(k) for k in ("scope", "model", "backend", "prompt", "fields") if k in raw}
        known.setdefault("model", defaults.get("model", ""))
        known.setdefault("backend", defaults.get("backend", ""))
        if known["backend"] not in backends:
            raise ValueError(f"agent {base_id!r}: backend {known['backend']!r} is not declared")
        scopes = known.get("scope")
        # A list of scopes means one instance per scope (e.g. one scout per source family).
        if isinstance(scopes, list):
            for s in scopes:
                agents.append(Agent(id=f"{base_id}-{s}", role=role, **{**known, "scope": s}, options=raw))
        elif count > 1:
            for i in range(1, count + 1):
                agents.append(Agent(id=f"{base_id}-{i}", role=role, **known, options=raw))
        else:
            agents.append(Agent(id=base_id, role=role, **known, options=raw))

    ids = [a.id for a in agents]
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate agent ids in {path.name}: {ids}")
    agents.sort(key=lambda a: ROLE_ORDER.index(a.role))
    return Protocol(
        path=path,
        name=census.get("name", ""),
        table=BASE_DIR / census.get("table", "input/papers.csv"),
        research_questions=BASE_DIR / census.get("research_questions", "prompts/research_questions.md"),
        round=census["round"],
        backends=backends,
        agents=agents,
    )


def backend_can_serve(kind: str, model: str) -> bool:
    return any(model.startswith(prefix) for prefix in SERVES[kind])
