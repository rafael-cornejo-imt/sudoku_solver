# image_processing/classes/GridDetector.py

import cv2
import numpy as np

class GridDetector:
    def detect_grid(self, image, visualize=False):
        # Convierte a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Aplica desenfoque Gaussiano para suavizar la imagen
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Detección de bordes
        edges = cv2.Canny(blurred, 50, 150)
        # Encuentra contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Buscar el contorno más grande, presumiblemente la cuadrícula
        sudoku_contour = max(contours, key=cv2.contourArea)
        # Aproxima el contorno a una forma poligonal
        epsilon = 0.1 * cv2.arcLength(sudoku_contour, True)
        approx = cv2.approxPolyDP(sudoku_contour, epsilon, True)

        if len(approx) == 4:
            # Realiza la transformación de perspectiva
            grid_image = self.four_point_transform(image, approx.reshape(4, 2))

            # Mostrar la imagen de la cuadrícula detectada si se solicita
            if visualize:
                self.show_image(grid_image, "Detected Grid")
            return grid_image
        else:
            raise ValueError("No Sudoku grid detected.")

    def four_point_transform(self, image, pts):
        # Reordena los puntos para la transformación de perspectiva
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect
        
        # Calcula las dimensiones de la cuadrícula
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped

    def order_points(self, pts):
        # Ordena los puntos en el orden [top-left, top-right, bottom-right, bottom-left]
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    def show_image(self, image, title="Image"):
        """Muestra la imagen en una ventana."""
        cv2.imshow(title, image)
        cv2.waitKey(0)  # Espera hasta que se presione una tecla
        cv2.destroyAllWindows()  # Cierra la ventana
