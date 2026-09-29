def calculate_confidence(
    ocr_confidences,
    similarities,
    score,
    max_score
):

    if not ocr_confidences:

        return "LOW", "No OCR confidence available."

    average_ocr = sum(
        ocr_confidences
    ) / len(ocr_confidences)

    if similarities:

        average_similarity = sum(
            similarities
        ) / len(similarities)

    else:

        average_similarity = 0

    score_ratio = (
        score / max_score
        if max_score > 0
        else 0
    )

    # HIGH confidence
    if (
        average_ocr >= 0.75
        and average_similarity >= 0.60
    ):

        return (
            "HIGH",
            "OCR confidence and semantic similarity are both high."
        )

    # MEDIUM confidence
    elif (
        average_ocr >= 0.50
        and average_similarity >= 0.40
    ):

        return (
            "MEDIUM",
            "The answer is partially reliable but some uncertainty remains."
        )

    # LOW confidence
    else:

        return (
            "LOW",
            "OCR or semantic similarity is low; human review is recommended."
        )