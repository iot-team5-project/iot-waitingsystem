import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

rest_control = uic.loadUiType("rest_control.ui")[0]
user_basic = uic.loadUiType("user_basic.ui")[0]
user_reg = uic.loadUiType("user_reg.ui")[0]
user_reg_complete = uic.loadUiType("user_reg_complete.ui")[0]
user_status = uic.loadUiType("user_status.ui")[0]

WaitNewCustomer = False
waitCount = 0

class Control_TowerClass(QDialog, rest_control) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Restaurant Control Tower")
        self.btnUser.clicked.connect(self.customerWindow)

    def customerWindow(self):
        window_2 = Customer()
        window_2.exec_()

    def waitinglist(self, headcount):
        global WaitNewCustomer, waitCount
        row = self.WaitingList.rowCount()
        if WaitNewCustomer == True:
            self.WaitingList.insertRow(row)
            self.WaitingList.setItem(row, 0, QTableWidgetItem(str(waitCount)))
            self.WaitingList.setItem(row, 1, QTableWidgetItem(headcount+"명"))
            self.WaitingList.setItem(row, 2, QTableWidgetItem('입장대기'))
            for i in range(3):
                self.WaitingList.item(row, i).setTextAlignment(Qt.AlignCenter)
            WaitNewCustomer = False

class Customer(QDialog, user_basic, user_reg, user_reg_complete, user_status) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("USER UI")
        self.regMode = False
        self.btnLine.clicked.connect(self.customMakeLine)
        

    def customMakeLine(self):
        dialog = QDialog()
        uic.loadUi("user_reg.ui", dialog)
        dialog.setWindowTitle("USER UI Register")
        dialog.btnReg.clicked.connect(lambda : self.customerReg(dialog))
        dialog.exec_()

    def customerReg(self, dialog):
        global WaitNewCustomer, waitCount
        headcount = dialog.cbHeadCount.currentText()
        WaitNewCustomer = True
        waitCount += 1
        myWindows.waitinglist(headcount)
        dialog.close()
        self.customerRegComplete(waitCount)

    def customerRegComplete(self, waitCount):
        dialog = QDialog()
        uic.loadUi("user_reg_complete.ui", dialog)
        dialog.setWindowTitle("USER UI Complete")
        dialog.entranceNum.setText(str(waitCount))
        dialog.exec_()

    def customRegStatus(self, entrance_num):
        dialog = QDialog()
        uic.loadUi("user_status.ui", dialog)
        dialog.setWindowTitle("USER UI Status")
        dialog.entranceNum.setText(str(entrance_num))
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = Control_TowerClass()
    myWindows.show()
    sys.exit(app.exec_())


