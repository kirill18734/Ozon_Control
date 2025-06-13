import win32print
import win32ui

PRINTER_NAME = "CHITENG-CT221B"
TEXT_TO_PRINT = "Пример текста для печати\nСледующая строка"

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

print_text(TEXT_TO_PRINT)
