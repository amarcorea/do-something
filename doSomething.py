#Author Marco Rea <amarco.rea@gmail.com>
#v1. New program. Do click every N seconds to keep alive the host

from pynput import keyboard as kb
from pynput import mouse as ml
from datetime import datetime
from datetime import time as dt_time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import pyautogui
import time
from random import randint

pyautogui.FAILSAFE = False
lastMovement = datetime.now()
timeCurrent = datetime.now()
lastMovementAux = None
timeElapsed = None
debug = False # True if you want to see the debug messages, Ex. True

XSCREEN,YSCREEN = pyautogui.size() # X,Y coordinates to init with the resolution, Ex. x=15, y=1059
CLICK_RANDOM = False # True if you want click in random coordinates
XCOOR, YCOOR = [21, 1059] # If CLICK_RANDOM is true, this value is taken by default in another way it takes XSCREEN,YSCREEN
NOACTIVITY = 60 * 1   # Value in seconds, it must be less than screensaver time, Ex. 240 seconds.
SENSORTIME = 30 # Value in seconds, as a ping command to exec the clic activity, Ex. every 30 seconds exec click (random or not) as long as you dont have an activity previously
TIME_START = "07:30" # Time to start the activity, Ex. 08:00
TIME_END = "18:10" # Time to end the activity, Ex. 18

def log(msg, fn=""):
    dateLog = datetime.now()
    print("[{0}] - {1} - {2}".format(dateLog, fn, msg))


def refreshTime():
    global lastMovement

    lastMovementAux = lastMovement
    lastMovement = datetime.now()

    if debug:
        log("Older last activity  : {0}".format(lastMovementAux), refreshTime.__name__)
        log("Current last activity: {0}".format(lastMovement), refreshTime.__name__)


def onPress(key):
    global debug
    if debug:
        log("Key pressed: {0}".format(key), onPress.__name__)
    refreshTime()


def onClick(x, y, button, pressed):
    global debug
    if pressed:
        if debug:
            log("Click button {0} in ({1},{2})".format(
            button, x, y), onClick.__name__)
        refreshTime()


def onScroll(x, y, dx, dy):
    global debug
    if debug:
        log("Scroll identified in: ({0},({1},{2},{3})".format(
            x, y, dx, dy), onScroll.__name__)
    refreshTime()


def getDifference(start, end=datetime.now()):
    duration = end - start
    return duration.total_seconds()


def is_time_in_range(start_time, end_time, timezone="America/Mexico_City"):
    """
    Return True if current local time in `timezone` is inside [start_time, end_time].

    Accepted `start_time` / `end_time` formats:
    - "HH:MM"
    - "HH:MM:SS"
    - datetime.time

    Supports ranges crossing midnight, e.g. 22:00 -> 06:00.
    """
    tz_aliases = {
        "ciudad de mexico": "America/Mexico_City",
        "mexico city": "America/Mexico_City",
        "mexico": "America/Mexico_City",
        "mazatlan": "America/Mazatlan",
        "colombia": "America/Bogota",
        "bogota": "America/Bogota",
    }

    def _parse_time(value):
        if isinstance(value, dt_time):
            return value

        if isinstance(value, str):
            for fmt in ("%H:%M:%S", "%H:%M"):
                try:
                    return datetime.strptime(value.strip(), fmt).time()
                except ValueError:
                    pass

        raise ValueError(
            "start_time/end_time must be 'HH:MM', 'HH:MM:SS' or datetime.time"
        )

    start = _parse_time(start_time)
    end = _parse_time(end_time)

    tz_name = tz_aliases.get(str(timezone).strip().lower(), timezone)
    try:
        now_local = datetime.now(ZoneInfo(tz_name)).time()
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unknown timezone: {timezone}") from exc

    if start <= end:
        return start <= now_local <= end

    # Range crosses midnight, e.g. 22:00-06:00.
    return now_local >= start or now_local <= end


def initKeyboardListener():
    listener = kb.Listener(on_press=onPress)
    listener.start()


def initMouseListener():
    listener = ml.Listener(on_click=onClick, on_scroll=onScroll)
    listener.start()


def doMovement():
    global timeCurrent
    global XSCREEN, YSCREEN
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
    

    log("Starting variables", init.__name__)

    while True:
        if is_time_in_range(TIME_START, TIME_END):
            log(f"Current time is in range {TIME_START} - {TIME_END} hrs", init.__name__)
        
            diff_seconds = getDifference(lastMovement, datetime.now())
            diff_minutes = divmod(diff_seconds, 60)[0]

            if diff_seconds > NOACTIVITY:
                log("Elapsed time in seconds: {0} seconds(s)".format(diff_seconds), init.__name__)
                log("Elapsed time in minutes: {0} minutes(s)".format(diff_minutes), init.__name__)
                doMovement()

        else:
            log(f"Current time is out of range {TIME_START} - {TIME_END} hrs, pinging after {SENSORTIME} seconds", init.__name__)

        time.sleep(SENSORTIME)


def run():
    initKeyboardListener()
    initMouseListener()
    init()

if __name__ == "__main__":
    run()
