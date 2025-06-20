import time
from time import sleep
import win32ui
from PIL import Image
import pytesseract
import os
from PySide6.QtGui import QGuiApplication, QScreen
from config import load_config, OUTPUT_IMAGE, CONFIG_PATH, Tesseract_FILE_PATH, Tesseract_DIR_PATH, \
    CONFIG_CHECK_INTERVAL, pattern, INTERVAL
import re

def load_area_from_config():
        config = load_config()
        area = config.get("area", {})
        print(area)
        x = area.get("x", 0)
        y = area.get("y", 0)
        width = area.get("width", 100)
        height = area.get("height", 100)
        return x, y, width, height

def ImageText():
    pytesseract.pytesseract.tesseract_cmd = Tesseract_FILE_PATH

    # Укажи путь к tessdata
    os.environ['TESSDATA_PREFIX'] = Tesseract_DIR_PATH
    # Загрузи изображение
    img = Image.open(OUTPUT_IMAGE)

    # Распознай текст
    text = pytesseract.image_to_string(img)
    return str(text).rstrip().lstrip()


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
def main():
    last_coords = None
    last_config_mtime = 0
    last_config_check = 0
    last_text = None
    first_valid_skipped = False  # <-- флаг для пропуска первого валидного текста
    try:
        while True:
            now = time.time()

            # Проверка конфигурации не чаще, чем раз в CONFIG_CHECK_INTERVAL
            if now - last_config_check > CONFIG_CHECK_INTERVAL:
                current_mtime = os.path.getmtime(CONFIG_PATH)
                if current_mtime != last_config_mtime:
                    config = load_config()
                    print(config)
                    last_config_mtime = current_mtime
                    last_coords = config.get("area")
                    is_running = config.get("is_running", False)
                    print(f"[INFO] Конфиг обновлён: is_running={is_running}, area={last_coords}")
                    if not is_running:
                        print("[INFO] main() завершает работу по флагу is_running=False")
                        break
                last_config_check = now

            if last_coords:
                x, y, w, h = last_coords.values()
                screen: QScreen = QGuiApplication.primaryScreen()
                if screen is None:
                    print("[ERROR] primaryScreen вернул None")
                    break
                screenshot = screen.grabWindow(0, x, y, w, h)
                screenshot.save(OUTPUT_IMAGE, "png")

                text = ImageText()
                # print("Найденный текст:", text, "| Длина:", len(text))
                print(text != last_text)
                if text != last_text and re.fullmatch(pattern, text):
                    if not first_valid_skipped:
                        # Пропускаем первую подходящую строку
                        print(f"[INFO] Пропущен первый валидный текст: {text}")
                        first_valid_skipped = True
                    else:
                        print("[INFO] Распечатка текста")
                        # print_text(text)
                        print_text(f"{str(text).split('-')[0]}.")
                    last_text = text

            sleep(INTERVAL)  # или INTERVAL

    except Exception as e:
        print(f"[ERROR] main() завершился с ошибкой: {e}")