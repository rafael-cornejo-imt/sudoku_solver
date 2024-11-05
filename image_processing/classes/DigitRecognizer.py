# image_processing/classes/DigitRecognizer.py

import cv2
import pytesseract

# Configura la ruta a tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class DigitRecognizer:
    def recognize_digits(self, cells):
        sudoku_grid = []
        
        for row in cells:
            row_values = []
            for cell in row:
                # Convertir la celda a escala de grises y binarizar
                gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
                _, binary_cell = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
                
                # Usa Tesseract OCR para reconocer el dígito
                digit = pytesseract.image_to_string(binary_cell, config='--psm 10 digits')
                
                # Si hay un dígito válido, agrégalo, si no, agrega 0
                row_values.append(int(digit) if digit.isdigit() else 0)
            sudoku_grid.append(row_values)
        
        return sudoku_grid
