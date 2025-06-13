from flask import Flask, request
from flask_cors import CORS
import win32print
import psutil
import time
import win32ui

PORT = 4025
PRINTER_NAME = "CHITENG-CT221B"

def free_port(port):
    """Завершить процесс, использующий указанный порт."""
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
            pid = conn.pid
            if pid:
                print(f"⚠️ Порт {port} уже используется. Завершаем процесс с PID {pid}...")
                try:
                    p = psutil.Process(pid)
                    p.terminate()
                    p.wait(timeout=3)
                    print("✅ Процесс завершён.")
                except Exception as e:
                    print(f"❌ Не удалось завершить процесс: {e}")
            else:
                print(f"❌ Порт {port} занят, но не удалось найти PID.")

# Проверяем порт перед запуском
free_port(PORT)

# Немного подождать, чтобы порт освободился
time.sleep(1)

app = Flask(__name__)
CORS(app)

def print_text(text):
    # Открываем указанный принтер
    printer = win32print.OpenPrinter(PRINTER_NAME)
    try:
        # Получаем информацию о принтере
        printer_info = win32print.GetPrinter(printer, 2)
        # Создаем DC (device context) для печати
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(PRINTER_NAME)

        # Начинаем документ
        hdc.StartDoc("Печать текста через Python")
        hdc.StartPage()

        # Устанавливаем шрифт (по желанию можно поменять)
        font = win32ui.CreateFont({
            "name": "Consolas",
            "height": 20,
            "weight": 400,
        })
        hdc.SelectObject(font)

        # Печатаем текст
        hdc.TextOut(100, 100, text)

        # Завершаем страницу и документ
        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()
    finally:
        # Закрываем принтер
        win32print.ClosePrinter(printer)

@app.route('/print', methods=['POST'])
def print_from_data():
    try:
        data = request.get_json()
        print("📥 Пришли данные:", data)
        text = data.get('text', '').strip()

        print("📝 Текст для печати:", text)

        if not text:
            return {'status': 'error', 'message': 'Empty text'}, 400
            ## тут нужные права на использование принтеров
        print(f'Отправил на распечатку: \'{str(text).split("-")[0]}.\' ')
        print_text(f"{str(text).split('-')[0]}.") # разбил строку по знаку тире, и получичил только первое значение в номере

        print(f"✅ Напечатано: {text}")
        return {'status': 'success', 'message': f'Printed: {text}'}

    except Exception as e:
        print("❌ Ошибка во Flask-приложении:", e)
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run(port=PORT)
