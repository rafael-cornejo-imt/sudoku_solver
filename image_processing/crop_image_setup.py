import cv2
from classes.imageCropper import ImageCropper

if __name__ == "__main__":
    cropper = ImageCropper()
    # Reemplaza 'ruta/a/tu/imagen.jpg' con la ruta a tu imagen
    cropped_image = cropper.select_region("data/images/crop_ref.jpg")

    # Muestra la imagen recortada
    cv2.imshow("Cropped Image", cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
