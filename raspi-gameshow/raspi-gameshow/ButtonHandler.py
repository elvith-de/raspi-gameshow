class ButtonHandler(object):

    lastPin = None

    def pressed(self,pin_num):
        print "Pin",pin_num,"pressed"
        self.lastPin = pin_num
        
    def __init__(self):
        return super(ButtonHandler, self).__init__()




