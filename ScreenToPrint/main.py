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

from print_text import print_text


def load_area_from_config():
        config = load_config()
        area = config.get("area", {})
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
    return text.replace(' ', '')


def main_neiro():
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
                x = last_coords.get("x", 0)
                y = last_coords.get("y", 0)
                w = last_coords.get("width", 0)
                h = last_coords.get("height", 0)
                screen: QScreen = QGuiApplication.primaryScreen()
                if screen is None:
                    print("[ERROR] primaryScreen вернул None")
                    break
                screenshot = screen.grabWindow(0, x, y, w, h)
                screenshot.save(OUTPUT_IMAGE, "png")

                text = ImageText()
                print("Найденный текст:", text, "| Длина:", len(text))
                # print(text != last_text)
                if text != last_text:
                    match = re.search(pattern, text)
                    if match:
                        found_number = match.group()
                        if not first_valid_skipped:
                            print(f"[INFO] Пропущен первый валидный текст: {found_number}")
                            first_valid_skipped = True
                        else:
                            print("[INFO] Распечатка текста")
                            print_text(f"{found_number.split('-')[0]}.")
                        last_text = text

            sleep(INTERVAL)  # или INTERVAL

    except Exception as e:
        print(f"[ERROR] main() завершился с ошибкой: {e}")
