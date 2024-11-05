import json
from rich.console import Console
from rich.text import Text


class SudokuValidator:
    def __init__(self, reference_file, output_file):
        self.reference_file = reference_file
        self.output_file = output_file
        self.console = Console()

    def load_sudoku_grid(self, file_path):
        """Load a Sudoku grid from a JSON file."""
        with open(file_path, "r") as file:
            data = json.load(file)
            return data["sudoku_grid"]

    def compare_grids(self, reference_grid, output_grid):
        """Compare two Sudoku grids and return the number of errors."""
        errors = []
        for i in range(9):
            for j in range(9):
                if reference_grid[i][j] != output_grid[i][j]:
                    errors.append((i, j, reference_grid[i][j], output_grid[i][j]))
        return errors

    def display_results(self, reference_grid, output_grid, errors):
        """Display the comparison results in a professional format."""
        self.console.print("\n[bold green]Sudoku Comparison Results[/bold green]")
        error_count = len(errors)

        # Create a 2D array for output with errors marked
        for i in range(9):
            row_str = ""
            for j in range(9):
                cell_value = output_grid[i][j]
                # Check for errors and format accordingly
                if (i, j, reference_grid[i][j], cell_value) in errors:
                    # Mark the error with red X and the number
                    error_display = Text(f"x", style="bold red")
                    row_str += f"{error_display} "  # Use rich text for styling
                else:
                    row_str += f"{cell_value if cell_value != 0 else '.'} "

            # Add horizontal divider every 3 rows for 3x3 subgrid visualization
            if i % 3 == 0 and i != 0:
                self.console.print("[bold]- - - + - - - + - - -[/bold]")

            # Add vertical dividers for 3x3 subgrid format
            formatted_row = f"{row_str[:5]} | {row_str[6:11]} | {row_str[12:]}"
            self.console.print(formatted_row)

        # Print the total number of errors
        self.console.print(f"\nTotal Errors: [bold red]{error_count}[/bold red]")
        for i, j, ref, actual in errors:
            self.console.print(
                f"Error at [{i + 1},{j + 1}] > Ref: {ref}, Actual: {actual}"
            )

    def validate(self):
        """Main method to validate the Sudoku grids."""
        reference_grid = self.load_sudoku_grid(self.reference_file)
        output_grid = self.load_sudoku_grid(self.output_file)

        errors = self.compare_grids(reference_grid, output_grid)
        self.display_results(reference_grid, output_grid, errors)
