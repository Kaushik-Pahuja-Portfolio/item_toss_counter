import pyautogui
import cv2 as cv
import numpy as np
from PIL import ImageGrab
import time
import keyboard
import csv
import keybinds
from consts import get_item_index, item_mapping, scrsht_time, scrsht_bounds, delete_failed_captures
from threading import Event, Thread, Lock
from math import floor
from copy import copy


#this is the list that you'll use to determine toss order. default just one normal item toss
#assumes it is set to normal when you start executing
toss_order = ['minifaust','normal']
num_iterations = 24
last_toss = 0
failcount = 0
template = {
    "minifaust": cv.imread("templates/minifaust.png", cv.IMREAD_GRAYSCALE),
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
high_items  = ['minifaust', 'trumpet', 'hammer', 'bomb', '100t']
low_items = ['afro', 'banana', 'meteor', 'peel', 'donut']

count = {
    "bomb": 0,
    "100t": 0,
    "donut": 0,
    "banana": 0,
    "afro": 0,
    "meteor": 0,
    "minifaust": 0,
    "trumpet": 0,
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
    num_presses = abs(floor(get_item_index(item) - last_toss))
    if num_presses > 0:
        keybinds.press(keybinds.menu)
        sleep(0.3)
        button = keybinds.left if (num_presses > 5) != (get_item_index(item) < last_toss) else keybinds.right
        if num_presses > 5: num_presses = abs(10 - num_presses)
        for i in range(num_presses):
            keybinds.press(button)
        sleep(0.1)
        keybinds.press(keybinds.menu)
        last_toss = get_item_index(item)
        sleep(0.22)
    duration = keybinds.item()
    sleep(scrsht_time)
    if floor(item_mapping[item]) == 4:
        correct_nanner = check_item(cv.cvtColor(np.array(ImageGrab.grab(bbox=scrsht_bounds)), cv.COLOR_RGB2GRAY), item, False)
        while correct_nanner < 0.9 and not quit_req.is_set():
            keybinds.press(keybinds.reset)
            sleep(0.2)
            duration = keybinds.item()
            sleep(scrsht_time)
            correct_nanner = check_item(cv.cvtColor(np.array(ImageGrab.grab(bbox=scrsht_bounds)), cv.COLOR_RGB2GRAY), item, True)
            print(correct_nanner)
    return duration

def check_item(screenshot, item, must_match = False):
    result = cv.matchTemplate(screenshot, template[item], cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if max_val >= 0.9:
        print("i see " + item)
    elif must_match:
        cv.imwrite("failed_captures/not_{}_{}_{}.png".format(item, failcount, max_val), screenshot)
    return max_val

lock = Lock()
best_match = ["none", 0]

def match_items(templates:list = None, trigger:Event = None, add=True, item=None):
    global screenshot
    global best_match
    global failcount
    while not quit_req.is_set():
        trigger.wait()
        if quit_req.is_set():
            return
        trigger.clear()
        found = False
        for k in templates:
            if trigger_matched.is_set():
                break
            m_coeff = check_item(screenshot, k)
            if m_coeff >= 0.9:
                if add:
                    count[k] += 1
                trigger_matched.set()
                break
            elif m_coeff > best_match[1]:
                lock.acquire()
                best_match[0] = k
                best_match[1] = m_coeff
                lock.release()


trigger_matched = Event()
screenshot = None

def main():
    global screenshot
    global failcount
    trigger_check_low = Event()
    trigger_check_high = Event()
    thread_high = Thread(target=match_items, args=(high_items, trigger_check_high, ))
    thread_low = Thread(target=match_items, args=(low_items, trigger_check_low))
    thread_high.start()
    thread_low.start()
    sleep(0.5)
    x  = 0
    while not quit_req.is_set():
        x += 1
        if(x > num_iterations):
            print("done")
            quit_req.set()
            trigger_check_high.set()
            trigger_check_low.set()
            break
        
        keybinds.press(keybinds.reset)
        sleep(0.3)
        if not quit_req.is_set():
            for i in toss_order:
                #toss an item
                toss_item(i)
                if i == 'normal':
                    screenshot = cv.cvtColor(np.array(ImageGrab.grab(bbox=scrsht_bounds)), cv.COLOR_RGB2GRAY)
                    trigger_check_low.set()
                    trigger_check_high.set()
                sleep(0.4 - scrsht_time)
                if(trigger_matched.is_set()):
                    trigger_matched.clear()
                elif screenshot is not None:
                    failcount += 1
                    cv.imwrite("failed_captures/{}_{}.png".format(best_match, failcount), screenshot)
            print()
    trigger_check_low.set()
    trigger_check_high.set()
    keybinds.press(keybinds.quit)
    thread_high.join()
    thread_low.join()
    print_data()

def print_data():
    try:
        with open('item_counts.csv', mode='r') as infile:
            if infile is not None:
                reader = csv.reader(infile)
                mydict = dict((row[0],int(row[1])) for row in reader)
                for k in mydict.keys():
                    if k in count.keys():
                        count[k] += mydict[k]
    except:
        print("item_counts.csv doesn't exist yet. no data to read.")

    with open('item_counts.csv', 'w') as csvfile:
        csvfile.writelines('\n'.join(map(lambda x: x+",{}".format(count[x]), count.keys())))

    try:
        with open('item_proportions.csv', 'w') as file:
            file.writelines("\n".join(map(lambda x: x+",{}".format(count[x]/sum(count.values())), count.keys())))
    except:
        pass


if __name__ == "__main__":
    delete_failed_captures()
    while True:
        if keyboard.is_pressed(keybinds.quit):
            print_data()
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