# shared input/output formats for each agent.

from dataclasses import dataclass
from typing import List

@dataclass
class PlannerOutput:
    research_topic: str
    questions: List[str]


@dataclass
class RetrievalResult:
    question: str
    sources: List[str]
    summaries: List[str]


@dataclass
class ExecutorOutput:
    report: str


@dataclass
class CriticOutput:
    issues_found: List[str]
    improved_report: str