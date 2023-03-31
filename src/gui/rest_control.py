import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

control_class = uic.loadUiType("rest_control.ui")[0]
user_class = uic.loadUiType("user_reg.ui")[0]

WaitNewCustomer = False
waitCount = 0

class Control_TowerClass(QDialog, control_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnUser.clicked.connect(self.customerWindow)

    def customerWindow(self):
        window_2 = Customer()
        window_2.exec_()

    def waitinglist(self, customer):
        global WaitNewCustomer, waitCount
        row = self.WaitingList.rowCount()
        if WaitNewCustomer == True:
            self.WaitingList.insertRow(row)
            self.WaitingList.setItem(row, 0, QTableWidgetItem(waitCount))
            self.WaitingList.setItem(row, 1, QTableWidgetItem(customer))
            # self.WaitingList.setItem(row, 2, QTableWidgetItem(self.ui.textEdit.toPlainText()))
            WaitNewCustomer = False

class Customer(QDialog, user_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)          
        self.btnReg.clicked.connect(self.customerReg)

    def customerReg(self):
        global WaitNewCustomer, waitCount
        customer = self.customer.currentText()
        WaitNewCustomer = True
        waitCount += 1
        myWindows.waitinglist(customer)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = Control_TowerClass()
    myWindows.show()
    sys.exit(app.exec_())


