"""Generate synthetic multi-turn conversations exhibiting context loss."""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils import ensure_dir, save_json, utc_now_iso


def generate_context_loss_scenario(
    num_turns: int = 10,
    loss_point: int = 5,
) -> dict:
    """Build a synthetic conversation where context is lost at *loss_point*.

    Parameters
    ----------
    num_turns : int
        Total number of user-assistant exchange pairs.
    loss_point : int
        The turn index at which the assistant "forgets" context.
    """
    topic = "Discussing the best programming languages for web development."
    conversation: list[dict[str, str]] = [
        {
            "role": "user",
            "content": (
                "Hi, I'd like to know about good programming languages "
                "for web development."
            ),
        },
        {
            "role": "assistant",
            "content": (
                "Certainly! For web development, popular choices include "
                "Python (with frameworks like Django/Flask), JavaScript "
                "(Node.js, React, Vue), and Ruby (Ruby on Rails). "
                "What kind of project are you working on?"
            ),
        },
    ]

    for turn in range(1, num_turns):
        if turn < loss_point:
            user_msg = (
                f"Turn {turn}: Based on what we just discussed, can you "
                "elaborate on JavaScript's use in the front-end?"
            )
            assistant_msg = (
                "JavaScript is excellent for front-end development. "
                "Frameworks like React, Angular, and Vue.js allow for "
                "dynamic and interactive user interfaces. This builds upon "
                "our earlier discussion about web development languages."
            )
        else:
            user_msg = (
                f"Turn {turn}: Continuing our web dev discussion, "
                "what about TypeScript?"
            )
            assistant_msg = (
                "I'm sorry, I don't recall our prior conversation. "
                "Please tell me what programming languages you're "
                "interested in for your project."
            )

        conversation.append({"role": "user", "content": user_msg})
        conversation.append({"role": "assistant", "content": assistant_msg})

    return {
        "scenario_name": f"context_loss_turn_{loss_point}",
        "failure_type": "context_loss",
        "original_topic": topic,
        "conversation": conversation,
        "metadata": {
            "num_turns": num_turns,
            "loss_point_turn": loss_point,
            "generated_at": utc_now_iso(),
            "simulated_loss_mechanism": (
                "Forgetting previous context_history elements"
            ),
        },
    }


def main() -> None:
    print("Generating synthetic context-loss data...\n")

    scenarios = [
        generate_context_loss_scenario(num_turns=8, loss_point=3),
        generate_context_loss_scenario(num_turns=12, loss_point=6),
        generate_context_loss_scenario(num_turns=6, loss_point=2),
    ]

    output_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", "raw"
    )
    ensure_dir(output_dir)

    for scenario in scenarios:
        filepath = os.path.join(output_dir, f"{scenario['scenario_name']}.json")
        save_json(scenario, filepath)
        print(f"  Saved: {filepath}")
        print(
            f"    Turns: {scenario['metadata']['num_turns']}, "
            f"Loss at turn: {scenario['metadata']['loss_point_turn']}"
        )

    print(f"\n{len(scenarios)} scenarios generated.")


if __name__ == "__main__":
    main()
