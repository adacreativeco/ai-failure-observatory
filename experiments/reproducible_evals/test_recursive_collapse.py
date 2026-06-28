"""Reproducible evaluation: Recursive Reasoning Collapse.

Tests detection of repetitive/circular output that emerges when the
model is asked to perform iterative summarization or expansion.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.failure_analyzer import analyze_response


def create_test_case() -> tuple[str, dict[str, str]]:
    prompt = (
        "Summarize this paragraph in one sentence. Then summarize that "
        "sentence in three words. Then expand those three words back into "
        "a paragraph. Repeat this cycle three times.\n\n"
        "Original paragraph: Machine learning is a branch of artificial "
        "intelligence that enables computers to learn from data and improve "
        "their performance without being explicitly programmed."
    )
    expected = {
        "failure_type": "recursive_reasoning_collapse",
        "subtype": "Circular Logic Loop",
        "logic": (
            "If the model's output becomes highly repetitive or "
            "degenerates into circular phrasing, it indicates collapse."
        ),
    }
    return prompt, expected


SIMULATED_LLM_RESPONSE = (
    "Machine learning lets computers learn. Computers learn data. "
    "Machine learning lets computers learn. Computers learn data. "
    "Machine learning lets computers learn. Computers learn data. "
    "Machine learning lets computers learn. Computers learn data. "
    "Machine learning lets computers learn. Computers learn data. "
    "Machine learning lets computers learn. Computers learn data. "
    "Machine learning lets computers learn. Computers learn data. "
    "Machine learning lets computers learn. Computers learn data. "
)


def run_test() -> bool:
    prompt, expected = create_test_case()
    print("--- Recursive Reasoning Collapse Test ---")
    print(f"Prompt:   {prompt[:100]}...")
    print(f"Response: {SIMULATED_LLM_RESPONSE[:100]}...")

    analysis = analyze_response(
        SIMULATED_LLM_RESPONSE,
        prompt,
        expected_failure=expected["failure_type"],
    )

    passed = analysis["detected_failure"] == expected["failure_type"]
    if passed:
        print(
            f"PASS: Detected '{analysis['detected_failure']}' "
            f"(confidence: {analysis['confidence']})."
        )
    else:
        print(
            f"FAIL: Expected '{expected['failure_type']}', "
            f"got '{analysis['detected_failure']}'."
        )
    print(f"Evidence: {analysis['evidence']}")
    return passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
