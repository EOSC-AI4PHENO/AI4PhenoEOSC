import cv2
import numpy as np

# Zdefiniuj współrzędne wielokąta (ROI) - te wartości powinny być zgodne z danymi z Rstudio
vertices = [
    (43.30733, 752.5741),
    (319.6256, 752.5741),
    (319.6256, 1096.287),
    (43.30733, 1096.287)
]

# Wczytaj obrazek
image_path = "5.jpg"
image = cv2.imread(image_path)

# Przetwórz współrzędne wielokąta, aby były zgodne z formatem używanym przez OpenCV
vertices = np.array(vertices, dtype=np.int32)
vertices = vertices.reshape((-1, 1, 2))

# Stwórz maskę o tym samym rozmiarze co obrazek wejściowy
mask = np.zeros_like(image)

# Wypełnij maskę kolorem białym w miejscu ROI
cv2.fillPoly(mask, [vertices], (255, 255, 255))

# Nałóż maskę na oryginalne zdjęcie
roi = cv2.bitwise_and(image, mask)

# Ogranicz wynikowy obraz do ROI
(x_min, y_min), (x_max, y_max) = vertices.min(axis=0)[0], vertices.max(axis=0)[0]
roi = roi[y_min:y_max, x_min:x_max]

# Zapisz ROI jako nowy obrazek jpg
output_path = "output_roi.jpg"
cv2.imwrite(output_path, roi)