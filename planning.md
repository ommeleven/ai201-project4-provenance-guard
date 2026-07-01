# Provenance Guard Planning

## Detection Signals

### Signal 1 – LLM Classification

Uses Groq Llama 3.3 to estimate whether text appears AI-generated.

Output:
- Score between 0 and 1

Strength:
- Captures semantic consistency.

Weakness:
- May overestimate polished human writing.

---

### Signal 2 – Stylometric Heuristics

Measures:

- Vocabulary diversity
- Sentence length variance
- Average sentence length

Output:
- Score between 0 and 1

Strength:
- Captures structural writing characteristics.

Weakness:
- Can misclassify poems or academic writing.

---

## Confidence Scoring

Final confidence:

65% LLM

35% Heuristics

Thresholds

Likely AI

0.75–1.0

Uncertain

0.45–0.74

Likely Human

0.00–0.44

---

## Transparency Labels

### High-confidence AI

Likely AI-generated (High Confidence)

Our system found strong evidence that this content was generated using AI.

---

### High-confidence Human

Likely Human-written (High Confidence)

Our system found strong evidence that this content was written by a human.

---

### Uncertain

Uncertain Attribution

The available evidence is mixed. We cannot confidently determine the origin of this content.

---

## Appeals Workflow

Creators submit:

- content_id
- reasoning

System:

- changes status to under_review
- records appeal
- stores creator reasoning

---

## Edge Cases

- Poems
- Song lyrics
- Technical documentation
- ESL writers

---

# Architecture

```
POST /submit
      │
      ▼
Groq Detector
      │
      ▼
Stylometric Detector
      │
      ▼
Confidence Calculator
      │
      ▼
Transparency Label
      │
      ▼
Audit Log
      │
      ▼
JSON Response

Appeal Flow

POST /appeal
      │
      ▼
Update Status
      │
      ▼
Audit Log
      │
      ▼
Response
```

Submission flows through two detectors before producing a confidence score and transparency label. Appeals update the content status to "under review" and are recorded in the audit log.

## AI Tool Plan

### Milestone 3
Generate the Flask app skeleton and first detection signal. Verify endpoint responses manually.

### Milestone 4
Generate the stylometric detector and confidence scoring. Test with clearly AI-generated and human-written examples.

### Milestone 5
Generate the transparency label logic and appeal endpoint. Verify all three label variants and appeal status updates.