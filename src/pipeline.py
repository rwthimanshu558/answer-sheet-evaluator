import os
import json

from src.pdf_utils import pdf_to_images
from src.ocr import OCRProcessor
from src.structure import (
    group_into_lines,
    lines_to_text,
    group_answers_by_question
)
from src.scoring import AnswerScorer
from src.confidence import calculate_confidence


class AnswerSheetPipeline:

    def __init__(
        self,
        pdf_path,
        answer_key_path
    ):

        self.pdf_path = pdf_path
        self.answer_key_path = answer_key_path

        self.ocr = OCRProcessor()

        self.scorer = AnswerScorer(
            answer_key_path
        )

    def run(
        self,
        start_page=0,
        end_page=None
    ):

        print("\nSTEP 1: Converting PDF pages...\n")

        image_paths = pdf_to_images(
            self.pdf_path,
            "data/processed",
            start_page,
            end_page
        )

        all_questions = {}

        print("\nSTEP 2: Running OCR...\n")

        for image_path in image_paths:

            print(
                f"Processing: {image_path}"
            )

            detections = self.ocr.extract_text(
                image_path
            )

            lines = group_into_lines(
                detections
            )

            structured_lines = lines_to_text(
                lines
            )

            questions = group_answers_by_question(
                structured_lines
            )

            # Merge questions across pages
            for question_number, data in questions.items():

                if question_number not in all_questions:

                    all_questions[
                        question_number
                    ] = {
                        "answer_lines": [],
                        "ocr_confidences": []
                    }

                all_questions[
                    question_number
                ]["answer_lines"].extend(
                    data["answer_lines"]
                )

                all_questions[
                    question_number
                ]["ocr_confidences"].extend(
                    data["ocr_confidences"]
                )

        print("\nSTEP 3: Scoring answers...\n")

        final_results = []

        for question_number in sorted(
            all_questions.keys()
        ):

            data = all_questions[
                question_number
            ]

            answer = " ".join(
                data["answer_lines"]
            )

            score_data = self.scorer.score_answer(
                question_number,
                answer
            )

            confidence, reason = calculate_confidence(
                data["ocr_confidences"],
                score_data["similarities"],
                score_data["score"],
                score_data["max_score"]
            )

            result = {
                "question_no": question_number,
                "extracted_answer": answer,
                "score": score_data["score"],
                "max_score": score_data["max_score"],
                "confidence": confidence,
                "reason": reason
            }

            final_results.append(result)

        return final_results