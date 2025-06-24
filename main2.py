# from PIL import Image, ImageOps
# import pytesseract
# import os
#
# from config import OUTPUT_IMAGE, Tesseract_FILE_PATH, Tesseract_DIR_PATH
#
#
# def preprocess_and_ocr(image_path, tesseract_cmd, tessdata_prefix, lang):
#     pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
#     os.environ['TESSDATA_PREFIX'] = tessdata_prefix
#
#     img = Image.open(image_path)
#
#     # Преобразуем в градации серого
#     img = img.convert('L')
#
#     # Инвертируем (если фон светлый)
#     img = ImageOps.invert(img)
#
#     # Применим бинаризацию
#     threshold = 128
#     img = img.point(lambda x: 0 if x < threshold else 255, '1')
#
#     # Опционально: сохраним для отладки
#     img.save("processed.png")
#
#     text = pytesseract.image_to_string(img)
#     print(text)
#     print(f"Распознанный текст: {text.strip()}")
#     return text.strip()
#
# print(preprocess_and_ocr(OUTPUT_IMAGE,Tesseract_FILE_PATH, Tesseract_DIR_PATH, 'eng'))
from PIL import Image, ImageOps
import pytesseract
import os

from config import OUTPUT_IMAGE, Tesseract_FILE_PATH, Tesseract_DIR_PATH

def preprocess_and_ocr(image_path, tesseract_cmd, tessdata_prefix, lang):
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    os.environ['TESSDATA_PREFIX'] = tessdata_prefix

    img = Image.open(image_path)

    # 👉 Проверим и выведем DPI и размер изображения
    dpi = img.info.get('dpi', (72, 72))  # если не указано — по умолчанию 72 dpi
    print(f"[INFO] DPI изображения: {dpi}")
    print(f"[INFO] Размер изображения в пикселях: {img.size}")  # (width, height)

    # Преобразуем в градации серого
    img = img.convert('L')

    # Инвертируем (если фон светлый)
    img = ImageOps.invert(img)

    # Применим бинаризацию
    threshold = 128
    img = img.point(lambda x: 0 if x < threshold else 255, '1')

    # Опционально: сохраним для отладки
    img.save("processed.png")

    text = pytesseract.image_to_string(img)
    print(f"[INFO] Распознанный текст: {text.strip()}")
    return text.strip()

print(preprocess_and_ocr(OUTPUT_IMAGE, Tesseract_FILE_PATH, Tesseract_DIR_PATH, 'eng'))
