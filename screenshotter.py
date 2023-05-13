import pyautogui
import cv2 as cv
import numpy as np
from PIL import ImageGrab
import time
import keyboard  # using module keyboard

screenshot = None
items = ["bomb.png", "100t.png", "donut.png", "banana.png", "afro.png", "meteor.png", "minifaust.png", "trumpet.png", "hammer.png"]
start = ' ' #which button do you want to start execution?
quit = 'q' #which button do you want to quit execution?
reset = "m" #what is your position reset button?

print("set item toss to bomb. toss the item and take the screenshot, press your start button while in game.\nafter each item toss, move on to the next item and repeat this process")
for item in items:
    while True:  # making a loop
        if keyboard.is_pressed(start):  # if key 'q' is pressed 
            pyautogui.keyDown(reset)
            pyautogui.keyUp(reset)
            
            time.sleep(0.3)
            screenshot = ImageGrab.grab()
            screenshot = np.array(screenshot)
            cv.imwrite(item, screenshot)
            time.sleep(1) #ensures no performance tanks from writing files
            break 
        elif keyboard.is_pressed(quit):
            exit()

print("please set it back to banana so we can get a peel (or banana if you got peel the first time)\npress start when you're ready. hit quit when you get the right one")
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed(start):  # if key 'q' is pressed 
            pyautogui.keyDown(reset)
            pyautogui.keyUp(reset)
            time.sleep(0.3)
            screenshot = ImageGrab.grab()
            screenshot = np.array(screenshot)
            cv.imwrite("peel.png", screenshot)
            time.sleep(1)
        if keyboard.is_pressed(quit):
            exit()
    except:
        break