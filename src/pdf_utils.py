import fitz
import os


def pdf_to_images(pdf_path, output_folder, start_page=0, end_page=None):
    """
    Convert PDF pages into PNG images.

    start_page and end_page use Python indexing:
    page 0 = PDF page 1
    """

    os.makedirs(output_folder, exist_ok=True)

    pdf = fitz.open(pdf_path)

    if end_page is None:
        end_page = len(pdf)

    image_paths = []

    for page_number in range(start_page, end_page):

        page = pdf[page_number]

        # 2x resolution
        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2)
        )

        output_path = os.path.join(
            output_folder,
            f"page_{page_number + 1}.png"
        )

        pix.save(output_path)

        image_paths.append(output_path)

        print(f"Converted page {page_number + 1}")

    pdf.close()

    return image_paths