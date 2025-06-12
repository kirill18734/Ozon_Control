from flask import Flask, request
from flask_cors import CORS
import win32print
import socket
import psutil
import os
import signal
import time

PORT = 4025
PRINTER_NAME = win32print.GetDefaultPrinter()

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

@app.route('/print', methods=['POST'])
def print_from_data():
    try:
        data = request.get_json()
        print("📥 Пришли данные:", data)
        text = data.get('text', '').strip()
        print("📝 Текст для печати:", text)

        if not text:
            return {'status': 'error', 'message': 'Empty text'}, 400

        hPrinter = win32print.OpenPrinter(PRINTER_NAME)
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("PrintJob", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, text.encode('utf-8'))
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)

        print(f"✅ Напечатано: {text}")
        return {'status': 'success', 'message': f'Printed: {text}'}

    except Exception as e:
        print("❌ Ошибка во Flask-приложении:", e)
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run(port=PORT)
