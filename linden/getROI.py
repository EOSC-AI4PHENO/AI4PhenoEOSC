import cv2
def crop_and_save_image(image_path, output_path, xmin, xmax, ymin, ymax):
    # Wczytaj obrazek
    image = cv2.imread(image_path)

    # Sprawdź, czy obrazek został poprawnie wczytany
    if image is None:
        print(f"Nie można wczytać obrazka: {image_path}")
        return

    # Wytnij ROI z obrazka
    roi = image[ymin:ymax, xmin:xmax]

    # Zapisz nowy obrazek
    cv2.imwrite(output_path, roi)

# Parametry wejściowe
image_path = "5.jpg"          # ścieżka do obrazka wejściowego
output_path = "5_out.jpg"        # ścieżka do obrazka wyjściowego
#xmin, xmax, ymin, ymax = 43.30733, 319.6256, 752.5741, 1096.287    # współrzędne ROI
xmin, xmax, ymin, ymax = 43, 319, 752, 1096    # współrzędne ROI

# Wywołaj funkcję
crop_and_save_image(image_path, output_path, xmin, xmax, ymin, ymax)
