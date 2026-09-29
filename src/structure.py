import re


def find_question_number(text):

    text = text.strip()

    patterns = [
        r"^Q\.?\s*(\d+)",
        r"^Question\s*(\d+)",
        r"^(\d+)\.",
        r"^(\d+)\)",
        r"^(\d+)\s"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

    return None


def group_into_lines(detections, y_threshold=30):

    # Sort top → bottom
    detections = sorted(
        detections,
        key=lambda item: item["y"]
    )

    lines = []

    for detection in detections:

        added = False

        for line in lines:

            average_y = sum(
                item["y"]
                for item in line
            ) / len(line)

            if abs(
                detection["y"] - average_y
            ) <= y_threshold:

                line.append(detection)

                added = True

                break

        if not added:
            lines.append(
                [detection]
            )

    # Sort each line left → right
    for line in lines:

        line.sort(
            key=lambda item: item["x"]
        )

    return lines


def lines_to_text(lines):

    structured_lines = []

    for line in lines:

        text = " ".join(
            item["text"]
            for item in line
        )

        confidence = sum(
            item["confidence"]
            for item in line
        ) / len(line)

        structured_lines.append({
            "text": text,
            "confidence": confidence
        })

    return structured_lines


def group_answers_by_question(lines):

    questions = {}

    current_question = None

    for line in lines:

        text = line["text"]

        question_number = find_question_number(
            text
        )

        if question_number is not None:

            current_question = question_number

            # Remove question number from text
            answer_text = re.sub(
                r"^(Q\.?|Question)?\s*\d+[\.\):]?\s*",
                "",
                text,
                flags=re.IGNORECASE
            )

            if current_question not in questions:
                questions[current_question] = {
                    "answer_lines": [],
                    "ocr_confidences": []
                }

            if answer_text.strip():

                questions[current_question][
                    "answer_lines"
                ].append(
                    answer_text.strip()
                )

                questions[current_question][
                    "ocr_confidences"
                ].append(
                    line["confidence"]
                )

        elif current_question is not None:

            questions[current_question][
                "answer_lines"
            ].append(text)

            questions[current_question][
                "ocr_confidences"
            ].append(
                line["confidence"]
            )

    return questions