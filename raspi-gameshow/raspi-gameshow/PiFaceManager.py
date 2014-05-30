#Check if module pifacedigitalio is available - if not, revert to keyboard controls...
piFaceAvail = True
try:
    import pifacedigitalio  
except:
    print "Module pifacedigitalio could not be imported, reverting to keyboard controls"
    piFaceAvail = False

class PiFaceManager(object):

    pifacedigital = None
    buttonHandler = None
    buttonListener = None

    def buttonPressed(self,event):
        self.buttonHandler.pressed(event.pin_num)

    def deactivate(self):
        if piFaceAvail:
            self.buttonListener.deactivate()
            self.pifacedigital.deinit_board()
    
    def __init__(self, buttonHandler):
        self.buttonHandler = buttonHandler
        if piFaceAvail:
            self.pifacedigital = pifacedigitalio.PiFaceDigital()
            self.buttonListener = pifacedigitalio.InputEventListener(chip=self.pifacedigital)
            self.buttonListener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, self.buttonPressed)
            self.buttonListener.register(1, pifacedigitalio.IODIR_FALLING_EDGE, self.buttonPressed)
            self.buttonListener.activate()
        else:
            #Todo
            pass
        return super(PiFaceManager, self).__init__()

    def __del__(self):
        self.deactivate()
