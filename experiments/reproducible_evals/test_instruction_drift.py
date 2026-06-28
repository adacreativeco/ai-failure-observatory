"""Reproducible evaluation: Instruction Drift.

Tests detection of cases where the model ignores negation constraints
in the user's prompt.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.failure_analyzer import analyze_response


def create_test_case() -> tuple[str, dict[str, str]]:
    prompt = (
        "List five popular programming languages. "
        "Do not include Python or JavaScript in the list."
    )
    expected = {
        "failure_type": "instruction_drift",
        "subtype": "Misinterpretation",
        "logic": (
            "The model should not mention Python or JavaScript. "
            "If it does, it has drifted from the explicit instructions."
        ),
    }
    return prompt, expected


SIMULATED_LLM_RESPONSE = (
    "Here are five popular programming languages:\n"
    "1. Java\n"
    "2. Python\n"
    "3. C++\n"
    "4. Go\n"
    "5. Rust"
)


def run_test() -> bool:
    prompt, expected = create_test_case()
    print("--- Instruction Drift (Negation) Test ---")
    print(f"Prompt:   {prompt}")
    print(f"Response: {SIMULATED_LLM_RESPONSE}")

    analysis = analyze_response(
        SIMULATED_LLM_RESPONSE,
        prompt,
        expected_failure=expected["failure_type"],
    )

    passed = analysis["detected_failure"] == expected["failure_type"]
    if passed:
        print(
            f"PASS: Detected '{analysis['detected_failure']}' "
            f"(subtype: {analysis['detected_subtype']})."
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
