import pyautogui
import cv2 as cv
import numpy as np
from PIL import ImageGrab
import time
import keyboard
import csv

screenshot = None
start = ' ' #which button do you want to start execution?
quit = 'q' #which button do you want to quit execution?
reset = "m" #what is your position reset button?

print("initializing...")
template = {
    "100t": cv.imread("templates/100t.png", cv.IMREAD_GRAYSCALE),
    "afro": cv.imread("templates/afro.png", cv.IMREAD_GRAYSCALE),
    "banana": cv.imread("templates/banana.png", cv.IMREAD_GRAYSCALE),
    "bomb": cv.imread("templates/bomb.png", cv.IMREAD_GRAYSCALE),
    "donut": cv.imread("templates/donut.png", cv.IMREAD_GRAYSCALE),
    "hammer": cv.imread("templates/hammer.png", cv.IMREAD_GRAYSCALE),
    "meteor": cv.imread("templates/meteor.png", cv.IMREAD_GRAYSCALE),
    "minfaust": cv.imread("templates/minifaust.png", cv.IMREAD_GRAYSCALE),
    "peel": cv.imread("templates/peel.png", cv.IMREAD_GRAYSCALE),
    "tumpet": cv.imread("templates/trumpet.png", cv.IMREAD_GRAYSCALE)
}
count = {
    "100t": 0,
    "afro": 0,
    "banana": 0,
    "bomb": 0,
    "donut": 0,
    "hammer": 0,
    "meteor": 0,
    "minfaust": 0,
    "peel": 0,
    "tumpet": 0
}
print("ready")

while True:
    if keyboard.is_pressed(quit):
        exit()
    if keyboard.is_pressed(start):
        break
print("pressing restart repeatedly")
while (True):
    if keyboard.is_pressed(quit): break
    pyautogui.keyDown(reset)
    pyautogui.keyUp(reset)
    time.sleep(.3)
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY)
    for k in template:
        w, h = template[k].shape[::-1]
        result = cv.matchTemplate(screenshot, template[k], cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.98)
        for pt in zip(*loc[::-1]):
            count[k] += 1
            print("i see " + k + " #{}".format(count[k]))
            break

with open('item_counts.csv', 'w') as csvfile:
    csvfile.writelines([','.join(count.keys()) + "\n", ','.join(map(str, list(count.values())))])