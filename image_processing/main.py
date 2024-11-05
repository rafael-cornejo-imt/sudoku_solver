# image_processing/main.py

from classes.GridDetector import GridDetector
from classes.CellExtractor import CellExtractor
from classes.DigitRecognizer import DigitRecognizer
import json
import cv2

def process_sudoku_image(image_path, output_path, visualize_grid=False, visualize_cells=False):
    image = cv2.imread(image_path)
    
    # Paso 1: Detectar la cuadrícula
    detector = GridDetector()
    grid_image = detector.detect_grid(image, visualize=visualize_grid)
    
    # Paso 2: Extraer celdas
    extractor = CellExtractor()
    cells = extractor.extract_cells(grid_image, visualize=visualize_cells)

    # # Paso 3: Reconocer dígitos (puedes comentar esta parte si no quieres probarlo aún)
    # recognizer = DigitRecognizer()
    # sudoku_grid = recognizer.recognize_digits(cells)
    
    # # Guardar el resultado en JSON
    # with open(output_path, 'w') as f:
    #     json.dump({"sudoku_grid": sudoku_grid}, f)

if __name__ == "__main__":
    process_sudoku_image("data/images/1.jpg", "output/extracted_grid.json", visualize_grid=True, visualize_cells=True)
