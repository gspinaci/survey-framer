"""Pipeline stages of the round-based engine (census.py).

Every stage module exposes the same interface:
    scaffold(protocol, agent) -> str   the prompt minus the paper, frozen by the round
    run(protocol, agent, paper, backend_name) -> {artifact name: data}
    summary(artifacts) -> str          one line for the console
"""

from src.stages import reader, reviewer, supervisor

STAGES = {"reader": reader, "supervisor": supervisor, "reviewer": reviewer}
