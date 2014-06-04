import PiFaceManager
import ButtonHandler
import time

def testInput():
    handler = ButtonHandler.ButtonHandler()
    piFaceManager = PiFaceManager.PiFaceManager(handler)
    print "You have 45 seconds to smash the buttons"
    time.sleep(45)
    print "Time's up, cleaning up and ending program..."
    piFaceManager.deactivate()

def testButtonLock():
    handler = ButtonHandler.ButtonHandler()
    piFaceManager = PiFaceManager.PiFaceManager(handler)
    print "Button 0"
    handler.pressed(0)
    time.sleep(5)
    print "Button reset"
    handler.pressed(2)
    time.sleep(5)
    print "Button 1"
    handler.pressed(1)
    time.sleep(5)
    print "Button reset"
    handler.pressed(2)
    time.sleep(5)
    print "Button 1"
    handler.pressed(1)
    time.sleep(5)
    print "Button 1 (w/o reset)"
    handler.pressed(1)
    time.sleep(5)
    print "Button 0 (w/o reset)"
    handler.pressed(0)
    time.sleep(5)
    print "cleaning up and ending program..."
    piFaceManager.deactivate()

def testColor():
    handler = ButtonHandler.ButtonHandler()
    piFaceManager = PiFaceManager.PiFaceManager(handler)
    
    piFaceManager.setPlayerButtonColor(0,"white")
    time.sleep(5)
    piFaceManager.setPlayerButtonColor(1,"white",True)
    time.sleep(5)
    piFaceManager.setPlayerButtonColor(0,"red")
    time.sleep(5)
    piFaceManager.setPlayerButtonColor(0,"green")
    time.sleep(5)
    piFaceManager.setPlayerButtonColor(0,"blue")
    time.sleep(5)
    
    piFaceManager.setPlayerButtonColor(1,"yellow")
    time.sleep(5)
    
    piFaceManager.setPlayerButtonColor(1,"pink")
    time.sleep(5)
    
    piFaceManager.setPlayerButtonColor(0,"turquois")
    time.sleep(5)

    print "cleaning up and ending program..."
    piFaceManager.deactivate()

if __name__ == '__main__':
    #testInput()
    #testButtonLock()
    testColor()