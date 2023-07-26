#Author Marco Rea <amarco.rea@gmail.com>
#v1. New program. Do click every N seconds to keep alive the host

from pynput import keyboard as kb
from pynput import mouse as ml
from datetime import datetime
import pyautogui
import time
from random import randint

pyautogui.FAILSAFE = False
lastMovement = datetime.now()
timeCurrent = datetime.now()
lastMovementAux = None
timeElapsed = None
debug = True

XSCREEN,YSCREEN = pyautogui.size() # X,Y coordinates to init with the resolution, Ex. x=15, y=1059
CLICK_RANDOM = False # True if you want click in random coordinates
XCOOR, YCOOR = [21, 1059] # If CLICK_RANDOM is true, this value is taken by default in another way it takes XSCREEN,YSCREEN
NOACTIVITY = 4 * 60  # Value in seconds, it must be less than screensaver time, Ex. 240 seconds.
SENSORTIME = 30 # Value in seconds, as a ping command to exec the clic activity, Ex. every 30 seconds exec click (random or not) as long as you dont have an activity previously


def log(msg, fn=""):
    if debug:
        dateLog = datetime.now()
        print("[{0}] - {1} - {2}".format(dateLog, fn, msg))


def refreshTime():
    global lastMovement

    lastMovementAux = lastMovement
    lastMovement = datetime.now()

    log("Older last activity  : {0}".format(lastMovementAux), refreshTime.__name__)
    log("Current last activity: {0}".format(lastMovement), refreshTime.__name__)


def onPress(key):
    log("Key pressed: {0}".format(key), onPress.__name__)
    refreshTime()


def onClick(x, y, button, pressed):
    if pressed:
        log("Click button {0} in ({1},{2})".format(
            button, x, y), onClick.__name__)
        refreshTime()


def onScroll(x, y, dx, dy):
    log("Scroll identified in: ({0},({1},{2},{3})".format(
        x, y, dx, dy), onScroll.__name__)
    refreshTime()


def getDifference(start, end=datetime.now()):
    duration = end - start
    return duration.total_seconds()


def initKeyboardListener():
    listener = kb.Listener(on_press=onPress)
    listener.start()


def initMouseListener():
    listener = ml.Listener(on_click=onClick, on_scroll=onScroll)
    listener.start()


def doMovement():
    global timeCurrent
    global XCREEN, YSCCREEN
    XSCREEN,YSCREEN = pyautogui.size()
    x = randint(1, XSCREEN) if CLICK_RANDOM == True else XCOOR
    y = randint(1, YSCREEN) if CLICK_RANDOM == True else YCOOR
    pyautogui.moveTo(x, y)
    pyautogui.click()
    if not CLICK_RANDOM:
        time.sleep(1)
        pyautogui.click()
    refreshTime()
    log("Activating host - click in coordinates ({0},{1})".format(x,y), doMovement.__name__)

def init():
    global lastMovement
    global timeCurrent
    

    log("Starting variables", run.__name__)

    while True:
        diff_seconds = getDifference(lastMovement, datetime.now())
        diff_minutes = divmod(diff_seconds, 60)[0]

        if diff_seconds > NOACTIVITY:
            log("Elapsed time in seconds: {0} seconds(s)".format(diff_seconds), run.__name__)
            log("Elapsed time in minutes: {0} minutes(s)".format(diff_minutes), run.__name__)
            doMovement()

        time.sleep(SENSORTIME)


def run():
    initKeyboardListener()
    initMouseListener()
    init()

if __name__ == "__main__":
    run()