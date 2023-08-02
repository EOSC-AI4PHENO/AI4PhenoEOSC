import os
import base64

def convert_file_to_base64(fullname: str):
    # Otwórz plik w trybie binarnym
    with open(fullname, "rb") as file:
        # Odczytaj plik jako bajty
        byte_content = file.read()
        # Konwertuj bajty na base64
        base64_content = base64.b64encode(byte_content)
    # Zwróć base64 jako string
    return base64_content.decode()

fullname = 'E:/!DeepTechnology/!Customers/!2023/Seth Software EOSC-AI4Pheno/AI4PhenoEOSC/apple/dataset_2023_07_05_17_28_03/test/20220706_0852_0700F136_PIC_79_CAM_2.xml.pi.jpg'
size1 = os.path.getsize(fullname)
print(size1)

imageBase64 = convert_file_to_base64(fullname)
image_bytes = base64.b64decode(imageBase64)
image_size = len(image_bytes)
print(image_size)