from pynput import keyboard as kb
from pynput import mouse as ml
from datetime import datetime
import pyautogui
import time

pyautogui.FAILSAFE = False
lastMovement = datetime.now()
timeCurrent = datetime.now()
lastMovementAux = None
timeElapsed = None
debug = True

CLIC_COORDINATES = (13,1059)
NOACTIVITY = 10  # En segundos
SENSORTIME = 3


def log(msg, fn=""):
    if debug:
        dateLog = datetime.now()
        print("[{0}] - {1} - {2}".format(dateLog, fn, msg))


def refreshTime():
    global lastMovement

    lastMovementAux = lastMovement
    lastMovement = datetime.now()

    log("Último movimiento anterior: {0}".format(lastMovementAux), refreshTime.__name__)
    log("Último movimiento actual  : {0}".format(lastMovement), refreshTime.__name__)


def onPress(key):
    log("Se ha pulsado la tecla {0}".format(key), onPress.__name__)
    refreshTime()


def onClick(x, y, button, pressed):
    if pressed:
        log("Se ha clickeado el botón {0} en ({1},{2})".format(
            button, x, y), onClick.__name__)
        refreshTime()


def onScroll(x, y, dx, dy):
    log("Se ha hecho scroll en ({0},({1},{2},{3})".format(
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
    pyautogui.moveTo(CLIC_COORDINATES[0], CLIC_COORDINATES[1])
    pyautogui.click()
    refreshTime()
    log("Activando equipo - click en coordenadas ({0},{1})".format(CLIC_COORDINATES[0],CLIC_COORDINATES[1]), doMovement.__name__)

def init():
    global lastMovement
    global timeCurrent

    log("Inicializando variables", run.__name__)

    while True:
        diff_seconds = getDifference(lastMovement, datetime.now())
        diff_minutes = divmod(diff_seconds, 60)[0]

        log(str(diff_seconds)+" > " + str(NOACTIVITY), run.__name__)
        if diff_seconds > NOACTIVITY:
            log("Tiempo transcurrido en segundos: {0} minuto(s)".format(diff_seconds), run.__name__)
            log("Tiempo transcurrido en minutos : {0} minuto(s)".format(diff_minutes), run.__name__)
            doMovement()

        time.sleep(SENSORTIME)


def run():
    initKeyboardListener()
    initMouseListener()
    init()

if __name__ == "__main__":
    run()
