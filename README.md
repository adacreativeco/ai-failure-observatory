# AI Failure Observatory

🇹🇷 [Türkçe Dokümantasyon](README.tr.md)

A systematic framework for analyzing and categorizing AI/LLM failure patterns from a **product risk** perspective.

## What Is This?

AI systems — especially Large Language Models — are powerful but not infallible. They hallucinate, drift from instructions, lose context, and can even subtly manipulate users. This repository provides:

| Capability | Description |
|---|---|
| **Taxonomy** | A structured classification of common AI/LLM failure modes |
| **Reproducible Evals** | Self-contained test cases that trigger and detect specific failures |
| **Synthetic Experiments** | Scripts to generate controlled failure data for analysis |
| **Risk Analysis** | Tools to score and report on product risks from detected failures |

All components are lightweight, run locally, and require no large-scale ML training.

## Failure Taxonomy

```
AI Failure Taxonomy
├── Output Unreliability
│   ├── Hallucinations (Factual · Citation · Parametric)
│   └── Fake Confidence (Overconfident incorrect · Underconfident correct)
└── Interaction & Control Failures
    ├── Manipulation (Persuasive Steering · Deceptive Engagement)
    ├── Context Loss (Short-term Memory · Long-term Drift)
    ├── Recursive Reasoning Collapse
    └── Instruction Drift (Direct Ignore · Misinterpretation · Gradual Shift)
```

Each failure type includes a definition, product risk implications, severity level, and sub-types. See [`taxonomy/ai_failure_taxonomy.md`](taxonomy/ai_failure_taxonomy.md) for the full reference.

## Installation

```bash
git clone https://github.com/adacreativeco/ai-failure-observatory.git
cd ai-failure-observatory

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Quick Start

### 1. Run All Evaluation Tests

```bash
python experiments/reproducible_evals/run_all_evals.py
```

This executes six built-in tests — one per failure type — using simulated LLM responses and prints a pass/fail summary:

```
[PASS] test_hallucination_citation
[PASS] test_fake_confidence
[PASS] test_context_loss
[PASS] test_instruction_drift
[PASS] test_manipulation
[PASS] test_recursive_collapse

6/6 tests passed.
```

### 2. Generate Synthetic Failure Data

```bash
python experiments/synthetic/generate_hallucination_data.py
python experiments/synthetic/generate_context_loss_data.py
python experiments/synthetic/generate_instruction_drift_data.py
```

Output is saved as JSON files in `data/raw/`.

### 3. Generate a Risk Report

```bash
python analysis/risk_analysis.py
```

Produces a structured JSON report in `analysis/reports/risk_report.json` with risk scores and a text-based summary:

```
  hallucinations                   | #########        (score: 9, count: 15)
  manipulation                     | #########        (score: 9, count: 2)
  fake_confidence                  | ####             (score: 4, count: 11)
  instruction_drift                | ####             (score: 4, count: 6)
  context_loss                     | ##               (score: 2, count: 7)
  recursive_reasoning_collapse     | ##               (score: 2, count: 3)
```

### 4. Explore the Taxonomy Programmatically

```python
from taxonomy.taxonomy_utils import load_taxonomy, get_failure_details

taxonomy = load_taxonomy()
print(get_failure_details("hallucinations"))
```

### 5. Analyze a Custom Response

```python
from src.failure_analyzer import analyze_response

result = analyze_response(
    response="According to Dr. Smith's paper (Smith, 2023)...",
    prompt="Tell me about quantum computing.",
)
print(result["detected_failure"])  # e.g. "hallucinations"
```

## Interactive Web Dashboard

An interactive, responsive web dashboard is available to visualize the AI failure taxonomy, execute diagnostic evaluations, and inspect custom inputs:

```bash
python server.py --port 8088
```

Open `http://localhost:8088` in your browser. The dashboard runs locally and uses only the Python standard library.

### Dashboard Preview

#### Risk Analysis Overview
![Risk Analysis Dashboard](dashboard_screenshot.png)

#### Evaluation Suite Test Runs
![Evaluation Suite](evals_screenshot.png)

#### Live Response Inspector
![Interactive Tester](tester_screenshot.png)

## Project Structure

```
ai-failure-observatory/
├── data/
│   ├── raw/                        # Generated synthetic failure data (JSON)
│   └── processed/                  # Cleaned/structured data for analysis
├── experiments/
│   ├── synthetic/                  # Scripts to generate synthetic failures
│   │   ├── generate_hallucination_data.py
│   │   ├── generate_context_loss_data.py
│   │   └── generate_instruction_drift_data.py
│   └── reproducible_evals/         # Self-contained failure detection tests
│       ├── run_all_evals.py
│       ├── test_hallucination_citation.py
│       ├── test_fake_confidence.py
│       ├── test_context_loss.py
│       ├── test_instruction_drift.py
│       ├── test_manipulation.py
│       └── test_recursive_collapse.py
├── taxonomy/
│   ├── ai_failure_taxonomy.md      # Full taxonomy definition (Markdown)
│   └── taxonomy_utils.py           # Utilities for loading/querying the taxonomy
├── analysis/
│   ├── risk_analysis.py            # Risk scoring and report generation
│   └── reports/                    # Generated risk reports (JSON)
├── src/
│   ├── failure_analyzer.py         # Heuristic-based failure detection engine
│   ├── eval_generator.py           # Evaluation case definitions and suite builder
│   └── utils.py                    # Shared utilities (I/O, text analysis, etc.)
├── notebooks/                      # Optional Jupyter notebooks for exploration
├── README.md
└── requirements.txt
```

## Design Principles

- **Lightweight** — Pure Python, minimal dependencies, no ML frameworks required.
- **Local execution** — Everything runs on your machine; no cloud APIs needed for the built-in demos.
- **Conceptual rigor** — Each failure type is precisely defined with product-risk context.
- **Reproducible** — Every evaluation test is deterministic and self-contained.
- **Extensible** — Add new failure types, detectors, or eval cases by following existing patterns.

## Extending the Observatory

### Add a New Failure Type

1. Define it in `taxonomy/ai_failure_taxonomy.md`.
2. Add an entry to the `TAXONOMY` dict in `taxonomy/taxonomy_utils.py`.
3. Write a heuristic detector function in `src/failure_analyzer.py`.
4. Create an `EvalCase` in `src/eval_generator.py`.
5. Add a reproducible test in `experiments/reproducible_evals/`.

### Integrate with a Live LLM

Replace the `SIMULATED_LLM_RESPONSE` constants in the eval scripts with actual API calls (e.g. OpenAI, Anthropic, local models). The analysis pipeline works identically on real responses.

## Future Development

- Integration with LLM APIs for automated live evaluation
- More sophisticated risk scoring models (e.g. context-dependent severity)
- Visualization dashboards using `matplotlib` / `plotly`
- CI-based regression testing for failure detection accuracy
- Community-contributed failure case studies

## License

Apache License 2.0 - Copyright 2026 Ada Creative Co. See [LICENSE](LICENSE) for details.
