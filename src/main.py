import json
import os

from src.pipeline import AnswerSheetPipeline


PDF_PATH = "data/input/English_Core.pdf"
ANSWER_KEY_PATH = "answer_key.json"

OUTPUT_PATH = "output/evaluation_results.json"


def main():

    print("=" * 60)
    print("AI/ML ANSWER SHEET EVALUATION")
    print("=" * 60)

    pipeline = AnswerSheetPipeline(
        PDF_PATH,
        ANSWER_KEY_PATH
    )

    # For the first test, process only pages 20-23.
    #
    # Python indexing:
    # page 20 = index 19
    # page 23 = index 22
    #
    # These pages are useful for testing our long-answer
    # / continuation handling.

    results = pipeline.run(
        start_page=19,
        end_page=23
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60)

    print(
        f"\nResults saved to: {OUTPUT_PATH}"
    )

    for result in results:

        print("\nQuestion:",
              result["question_no"])

        print(
            "Score:",
            f"{result['score']}/{result['max_score']}"
        )

        print(
            "Confidence:",
            result["confidence"]
        )


if __name__ == "__main__":
    main()