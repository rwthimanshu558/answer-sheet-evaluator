# AI/ML Engineer -- Handwritten Answer Sheet Evaluation

An AI/ML pipeline that extracts handwritten answers from scanned answer
sheets, structures them by question number, evaluates them against a
custom answer key/rubric using semantic similarity, and assigns an
evaluation confidence level.

## Project Overview

The system is designed to automate the basic workflow of answer-sheet
evaluation:

``` text
Handwritten Answer Sheet
          ↓
      PDF → Images
          ↓
       EasyOCR
          ↓
 Text + Bounding Boxes
          ↓
     Line Grouping
          ↓
 Question Detection
          ↓
 Answer Reconstruction
          ↓
 Semantic Similarity
          ↓
       Scoring
          ↓
 Confidence + Human Review Flag
          ↓
      JSON Results
```

The project uses a pretrained OCR engine and a pretrained
sentence-embedding model. No custom ML model is trained from scratch.

## Key Features

-   Converts PDF answer sheets into page images.
-   Extracts text using EasyOCR.
-   Captures OCR confidence and text bounding boxes.
-   Groups OCR detections into approximate handwritten lines.
-   Detects question numbers using layout/text patterns.
-   Groups answer lines under their corresponding question.
-   Supports answers that continue across multiple processed pages by
    merging question data.
-   Uses semantic similarity instead of simple keyword matching for
    rubric evaluation.
-   Produces a score and maximum score for each evaluated question.
-   Assigns `HIGH`, `MEDIUM`, or `LOW` confidence.
-   Provides a reason for the confidence level.
-   Saves final results as JSON for further analysis.

## Technologies Used

-   Python
-   EasyOCR
-   PyMuPDF
-   OpenCV
-   NumPy
-   Pandas
-   scikit-learn
-   Sentence Transformers
-   PyTorch

## Project Structure

``` text
answer-sheet-evaluator/
│
├── data/
│   ├── input/
│   │   └── English_Core.pdf
│   └── processed/
│
├── output/
│   └── evaluation_results.json
│
├── src/
│   ├── __init__.py
│   ├── pdf_utils.py
│   ├── ocr.py
│   ├── structure.py
│   ├── scoring.py
│   ├── confidence.py
│   └── pipeline.py
│
├── answer_key.json
├── main.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd answer-sheet-evaluator
```

### 2. Create a virtual environment

Windows:

``` bash
python -m venv .venv
```

Activate it:

``` bash
.venv\Scripts\activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

If `requirements.txt` has not been created yet:

``` bash
pip install easyocr pymupdf opencv-python pillow numpy pandas scikit-learn sentence-transformers torch torchvision
```

## Input Data

Place the handwritten answer-sheet PDF inside:

``` text
data/input/
```

Example:

``` text
data/input/English_Core.pdf
```

The current project uses a handwritten English answer sheet as the
primary test dataset.

## Answer Key and Rubric

The file:

``` text
answer_key.json
```

contains the custom evaluation rubric.

Example:

``` json
{
    "12": {
        "max_score": 5,
        "expected_points": [
            "identifies the central difficulty faced by the characters",
            "explains the challenges or obstacles",
            "explains determination or efforts",
            "provides a relevant comparison",
            "gives a clear overall interpretation"
        ]
    }
}
```

The rubric is a project-defined evaluation rubric and should not be
presented as an official examination marking scheme unless independently
verified.

## Running the Project

From the project root:

``` bash
python main.py
```

If `main.py` is currently inside `src/`, run:

``` bash
python -m src.main
```

The pipeline processes the configured page range in `main.py`.

For example:

``` python
results = pipeline.run(
    start_page=19,
    end_page=23
)
```

Python uses zero-based page indexing, so:

``` text
start_page=19 → PDF page 20
end_page=23   → processes pages 20–23
```

## Output

The final evaluation results are saved to:

``` text
output/evaluation_results.json
```

Example:

``` json
[
    {
        "question_no": 12,
        "extracted_answer": "The extracted handwritten answer...",
        "score": 4,
        "max_score": 5,
        "confidence": "MEDIUM",
        "reason": "The answer is partially reliable but some uncertainty remains."
    }
]
```

### Output Fields

  Field                Description
  -------------------- ----------------------------------------
  `question_no`        Detected question number
  `extracted_answer`   OCR-extracted and reconstructed answer
  `score`              Assigned score
  `max_score`          Maximum score defined in the rubric
  `confidence`         `HIGH`, `MEDIUM`, or `LOW`
  `reason`             Explanation for the confidence level

## How Semantic Scoring Works

The system uses the Sentence Transformers model:

``` text
all-MiniLM-L6-v2
```

The student's extracted answer and each rubric criterion are converted
into numerical embeddings.

The system then calculates cosine similarity:

``` text
Student Answer
      ↓
Sentence Embedding
      ↓
Cosine Similarity
      ↑
Rubric Criterion
      ↓
Sentence Embedding
```

A similarity threshold is used to estimate whether a rubric criterion is
sufficiently represented in the student's answer.

The current implementation uses an initial threshold of:

``` text
0.45
```

This is a configurable experimental threshold and should be validated
against manually reviewed examples before being treated as a reliable
grading threshold.

## Confidence System

The system considers OCR confidence and semantic similarity.

### HIGH

Generally assigned when:

-   OCR confidence is high.
-   Semantic similarity is high.

### MEDIUM

Generally assigned when:

-   OCR confidence is moderate.
-   Semantic similarity is reasonably strong.
-   Some uncertainty remains.

### LOW

Generally assigned when:

-   OCR confidence is low, or
-   Semantic similarity is low.

Low-confidence answers should be sent for human review rather than being
treated as automatically reliable.

## Important Limitations

### 1. Handwriting Recognition

EasyOCR is not a dedicated handwriting-recognition model. Handwritten
exam answers may therefore contain:

-   incorrect characters
-   missing words
-   merged words
-   incorrectly detected question numbers
-   low-confidence detections

The project therefore treats OCR as an imperfect upstream component.

### 2. Question Detection

Question detection currently relies on OCR text patterns such as:

``` text
Q12
Q.12
12.
12)
12
```

Handwriting may cause these patterns to be misread.

### 3. Line Grouping

Detected OCR regions are grouped using their vertical positions. The
grouping threshold is configurable and may need adjustment for different
page resolutions and handwriting styles.

### 4. Semantic Scoring

Semantic similarity does not guarantee that an answer is factually
correct. It provides a useful similarity signal against the defined
rubric.

### 5. Confidence

The confidence level is an engineering heuristic, not a calibrated
probability.

## Testing Strategy

The system should be tested in stages:

1.  Verify that the PDF opens correctly.
2.  Convert a sample page to an image.
3.  Run EasyOCR on the sample page.
4.  Inspect OCR text and OCR confidence.
5.  Test line grouping.
6.  Test question-number detection.
7.  Test answer reconstruction.
8.  Test semantic scoring against manually reviewed answers.
9.  Test confidence classification.
10. Test multi-page answer continuation.

Example test cases:

  -----------------------------------------------------------------------
  Test Case                           Expected Behavior
  ----------------------------------- -----------------------------------
  Clear handwritten text              OCR should produce mostly readable
                                      text

  Poor handwriting                    OCR confidence should decrease

  Question number detected            Following lines should belong to
                                      that question

  Answer continues on next page       Lines should be merged under the
                                      same question when the question is
                                      recognized

  Strong semantic answer              Relevant rubric criteria should
                                      receive higher similarity

  Unclear answer                      Confidence should be reduced and
                                      human review recommended
  -----------------------------------------------------------------------

## Human Review

The system is designed as a **human-in-the-loop** evaluation pipeline.

The intended workflow is:

``` text
Automatic Evaluation
        ↓
Confidence Check
        ↓
   ┌────┴────┐
   ↓         ↓
HIGH/MED   LOW
   ↓         ↓
Accept    Human Review
```

This is particularly important for handwritten material because OCR
errors can propagate into question structuring and scoring.

## Design Decisions

### Why EasyOCR?

EasyOCR provides:

-   easy Python integration
-   text detection
-   text recognition
-   OCR confidence scores
-   bounding boxes

It is suitable for building a compact prototype quickly.

### Why Sentence Transformers?

Simple keyword matching can fail when two answers use different words
but express the same idea.

For example:

``` text
Expected:
"The character overcame his fear through determination."

Student:
"He gradually became confident and faced his fear."
```

These answers share meaning even though the exact words differ.

Semantic embeddings allow the system to compare meaning more directly
than exact keyword matching.

### Why JSON?

JSON provides a simple machine-readable format for storing:

-   question number
-   extracted answer
-   score
-   maximum score
-   confidence
-   explanation

The JSON can later be converted to CSV, displayed in a dashboard, or
stored in a database.

## Future Improvements

Possible improvements include:

-   Better handwriting-specific OCR/HTR.
-   Image deskewing and perspective correction.
-   Automatic detection of answer regions.
-   More robust question-number detection.
-   Better handling of diagrams and interrupted answers.
-   Automatic continuation detection across pages.
-   Calibrated confidence scores.
-   Human-review interface.
-   CSV/Excel export.
-   Evaluation metrics such as OCR accuracy and agreement with human
    scores.
-   More extensive validation of semantic-similarity thresholds.
-   Separate scoring for individual rubric criteria.

## Assignment Deliverables

This repository contains the main implementation required for the
prototype:

-   Runnable Python code
-   OCR pipeline
-   Answer structuring
-   Custom answer key/rubric
-   Semantic scoring
-   Confidence estimation
-   JSON output
-   Project documentation

## Author

**Himanshu Rawat**

Diploma in Information Technology

Government Polytechnic Kashipur

## Disclaimer

This project is an academic/technical prototype for demonstrating an
AI/ML answer-sheet evaluation pipeline. Automated scores should not be
treated as authoritative without validation and appropriate human
review, especially for low-confidence handwritten answers.
