import pyautogui

start = ' ' #which button do you want to start execution?
quit = 'q' #which button do you want to quit execution?
reset = 'm' #what is your position reset button?
down = 'p' #down if you're using arrow keys. I just used a weird set of keybinds
left = 'o' #similarly, left if you're using arrow keys
right = '[' #you get the idea
punch = 'f' #your punch button in game
menu = 'enter' #your start button in game
pyautogui.PAUSE = 0.02

def press(button:str):
    pyautogui.keyDown(button)
    pyautogui.keyUp(button)

def item():
    pyautogui.keyDown(down)
    pyautogui.keyDown(right)
    pyautogui.keyUp(down)
    pyautogui.keyUp(right)
    press(punch)