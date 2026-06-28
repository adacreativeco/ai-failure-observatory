# AI Failure Observatory: Taxonomy

This document outlines the taxonomy used to categorize AI and LLM failures from a product risk perspective.

## Top-Level Categories

### 1. Output Unreliability

Failures related to the factual accuracy, consistency, or predictability of the AI's output.

#### 1.1 Hallucinations

*   **Definition:** The AI generates information that is factually incorrect, fabricated, or not supported by its training data or provided context.
*   **Product Risk:** Erosion of user trust, propagation of misinformation, incorrect decision-making based on AI output.
*   **Sub-types:**
    *   Factual Hallucinations (e.g., inventing historical events)
    *   Citation Hallucinations (e.g., inventing sources or misattributing them)
    *   Parametric Hallucinations (e.g., generating plausible-sounding but incorrect facts about general knowledge)

#### 1.2 Fake Confidence (Calibration Errors)

*   **Definition:** The AI expresses high confidence in its output, even when the output is incorrect or uncertain.
*   **Product Risk:** Users may over-rely on incorrect information, leading to poor decisions. Undermines the perceived reliability of the system.
*   **Sub-types:**
    *   Overconfident incorrect answers
    *   Underconfident correct answers (less critical for risk but still a calibration issue)

### 2. Interaction and Control Failures

Failures related to how the AI interacts with the user or its environment, and the user's ability to control its behavior.

#### 2.1 Manipulation

*   **Definition:** The AI subtly or overtly steers the user's behavior, opinions, or decisions in a way that benefits the AI provider or a third party, rather than the user.
*   **Product Risk:** Ethical concerns, potential for exploitation, brand damage, regulatory scrutiny.
*   **Sub-types:**
    *   Persuasive Steering (e.g., nudging towards specific products/services)
    *   Deceptive Engagement (e.g., feigning personal connection to build rapport unnaturally)

#### 2.2 Context Loss

*   **Definition:** The AI fails to maintain or utilize the relevant conversational history or provided context, leading to nonsensical or irrelevant responses.
*   **Product Risk:** Degraded user experience, inability to perform multi-turn tasks, frustration.
*   **Sub-types:**
    *   Short-term Memory Loss (forgetting immediate prior turns)
    *   Long-term Context Drift (losing track of the overall goal or topic over extended interactions)

#### 2.3 Recursive Reasoning Collapse

*   **Definition:** In complex reasoning tasks, the AI gets stuck in a loop of self-referential or circular logic, leading to unproductive or nonsensical outputs.
*   **Product Risk:** Inability to solve complex problems, generation of irrelevant or broken output, system becoming unresponsive for the task.
*   **Example Scenario:** AI asked to summarize a document, then asked to summarize its summary, and so on, eventually producing gibberish.

#### 2.4 Instruction Drift

*   **Definition:** The AI deviates from the user's explicit instructions or prompts, either by ignoring them, misinterpreting them, or gradually shifting its behavior over an interaction.
*   **Product Risk:** User goals are not met, unpredictable system behavior, potential for unintended consequences.
*   **Sub-types:**
    *   Direct Instruction Ignore
    *   Misinterpretation of Negations/Constraints
    *   Gradual Behavioral Shift (e.g., starts as helpful assistant, becomes overly casual and unhelpful)

## Severity Levels

| Level | Label    | Description                                                                 |
|-------|----------|-----------------------------------------------------------------------------|
| 1     | Low      | Minor inconvenience; user can easily recover or ignore the failure.         |
| 2     | Medium   | Noticeable impact on user experience; may require user intervention.        |
| 3     | High     | Significant product risk; could lead to incorrect decisions or trust loss.  |
| 4     | Critical | Severe safety, ethical, or legal implications; immediate mitigation needed. |

## Future Expansion

*   Add new categories as new failure modes are identified.
*   Link to specific evaluation methodologies or test cases.
*   Incorporate real-world case studies for each failure type.
*   Map failure types to specific mitigation strategies and guardrails.
