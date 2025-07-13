import os
import json
from threading import Lock
import re
addres = {
    "Чонграский, 9": True,
    "3, Павелецкий проезд, 4":False
}
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
OUTPUT_IMAGE = os.path.join(os.path.dirname(__file__), "screenshot.png")
Neiro_lang = 'eng+rus'
pattern = r'\d+-\d+'

PORT = 4025
INTERVAL = 0.2  # интервал скриншота
CONFIG_CHECK_INTERVAL = 0.1  # интервал проверки изменения конфига
FONT = {
"name": "Arial",
"height": 130 if addres["Чонграский, 9"] else  80,
"weight": 400,  # ширина
}
Tesseract_DIR_PATH = r"Tesseract-OCR/tessdata"
Tesseract_FILE_PATH =r"Tesseract-OCR\tesseract.exe"
Title_icon = os.path.join(os.path.dirname(__file__), "UI/icons/title_icon.png")
Github_icon_black =  os.path.join(os.path.dirname(__file__), "UI/icons/github_black.svg")
Github_icon_white =  os.path.join(os.path.dirname(__file__), "UI/icons/github_white.svg")
LIGHT_STYLE = """
/* Основной фон окна с легким градиентом */
QMainWindow {
    background-color: white;
    color: black;
    font-size: 14px;
}
QWidget {
    background-color: white;
    color:black;
}

/* Заголовки секций */
QLabel#label_title_printer, QLabel#label_title_window {
    font-size: 18px;
    font-weight: bold;
    color: #333333;
    padding-bottom: 6px;
}

/* Текстовые подписи */
QLabel {
    color: #222222;
}

/* Комбобокс (выбор принтера) */
QComboBox {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 6px;
    padding: 6px 10px;
}

QComboBox:hover {
    border: 1px solid #4E89FF;
}

/* Кнопки */
QPushButton#btn_change, QPushButton#btn_show  {
    background-color: #4E89FF;
    color: white;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: bold;
}

QPushButton#btn_change:hover,QPushButton#btn_show:hover {
    background-color: #3A6FCC;
}

/* Стиль для отключённых кнопок */
QPushButton#btn_change:disabled, QPushButton#btn_show:disabled {
    background-color: #b0b0b0;
    color: #666666;
}

QPushButton#btn_change_them {
    background-color: black;
    color: white;
    width: 30px;
    height: 30px;
    border-radius: 20px;  /* половина размера — круг */
    padding: 0px;
    font-size: 16px;
}

QPushButton#btn_change_them:hover {
    background-color: #3A6FCC;  /* немного серее при наведении */
}
QPushButton#btn_update_list_print{
                background-color: #4E89FF;
                color: white;
                font-size: 25px; /* Увеличение размера символа */
                border-radius:6px;
                
}
QPushButton#btn_update_list_print:hover {
    background-color: #3A6FCC;
}
QPushButton#btn_update_list_print:pressed {
    background-color: #4E89FF;
}
QPushButton#btn_github {
    border: 1px solid black;
    border-radius:15px;
}
QPushButton#btn_github:hover{
    border: 1px solid white;
}
QPushButton#btn_help {
    border: 1px solid black;
    border-radius:10px;
}
QPushButton#btn_help:hover{
    border: 1px solid white;
}
/* Кнопки 
QPushButton#btn_update_repo  {
    background-color: orange;
    color: white;
    border-radius: 8px;
    font-weight: bold;
}

QPushButton#btn_update_repo:hover {
    background-color: #3A6FCC;
}
*/
"""

DARK_STYLE = """
/* Основной фон окна с легким градиентом */
QMainWindow {
    background-color: #2b2d30;
    color: white;
    font-size: 14px;
}
QWidget {
    background-color: #2b2d30;
    color: white;
}


/* Комбобокс (выбор принтера) */
QComboBox {
    background-color: #ffffff;
    color:black;
    border: 1px solid #cccccc;
    border-radius: 6px;
    padding: 6px 10px;
}

QComboBox:hover {
    border: 1px solid #676767;
}

/* Кнопки */
QPushButton#btn_change, QPushButton#btn_show {
    background-color: #676767;
    color: white;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: bold;
}

QPushButton#btn_change:hover, QPushButton#btn_show:hover {
    background-color: #4f4f4f;
}

/* Стиль для отключённых кнопок */
QPushButton#btn_change:disabled, QPushButton#btn_show:disabled {
    background-color: #444444;
    color: #888888;
}

QPushButton#btn_change_them {
    background-color: white;
    color: white;
    width: 30px;
    height: 30px;
    border-radius: 20px;  /* половина размера — круг */
    padding: 0px;
    font-size: 16px;
}

QPushButton#btn_change_them:hover {
    background-color: #4E89FF;  /* немного серее при наведении */
}
QPushButton#btn_update_list_print {
                background-color: #676767;
                color: white;
                font-size: 25px; /* Увеличение размера символа */
                border-radius:6px;
}
QPushButton#btn_update_list_print:hover {
    background-color: #4f4f4f;
}
QPushButton#btn_update_list_print:pressed {
    background-color: #555555;
}
QPushButton#btn_github {
    border: 1px solid white;
    color:white;
    border-radius:15px;
}
QPushButton#btn_github:hover{
    border: 1px solid  #2b2d30;;
}
QPushButton#btn_help {
    border: 1px solid white;
    color: white;
    border-radius:10px;
}
QPushButton#btn_help:hover{
    border: 1px solid  #2b2d30;;
}
/* Кнопки
QPushButton#btn_update_repo{
    background-color: orange;
    color: white;
    border-radius: 8px;
    font-weight: bold;
}

QPushButton#btn_update_repo:hover {
    background-color: #4f4f4f;
}*/
"""
def format_number(text):
    if pattern:
        text = re.search(pattern, text).group() if re.search(pattern, text) else ''
        # добалвенныое условие
        if text:
            return f"{str(text).split('-')[0]}." if addres["Чонграский, 9"] else   f"{str(text).split('-')[0]}." if  int(str(text).split('-')[0]) < 450  else text
    return text
config_lock = Lock()  # глобальный замок для синхронизации доступа

# Загрузка конфигурации из файла
def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with config_lock:
                if os.path.getsize(CONFIG_PATH) == 0:
                    raise ValueError("Файл пустой")
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"[Ошибка чтения конфига]: {e}")
    return {}

# Сохранение данных в конфигурационный файл
def save_config(config):
    try:
        with config_lock:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Ошибка сохранения конфига]: {e}")