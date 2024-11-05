# Standard library imports
import cv2


class GridDetector:
    """
    Class for detecting and cropping the grid from a Sudoku image.
    """

    def crop_image(self, image_path, coordinates, visualize=False):
        """
        Crops the specified region from the image, processes it, and
        optionally visualizes the result.

        Args:
            image_path (str): Path to the input image.
            coordinates (dict): Coordinates for cropping the image
                                in the format {'x1': int, 'y1': int,
                                'x2': int, 'y2': int}.
            visualize (bool): If True, display the cropped and processed image.

        Returns:
            np.array: The processed binary image of the cropped grid.
        """
        # Read the original image
        image = cv2.imread(image_path)

        # Crop the image using the specified coordinates
        x1, y1, x2, y2 = (
            coordinates["x1"],
            coordinates["y1"],
            coordinates["x2"],
            coordinates["y2"],
        )
        cropped_image = image[y1:y2, x1:x2]

        # Convert the cropped image to grayscale
        gray_cropped = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred_cropped = cv2.GaussianBlur(gray_cropped, (5, 5), 0)

        # Binarization: keeping lighter colors
        _, binary_cropped = cv2.threshold(
            blurred_cropped, 55, 200, cv2.THRESH_BINARY_INV
        )

        # Show the detected grid image if visualization is requested
        if visualize:
            self.show_image(binary_cropped, "Detected Grid")

        return binary_cropped

    def show_image(self, image, title="Image"):
        """
        Displays an image in a window.

        Args:
            image (np.array): The image to display.
            title (str): The title of the display window.
        """
        cv2.imshow(title, image)
        cv2.waitKey(0)  # Wait until a key is pressed
        cv2.destroyAllWindows()  # Close the display window
