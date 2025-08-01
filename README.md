# Печать ячеек

**Печать ячеек** — небольшое приложение для Windows, которое отслеживает номер в заданной области экрана и автоматически отправляет его на печать. Вместе с программой поставляется браузерное расширение `expansion/send_number_goods`, позволяющее передавать номера напрямую на локальный принт‑сервер.

## Внешний вид

Приложение поддерживает светлую и тёмную темы. Ниже приведены примеры интерфейса в обеих темах:

| Светлая тема | Тёмная тема |
|--------------|-------------|
|![img_5.png](img_black.png)|![img_4.png](img_white.png)|
## Возможности

- выбор принтера из списка установленных устройств;
- сохранение координат области экрана в файл `config.json`;
- переключение светлой/тёмной темы интерфейса;
- проверка обновлений репозитория и установка их одной кнопкой (кнопка появится, если в системе установлен Git);
- возможность работы через локальный сервер печати или напрямую через Tesseract.

## Требования

- Python 3.10+
- Windows с настроенным принтером (используется API `win32ui`)

Необходимые зависимости перечислены в `requirements.txt`.

### Установка Python и зависимостей

1. Загрузите и установите Python 3.10+ с сайта [python.org](https://www.python.org/),
   отметив опцию *Add Python to PATH*.
2. В каталоге проекта создайте виртуальное окружение:
   ```bash
   python -m venv venv
   ```
3. Активируйте его командой:
   ```bash
   venv\Scripts\activate
   ```
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Запуск
Для старта интерфейса выполните:

запустите файл: 
```
Печать_ячеек.bat
```


При первом запуске выберите подходящий режим работы:

### Режим расширения (рекомендуется)
1. Откройте `chrome://extensions` в браузере на базе Chromium.
2. Включите режим разработчика и нажмите «Загрузить распакованное расширение».
3. Укажите путь к каталогу `expansion/send_number_goods` из данного проекта.
4. После установки расширения обновите вкладку сайта Ozon, если она была открыта заранее.
5. Запустите приложение.

### Режим нейросети
1. Укажите принтер для печати.
2. Выберите область экрана, которую необходимо отслеживать.
3. Запустите приложение.

## Структура проекта

- `UI/` — код интерфейса и сгенерированные формы Qt
- `ScreenToPrint/` — захват экрана и печать текста
- `expansion/` — расширение для сайта Ozon
- `local_print_server/` — локальный сервер печати
- `Tesseract-OCR/` — бинарные файлы и данные Tesseract

## Примечания

Приложение ориентировано на Windows и использует Win32 API. Работа на других платформах не гарантируется.
