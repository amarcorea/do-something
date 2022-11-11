from email.utils import localtime
from numpy import result_type
from pynput import keyboard as kb
from datetime import datetime, timedelta
import pyautogui
import time
import random

lastMovement = datetime.now()
lastMovementAux = None
timeElapsed= None


def onPress(key):
    global lastMovement
    
    timeCurrent=datetime.now()
    lastMovementAux = lastMovement
    timeElapsed=timeCurrent - lastMovement
    lastMovement = timeCurrent
    
    print("Se ha pulsado la tecla "+str(key))
    print("Fecha anterior: "+str(lastMovementAux))
    print("Fecha actual: "+str(timeCurrent))
    print("Tiempo transcurrido: "+str(timeElapsed))
 
def getDifference(start, end = datetime.now()):
    
    duration = end - start
    
    

def initKeyboardListener():
    listener = kb.Listener(on_press=onPress)
    listener.start()

def doMovement():
    print("Clic in Windows Logo")
    x = 20
    y = 1060
    pyautogui.moveTo(x,y)
    pyautogui.click()

def run():
    global lastMovement
    while True:
        time.sleep(3)
        
        #TODO Compare last movement against current
        if (timeCurrent - lastMovement) < 5:
            doMovement()
#
#    localtime = time.localtime()
#
#    result = time.strftime("%I:%M:%S %p", localtime)
#
#    print("Move at " + str(result) + "(" + str(x) + ", " + str(y) + ")" )
#    time.sleep(5)

if __name__ == "__main__":
    initKeyboardListener()
    run()