import cv2
import json
import os  # Importa os para manejar directorios


class ImageCropper:
    def __init__(self):
        self.points = []

    def click_and_crop(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Marca el punto
            cv2.imshow("Image", image)

    def resize_image(self, image, scale_percent):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    def select_region(self, image_path):
        global image
        image = cv2.imread(image_path)
        clone = image.copy()

        # Redimensionar la imagen para la visualización
        scale_percent = 50  # Ajustar el porcentaje de escala según sea necesario
        image = self.resize_image(image, scale_percent)
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", self.click_and_crop)

        while True:
            cv2.imshow("Image", image)
            key = cv2.waitKey(1) & 0xFF

            # Presiona 'r' para resetear los puntos
            if key == ord("r"):
                self.points = []
                image = clone.copy()
                image = self.resize_image(image, scale_percent)
            # Presiona 'c' para confirmar y recortar
            elif key == ord("c") and len(self.points) == 2:
                break

        cv2.destroyAllWindows()

        if len(self.points) == 2:
            # Define las coordenadas de recorte
            x1, y1 = self.points[0]
            x2, y2 = self.points[1]
            # Asegúrate de que las coordenadas sean válidas
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])

            # Ajustar coordenadas a la imagen original
            height, width = clone.shape[:2]
            x1_original = int(x1 * width / (width * scale_percent / 100))
            y1_original = int(y1 * height / (height * scale_percent / 100))
            x2_original = int(x2 * width / (width * scale_percent / 100))
            y2_original = int(y2 * height / (height * scale_percent / 100))

            # Recortar la imagen original
            cropped_image = clone[y1_original:y2_original, x1_original:x2_original]
            self.save_coordinates(
                x1_original, y1_original, x2_original, y2_original
            )  # Guarda las coordenadas en JSON
            return cropped_image
        else:
            raise ValueError("No se seleccionaron dos puntos válidos.")

    def save_coordinates(self, x1, y1, x2, y2):
        # Crear el directorio 'data/json' si no existe
        os.makedirs("data/json", exist_ok=True)

        coordinates = {"coordinates": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}}
        with open("data/json/crop_coordinates.json", "w") as json_file:
            json.dump(coordinates, json_file, indent=4)
        print("Coordenadas guardadas en 'data/json/crop_coordinates.json'.")
