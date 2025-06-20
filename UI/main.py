import sys
import threading

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PySide6.QtPrintSupport import QPrinterInfo
from PySide6 import QtCore, QtGui, QtWidgets

from ScreenToPrint.main import main
from UI.ui_mainwindow import Ui_MainWindow

from config import DARK_STYLE, LIGHT_STYLE, load_config, save_config


# pyside6-uic application.ui -o ui_mainwindow.py

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
        self.dot_animation_timer = QtCore.QTimer(self)
        self.dot_animation_timer.timeout.connect(self.update_label_dots)

        # Установка начальных текстов и заголовков
        # Заголовок приложения
        self.setWindowTitle("Настройки мониторинга экрана и печати")

        # Принтер
        self.ui.lable_title_printer.setText("Принтер")
        self.ui.label_text_select_printer.setText("Выбор принтера")
        self.ui.btn_update_list_print.setText("↻")
        self.ui.btn_update_list_print.clicked.connect(self.populate_printer_list)
        self.ui.btn_update_list_print.setToolTip("Обновить список принтеров")  # выпадающая подсказка

        self.populate_printer_list()  # Заполнение списка принтеров
        self.ui.select_printer.currentTextChanged.connect(self.save_change)

        self.ui.label_title_window.setText("Область экрана")

        self.ui.btn_show.setText("🔍 Показать текущую область")
        self.ui.btn_show.clicked.connect(self.show_saved_area)

        self.ui.btn_change.setText("✏ Изменить область отслеживания")
        self.ui.btn_change.clicked.connect(self.activate_snipping)

        self.snipper = SnippingWidget()
        self.snipper.selection_done.connect(self.save_change)

        self.countdown_label = QLabel("", self)
        self.countdown_label.setAlignment(QtCore.Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 48px; color: white; background-color: rgba(0, 0, 0, 160);")
        self.countdown_label.setVisible(False)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.countdown = 3

        self.btn_is_running(load_config().get("is_running", False))
        self.ui.btn_enable.clicked.connect(lambda: self.save_change(True))

        self.apply_theme(load_config().get("theme", "light"))  # Применить тему из конфига
        self.ui.btn_change_them.clicked.connect(lambda: self.save_change(load_config().get("theme", "light")))

        config = load_config()
        is_running = config.get("is_running", False)
        self.btn_is_running(is_running)

        if is_running:
            self.start_backend()


    def start_backend(self):
        if not hasattr(self, 'backend_thread') or not self.backend_thread.is_alive():
            self.backend_thread = threading.Thread(target=main, daemon=True)
            self.backend_thread.start()
            print("[INFO] Бэкенд запущен")
        else:
            print("[INFO] Бэкенд уже работает")
        print(self.backend_thread.is_alive())
    def update_label_dots(self):
        base_text = "Приложение работает"
        dots = "." * (self.dot_animation_step % 4)  # "", ".", "..", "..."
        self.ui.label_title_is_running.setText(f"{base_text}{dots}")
        self.dot_animation_step += 1

    def btn_is_running(self, is_running):
        if is_running:
            self.dot_animation_step = 0
            self.dot_animation_timer.start(500)  # Запускаем таймер анимации label
            self.ui.btn_enable.setText(f"Остановить")
            self.ui.btn_enable.setStyleSheet("""
                QPushButton#btn_enable  {
                    background-color: red;
                    color: white;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton#btn_enable:hover {
                    background-color: darkred;
                }
            """)

        else:
            self.ui.label_title_is_running.setText("Приложение остановлено")
            self.ui.btn_enable.setText(f"Запустить")
            self.ui.btn_enable.setStyleSheet("""
                QPushButton#btn_enable {
                    background-color: green;
                    color: white;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton#btn_enable:hover {
                    background-color: darkgreen;
                }
            """)
            self.dot_animation_timer.stop()

    def save_change(self, *args):

        config = load_config()
        if len(args) == 1 and args[0] not in ('dark', 'light') and args[0] not in (False, True):
            config["printer"] = args[0]
        if len(args) == 1 and args[0] in ('dark', 'light') and args[0] not in (False, True):
            config["theme"] = 'dark' if args[0] == 'light' else 'light'
            self.apply_theme(args[0])

        if len(args) == 1 and args[0] in (False, True):
            config["is_running"] = not config.get("is_running", False)
            print(config["is_running"] )
            self.btn_is_running(config["is_running"])
            save_config(config)
            if config["is_running"]:
                self.start_backend()
                print("[INFO] Бэкенд активирован вручную")
            else:
                print("[INFO] Ожидание завершения — поток завершится сам при следующей проверке флага")

        if len(args) > 1:
            config["area"] = {"x": args[0], "y": args[1], "width": args[2], "height": args[3]}
            self.show()
            self.adjustSize()

        save_config(config)
        self.check_config_state()

    # Заполнение списка доступных принтеров и установка сохранённого
    def populate_printer_list(self):
        # Отключаем временно сигнал, чтобы не вызывался save_change
        self.ui.select_printer.blockSignals(True)

        self.ui.select_printer.clear()
        printers = QPrinterInfo.availablePrinters()
        printer_names = [printer.printerName() for printer in printers]
        self.ui.select_printer.addItems(printer_names)

        saved_printer = load_config().get("printer", "")
        if saved_printer and saved_printer in printer_names:
            index = self.ui.select_printer.findText(saved_printer)
            self.ui.select_printer.setCurrentIndex(index)
        else:
            self.ui.select_printer.setCurrentIndex(-1)

        # Снова включаем сигнал
        self.ui.select_printer.blockSignals(False)

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

    # Проверка наличия необходимых данных в конфиге и вывод предупреждений
    def check_config_state(self):
        config = load_config()

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
        config = load_config()
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
        config = load_config()
        current = config.get("theme", "light")
        new_theme = "dark" if current == "light" else "light"
        config["theme"] = new_theme
        save_config(config)
        self.apply_theme(new_theme)

    # Применение темы (светлая или тёмная)
    def apply_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet(DARK_STYLE)
            self.ui.btn_change_them.setText("☀️")
        else:
            self.setStyleSheet(LIGHT_STYLE)
            self.ui.btn_change_them.setText("🌙")


# Основная точка входа — запуск интерфейса и фонового потока
def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


run()
