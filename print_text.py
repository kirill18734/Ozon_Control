import win32ui
from config import load_config

def print_text(text):
    if load_config()["printer"] != '' and text:
        try:
            # Создаем контекст принтера
            printer_dc = win32ui.CreateDC()
            printer_dc.CreatePrinterDC(load_config()["printer"])

            # Получаем размер printable area
            horz_res = printer_dc.GetDeviceCaps(8)  # HORZRES
            vert_res = printer_dc.GetDeviceCaps(10)  # VERTRES
            # Создаем шрифт
            font = win32ui.CreateFont({
                "name": "Arial",
                "height": 100,  # Размер шрифта
                "weight": 400,
            })
            printer_dc.SelectObject(font)

            # Вычисляем размеры текста
            text_size = printer_dc.GetTextExtent(text)
            text_width, text_height = text_size

            # Центрируем
            x = (horz_res - text_width) // 2
            y = (vert_res - text_height) // 2

            # Печать
            printer_dc.StartDoc("Centered Text")
            printer_dc.StartPage()
            printer_dc.TextOut(x, y, text)
            printer_dc.EndPage()
            printer_dc.EndDoc()
            printer_dc.DeleteDC()
        except Exception as e:
            print('Ошибка при печати:', e)
