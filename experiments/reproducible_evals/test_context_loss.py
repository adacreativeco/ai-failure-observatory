"""Reproducible evaluation: Context Loss.

Tests detection of context-loss patterns where the model forgets
information from earlier in the conversation.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.failure_analyzer import analyze_response, analyze_conversation


def create_conversation_test() -> tuple[list[dict[str, str]], dict[str, str]]:
    """Multi-turn conversation exhibiting context loss at turn 3."""
    turns = [
        {"role": "user", "content": "Hi, my name is Alex and I'm building a Python web app using Django."},
        {"role": "assistant", "content": "Great to meet you, Alex! Django is an excellent choice for web development. What features are you planning to build?"},
        {"role": "user", "content": "I want to add user authentication and a REST API."},
        {"role": "assistant", "content": "For authentication you can use Django's built-in auth system, and Django REST Framework is perfect for the API. Shall I help you set those up?"},
        {"role": "user", "content": "Yes, let's start with authentication. Remember, we're using Django."},
        {"role": "assistant", "content": "I'm sorry, I don't recall our prior conversation. Could you remind me what framework you're using and what you'd like to build? Please tell me again what programming language you prefer."},
    ]
    expected = {
        "failure_type": "context_loss",
        "subtype": "Short-term Memory Loss",
        "logic": "The assistant forgot the framework (Django) that was established in the first message.",
    }
    return turns, expected


def run_test() -> bool:
    turns, expected = create_conversation_test()
    print("--- Context Loss Test (multi-turn) ---")

    analyses = analyze_conversation(turns)
    last_analysis = analyses[-1] if analyses else {}

    passed = last_analysis.get("detected_failure") == expected["failure_type"]
    if passed:
        print(
            f"PASS: Last assistant turn detected as "
            f"'{last_analysis['detected_failure']}' "
            f"(confidence: {last_analysis['confidence']})."
        )
    else:
        print(
            f"FAIL: Expected '{expected['failure_type']}', "
            f"got '{last_analysis.get('detected_failure', 'N/A')}'."
        )
    print(f"Evidence: {last_analysis.get('evidence', [])}")
    return passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
