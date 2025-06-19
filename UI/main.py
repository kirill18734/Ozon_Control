import sys
import json
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PySide6.QtPrintSupport import QPrinterInfo
from PySide6 import QtCore, QtGui, QtWidgets
from UI.ui_mainwindow import Ui_MainWindow
import threading
from ScreenToPrint.main import main  # ваша фоновая функция
from PySide6.QtWidgets import QInputDialog, QMessageBox

# pyside6-uic application.ui -o ui_mainwindow.py
CONFIG_PATH = "config.json"
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
"""


# Класс виджета для выбора области экрана пользователем
class SnippingWidget(QtWidgets.QMainWindow):
    selection_done = QtCore.Signal(int, int, int, int)  # Сигнал по завершению выделения области (x, y, w, h)

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__(parent)
        # Настройка прозрачности и безрамочного окна
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.outsideSquareColor = "red"
        self.squareThickness = 2

        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    # Обработка нажатия мыши — начало выделения
    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = event.pos()
        self.update()

    # Обработка перемещения мыши — обновление прямоугольника
    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
        self.update()

    # Обработка отпускания кнопки мыши — завершение выделения
    def mouseReleaseEvent(self, QMouseEvent):
        r = QtCore.QRect(self.start_point, self.end_point).normalized()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.hide()
        x, y, w, h = r.x(), r.y(), r.width(), r.height()
        self.selection_done.emit(x, y, w, h)  # Отправка сигнала
        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    # Отрисовка полупрозрачного выделения на экране
    def paintEvent(self, event):
        trans = QtGui.QColor(22, 100, 233)
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        qp = QtGui.QPainter(self)
        trans.setAlphaF(0.2)
        qp.setBrush(trans)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(r)
        r_path = outer - inner
        qp.drawPath(r_path)
        qp.setPen(QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness))
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)


# Основное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Установка начальных текстов и заголовков
        self.setWindowTitle("Настройки мониторинга экрана и печати")
        self.ui.btn_show.setText("🔍 Показать текущую область")
        self.ui.btn_change.setText("✏ Изменить область отслеживания")
        self.ui.label_text_select_printer.setText("Выбор принтера")
        self.ui.lable_title_printer.setText("Принтер")

        self.ui.label_title_window.setText("Область экрана")
        self.ui.label_text_select_format_number.setText("Какой формат номера ищем")
        self.ui.label_title_format_number.setText("Формат поиска номера")
        self.populate_printer_list()  # Заполнение списка принтеров
        self.populate_format_number_list()  # Заполнение списка форматов номеров

        self.check_config_state()  # Проверка состояния конфигурации

        # Привязка сигналов к обработчикам
        self.ui.select_printer.currentTextChanged.connect(self.save_selected_printer)
        self.ui.select_format_number.currentTextChanged.connect(self.save_selected_search_number)
        self.ui.btn_change.clicked.connect(self.activate_snipping)
        self.ui.btn_show.clicked.connect(self.show_saved_area)
        self.ui.pushButton.clicked.connect(self.toggle_theme)

        self.snipper = SnippingWidget()
        self.snipper.selection_done.connect(self.on_area_selected)

        # Метка обратного отсчета при выборе области
        self.countdown_label = QLabel("", self)
        self.countdown_label.setAlignment(QtCore.Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 48px; color: white; background-color: rgba(0, 0, 0, 160);")
        self.countdown_label.setVisible(False)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.countdown = 3

        self.apply_theme(self.load_config().get("theme", "light"))  # Применить тему из конфига

    # Заполнение списка доступных принтеров и установка сохранённого
    def populate_printer_list(self):
        self.ui.select_printer.clear()
        printers = QPrinterInfo.availablePrinters()
        printer_names = [printer.printerName() for printer in printers]
        self.ui.select_printer.addItems(printer_names)

        saved_printer = self.load_config().get("printer", "")
        if saved_printer and saved_printer in printer_names:
            index = self.ui.select_printer.findText(saved_printer)
            self.ui.select_printer.setCurrentIndex(index)
        else:
            self.ui.select_printer.setCurrentIndex(-1)

    def populate_format_number_list(self):
        self.ui.select_format_number.clear()
        self.printer_names = ["777-777", "777", "Другой формат"]
        self.ui.select_format_number.addItems(self.printer_names)

        saved_format = self.load_config().get("search_number", "")
        if saved_format and saved_format in self.printer_names:
            index = self.ui.select_format_number.findText(saved_format)
            self.ui.select_format_number.setCurrentIndex(index)
        elif saved_format:
            self.ui.select_format_number.insertItem(0, saved_format)
            self.ui.select_format_number.setCurrentIndex(0)
            self.printer_names.insert(0, saved_format)
        else:
            self.ui.select_format_number.setCurrentIndex(-1)

        # Подключаем только один раз
        self.ui.select_format_number.currentTextChanged.connect(self.on_format_number_changed)

    def restore_previous_format_selection(self):
        saved_format = self.load_config().get("search_number", "")
        if saved_format in self.printer_names:
            index = self.ui.select_format_number.findText(saved_format)
            self.ui.select_format_number.setCurrentIndex(index)
        else:
            self.ui.select_format_number.setCurrentIndex(-1)

    def on_format_number_changed(self, text):
        if text == "Другой формат":
            # Отключаем временно сигнал, чтобы не сохранить "Другой формат"
            self.ui.select_format_number.blockSignals(True)

            format_text, ok = QInputDialog.getText(self, "Введите формат", "Введите свой формат номера:")
            if ok and format_text:
                # Добавляем в список, если его нет
                if format_text not in self.printer_names:
                    self.ui.select_format_number.insertItem(0, format_text)
                    self.printer_names.insert(0, format_text)

                # Устанавливаем выбранное
                index = self.ui.select_format_number.findText(format_text)
                self.ui.select_format_number.setCurrentIndex(index)

                # Сохраняем в конфиг
                self.save_selected_search_number(format_text)

                QMessageBox.information(self, "Выбран формат", f"Вы выбрали формат: {format_text}")
            else:
                self.restore_previous_format_selection()

            # Возвращаем сигналы обратно
            self.ui.select_format_number.blockSignals(False)
        else:
            # Любой другой выбор сохраняем сразу
            self.save_selected_search_number(text)

    def save_config_value(self, key, value):
        config = self.load_config()
        config[key] = value
        self.save_config(config)
        self.check_config_state()

    # Сохранение выбранного принтера в конфиг
    def save_selected_printer(self, printer_name):
        config = self.load_config()
        config["printer"] = printer_name
        self.save_config(config)
        self.check_config_state()

        # Сохранение выбранного принтера в конфиг

    def save_selected_search_number(self, search_number):
        config = self.load_config()
        config["search_number"] = search_number
        self.save_config(config)
        self.check_config_state()

    # Активация выбора области экрана с обратным отсчетом
    def activate_snipping(self):
        self.countdown = 3
        self.countdown_label.setGeometry(self.rect())
        self.countdown_label.setText(str(self.countdown))
        self.countdown_label.setVisible(True)
        self.timer.start(1000)

    # Обновление значения обратного отсчета каждую секунду
    def update_countdown(self):
        self.countdown -= 1
        if self.countdown <= 0:
            self.timer.stop()
            self.countdown_label.setVisible(False)
            self.snipper.showFullScreen()
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
            self.hide()
        else:
            self.countdown_label.setText(str(self.countdown))

    # Обработка выбора области — сохранение в конфиг
    def on_area_selected(self, x, y, w, h):
        config = self.load_config()
        config["area"] = {"x": x, "y": y, "width": w, "height": h}
        self.save_config(config)
        self.show()
        self.adjustSize()
        self.check_config_state()

    # Проверка наличия необходимых данных в конфиге и вывод предупреждений
    def check_config_state(self):
        config = self.load_config()

        if config.get('printer', '') == '':
            self.ui.label_error_printer.setText("Принтер не указан")
        else:
            self.ui.label_error_printer.setText("")

        area = config.get("area", {})
        cooridname = next((key for key in area if area.get(key, 0) != 0), False)
        if not cooridname:
            self.ui.label_error_show.setText("Область отслеживания не добавлена")
        else:
            self.ui.label_error_show.setText("")

    # Отображение сохранённой области на экране в виде зеленого прямоугольника
    def show_saved_area(self):
        config = self.load_config()
        area = config.get("area", {})

        if not all(k in area and area[k] > 0 for k in ("x", "y", "width", "height")):
            print("❌ Область не указана или некорректна.")
            return

        self.overlay = QWidget()
        self.overlay.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.overlay.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.overlay.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.overlay.showFullScreen()
        self.overlay.paintEvent = lambda event: self.paint_saved_area(event, area)

        QtCore.QTimer.singleShot(1500, self.overlay.close)

    # Отрисовка сохранённой области
    def paint_saved_area(self, event, area):
        painter = QtGui.QPainter(self.overlay)
        painter.fillRect(self.overlay.rect(), QtGui.QColor(0, 0, 0, 100))
        pen = QtGui.QPen(QtGui.QColor("green"))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(0, 255, 0, 50))
        rect = QtCore.QRect(area["x"], area["y"], area["width"], area["height"])
        painter.drawRect(rect)

    # Переключение между светлой и тёмной темами
    def toggle_theme(self):
        config = self.load_config()
        current = config.get("theme", "light")
        new_theme = "dark" if current == "light" else "light"
        config["theme"] = new_theme
        self.save_config(config)
        self.apply_theme(new_theme)

    # Применение темы (светлая или тёмная)
    def apply_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet(DARK_STYLE)
            self.ui.pushButton.setText("☀️")
        else:
            self.setStyleSheet(LIGHT_STYLE)
            self.ui.pushButton.setText("🌙")

    # Загрузка конфигурационного файла
    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Ошибка чтения конфига]: {e}")
        return {}

    # Сохранение данных в конфигурационный файл
    def save_config(self, config):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Ошибка сохранения конфига]: {e}")


# Основная точка входа — запуск интерфейса и фонового потока
def run():
    app = QApplication(sys.argv)
    window = MainWindow()

    # Создаём событие для остановки фонового процесса
    stop_event = threading.Event()

    # Запуск фоновой функции main в отдельном потоке
    thread = threading.Thread(target=main, args=(stop_event,), daemon=True)
    thread.start()

    # Обработка закрытия окна — остановка потока
    def on_close(event):
        print("[INFO] Закрытие окна, останавливаем фон...")
        stop_event.set()
        thread.join()
        event.accept()

    window.closeEvent = on_close

    window.show()
    sys.exit(app.exec())
