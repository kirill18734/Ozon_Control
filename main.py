import threading
from UI.main import run
from ScreenToPrint.main import main

# Оборачиваем каждую функцию в поток
thread1 = threading.Thread(target=run)
thread2 = threading.Thread(target=main)

# Запускаем оба потока
thread1.start()
thread2.start()

# Опционально: ждём завершения обоих потоков
thread1.join()
thread2.join()
