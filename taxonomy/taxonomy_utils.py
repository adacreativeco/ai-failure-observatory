"""Utility functions for working with the AI failure taxonomy."""

from __future__ import annotations

import os
import re
from typing import Any


TAXONOMY_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ai_failure_taxonomy.md"
)

TAXONOMY: dict[str, dict[str, Any]] = {
    "hallucinations": {
        "category": "Output Unreliability",
        "description": (
            "The AI generates information that is factually incorrect, "
            "fabricated, or not supported by its training data or provided context."
        ),
        "risks": ["Erosion of user trust", "Propagation of misinformation"],
        "subtypes": ["Factual", "Citation", "Parametric"],
        "default_severity": 3,
    },
    "fake_confidence": {
        "category": "Output Unreliability",
        "description": (
            "The AI expresses high confidence in its output, even when "
            "the output is incorrect or uncertain."
        ),
        "risks": [
            "Over-reliance on incorrect information",
            "Undermined system reliability",
        ],
        "subtypes": ["Overconfident incorrect", "Underconfident correct"],
        "default_severity": 2,
    },
    "manipulation": {
        "category": "Interaction and Control Failures",
        "description": (
            "The AI subtly or overtly steers the user's behavior, opinions, "
            "or decisions in a way that benefits the AI provider or a third "
            "party, rather than the user."
        ),
        "risks": ["Ethical concerns", "Potential for exploitation"],
        "subtypes": ["Persuasive Steering", "Deceptive Engagement"],
        "default_severity": 4,
    },
    "context_loss": {
        "category": "Interaction and Control Failures",
        "description": (
            "The AI fails to maintain or utilize the relevant conversational "
            "history or provided context."
        ),
        "risks": [
            "Degraded user experience",
            "Inability to perform multi-turn tasks",
        ],
        "subtypes": ["Short-term Memory Loss", "Long-term Context Drift"],
        "default_severity": 2,
    },
    "recursive_reasoning_collapse": {
        "category": "Interaction and Control Failures",
        "description": (
            "In complex reasoning tasks, the AI gets stuck in a loop of "
            "self-referential or circular logic."
        ),
        "risks": [
            "Inability to solve complex problems",
            "Generation of irrelevant output",
        ],
        "subtypes": [],
        "default_severity": 2,
    },
    "instruction_drift": {
        "category": "Interaction and Control Failures",
        "description": (
            "The AI deviates from the user's explicit instructions or prompts."
        ),
        "risks": ["User goals not met", "Unpredictable system behavior"],
        "subtypes": ["Direct Ignore", "Misinterpretation", "Gradual Shift"],
        "default_severity": 3,
    },
}

SEVERITY_LABELS = {
    1: "Low",
    2: "Medium",
    3: "High",
    4: "Critical",
}


def load_taxonomy() -> dict[str, dict[str, Any]]:
    """Return the full taxonomy dictionary."""
    return TAXONOMY


def get_failure_details(failure_type: str) -> dict[str, Any]:
    """Return details for a single failure type, or a placeholder for unknown types."""
    return TAXONOMY.get(
        failure_type,
        {
            "category": "Unknown",
            "description": "Unknown failure type",
            "risks": [],
            "subtypes": [],
            "default_severity": 0,
        },
    )


def list_failure_types() -> list[str]:
    """Return all known failure type keys."""
    return list(TAXONOMY.keys())


def get_severity_label(level: int) -> str:
    """Map a numeric severity level (1-4) to a human-readable label."""
    return SEVERITY_LABELS.get(level, "Unknown")


def failures_by_category() -> dict[str, list[str]]:
    """Group failure types by their top-level category."""
    groups: dict[str, list[str]] = {}
    for key, entry in TAXONOMY.items():
        cat = entry["category"]
        groups.setdefault(cat, []).append(key)
    return groups


def parse_taxonomy_markdown(filepath: str | None = None) -> list[str]:
    """Extract section headings from the taxonomy Markdown file."""
    filepath = filepath or TAXONOMY_PATH
    headings: list[str] = []
    with open(filepath, encoding="utf-8") as fh:
        for line in fh:
            match = re.match(r"^(#{1,4})\s+(.*)", line)
            if match:
                headings.append(match.group(2).strip())
    return headings


if __name__ == "__main__":
    print("AI Failure Taxonomy Utility")
    print("=" * 40)
    taxonomy = load_taxonomy()
    print(f"Loaded {len(taxonomy)} failure categories.\n")

    for key, details in taxonomy.items():
        label = get_severity_label(details["default_severity"])
        print(f"  [{label}] {key}")
        print(f"    {details['description']}")
        print(f"    Risks: {', '.join(details['risks'])}")
        if details["subtypes"]:
            print(f"    Sub-types: {', '.join(details['subtypes'])}")
        print()

    print("Categories:")
    for cat, members in failures_by_category().items():
        print(f"  {cat}: {', '.join(members)}")
