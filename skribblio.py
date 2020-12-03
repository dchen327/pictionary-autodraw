"""
A python script to draw in the game skribblio

Author: David Chen
"""
import pyautogui
import numpy as np
import random
from PIL import Image
from time import sleep, time
from pathlib import Path

GAME = 'sketchful'  # sketchful or skribbl
if GAME == 'skribbl':
    # drawing canvas params
    CANVAS_TOP_LEFT = (370, 195)
    CANVAS_WIDTH, CANVAS_HEIGHT = 1000, 750
    CANVAS_BOTTOM_RIGHT = (
        CANVAS_TOP_LEFT[0] + CANVAS_WIDTH, CANVAS_TOP_LEFT[1] + CANVAS_HEIGHT)
    # color palette params
    PALETTE_TOP_LEFT = (480, 980)
    PALLETE_DIMS = (2, 11)  # 2 rows, 11 columns of colors
    SINGLE_COLOR_SIZE = 29  # size of one color tile
    RESIZE = (64, 64)  # max image size after resize
    IMG_SCALE = 10
elif GAME == 'sketchful':
    # drawing canvas params
    CANVAS_TOP_LEFT = (330, 270)
    CANVAS_WIDTH, CANVAS_HEIGHT = 1000, 750
    CANVAS_BOTTOM_RIGHT = (
        CANVAS_TOP_LEFT[0] + CANVAS_WIDTH, CANVAS_TOP_LEFT[1] + CANVAS_HEIGHT)
    # color palette params
    PALETTE_TOP_LEFT = (1372, 403)
    PALLETE_DIMS = (3, 13)
    SINGLE_COLOR_SIZE = 24  # size of one color tile
    RESIZE = (64, 64)  # max image size after resize
    IMG_SCALE = 12


# other
ASSETS_PATH = Path('./assets')

pyautogui.PAUSE = 0


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
    sleep(0.3)
    pyautogui.scroll(size)
    sleep(0.3)


def img_resize(img, size):
    """ Resize image to size, preserve aspect ratio """
    img.thumbnail(size, Image.ANTIALIAS)


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
    # return np.sum((color1 - color2) ** 2)
    # return sum((color1[i] - color2[i]) ** 2 for i in range(3))
    return sum(abs(color1[i] - color2[i]) for i in range(3))


def print_color_grid(img_2d):
    """ Print color ids in grid """
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,./'
    for i in range(len(img_2d)):
        for j in range(len(img_2d[0])):
            idx = int(img_2d[i][j])
            print(alpha[idx], end=' ')
        print()


def arr_coords_to_canvas(i, j, scale):
    """ Converts (x, y) array position to canvas """
    x = CANVAS_TOP_LEFT[0] + scale * j
    y = CANVAS_TOP_LEFT[1] + scale * i
    return (x, y)


def get_hex_array():
    pallete_rgb = []  # store rgb values of colors
    pallete_coords = []  # store coordinates of where to click on screen
    palette_img = Image.open(
        ASSETS_PATH / 'sketchful_palette.png').convert('RGB')
    curr_row = 0
    for color_idx in range(PALLETE_DIMS[0] * PALLETE_DIMS[1]):
        # start next row
        if color_idx > 0 and color_idx % PALLETE_DIMS[1] == 0:
            curr_row += 1
        curr_col = color_idx % PALLETE_DIMS[1]
        i = int(curr_col * SINGLE_COLOR_SIZE + SINGLE_COLOR_SIZE / 2)
        j = int(curr_row * SINGLE_COLOR_SIZE + SINGLE_COLOR_SIZE / 2)
        rgb = palette_img.getpixel((i, j))
        pallete_rgb.append(rgb)
        x = PALETTE_TOP_LEFT[0] + i
        y = PALETTE_TOP_LEFT[1] + j
        pallete_coords.append((x, y))
        # print('#{0:02x}{1:02x}{2:02x}'.format(*rgb))
    return pallete_rgb, pallete_coords


def get_closest_color(color, pallete_rgb):
    """ Given an RGB tuple, return the index in the color array of the
        closest color """
    min_dist = float('inf')
    closest_idx = -1
    for idx, palette_color in enumerate(pallete_rgb):
        dist = rgb_dist(color, palette_color)
        if dist < min_dist:
            min_dist = dist
            closest_idx = idx

    return closest_idx


def coord_manhattan_dist(x0, y0, x1, y1):
    """ Return manhattan dist between two points """
    return abs(x1 - x0) + abs(y1 - y0)


def pick_color(color, pallete_coords):
    """ Click and pick color in palette """
    x, y = pallete_coords[color]
    pyautogui.click(x, y)


def draw_commands(commands):
    """ draw commands of the given format:
        color, start_pos, end_pos
    """
    # random.shuffle(commands)
    for command in commands:
        color, start_pos, end_pos = command
        if color == 0:  # skip white
            continue
        x0, y0 = arr_coords_to_canvas(*start_pos, scale=IMG_SCALE)
        x1, y1 = arr_coords_to_canvas(*end_pos, scale=IMG_SCALE)
        pick_color(color, pallete_coords)
        pyautogui.moveTo(x0, y0)
        drag_dist = coord_manhattan_dist(x0, y0, x1, y1)
        if drag_dist <= 20:
            pyautogui.dragTo(x1, y1)
        else:
            pyautogui.dragTo(x1, y1, duration=0.12)


def create_commands(img_2d):
    """ Given 2D array with colors, create commands """
    commands_horiz = []
    commands_vert = []

    # loop through rows
    for i, row in enumerate(img_2d):
        curr_color, start_idx = row[0], 0
        # add on -1 at the end to grab all sequences
        for idx, color in enumerate(row + [-1]):
            if color != curr_color:
                # color, start_pos, end_pos
                if curr_color != 0:
                    commands_horiz.append(
                        (curr_color, (i, start_idx), (i, idx)))
                curr_color, start_idx = color, idx  # update colors and start idx

    # loop through columns
    for j in range(len(img_2d[0])):
        col = [img_2d[i][j] for i in range(len(img_2d))]
        curr_color, start_idx = col[0], 0
        # add on -1 at the end to grab all sequences
        for idx, color in enumerate(col + [-1]):
            if color != curr_color:
                # color, start_pos, end_pos
                if curr_color != 0:
                    commands_vert.append(
                        (curr_color, (start_idx, j), (idx, j)))
                curr_color, start_idx = color, idx  # update colors and start idx

    if len(commands_horiz) <= len(commands_vert):
        return commands_horiz
    return commands_vert


pallete_rgb, pallete_coords = get_hex_array()

img = Image.open(ASSETS_PATH / 'impossible_cube.png').convert('RGBA')
img_resize(img, RESIZE)
# we paste the image on a white background to ensure transparency is white and not black
white_bg = Image.new('RGBA', img.size, 'WHITE')  # create white background
white_bg.paste(img, (0, 0), img)
img = white_bg.convert('RGB')
img_w, img_h = img.size
img_arr = np.array(img)
img_2d = [[0] * img_w for _ in range(img_h)]
for i in range(img_h):
    for j in range(img_w):
        color = tuple(img_arr[i, j])
        img_2d[i][j] = get_closest_color(color, pallete_rgb)

# print_color_grid(img_2d)
alt_tab()
sleep(0.5)
brush_size(2)
commands = create_commands(img_2d)
start_time = time()
print(f'Number of commands: {len(commands)}')
draw_commands(commands)
print('{0:.2f}'.format(time() - start_time))
