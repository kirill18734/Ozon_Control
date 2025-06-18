import json
import time
import pyautogui
from time import sleep
import win32print
import win32ui
from PIL import Image
import pytesseract
import os
import re

pattern = r'^\d+-\d+$'
CONFIG_PATH = "../config.json"
OUTPUT_IMAGE = "screenshot.png"
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
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
        area = config.get("area", {})
        x = area.get("x", 0)
        y = area.get("y", 0)
        width = area.get("width", 100)
        height = area.get("height", 100)
        return x, y, width, height


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Ошибка чтения конфига]: {e}")
    return {}


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
        # Открываем указанный принтер
        printer = win32print.OpenPrinter(load_config()["printer"])
        try:
            # Получаем информацию о принтере
            printer_info = win32print.GetPrinter(printer, 2)

            # Создаем DC (device context) для печати
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(load_config()["printer"])

            # Начинаем документ
            hdc.StartDoc("Печать текста через Python")
            hdc.StartPage()

            # Устанавливаем шрифт
            font = win32ui.CreateFont({
                "name": "Arial",
                "height": 150,  # размер шрифта в логических единицах
                "weight": 400,
            })
            hdc.SelectObject(font)

            # Получаем размеры страницы
            page_width = 430  # HORZRES
            page_height = 250

            # Вычисляем размер текста
            text_width, text_height = hdc.GetTextExtent(text)

            # Центрируем
            x = (page_width - text_width) // 2
            y = (page_height - text_height) // 2

            # Печатаем текст по центру
            hdc.TextOut(x, y, text)

            # Завершаем печать
            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()
        finally:
            # Закрываем принтер
            win32print.ClosePrinter(printer)


def main():
    print("Начинаю захват экрана... Нажмите Ctrl+C для остановки.")
    last_coords = None
    last_config_mtime = 0
    last_config_check = 0
    last_text = None
    try:

        while True:
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
                screenshot = pyautogui.screenshot(region=(x, y, w, h))
                screenshot.save(OUTPUT_IMAGE)
            text = ImageText()
            # распечатываем
            if text != last_text:# and re.fullmatch(pattern, text):
                print_text(text)

            sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nОстановка по Ctrl+C")


if __name__ == "__main__":
    main()
