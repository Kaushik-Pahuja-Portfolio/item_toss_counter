import keyboard
import keybinds
import time
import consts
import cv2 as cv
import numpy as np
from PIL import ImageGrab

template = {
    "minfaust": cv.imread("templates/minifaust.png", cv.IMREAD_GRAYSCALE),
    "trumpet": cv.imread("templates/trumpet.png", cv.IMREAD_GRAYSCALE),
    "hammer": cv.imread("templates/hammer.png", cv.IMREAD_GRAYSCALE),
    "bomb": cv.imread("templates/bomb.png", cv.IMREAD_GRAYSCALE),
    "100t": cv.imread("templates/100t.png", cv.IMREAD_GRAYSCALE),
    "afro": cv.imread("templates/afro.png", cv.IMREAD_GRAYSCALE),
    "banana": cv.imread("templates/banana.png", cv.IMREAD_GRAYSCALE),
    "meteor": cv.imread("templates/meteor.png", cv.IMREAD_GRAYSCALE),
    "peel": cv.imread("templates/peel.png", cv.IMREAD_GRAYSCALE),
    "donut": cv.imread("templates/donut.png", cv.IMREAD_GRAYSCALE),
}

while True:
    if keyboard.is_pressed(keybinds.quit):
        exit()
    if keyboard.is_pressed(keybinds.start):
        break

failcount = 0

def match_items(screenshot, add=True, item=None):
    global failcount
    result = cv.matchTemplate(screenshot, template[item], cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if max_val >= 0.9:
        print("i see " + item)
    else:
        cv.imwrite("failed_captures/not_{}_{}_{}.png".format(item, failcount, max_val), screenshot)
        failcount += 1
    return max_val

def increment_item():
    keybinds.press(keybinds.reset)
    time.sleep(0.3)
    keybinds.press(keybinds.menu)
    time.sleep(0.3)
    keybinds.press(keybinds.right)
    time.sleep(0.2)
    keybinds.press(keybinds.menu)
    time.sleep(0.3)

consts.delete_failed_captures()
for i in range(9):
    increment_item()
    keybinds.item()
    time.sleep(consts.scrsht_time)
    screenshot = ImageGrab.grab(bbox=consts.scrsht_bounds)
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY)
    for item in template.keys():
        print(item)
        match_items(screenshot, False, item)
increment_item()