from dataclasses import dataclass, field
from typing import List
from datetime import datetime, timezone

@dataclass
class Turn:
    round: int
    speaker: str
    phase: str
    content: str
    citations: List[str] = field(default_factory=list)
    objections_raised: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

@dataclass
class Ruling:
    objection: str
    decision: str  # "SUSTAINED" | "OVERRULED" | "DEFERRED" | "FINAL RULING"
    reasoning: str
    citations: List[str] = field(default_factory=list)

@dataclass
class SimulationState:
    case_id: str
    phase: str = "opening"             # "opening" | "evidence" | "rebuttal" | "closing"
    round: int = 1
    transcript: List[Turn] = field(default_factory=list)
    pending_objections: List[str] = field(default_factory=list)
    rulings: List[Ruling] = field(default_factory=list)
    human_interventions: List[str] = field(default_factory=list)
