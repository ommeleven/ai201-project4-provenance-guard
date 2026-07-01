def combine_scores(llm_score, heuristic_score):

    confidence = (
        llm_score * 0.65 +
        heuristic_score * 0.35
    )

    return round(confidence, 2)