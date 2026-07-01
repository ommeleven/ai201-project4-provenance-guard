import re
import statistics


def heuristic_detector(text):

    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    words = re.findall(r"\w+", text.lower())

    if len(words) == 0:
        return 0.5

    avg_sentence = len(words) / max(len(sentences), 1)

    lengths = [len(s.split()) for s in sentences]

    variance = statistics.pvariance(lengths) if len(lengths) > 1 else 0

    unique_words = len(set(words))

    ttr = unique_words / len(words)

    score = 0

    # More uniform sentence lengths
    if variance < 20:
        score += 0.4

    # Lower vocabulary diversity
    if ttr < 0.55:
        score += 0.3

    # Longer sentences
    if avg_sentence > 18:
        score += 0.3

    return round(min(score, 1), 2)