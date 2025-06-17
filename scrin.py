import json
import time
import os
import pyautogui

CONFIG_PATH = "config.json"
OUTPUT_IMAGE = "screenshot.png"
INTERVAL = 0.3  # интервал скриншота
CONFIG_CHECK_INTERVAL = 1.0  # интервал проверки изменения конфига

def load_area_from_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
        area = config.get("area", {})
        x = area.get("x", 0)
        y = area.get("y", 0)
        width = area.get("width", 100)
        height = area.get("height", 100)
        return x, y, width, height

def main():
    print("Начинаю захват экрана... Нажмите Ctrl+C для остановки.")
    last_coords = None
    last_config_mtime = 0
    last_config_check = 0

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

            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nОстановка по Ctrl+C")

if __name__ == "__main__":
    main()
