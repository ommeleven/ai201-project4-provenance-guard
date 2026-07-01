# AI Provenance Guard

AI Provenance Guard is a Flask-based API that analyzes text submissions and estimates whether they are likely AI-generated or human-written. The system combines multiple detection signals, produces a confidence score, presents a user-friendly transparency label, supports creator appeals, applies rate limiting, and records every decision in a structured audit log.

---

# Features

- Multi-signal AI detection
- Confidence scoring
- Three transparency labels
- Appeals workflow
- Rate limiting
- Structured audit log
- REST API built with Flask

---

# Architecture Overview

## Submission Flow

```
POST /submit
        │
        ▼
LLM Detector (Groq)
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
```

## Appeal Flow

```
POST /appeal
       │
       ▼
Update Status
       │
       ▼
Audit Log
       │
       ▼
JSON Response
```

A text submission first passes through two independent detection signals. Their scores are combined into a confidence score, which determines the transparency label returned to the user. Every classification is recorded in the audit log. If a creator disputes the decision, an appeal updates the submission's status to **under_review** and records the creator's reasoning.

---

# Detection Signals

## Signal 1 — Groq LLM

The first detector uses the Groq API with the `llama-3.3-70b-versatile` model. The model evaluates the writing holistically and returns a probability between 0 and 1 that the text appears AI-generated.

**Captures**
- Overall writing style
- Semantic consistency
- AI-like phrasing

**Limitations**
- Formal human writing may resemble AI-generated content.

---

## Signal 2 — Stylometric Heuristics

The second detector measures structural properties of the writing.

Metrics used:

- Sentence length variance
- Average sentence length
- Type-token ratio (vocabulary diversity)

These metrics are combined into a heuristic score between 0 and 1.

**Captures**
- Structural consistency
- Vocabulary diversity
- Sentence variation

**Limitations**
- Poems, song lyrics, technical writing, and ESL writing may produce misleading scores.

---

# Confidence Scoring

The final confidence score combines both detection signals.

```
Confidence =
0.65 × LLM Score +
0.35 × Heuristic Score
```

Thresholds:

| Confidence | Result |
|------------|---------|
| 0.75 – 1.00 | Likely AI |
| 0.45 – 0.74 | Uncertain |
| 0.00 – 0.44 | Likely Human |

This design intentionally avoids forcing uncertain cases into a binary decision, reducing the chance of falsely labeling human-written content as AI-generated.

---

# Example Confidence Scores

### Example 1

Input:

```
Artificial intelligence represents a transformative paradigm shift...
```

Result

```
LLM Score: 0.89
Heuristic Score: 0.76
Confidence: 0.84

Likely AI
```

---

### Example 2

Input

```
ok so i finally tried that ramen place downtown...
```

Result

```
LLM Score: 0.28
Heuristic Score: 0.34
Confidence: 0.30

Likely Human
```

These examples demonstrate meaningful variation rather than producing nearly identical scores for all inputs.

---

# Transparency Labels

## High-Confidence AI

> **Likely AI-generated (High Confidence)**  
> Our system found strong evidence that this content was generated using AI.

---

## High-Confidence Human

> **Likely Human-written (High Confidence)**  
> Our system found strong evidence that this content was written by a human.

---

## Uncertain

> **Uncertain Attribution**  
> The available evidence is mixed. We cannot confidently determine whether this content was written by AI or a human.

---

# API Endpoints

## POST /submit

Request

```json
{
  "creator_id":"user1",
  "text":"Hello world"
}
```

Response

```json
{
  "content_id":"uuid",
  "llm_score":0.82,
  "heuristic_score":0.67,
  "confidence":0.77,
  "attribution":"likely_ai",
  "label":"Likely AI-generated (High Confidence)...",
  "status":"classified"
}
```

---

## POST /appeal

Request

```json
{
  "content_id":"uuid",
  "creator_reasoning":"I wrote this from personal experience."
}
```

Response

```json
{
  "status":"under_review"
}
```

---

## GET /log

Returns all audit log entries.

---

# Appeals Workflow

Creators may challenge a classification by submitting:

- content_id
- creator_reasoning

The system:

- updates the content status to **under_review**
- records the appeal reasoning
- preserves the original classification
- stores the updated record in the audit log

No automatic reclassification occurs.

---

# Rate Limiting

Limits used:

```
10 requests per minute
100 requests per day
```

These values allow normal use by writers while limiting automated abuse.

Example test output:

```
200
200
200
200
200
200
200
200
200
200
429
429
```

The final two requests exceed the configured rate limit.

---

# Audit Log

Each decision records:

- timestamp
- creator_id
- content_id
- LLM score
- heuristic score
- confidence score
- attribution
- transparency label
- status
- appeal reasoning (if applicable)

Example:

```json
{
  "content_id":"...",
  "creator_id":"om",
  "llm_score":0.81,
  "heuristic_score":0.60,
  "confidence":0.74,
  "status":"under_review",
  "appeal_reasoning":"I wrote this myself."
}
```

The project should include at least three entries in `audit_log.json`.

---

# Known Limitations

This detector is not perfect.

Potential failure cases include:

- Poetry
- Song lyrics
- Technical documentation
- Very short text
- ESL writing
- Highly edited AI-generated text

These styles may resemble AI or human writing depending on the detector being used.

---

# Spec Reflection

Creating the planning document before implementation clarified how each component should interact and helped define confidence thresholds before writing code.

One implementation change from the original plan was using a JSON audit log instead of SQLite. JSON simplified development while still satisfying the structured logging requirement.

---

# AI Usage

## Instance 1

Used AI to generate the initial Flask application structure and API endpoints.

Revisions:
- Added audit logging
- Adjusted endpoint responses
- Added rate limiting

---

## Instance 2

Used AI to generate the stylometric heuristic function.

Revisions:
- Simplified the scoring logic
- Changed weighting of sentence variance and vocabulary diversity
- Updated confidence calculation to better match project thresholds

---

# Installation

```bash
git clone <repository-url>

cd ai201-project4-provenance-guard

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file.

```
GROQ_API_KEY=YOUR_API_KEY
```

Run

```bash
python app.py
```

---

# Technologies

- Python
- Flask
- Flask-Limiter
- Groq API
- python-dotenv
- JSON Audit Logging

---

# Future Improvements

- Additional detection signals
- Better confidence calibration
- SQLite/PostgreSQL storage
- User authentication
- Web dashboard
- Human reviewer interface
- Multi-modal detection
