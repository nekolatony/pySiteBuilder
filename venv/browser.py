from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import threading
import sys
url = r"C:\Users\nekol\Documents\PycharmProjects\webSite-generator\venv\Site\site.html"


class Browser(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Browser,self).__init__(*args,**kwargs)
        self.setWindowTitle("HTML Builder")
        self.renderer = QWebEngineView()

        self.renderer.load(QUrl.fromLocalFile(url))

        self.setCentralWidget(self.renderer)
        self._updator = QTimer(self)
        self._updator.setSingleShot(False)
        self._updator.timeout.connect(self.reload)
        # Reload every 4 seconds
        self._updator.start(200)

    def reload(self):
        self.renderer.reload()

class BrowserOpener(threading.Thread): # convert html to pdf

    def __init__(self ,):
        threading.Thread.__init__(self)
        self.start()
    def run(self):
        app = QApplication(sys.argv)

        self.browser = Browser()
        self.browser.show()
        app.exec_()
    def Refresh(self):
        self.browser.reload()


# def new(*args, **kwargs):
#     return BrowserOpener()

BrowserOpener()