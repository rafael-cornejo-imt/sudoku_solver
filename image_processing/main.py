# image_processing/main.py

# Standard library imports
import json  # Import json for handling JSON files

# Third-party imports
import cv2  # Import OpenCV for image processing

# Local application imports
from classes.GridDetector import GridDetector  # Import GridDetector class
from classes.CellExtractor import CellExtractor  # Import CellExtractor class
from classes.DigitRecognizer import DigitRecognizer  # Import DigitRecognizer class
from classes.SudokuValidator import SudokuValidator  # Import SudokuValidator class


def load_coordinates_from_json(json_file="config/crop_coordinates.json"):
    """Load cropping coordinates from a JSON file."""
    with open(json_file, "r") as file:
        data = json.load(file)
        return data["coordinates"]


def process_sudoku_image(image_path, output_path):
    crop_coordinates = load_coordinates_from_json()  # Load crop coordinates from JSON

    # Step 1: Detect the Sudoku grid
    grid_detector = GridDetector()  # Create an instance of GridDetector
    grid_image = grid_detector.crop_image(
        image_path, visualize=True, coordinates=crop_coordinates
    )  # Crop the grid image

    # Step 2: Extract cells from the grid
    extractor = CellExtractor()  # Create an instance of CellExtractor
    cells = extractor.extract_cells(grid_image, visualize=True)  # Extract cells

    # Step 3: Recognize digits in the extracted cells (optional)
    recognizer = DigitRecognizer()  # Create an instance of DigitRecognizer
    sudoku_grid = recognizer.recognize_digits(cells, visualize=False, verbose=True)

    # Save the recognized Sudoku grid to a JSON file
    with open(output_path, "w") as f:
        json.dump({"sudoku_grid": sudoku_grid}, f)

    # Validate the Sudoku grid using the SudokuValidator
    validator = SudokuValidator(
        "data/json/extracted_grid_ref.json", "output/extracted_grid.json"
    )
    validator.validate()


if __name__ == "__main__":
    image_path = "data/images/main_test.jpg"  # Specify the image path
    output_path = "output/extracted_grid.json"  # Specify the output path
    process_sudoku_image(image_path, output_path)  # Process the Sudoku image
