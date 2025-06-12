from flask import Flask, request
from flask_cors import CORS
import win32print
import traceback  # для вывода ошибок

app = Flask(__name__)
CORS(app)

PRINTER_NAME = win32print.GetDefaultPrinter()  # или укажи явно

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
        print("❌ Ошибка во Flask-приложении:")
        traceback.print_exc()  # покажет точную строку ошибки
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run(port=4025)
