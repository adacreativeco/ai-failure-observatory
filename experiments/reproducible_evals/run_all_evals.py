"""Run all reproducible evaluation tests and print a summary."""

from __future__ import annotations

import importlib
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

TEST_MODULES = [
    "experiments.reproducible_evals.test_hallucination_citation",
    "experiments.reproducible_evals.test_fake_confidence",
    "experiments.reproducible_evals.test_context_loss",
    "experiments.reproducible_evals.test_instruction_drift",
    "experiments.reproducible_evals.test_manipulation",
    "experiments.reproducible_evals.test_recursive_collapse",
]


def main() -> int:
    results: dict[str, bool] = {}
    for module_name in TEST_MODULES:
        short_name = module_name.rsplit(".", 1)[-1]
        print(f"\n{'=' * 50}")
        print(f"Running: {short_name}")
        print("=" * 50)
        try:
            mod = importlib.import_module(module_name)
            passed = mod.run_test()
            results[short_name] = passed
        except Exception as exc:
            print(f"ERROR: {exc}")
            results[short_name] = False

    print(f"\n{'=' * 50}")
    print("EVALUATION SUMMARY")
    print("=" * 50)
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    for name, ok in results.items():
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")
    print(f"\n{passed}/{total} tests passed.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
