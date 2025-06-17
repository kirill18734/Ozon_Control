import pyautogui
from PIL import Image
import easyocr
import numpy as np

reader = easyocr.Reader(['ru', 'en'])
screenshot = pyautogui.screenshot()
result = reader.readtext(np.array(screenshot))

for _, text, _ in result:
    print(text)
