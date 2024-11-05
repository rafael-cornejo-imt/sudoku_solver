# 🧩 Sudoku Solver in Python

This project is a Python-based Sudoku solver designed to tackle the classic 9x9 puzzle using efficient algorithms and techniques. The solver analyzes an incomplete Sudoku grid and fills in the missing numbers while adhering to the game’s rules that each row, column, and 3x3 sub-grid must contain unique numbers from 1 to 9.

The project is designed to evolve over time, adding functionality, improving performance, and exploring various solving strategies. Initial implementations utilize simple backtracking, while future updates aim to incorporate constraint propagation and other advanced techniques to increase solving speed and accuracy.

Additionally, this project includes features for **image processing** to extract Sudoku puzzles from images, leveraging **OCR** (Optical Character Recognition) techniques to automate puzzle input.

---

## 📑 Table of Contents

- [Features](#-features)
- [Goals](#-goals)
- [Project Structure](#-project-structure)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔹 Features

- Solve 9x9 Sudoku grids using Python algorithms.
- Extract Sudoku puzzles from images using OCR techniques with Tesseract and OpenCV.
- Option to visualize the solving process (to be added in future updates).
- Clean and modular code structure to support easy updates and enhancements.

## 🎯 Goals

- Develop an interactive and efficient Sudoku-solving application.
- Gain a deeper understanding of algorithmic problem-solving.
- Experiment with different solving methods for performance optimization.
- Implement robust image processing features for automated puzzle extraction.

## 📂 Project Structure

- **/src**: Contains the main solver code.
- **/image_processing**: Contains code for image processing tasks, including Sudoku extraction from images.
- **/tests**: Unit tests for verifying the solver's accuracy and performance.
- **/docs**: Documentation and resources on the algorithms used.

## 🚀 Future Improvements

- **Visualization**: Add a step-by-step visualization of the solving process.
- **GUI**: Develop a graphical user interface for easy puzzle input and solution display.
- **Optimizations**: Implement more efficient solving algorithms like constraint propagation.
- **Enhanced OCR**: Improve the accuracy of image processing and digit recognition for better puzzle extraction.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests with suggestions, bug fixes, or new features.

## 📜 License

This project is licensed under the MIT License.

---

> _“This project is an exploration of algorithms and a journey to mastering Sudoku-solving techniques.”_
