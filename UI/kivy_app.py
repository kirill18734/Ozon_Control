import threading
import webbrowser
import win32print

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.clock import Clock

from ScreenToPrint.main import main_neiro
from local_print_server.print_number_goods import main_expansion
from print_text import status_printer
from config import load_config, save_config


class SnippingWidget(Widget):
    """Widget to select an area on screen"""
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.start = None
        self.rect = None
        Window.add_widget(self)
        Window.show_cursor = False

    def on_touch_down(self, touch):
        self.start = touch.pos
        with self.canvas:
            Color(0, 1, 0, 0.4)
            self.rect = Rectangle(pos=self.start, size=(1, 1))
        return True

    def on_touch_move(self, touch):
        if self.rect:
            x, y = self.start
            w = touch.x - x
            h = touch.y - y
            self.rect.size = (w, h)

    def on_touch_up(self, touch):
        x, y = self.start
        w = touch.x - x
        h = touch.y - y
        Window.remove_widget(self)
        Window.show_cursor = True
        if self.callback:
            self.callback(int(x), int(y), int(abs(w)), int(abs(h)))


class MainWidget(BoxLayout):
    status = StringProperty("Приложение остановлено")

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)
        self.backend_thread = None
        self.build_ui()
        Clock.schedule_once(lambda dt: self.populate_printer_list(), 0)
        config = load_config()
        self.mode_switch.active = config.get("mode", "expansion") == "neiro"
        if config.get("is_running", False):
            self.toggle_start()

    def build_ui(self):
        # Printer selection
        box = BoxLayout(size_hint_y=None, height="40dp")
        box.add_widget(Label(text="Принтер"))
        self.printer_spinner = Spinner(text="", values=[])
        self.printer_spinner.bind(text=self.on_printer_select)
        box.add_widget(self.printer_spinner)
        upd = Button(text="↻", size_hint_x=None, width="40dp")
        upd.bind(on_release=lambda x: self.populate_printer_list())
        box.add_widget(upd)
        self.add_widget(box)

        # Mode switch
        box = BoxLayout(size_hint_y=None, height="40dp")
        box.add_widget(Label(text="Режим нейросети"))
        self.mode_switch = Switch()
        self.mode_switch.bind(active=lambda inst, val: self.toggle_mode(val))
        box.add_widget(self.mode_switch)
        self.add_widget(box)

        # Area buttons
        box = BoxLayout(size_hint_y=None, height="40dp")
        btn_show = Button(text="Показать область")
        btn_show.bind(on_release=lambda x: self.show_saved_area())
        box.add_widget(btn_show)
        btn_change = Button(text="Изменить область")
        btn_change.bind(on_release=lambda x: self.activate_snipping())
        box.add_widget(btn_change)
        self.add_widget(box)

        # Status label
        self.status_label = Label(text=self.status, size_hint_y=None, height="40dp")
        self.add_widget(self.status_label)

        # Start button
        self.start_btn = Button(text="Запустить", size_hint_y=None, height="50dp")
        self.start_btn.bind(on_release=lambda x: self.toggle_start())
        self.add_widget(self.start_btn)

        # Bottom buttons
        box = BoxLayout(size_hint_y=None, height="40dp")
        help_btn = Button(text="О программе")
        help_btn.bind(on_release=lambda x: self.show_help())
        box.add_widget(help_btn)
        gh_btn = Button(text="GitHub")
        gh_btn.bind(on_release=lambda x: self.open_github())
        box.add_widget(gh_btn)
        self.add_widget(box)

    def populate_printer_list(self):
        flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        printers = [p[2] for p in win32print.EnumPrinters(flags)]
        self.printer_spinner.values = printers
        saved = load_config().get("printer", "")
        if saved in printers:
            self.printer_spinner.text = saved
        elif printers:
            self.printer_spinner.text = printers[0]
            self.on_printer_select(printers[0])

    def on_printer_select(self, text):
        cfg = load_config()
        cfg["printer"] = text
        save_config(cfg)
        self.check_config_state()

    def toggle_mode(self, state):
        cfg = load_config()
        cfg["mode"] = "neiro" if state else "expansion"
        cfg["is_running"] = False
        save_config(cfg)
        self.status = "Приложение остановлено"
        self.status_label.text = self.status
        self.start_btn.text = "Запустить"
        self.check_config_state()

    def toggle_start(self):
        cfg = load_config()
        running = not cfg.get("is_running", False)
        cfg["is_running"] = running
        save_config(cfg)
        if running:
            self.start_backend()
            self.status = "Приложение работает"
            self.start_btn.text = "Остановить"
        else:
            self.status = "Приложение остановлено"
            self.start_btn.text = "Запустить"
        self.status_label.text = self.status

    def start_backend(self):
        if self.backend_thread and self.backend_thread.is_alive():
            return
        cfg = load_config()
        target = main_neiro if cfg.get("mode", "expansion") == "neiro" else main_expansion
        self.backend_thread = threading.Thread(target=target, daemon=True)
        self.backend_thread.start()

    def show_help(self):
        msg = "\n".join([
            "Это небольшая утилита для Windows, которая:",
            "- отслеживает указанную область экрана или принимает номер из расширения;",
            "- распознаёт текст через Tesseract OCR;",
            "- отправляет найденный текст на выбранный принтер."
        ])
        Popup(title="О программе", content=Label(text=msg), size_hint=(0.8, 0.6)).open()

    def open_github(self):
        webbrowser.open("https://github.com/kirill18734/Ozon_Control")

    def check_config_state(self):
        cfg = load_config()
        err = []
        if not cfg.get("printer"):
            err.append("Принтер не указан")
        elif status_printer():
            err.append("Принтер отключен")
        if err:
            self.status_label.text = "\n".join(err)
        else:
            self.status_label.text = self.status

    def activate_snipping(self):
        SnippingWidget(self.save_area)

    def save_area(self, x, y, w, h):
        cfg = load_config()
        cfg["area"] = {"x": x, "y": y, "width": w, "height": h}
        save_config(cfg)
        self.check_config_state()

    def show_saved_area(self):
        cfg = load_config()
        area = cfg.get("area", {})
        if not all(k in area for k in ("x", "y", "width", "height")):
            return
        widget = Widget()
        with widget.canvas:
            Color(0, 1, 0, 0.3)
            Rectangle(pos=(area["x"], area["y"]), size=(area["width"], area["height"]))
        Window.add_widget(widget)
        Clock.schedule_once(lambda dt: Window.remove_widget(widget), 1.5)


class CellsPrintApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MainWidget()


def run():
    CellsPrintApp().run()


if __name__ == "__main__":
    run()
