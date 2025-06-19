import os
import json

CONFIG_PATH = "config.json"
OUTPUT_IMAGE = "screenshot.png"


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
QPushButton#btn_change, QPushButton#btn_show {
    background-color: #4E89FF;
    color: white;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: bold;
}

QPushButton#btn_change:hover, QPushButton#btn_show:hover {
    background-color: #3A6FCC;
    transition: background-color 0.3s ease;
}

QPushButton#pushButton {
    background-color: black;
    color: white;
    width: 30px;
    height: 30px;
    border-radius: 20px;  /* половина размера — круг */
    padding: 0px;
    font-size: 16px;
}

QPushButton#pushButton:hover {
    background-color: #3A3A3A;  /* немного серее при наведении */
}
QPushButton#btn_update_list_print {
                background-color: #4E89FF;
                color: white;
                font-size: 25px; /* Увеличение размера символа */
                border-radius:1px;
}
QPushButton#btn_update_list_print:hover {
    background-color: #3A3A3A;
}
QPushButton#btn_update_list_print:pressed {
    background-color: #555555;
}
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
    transition: background-color 0.3s ease;
}

QPushButton#pushButton {
    background-color: white;
    color: white;
    width: 30px;
    height: 30px;
    border-radius: 20px;  /* половина размера — круг */
    padding: 0px;
    font-size: 16px;
}

QPushButton#pushButton:hover {
    background-color: #3A3A3A;  /* немного серее при наведении */
}
QPushButton#btn_update_list_print {
                background-color: #2b2d30;
                color: white;
                font-size: 25px; /* Увеличение размера символа */
                border-radius:1px;
}
QPushButton#btn_update_list_print:hover {
    background-color: #676767;
}
QPushButton#btn_update_list_print:pressed {
    background-color: #555555;
}
"""

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Ошибка чтения конфига]: {e}")
    return {}




# Сохранение данных в конфигурационный файл
def save_config(config):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Ошибка сохранения конфига]: {e}")
