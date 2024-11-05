# Standard library imports
import numpy as np

# Third-party imports
import cv2
import pytesseract
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)
from rich.console import Console

# Configure Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class DigitRecognizer:
    """
    Class for recognizing digits in a 9x9 grid of image cells,
    specifically designed for Sudoku recognition.
    """

    def recognize_digits(self, cells, border_crop=6, visualize=False, verbose=False):
        """
        Recognizes digits in a grid of cell images using Tesseract OCR.

        Args:
            cells (list of list of np.array): 2D list containing cell images for OCR processing.
            border_crop (int): Crop border around each cell image (not implemented in this example).
            visualize (bool): Whether to display each cell's image step-by-step.
            verbose (bool): If True, print recognized digit info in terminal.

        Returns:
            sudoku_grid (list of list of int): Recognized 9x9 grid with detected digits.
        """
        sudoku_grid = []  # Initialize grid to store recognized digits

        # Calculate the total number of cells for progress tracking
        total_cells = len(cells) * len(cells[0])

        # Set up the progress bar for elegant terminal output
        with Progress(
            TextColumn("[bold blue]Recognizing digits", justify="right"),
            BarColumn(),
            TaskProgressColumn(),
            TextColumn("• Cell: {task.fields[celda]}"),
            TextColumn("• Digit: {task.fields[digit]}"),
            TimeRemainingColumn(),
        ) as progress:
            # Add progress task with custom fields
            task = progress.add_task(
                "Recognition", total=total_cells, celda="[0,0]", digit=""
            )

            # Iterate over each row and cell in the 9x9 grid
            for i, row in enumerate(cells):
                row_values = []  # Store digits recognized in the current row
                for j, cell in enumerate(row):

                    # Scale up the image to enhance Tesseract's recognition
                    large_cell = cv2.resize(
                        cell, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_LINEAR
                    )

                    # Tesseract OCR configuration
                    config = "--psm 10 -c tessedit_char_whitelist=0123456789"
                    digit = pytesseract.image_to_string(large_cell, config=config)

                    # Clean up and validate OCR result
                    recognized_digit = (
                        int(digit.strip())
                        if digit.strip().isdigit() and int(digit.strip()) <= 9
                        else 0
                    )
                    row_values.append(recognized_digit)

                    # Update progress bar with recognized digit and current cell
                    progress.update(
                        task, advance=1, celda=f"[{i},{j}]", digit=str(recognized_digit)
                    )

                sudoku_grid.append(row_values)  # Append row to the final grid

        # Close any visualization windows if opened
        if visualize:
            cv2.destroyAllWindows()

        # Display the recognized Sudoku grid as a formatted 9x9 matrix in the terminal
        if verbose:
            console = Console()
            console.print("\n[bold blue]Recognized Sudoku Grid:[/bold blue]")
            for i, row in enumerate(sudoku_grid):
                # Format row, using "." for unrecognized digits
                row_str = " ".join(f"{num}" if num != 0 else "." for num in row)

                # Add horizontal divider every 3 rows for 3x3 subgrid visualization
                if i % 3 == 0 and i != 0:
                    console.print("[bold]- - - + - - - + - - -[/bold]")

                # Add vertical dividers for 3x3 subgrid format
                formatted_row = f"{row_str[:5]} | {row_str[6:11]} | {row_str[12:]}"
                console.print(formatted_row)

        return sudoku_grid  # Return the 9x9 grid of recognized digits
