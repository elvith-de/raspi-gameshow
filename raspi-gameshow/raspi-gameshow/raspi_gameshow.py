import PiFaceManager
import ButtonHandler
import time

if __name__ == '__main__':
    handler = ButtonHandler.ButtonHandler()
    piFaceManager = PiFaceManager.PiFaceManager(handler)
    print "Press Button 0 to test, button 1 to exit"
    while handler.lastPin != 1:
        time.sleep(1)
    piFaceManager.deactivate()
    