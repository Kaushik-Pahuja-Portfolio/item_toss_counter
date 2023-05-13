import pyautogui
import cv2 as cv
import numpy as np
from PIL import ImageGrab
import time
import keyboard
import csv
import keybinds
from consts import item_mapping, scrsht_time
from threading import Event, Thread
from math import floor
print("initializing...")

#this is the list that you'll use to determine toss order. default just one normal item toss
#assumes it is set to normal when you start executing
toss_order = ["banana", "normal"]
last_toss = 0
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
    "bomb": 0,
    "100t": 0,
    "donut": 0,
    "banana": 0,
    "afro": 0,
    "meteor": 0,
    "minfaust": 0,
    "tumpet": 0,
    "hammer": 0,
    "peel": 0
}

#event to handle exit
quit_req = Event()

def sleep(time):
    quit_req.wait(time)
    

def quit_listen():
    while not quit_req.is_set():
        if keyboard.is_pressed(keybinds.quit):
            quit_req.set()
        sleep(0.001)

def toss_item(item: str):
    global last_toss
    num_presses = abs(floor(item_mapping[item]) - last_toss)
    
    if num_presses > 0:
        keybinds.press(keybinds.menu)
        sleep(0.3)
        button = keybinds.left if item_mapping[item] < last_toss else keybinds.right
        for i in range(num_presses):
            keybinds.press(button)
            sleep(0.1)
        keybinds.press(keybinds.menu)
        last_toss = floor(item_mapping[item])
        sleep(0.2)
    keybinds.item()
    sleep(scrsht_time)
    while item == 'peel' and read_item(False) != 'peel':
        keybinds.press(keybinds.reset)
        sleep(0.2)
        keybinds.item()
        sleep(scrsht_time)
        

def read_item(add=True):
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY)
    for k in template:
        w, h = template[k].shape[::-1]
        result = cv.matchTemplate(screenshot, template[k], cv.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.90)
        for pt in zip(*loc[::-1]):
            if add:
                count[k] += 1
            print("i see " + k + " #{}".format(count[k]))
            return k
            break

print("ready")


def main():
    while not quit_req.is_set():
        keybinds.press(keybinds.reset)
        sleep(0.3)
        for i in toss_order:
            #toss an item
            toss_item(i)
            if i == 'normal':
                read_item()
            sleep(0.55-scrsht_time)

while True:
    if keyboard.is_pressed(keybinds.quit):
        exit()
    if keyboard.is_pressed(keybinds.start):
        break
print("doing the do")
t1 = Thread(target=main)
t2 = Thread(target=quit_listen)
t1.start()
t2.start()
t1.join()
t2.join()
with open('item_counts.csv', 'w') as csvfile:
    csvfile.writelines([','.join(count.keys()) + "\n", ','.join(map(str, list(count.values())))])