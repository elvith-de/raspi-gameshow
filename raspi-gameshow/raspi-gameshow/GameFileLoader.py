import threading
import xml.etree.ElementTree as ET

class GameFileLoader(threading.Thread):
    """description of class"""

    file = None
    loader = None

    def __init__(self,file,loaderGameObject):
        self.file = file
        self.loader = loaderGameObject
        return super(GameFileLoader,self).__init__(name="XMLLoader")

    def run(self):
        import time as t
        t.sleep(1)
        self.loader.setText("Lade Datei")
        t.sleep(1)
        self.loader.setText("loading")
        t.sleep(1)
        self.loader.setText("still loading")
        t.sleep(1)
        self.loader.setText("and still loading")
        t.sleep(1)
        self.loader.setText("almost ready")
        t.sleep(1)
        self.loader.setText("haha just kidding")
        t.sleep(1)
        self.loader.setText("finished in 1s")
        t.sleep(1)
        self.loader.setText("finish")