import win32print
import win32ui

# Название твоего принтера
printer_name = "CHITENG-CT221B"

# Текст для печати
text = "500-7"

# Создаем контекст принтера
printer_dc = win32ui.CreateDC()
printer_dc.CreatePrinterDC(printer_name)

# Получаем размер printable area
horz_res = printer_dc.GetDeviceCaps(8)   # HORZRES
vert_res = printer_dc.GetDeviceCaps(10)  # VERTRES
# Создаем шрифт
font = win32ui.CreateFont({
    "name": "Arial",
    "height": 100,  # Размер шрифта
    "weight": 600,
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
