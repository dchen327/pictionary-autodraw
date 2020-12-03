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


def brush_size(size):
    pyautogui.scroll(-10)
    sleep(0.2)
    pyautogui.scroll(size)


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


def rgb_dist(color1, color2):
    """ Returns squared euclidean distance between two numpy RGB triples """
    return np.sum((color1 - color2) ** 2)

# if __name__ == '__main__':
#     alt_tab()
#     sleep(1)
#     # select_brush('mid')
#     brush_size(0)

#     # # img = Image.open(ASSETS_PATH / 'turtle.jpeg')
#     img = Image.open(ASSETS_PATH / 'pig.png').convert('RGB')
#     draw_arr = draw_img(img)
#     img_w, img_h = img.size

#     dist = 3

#     for i in range(img_w):
#         for j in range(img_h):
#             if draw_arr[i, j]:
#                 x = CANVAS_TOP_LEFT[0] + dist * i
#                 y = CANVAS_TOP_LEFT[1] + dist * j
#                 pyautogui.click(x, y)
#                 # print(x, y)


img = Image.open(ASSETS_PATH / 'soccerball.resized.png').convert('RGB')
# img = Image.open(ASSETS_PATH / 'soccerball.png').convert('RGB')
img_w, img_h = img.size
img_arr = np.array(img)
img_2d = [[0] * img_h for _ in range(img_w)]
for i in range(img_w):
    for j in range(img_h):
        color = img_arr[i, j]
        BLACK = np.array([0, 0, 0])
        WHITE = np.array([255, 255, 255])
        if np.array_equal(color, BLACK):  # transparent
            continue
        if rgb_dist(color, BLACK) <= rgb_dist(color, WHITE):
            img_2d[i][j] = 1


def print_color_grid():
    """ Print color ids in grid """
    for i in range(img_w):
        for j in range(img_h):
            print(int(img_2d[i][j]), end=' ')
        print()


def draw_commands(commands, scale):
    """ draw commands of the given format:
    color, start_pos, end_pos
    """
    for command in commands:
        color, start_pos, end_pos = command
        x0, y0 = arr_coords_to_canvas(*start_pos, scale=scale)
        x1, y1 = arr_coords_to_canvas(*end_pos, scale=scale)
        pyautogui.moveTo(x0, y0)
        pyautogui.dragTo(x1, y1)


def arr_coords_to_canvas(i, j, scale):
    """ Converts (x, y) array position to canvas """
    x = CANVAS_TOP_LEFT[0] + scale * j
    y = CANVAS_TOP_LEFT[1] + scale * i
    return (x, y)


commands = []

for i, row in enumerate(img_2d):
    curr_color, start_idx = row[0], 0
    # add on -1 at the end to grab all sequences
    for idx, color in enumerate(row + [-1]):
        if color != curr_color:
            # color, start_pos, end_pos
            if curr_color != 0:
                commands.append((curr_color, (i, start_idx), (i, idx)))
            curr_color, start_idx = color, idx  # update colors and start idx


# alt_tab()
# sleep(2)
# brush_size(1)
# draw_commands(commands, scale=3)
