# image_processing/main.py

from classes.GridDetector import GridDetector
from classes.CellExtractor import CellExtractor
from classes.DigitRecognizer import DigitRecognizer
from classes.SudokuValidator import SudokuValidator
import json
import cv2


def load_coordinates_from_json(json_file="config/crop_coordinates.json"):
    """Carga las coordenadas de recorte desde un archivo JSON."""
    with open(json_file, "r") as file:
        data = json.load(file)
        return data["coordinates"]


def process_sudoku_image(image_path, output_path):
    crop_coordinates = load_coordinates_from_json()
    image = cv2.imread(image_path)

    # Paso 1: Detectar la cuadrícula
    grid_detector = GridDetector()
    grid_image = grid_detector.crop_image(
        image_path, visualize=True, coordinates=crop_coordinates
    )

    # Paso 2: Extraer celdas
    extractor = CellExtractor()
    cells = extractor.extract_cells(grid_image, visualize=True)

    # Paso 3: Reconocer dígitos (puedes comentar esta parte si no quieres probarlo aún)
    recognizer = DigitRecognizer()
    sudoku_grid = recognizer.recognize_digits(cells, visualize=False, verbose=True)

    # Guardar el resultado en JSON
    with open(output_path, "w") as f:
        json.dump({"sudoku_grid": sudoku_grid}, f)

    validator = SudokuValidator(
        "data/json/extracted_grid_ref.json", "output/extracted_grid.json"
    )
    validator.validate()


if __name__ == "__main__":
    image_path = "data\images\main_test.jpg"
    output_path = "output\extracted_grid.json"
    process_sudoku_image(image_path, output_path)
