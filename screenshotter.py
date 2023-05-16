import pyautogui
import cv2 as cv
import numpy as np
from PIL import ImageGrab
import time
import keyboard  # using module keyboard
import keybinds
from consts import scrsht_time, scrsht_bounds, item_mapping, get_item_index

items = ["bomb", "100t", "donut", "banana", "afro", "meteor", "minifaust", "trumpet", "hammer"]

print("set item toss to bomb. toss the item and take the screenshot, press your start button while in game.\nafter each item toss, move on to the next item and repeat this process")
for item in items:
    while True:  # making a loop
        if keyboard.is_pressed(keybinds.start):  # if key 'q' is pressed 
            keybinds.press(keybinds.reset)
            time.sleep(0.3)
            keybinds.item()
            time.sleep(scrsht_time)
            screenshot = np.array(ImageGrab.grab(bbox=scrsht_bounds))
            cv.imwrite("templates/"+item+".png", screenshot)
            time.sleep(1) #ensures no performance tanks from writing files
            break 
        elif keyboard.is_pressed(keybinds.quit):
            exit()

print("please set it back to banana so we can get a peel (or banana if you got peel the first time)\npress start when you're ready. hit quit when you get the right one")
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed(keybinds.start):  # if key 'q' is pressed 
            keybinds.press(keybinds.reset)
            time.sleep(0.3)
            keybinds.item()
            time.sleep(scrsht_time)
            screenshot = ImageGrab.grab(bbox=scrsht_bounds)
            screenshot = np.array(screenshot)
            cv.imwrite("templates/peel.png", screenshot)
            time.sleep(1)
        if keyboard.is_pressed(keybinds.quit):
            exit()
    except:
        break