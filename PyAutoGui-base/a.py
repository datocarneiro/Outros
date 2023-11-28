# pip install pyautogui pynput

import pyautogui, time
from pynput import mouse

while True:
    # Move o cursor para as coordenadas (1130, 570) e clica.
    print("proxima interação")
    time.sleep(1)
    pyautogui.click(619,500)
    time.sleep(1)
    pyautogui.click(1130, 569)
    pyautogui.click(1130, 569)
    pyautogui.click(1130, 569)
    time.sleep(1)
    pyautogui.click(619,500)
    time.sleep(25)
