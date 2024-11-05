# image_processing/classes/CellExtractor.py

import cv2
import matplotlib.pyplot as plt

class CellExtractor:
    def extract_cells(self, grid_image, visualize=False):
        # Divide la imagen en una cuadrícula de 9x9
        cell_height = grid_image.shape[0] // 9
        cell_width = grid_image.shape[1] // 9
        cells = []
        
        for i in range(9):
            row = []
            for j in range(9):
                # Extrae cada celda
                cell = grid_image[i * cell_height:(i + 1) * cell_height, j * cell_width:(j + 1) * cell_width]
                row.append(cell)
            cells.append(row)

        if visualize:
            self.visualize_cells(cells)

        return cells

    def visualize_cells(self, cells):
        fig, axs = plt.subplots(9, 9, figsize=(12, 12))
        for i in range(9):
            for j in range(9):
                axs[i, j].imshow(cells[i][j], cmap='gray')
                axs[i, j].axis('off')  # Oculta los ejes
        plt.show()
