"""
A python script to draw in the game skribblio

Author: David Chen
"""
import pyautogui
from time import sleep
from pathlib import Path

# canvas params
CANVAS_TOP_LEFT = (370, 195)
CANVAS_WIDTH, CANVAS_HEIGHT = 1000, 750
CANVAS_BOTTOM_RIGHT = (
    CANVAS_TOP_LEFT[0] + CANVAS_WIDTH, CANVAS_TOP_LEFT[1] + CANVAS_HEIGHT)


# other
ICON_PATH = Path('./assets')

pyautogui.PAUSE = 0.0


def alt_tab():
    """ Switch to recent window """
    sleep(.5)
    pyautogui.keyDown('alt')
    sleep(.3)
    pyautogui.press('tab')
    sleep(.3)
    pyautogui.keyUp('alt')


alt_tab()


sleep(1)
brush_path = ICON_PATH / 'mid_brush.png'
x, y = pyautogui.locateCenterOnScreen(str(brush_path.absolute()))
pyautogui.click(x, y)

for y in range(CANVAS_TOP_LEFT[1], CANVAS_BOTTOM_RIGHT[1], 8):
    for x in range(CANVAS_TOP_LEFT[0], CANVAS_BOTTOM_RIGHT[0], 8):
        pyautogui.click(x, y)
