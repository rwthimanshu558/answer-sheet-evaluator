import easyocr
import cv2


class OCRProcessor:

    def __init__(self):
        print("Loading EasyOCR...")

        self.reader = easyocr.Reader(
            ['en']
        )

        print("EasyOCR loaded successfully.")

    def preprocess_image(self, image_path):
        """
        Convert image to grayscale.
        """

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(
                f"Could not read image: {image_path}"
            )

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        return gray

    def extract_text(self, image_path):
        """
        Extract text using EasyOCR.
        """

        results = self.reader.readtext(
            image_path
        )

        detections = []

        for result in results:

            bounding_box = result[0]
            text = result[1]
            confidence = float(result[2])

            x_coordinates = [
                int(point[0])
                for point in bounding_box
            ]

            y_coordinates = [
                int(point[1])
                for point in bounding_box
            ]

            center_x = sum(
                x_coordinates
            ) / len(x_coordinates)

            center_y = sum(
                y_coordinates
            ) / len(y_coordinates)

            detections.append({
                "text": text,
                "confidence": confidence,
                "x": center_x,
                "y": center_y,
                "bounding_box": bounding_box
            })

        return detections