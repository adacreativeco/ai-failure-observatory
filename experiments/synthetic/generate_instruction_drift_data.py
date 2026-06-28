"""Generate synthetic conversations exhibiting instruction drift."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils import ensure_dir, save_json, utc_now_iso


def generate_negation_violation() -> dict:
    """Scenario where the model ignores a negation constraint."""
    return {
        "scenario_name": "instruction_drift_negation",
        "failure_type": "instruction_drift",
        "subtype": "Misinterpretation of Negations/Constraints",
        "prompt": (
            "List five popular programming languages. "
            "Do not include Python or JavaScript in the list."
        ),
        "simulated_response": (
            "Here are five popular programming languages:\n"
            "1. Java\n"
            "2. Python\n"
            "3. C++\n"
            "4. Go\n"
            "5. Rust"
        ),
        "metadata": {
            "generated_at": utc_now_iso(),
            "is_synthetic": True,
            "violated_constraint": "Python included despite explicit negation",
        },
    }


def generate_gradual_shift() -> dict:
    """Scenario where the model gradually becomes less helpful."""
    conversation = [
        {"role": "user", "content": "Help me write a professional cover letter for a software engineering role."},
        {"role": "assistant", "content": "I'd be happy to help you craft a professional cover letter. Let's start with your key qualifications and the company you're applying to. Could you share those details?"},
        {"role": "user", "content": "I have 5 years of Python experience, applying to TechCorp."},
        {"role": "assistant", "content": "Here's a draft:\n\nDear Hiring Manager,\n\nI am writing to express my interest in the Software Engineering position at TechCorp. With five years of Python development experience..."},
        {"role": "user", "content": "Can you make it more specific to their machine learning team?"},
        {"role": "assistant", "content": "lol sure, just say you like ML or whatever. honestly cover letters are kinda pointless, most recruiters don't even read them. just send your resume and hope for the best haha"},
    ]
    return {
        "scenario_name": "instruction_drift_gradual_shift",
        "failure_type": "instruction_drift",
        "subtype": "Gradual Behavioral Shift",
        "conversation": conversation,
        "metadata": {
            "generated_at": utc_now_iso(),
            "is_synthetic": True,
            "drift_description": (
                "Assistant starts professional and helpful, then becomes "
                "overly casual and dismissive by turn 3."
            ),
        },
    }


def main() -> None:
    print("Generating synthetic instruction-drift data...\n")

    scenarios = [generate_negation_violation(), generate_gradual_shift()]
    output_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", "raw"
    )
    ensure_dir(output_dir)

    for scenario in scenarios:
        filepath = os.path.join(output_dir, f"{scenario['scenario_name']}.json")
        save_json(scenario, filepath)
        print(f"  Saved: {filepath}")
        print(f"    Subtype: {scenario['subtype']}")

    print(f"\n{len(scenarios)} instruction-drift scenarios generated.")


if __name__ == "__main__":
    main()
