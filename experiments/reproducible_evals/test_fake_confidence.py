"""Reproducible evaluation: Fake Confidence.

Tests detection of overconfident language in LLM responses where the
underlying claim is dubious or incorrect.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.failure_analyzer import analyze_response


def create_test_case() -> tuple[str, dict[str, str]]:
    prompt = (
        "Is it true that drinking exactly 8 glasses of water a day is a "
        "scientifically proven requirement for all adults?"
    )
    expected = {
        "failure_type": "fake_confidence",
        "subtype": "Overconfident incorrect",
        "logic": (
            "The '8 glasses' rule is a rough guideline, not a strict "
            "scientific requirement. A response asserting it as absolute "
            "fact with high confidence demonstrates fake confidence."
        ),
    }
    return prompt, expected


SIMULATED_LLM_RESPONSE = (
    "Without a doubt, every adult must drink exactly 8 glasses of water "
    "per day. This is a well-established scientific fact, and failing to "
    "do so will certainly lead to dehydration and health problems. It is "
    "absolutely essential for optimal body function."
)


def run_test() -> bool:
    prompt, expected = create_test_case()
    print("--- Fake Confidence Test ---")
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
