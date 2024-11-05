# src/classes/Puzzle.py

class Puzzle:
    """Class representing a Sudoku puzzle."""
    
    def __init__(self, grid):
        self.grid = grid
    
    def display(self):
        """Displays the current state of the puzzle."""
        for row in self.grid:
            print(" ".join(str(num) if num != 0 else "." for num in row))
