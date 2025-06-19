import json
import time
from time import sleep
import win32ui
from PIL import Image
import pytesseract
import os
from PySide6.QtGui import QGuiApplication, QScreen
from config import load_config, OUTPUT_IMAGE, CONFIG_PATH
import re

pattern = r'^\d+-\d+$'

INTERVAL = 0.3  # интервал скриншота
CONFIG_CHECK_INTERVAL = 1.0  # интервал проверки изменения конфига
# Tesseract_DIR_PATH = "../Tesseract-OCR"
# Tesseract_FILE_PATH = f"{Tesseract_DIR_PATH}/tesseract.exe"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # путь к текущему файлу main.py
Tesseract_DIR_PATH = os.path.join(BASE_DIR, "../Tesseract-OCR")
Tesseract_FILE_PATH = os.path.join(Tesseract_DIR_PATH, "tesseract.exe")

pytesseract.pytesseract.tesseract_cmd = os.path.abspath(Tesseract_FILE_PATH)
os.environ['TESSDATA_PREFIX'] = os.path.abspath(Tesseract_DIR_PATH)


def load_area_from_config():
    config = load_config()
    area = config.get("area", {})
    x = area.get("x", 0)
    y = area.get("y", 0)
    width = area.get("width", 0)
    height = area.get("height", 0)
    return x, y, width, height


def ImageText():
    pytesseract.pytesseract.tesseract_cmd = os.path.abspath(Tesseract_FILE_PATH)

    # Укажи путь к tessdata
    os.environ['TESSDATA_PREFIX'] = os.path.abspath(Tesseract_DIR_PATH)
    # Загрузи изображение
    img = Image.open(OUTPUT_IMAGE)

    # Распознай текст
    text = pytesseract.image_to_string(img)
    return text


def print_text(text):
    if load_config()["printer"] != '' and text:
        try:
            # Создаем контекст принтера
            printer_dc = win32ui.CreateDC()
            printer_dc.CreatePrinterDC(load_config()["printer"])

            # Получаем размер printable area
            horz_res = printer_dc.GetDeviceCaps(8)  # HORZRES
            vert_res = printer_dc.GetDeviceCaps(10)  # VERTRES
            # Создаем шрифт
            font = win32ui.CreateFont({
                "name": "Arial",
                "height": 100,  # Размер шрифта
                "weight": 600,
            })
            printer_dc.SelectObject(font)

            # Вычисляем размеры текста
            text_size = printer_dc.GetTextExtent(text)
            text_width, text_height = text_size

            # Центрируем
            x = (horz_res - text_width) // 2
            y = (vert_res - text_height) // 2

            # Печать
            printer_dc.StartDoc("Centered Text")
            printer_dc.StartPage()
            printer_dc.TextOut(x, y, text)
            printer_dc.EndPage()
            printer_dc.EndDoc()
            printer_dc.DeleteDC()
        except Exception as e:
            print('Ошибка при печати:', e)


def main(stop_event):
    print("Начинаю захват экрана... Нажмите Ctrl+C для остановки.")
    last_coords = None
    last_config_mtime = 0
    last_config_check = 0
    last_text = None
    try:

        while not stop_event.is_set():
            now = time.time()
            # Проверяем файл config.json не чаще чем раз в CONFIG_CHECK_INTERVAL
            if now - last_config_check > CONFIG_CHECK_INTERVAL:
                current_mtime = os.path.getmtime(CONFIG_PATH)
                if current_mtime != last_config_mtime:
                    last_config_mtime = current_mtime
                    last_coords = load_area_from_config()
                    print(f"[INFO] Обновлены координаты: {last_coords}")
                last_config_check = now

            # Если координаты ещё не загружены (например, первый раз)
            if last_coords is not None:
                x, y, w, h = last_coords
                # Получаем основной экран
                screen: QScreen = QGuiApplication.primaryScreen()

                # Захватываем нужную область
                screenshot = screen.grabWindow(0, x, y, w, h)
                # Сохраняем в файл
                screenshot.save(OUTPUT_IMAGE, "png")
            text = ImageText()

            # распечатываем
            print("Найденный текст", text, '\nДлина:', len(text))
            if str(text).rstrip().lstrip() != last_text and re.fullmatch(pattern,
                                                                         str(text).rstrip().lstrip()) and "500" in text:
                print('распечатываю')
                # print_text(str(text).split('-')[0])
                print_text(str(text).rstrip().lstrip())
                last_text = str(text).rstrip().lstrip()
            # break
            sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nОстановка по Ctrl+C")
