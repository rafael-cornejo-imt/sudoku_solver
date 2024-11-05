# Standard library imports
import os  # Import os to handle directories
import json  # Import json for handling JSON files

# Third-party imports
import cv2  # Import OpenCV for image processing


class ImageCropper:
    def __init__(self):
        """Initialize the ImageCropper class with an empty list for clicked points."""
        self.points = []  # Initialize an empty list to store clicked points

    def click_and_crop(self, event, x, y, flags, param):
        """
        Handle mouse events to capture points for cropping.

        Args:
            event: The type of mouse event.
            x: The x-coordinate of the mouse event.
            y: The y-coordinate of the mouse event.
            flags: Any relevant flags passed by OpenCV.
            param: Additional parameters (not used here).
        """
        if event == cv2.EVENT_LBUTTONDOWN:  # Check if the left mouse button was clicked
            self.points.append((x, y))  # Append the clicked point to the list
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Mark the point on the image
            cv2.imshow("Image", image)  # Display the updated image

    def resize_image(self, image, scale_percent):
        """
        Resize an image to a specified percentage of its original dimensions.

        Args:
            image: The input image to resize.
            scale_percent: The percentage to resize the image.

        Returns:
            The resized image.
        """
        width = int(image.shape[1] * scale_percent / 100)  # Calculate new width
        height = int(image.shape[0] * scale_percent / 100)  # Calculate new height
        dim = (width, height)  # Create a dimension tuple
        return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)  # Resize the image

    def select_region(self, image_path):
        """
        Allow the user to select a rectangular region in an image for cropping.

        Args:
            image_path: The path to the image from which to select a region.

        Returns:
            The cropped image based on user-selected points.

        Raises:
            ValueError: If invalid points are selected (less than two).
        """
        global image  # Declare the global image variable
        image = cv2.imread(image_path)  # Read the image from the specified path
        clone = image.copy()  # Create a copy of the original image

        # Resize the image for display
        scale_percent = 50  # Adjust the scale percentage as needed
        image = self.resize_image(image, scale_percent)  # Resize the image
        cv2.namedWindow("Image")  # Create a window for displaying the image
        cv2.setMouseCallback(
            "Image", self.click_and_crop
        )  # Set the mouse callback function

        while True:  # Loop until a valid selection is made
            cv2.imshow("Image", image)  # Display the image
            key = cv2.waitKey(1) & 0xFF  # Wait for a key press

            # Press 'r' to reset the points
            if key == ord("r"):
                self.points = []  # Reset the points list
                image = clone.copy()  # Reset the image to the original clone
                image = self.resize_image(
                    image, scale_percent
                )  # Resize the image again
            # Press 'c' to confirm and crop the selected area
            elif key == ord("c") and len(self.points) == 2:
                break  # Exit the loop if two points are selected

        cv2.destroyAllWindows()  # Close all OpenCV windows

        if len(self.points) == 2:
            # Define the cropping coordinates based on selected points
            x1, y1 = self.points[0]  # First point
            x2, y2 = self.points[1]  # Second point
            # Ensure that the coordinates are valid
            x1, x2 = sorted([x1, x2])  # Sort the x-coordinates
            y1, y2 = sorted([y1, y2])  # Sort the y-coordinates

            # Adjust coordinates to match the original image dimensions
            height, width = clone.shape[:2]  # Get the original image dimensions
            x1_original = int(x1 * width / (width * scale_percent / 100))  # Adjust x1
            y1_original = int(y1 * height / (height * scale_percent / 100))  # Adjust y1
            x2_original = int(x2 * width / (width * scale_percent / 100))  # Adjust x2
            y2_original = int(y2 * height / (height * scale_percent / 100))  # Adjust y2

            # Crop the original image using the adjusted coordinates
            cropped_image = clone[y1_original:y2_original, x1_original:x2_original]
            self.save_coordinates(  # Save the cropping coordinates in JSON
                x1_original, y1_original, x2_original, y2_original
            )
            return cropped_image  # Return the cropped image
        else:
            raise ValueError(
                "No valid two points were selected."
            )  # Raise error if invalid points

    def save_coordinates(self, x1, y1, x2, y2):
        """
        Save the cropping coordinates to a JSON file.

        Args:
            x1: The x-coordinate of the first point.
            y1: The y-coordinate of the first point.
            x2: The x-coordinate of the second point.
            y2: The y-coordinate of the second point.
        """
        # Create the 'data/json' directory if it doesn't exist
        os.makedirs("data/json", exist_ok=True)

        coordinates = {
            "coordinates": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
        }  # Prepare coordinates for JSON
        with open("data/json/crop_coordinates.json", "w") as json_file:
            json.dump(
                coordinates, json_file, indent=4
            )  # Write coordinates to JSON file
        print(
            "Coordinates saved in 'data/json/crop_coordinates.json'."
        )  # Print confirmation message
