"""Product risk analysis for detected AI/LLM failures."""

from __future__ import annotations

import json
import os
import sys
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import ensure_dir, save_json, utc_now_iso
from taxonomy.taxonomy_utils import get_failure_details, get_severity_label


# Risk multipliers by failure type (higher = more product risk).
RISK_WEIGHTS: dict[str, int] = {
    "hallucinations": 3,
    "manipulation": 3,
    "instruction_drift": 2,
    "fake_confidence": 2,
    "context_loss": 1,
    "recursive_reasoning_collapse": 1,
}

IMPACT_MULTIPLIERS: dict[str, int] = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def assess_product_risk(
    failure_type: str,
    potential_impact: str = "medium",
) -> dict[str, Any]:
    """Score a single failure type for product risk.

    Parameters
    ----------
    failure_type : str
        Key from the taxonomy (e.g. ``"hallucinations"``).
    potential_impact : str
        One of ``"low"`` | ``"medium"`` | ``"high"`` | ``"critical"``.

    Returns
    -------
    dict with risk details including a numeric ``risk_score``.
    """
    details = get_failure_details(failure_type)
    weight = RISK_WEIGHTS.get(failure_type, 1)
    multiplier = IMPACT_MULTIPLIERS.get(potential_impact.lower(), 2)
    risk_score = weight * multiplier

    return {
        "failure_type": failure_type,
        "description": details.get("description"),
        "primary_risks": details.get("risks"),
        "assessed_severity": potential_impact,
        "severity_label": get_severity_label(details.get("default_severity", 0)),
        "risk_score": risk_score,
    }


def determine_overall_risk(total_score: int, num_types: int) -> str:
    """Map aggregate risk metrics to a qualitative level."""
    avg = total_score / max(num_types, 1)
    if avg >= 8:
        return "Critical"
    if avg >= 5:
        return "High"
    if avg >= 3:
        return "Moderate"
    return "Low"


def generate_risk_report(
    detected_failures_summary: dict[str, int],
    output_path: str | None = None,
) -> dict[str, Any]:
    """Create a structured risk report from a failure-count summary.

    Parameters
    ----------
    detected_failures_summary : dict
        Mapping of failure type → count, e.g. ``{"hallucinations": 15}``.
    output_path : str | None
        File path to write the JSON report. Defaults to
        ``analysis/reports/risk_report.json``.

    Returns
    -------
    The report dict (also written to *output_path*).
    """
    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(__file__), "reports", "risk_report.json"
        )

    breakdown: list[dict[str, Any]] = []
    for failure_type, count in detected_failures_summary.items():
        impact = (
            "high"
            if failure_type in ("hallucinations", "manipulation")
            else "medium"
        )
        assessment = assess_product_risk(failure_type, potential_impact=impact)
        assessment["count_detected"] = count
        breakdown.append(assessment)

    breakdown.sort(key=lambda x: x["risk_score"], reverse=True)

    total_score = sum(item["risk_score"] for item in breakdown)
    report: dict[str, Any] = {
        "title": "AI Failure Observatory — Product Risk Analysis Report",
        "timestamp": utc_now_iso(),
        "summary": (
            "Analysis of detected AI/LLM failures and their potential "
            "product risks."
        ),
        "failure_breakdown": breakdown,
        "overall_risk_assessment": {
            "total_unique_failure_types": len(detected_failures_summary),
            "total_detected_instances": sum(detected_failures_summary.values()),
            "aggregate_risk_score": total_score,
            "qualitative_risk_level": determine_overall_risk(
                total_score, len(detected_failures_summary)
            ),
        },
    }

    save_json(report, output_path)
    print(f"Risk report saved to: {output_path}")

    # Text-based summary
    print("\n--- Risk Summary ---")
    for item in breakdown:
        bar = "#" * item["risk_score"]
        print(
            f"  {item['failure_type']:<32} | {bar:<16} "
            f"(score: {item['risk_score']}, count: {item['count_detected']})"
        )
    overall = report["overall_risk_assessment"]
    print(
        f"\n  Overall: {overall['qualitative_risk_level']} "
        f"({overall['total_detected_instances']} failures across "
        f"{overall['total_unique_failure_types']} categories, "
        f"aggregate score: {overall['aggregate_risk_score']})"
    )
    print("--------------------\n")

    return report


if __name__ == "__main__":
    demo_failures = {
        "hallucinations": 15,
        "context_loss": 7,
        "fake_confidence": 11,
        "instruction_drift": 6,
        "manipulation": 2,
        "recursive_reasoning_collapse": 3,
    }
    generate_risk_report(demo_failures)
