import os
import time
import multiprocessing
import psutil
from flask import Flask, request
from flask_cors import CORS

from config import PORT, CONFIG_PATH, load_config
from print_text import print_text

app = Flask(__name__)
CORS(app)

@app.route('/print', methods=['POST'])
def print_from_data():
    try:
        data = request.get_json()
        print("📥 Пришли данные:", data)
        text = data.get('text', '').strip()

        if not text:
            return {'status': 'error', 'message': 'Empty text'}, 400

        clean_text = str(text).split("-")[0].replace(" ", "")
        print(f'Отправил на распечатку: \'{clean_text}.\' ')
        print_text(f"{clean_text}.")
        return {'status': 'success', 'message': f'Printed: {text}'}

    except Exception as e:
        print("❌ Ошибка во Flask-приложении:", e)
        return {'status': 'error', 'message': str(e)}, 500


def run_flask():
    app.run(port=PORT, use_reloader=False)


def free_port(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
            pid = conn.pid
            if pid:
                try:
                    print(f"⚠️ Порт {port} уже используется. Завершаем процесс с PID {pid}...")
                    p = psutil.Process(pid)
                    p.terminate()
                    p.wait(timeout=3)
                    print("✅ Процесс завершён.")
                except Exception as e:
                    print(f"❌ Не удалось завершить процесс: {e}")


def main_expansion():
    print("[INFO] main_expansion() запущен")
    flask_process = None
    last_config_mtime = 0
    last_config_check = 0

    try:
        while True:
            now = time.time()

            if now - last_config_check > 1:
                if os.path.exists(CONFIG_PATH):
                    current_mtime = os.path.getmtime(CONFIG_PATH)
                    if current_mtime != last_config_mtime:
                        config = load_config()
                        is_running = config.get("is_running", False)
                        last_config_mtime = current_mtime
                        print(f"[INFO] Конфиг обновлён: is_running={is_running}")

                        if is_running and (flask_process is None or not flask_process.is_alive()) and config['mode'] == 'expansion':
                            print("[INFO] Запуск Flask-сервера...")
                            free_port(PORT)
                            flask_process = multiprocessing.Process(target=run_flask, daemon=True)
                            flask_process.start()

                        elif not is_running and flask_process and flask_process.is_alive() and config['mode'] != 'expansion':
                            print("[INFO] Остановка Flask-сервера...")
                            flask_process.terminate()
                            flask_process.join()
                            flask_process = None
                            print("[INFO] Flask-сервер остановлен.")

                last_config_check = now

            time.sleep(0.5)

    except Exception as e:
        print(f"[ERROR] main_expansion() завершился с ошибкой: {e}")

    finally:
        if flask_process and flask_process.is_alive():
            print("[INFO] Очистка: завершение Flask-сервера...")
            flask_process.terminate()
            flask_process.join()
