def generate_label(confidence):

    if confidence >= 0.75:
        return (
            "likely_ai",
            "Likely AI-generated (High Confidence). "
            "Our system found strong evidence that this content was generated using AI."
        )

    elif confidence >= 0.45:
        return (
            "uncertain",
            "Uncertain Attribution. "
            "The available evidence is mixed, and we cannot confidently determine whether this content was written by AI or a human."
        )

    else:
        return (
            "likely_human",
            "Likely Human-written (High Confidence). "
            "Our system found strong evidence that this content was written by a human."
        )