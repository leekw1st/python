import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import * 
import pykorbit

from_class = uic.loadUiType("pricewindow.ui")[0]


class MyWindow(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.inquery)

    def inquery(self):
        cur_time = QTime.currentTime()
        str_time = cur_time.toString("hh:mm:ss")
        self.statusBar().showMessage(str_time)
        price = pykorbit.get_current_price("BTC")
        self.lineEdit.setText(str(price))

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()