class ButtonHandler(object):

    piFaceManager = None

    isLocked = False
    lockedButton = None

    def unlock(self):
        self.isLocked = False
        self.lockedButton = None
        self.piFaceManager.setPlayerButtonColor(0,"off", False)

    def pressed(self,pin_num):
        if pin_num == 2 and self.isLocked:
            self.unlock()
        elif not self.isLocked:
            self.isLocked = True
            self.lockedButton = pin_num
            self.piFaceManager.setPlayerButtonColor(pin_num,"white",False)

    def setPiFaceManager(self,piFaceManager):
        self.piFaceManager = piFaceManager
        
    def __init__(self):
        return super(ButtonHandler, self).__init__()




