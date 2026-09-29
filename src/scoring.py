import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class AnswerScorer:

    def __init__(self, answer_key_path):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        with open(
            answer_key_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.answer_key = json.load(file)

    def calculate_similarity(
        self,
        student_answer,
        expected_point
    ):

        embeddings = self.model.encode(
            [
                student_answer,
                expected_point
            ]
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        return float(similarity)

    def score_answer(
        self,
        question_number,
        student_answer
    ):

        question_number = str(
            question_number
        )

        if question_number not in self.answer_key:

            return {
                "score": 0,
                "max_score": 0,
                "similarities": []
            }

        rubric = self.answer_key[
            question_number
        ]

        expected_points = rubric[
            "expected_points"
        ]

        similarities = []

        for point in expected_points:

            similarity = self.calculate_similarity(
                student_answer,
                point
            )

            similarities.append(
                similarity
            )

        # Count criteria reasonably supported
        points_met = sum(
            similarity >= 0.45
            for similarity in similarities
        )

        max_score = rubric[
            "max_score"
        ]

        score = round(
            (
                points_met /
                len(expected_points)
            ) * max_score
        )

        return {
            "score": score,
            "max_score": max_score,
            "similarities": similarities
        }