"""
A python script to draw in the game skribblio

Author: David Chen
"""
import pyautogui
import numpy as np
from PIL import Image
from time import sleep
from pathlib import Path

# canvas params
CANVAS_TOP_LEFT = (370, 195)
CANVAS_WIDTH, CANVAS_HEIGHT = 1000, 750
CANVAS_BOTTOM_RIGHT = (
    CANVAS_TOP_LEFT[0] + CANVAS_WIDTH, CANVAS_TOP_LEFT[1] + CANVAS_HEIGHT)


# other
ASSETS_PATH = Path('./assets')

pyautogui.PAUSE = 0.0


def alt_tab():
    """ Switch to recent window """
    sleep(.5)
    pyautogui.keyDown('alt')
    sleep(.3)
    pyautogui.press('tab')
    sleep(.3)
    pyautogui.keyUp('alt')


def select_brush(size):
    """ Select the brush using the icon screenshot 
    Sizes: small, mid, large, xlarge
    """
    brush_path = ASSETS_PATH / f'{size}_brush.png'
    x, y = pyautogui.locateCenterOnScreen(str(brush_path.absolute()))
    pyautogui.click(x, y)


def img_resize(img):
    """ resize image to fit screen """
    pass


def draw_img(img):
    """ Draw provided image on canvas """
    arr = np.array(img)
    arr = np.transpose(arr, (1, 0, 2))  # permute back to (width, height)
    WHITE = np.array([255, 255, 255])
    draw_arr = np.zeros(img.size)
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            if not np.array_equal(arr[x, y], WHITE):
                draw_arr[x][y] = 1
    return draw_arr


if __name__ == '__main__':
    alt_tab()
    sleep(1)
    select_brush('mid')

    img = Image.open(ASSETS_PATH / 'turtle.jpeg')
    draw_arr = draw_img(img)
    img_w, img_h = img.size

    dist = 4

    for i in range(img_w):
        for j in range(img_h):
            if draw_arr[i, j]:
                x = CANVAS_TOP_LEFT[0] + 4 * i
                y = CANVAS_TOP_LEFT[1] + 4 * j
                pyautogui.click(x, y)
                # print(x, y)
