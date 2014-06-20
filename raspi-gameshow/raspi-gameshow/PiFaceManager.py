#Check if module pifacedigitalio is available - if not, print out Warning. 
piFaceAvail = True
try:
    import pifacedigitalio  
except:
    print "Warning: Module 'pifacedigitalio' could not be imported - please install the piface libraries and make sure to run on a raspi, you can use the keyboard instead"
    piFaceAvail = False

# translate colors to pins. PiFace doesn't have PWM, but still some colors can be mixed on a RGB led...
colors = {"red":(0,None),"green":(1,None),"blue":(2,None),"white":(0,1,2),"yellow":(0,1),"pink":(0,2),"turquois":(0,1),"off":(None)}

class PiFaceManager(object):

    pifacedigital = None
    buttonHandler = None
    buttonListener = None

    # will be called by interrupt of PiFace when button 1-3 are pressed.
    def buttonPressed(self,event):
        print "Pressed:", event.pin_num
        # hand over to button handler
        self.buttonHandler.pressed(event.pin_num)

    # write out color to button. Player is 0 or 1, color consists of up to 3 pins. Calculate adress to write output...
    # First player gets pin 0-2, second 3-5. Order of connection is red, green, blue
    def setPlayerButtonColor(self,player,color, keep=False):
        print "Set player",player,"to color",color
        if not keep:
            print "Set all ports to 0"
            if piFaceAvail:
                self.pifacedigital.output_port.all_off()
        player = player * 3
        pins = colors[color]
        if pins is not None:
            for pin in pins:
                if pin is not None:
                    print "Set Port",(player+pin),"to high"
                    if piFaceAvail:
                        self.pifacedigital.leds[player+pin].set_high()

    # to be called when program ends, also called from __del__()
    def deactivate(self):
        if piFaceAvail:
            self.buttonListener.deactivate()
            self.pifacedigital.deinit_board()
    
    def __init__(self, buttonHandler):
        self.buttonHandler = buttonHandler
        self.buttonHandler.setPiFaceManager(self)
        if piFaceAvail:
            self.pifacedigital = pifacedigitalio.PiFaceDigital()
            self.buttonListener = pifacedigitalio.InputEventListener(chip=self.pifacedigital)
            self.buttonListener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, self.buttonPressed)
            self.buttonListener.register(1, pifacedigitalio.IODIR_FALLING_EDGE, self.buttonPressed)
            self.buttonListener.register(2, pifacedigitalio.IODIR_FALLING_EDGE, self.buttonPressed)
            self.buttonListener.activate()
        return super(PiFaceManager, self).__init__()

    def __del__(self):
        self.deactivate()
