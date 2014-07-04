#make sure to start in the right path since files might be referenced relative...
#see http://www.pygame.org/wiki/RunningInCorrectDirectory
def adjust_to_correct_appdir():
    import os, sys
    try:
        appdir = __file__
        if not appdir:
            raise ValueError
        appdir = os.path.abspath(os.path.dirname(__file__))
        os.chdir(appdir)
        if not appdir in sys.path:
            sys.path.insert(0,appdir)
    except:
        #placeholder for feedback, adjust to your app.
        #remember to use only python and python standard libraries
        #not any resource or module into the appdir 
        #a window in Tkinter can be adequate for apps without console
        #a simple print with a timeout can be enough for console apps
        print 'Please run from an OS console.'
        import time
        time.sleep(10)
        sys.exit(1)
adjust_to_correct_appdir()

import PiFaceManager
import ButtonHandler
import GameManager
import GameObject
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

def main():    
    handler = ButtonHandler.ButtonHandler()
    piFaceManager = PiFaceManager.PiFaceManager(handler)
    gameManager = GameManager.GameManager(GameObject.GameObject(),30,handler,piFaceManager)
    gameObject = GameObject.LoaderGameObject()
    gameManager.setActualGameObject(gameObject)

    gameManager.run()
    piFaceManager.deactivate()

if __name__ == '__main__':
    #testInput()
    #testButtonLock()
    #testColor()
    main()