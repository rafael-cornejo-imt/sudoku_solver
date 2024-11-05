# Standard library imports
import numpy as np

# Third-party imports
import matplotlib.pyplot as plt


class CellExtractor:
    """
    Class to extract and visualize individual cells from a 9x9 grid image.
    Designed specifically for Sudoku grid extraction.
    """

    def extract_cells(self, grid_image, visualize=False):
        """
        Extracts a 9x9 grid of cells from an image.

        Args:
            grid_image (np.array): Input image representing the entire Sudoku grid.
            visualize (bool): If True, visualizes the extracted cells in a 9x9 grid.

        Returns:
            cells (list of list of np.array): 2D list of extracted cells.
        """
        cell_height = grid_image.shape[0] // 9
        cell_width = grid_image.shape[1] // 9
        cells = []

        # Loop through rows and columns to extract each cell
        for i in range(9):
            row = []
            for j in range(9):
                # Extract each cell and append to row
                cell = grid_image[
                    i * cell_height : (i + 1) * cell_height,
                    j * cell_width : (j + 1) * cell_width,
                ]
                row.append(cell)
            cells.append(row)

        # Visualize the cells if requested
        if visualize:
            self.visualize_cells(cells)

        return cells

    def visualize_cells(self, cells):
        """
        Visualizes extracted cells in a 9x9 grid format.

        Args:
            cells (list of list of np.array): 2D list of cell images.
        """
        fig, axs = plt.subplots(9, 9, figsize=(12, 12))

        # Display each cell in its corresponding subplot
        for i in range(9):
            for j in range(9):
                axs[i, j].imshow(cells[i][j], cmap="gray")  # Display cell in grayscale
                axs[i, j].axis("off")  # Hide axes for cleaner look

        # Adjust layout and spacing
        plt.subplots_adjust(wspace=0.1, hspace=0.1)
        plt.show()
