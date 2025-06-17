from time import sleep

from PIL import Image
import pytesseract
import os


while True:
    # Укажи путь к tesseract.exe внутри проекта
    pytesseract.pytesseract.tesseract_cmd = os.path.abspath('Tesseract-OCR\\tesseract.exe')

    # Укажи путь к tessdata
    os.environ['TESSDATA_PREFIX'] = os.path.abspath('Tesseract-OCR')

    # Загрузи изображение
    img = Image.open('img.png')

    # Распознай текст
    text = pytesseract.image_to_string(img)

    print(text)
    sleep(0.3)