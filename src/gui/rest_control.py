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

waitCount = 0

class Control_TowerClass(QDialog, rest_control) :
    user_newWindow = None
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Restaurant Control Tower")
        self.btnUser.clicked.connect(self.customerWindow)
        self.btnUser_2.clicked.connect(self.customerWindow)
        self.btnUser_3.clicked.connect(self.customerWindow)
        
    def customerWindow(self):
        Control_TowerClass.user_newWindow = Customer()
        Control_TowerClass.user_newWindow.show()
                
    def waitinglist(self, headcount):
        global waitCount
        row = self.WaitingList.rowCount()
        self.WaitingList.insertRow(row)
        self.WaitingList.setItem(row, 0, QTableWidgetItem(str(waitCount)))
        self.WaitingList.setItem(row, 1, QTableWidgetItem(headcount+"명"))
        self.WaitingList.setItem(row, 2, QTableWidgetItem('입장대기'))
        for i in range(3):
            self.WaitingList.item(row, i).setTextAlignment(Qt.AlignCenter)
        
class Customer(QDialog, user_basic, user_reg, user_reg_complete, user_status) :
    regMode = False
    Waitcustomer_info = []
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("USER UI")
        self.btnVal.clicked.connect(self.phoneVal)
        self.btnLine.clicked.connect(self.customMakeLine)

    def phoneVal(self):
        phoneNum, ok = QInputDialog.getText(self, '줄서기 예약 확인', '예약하신 연락처를 적어주세요')
        if ok and phoneNum:
            self.customRegStatus(phoneNum)

    def customMakeLine(self):
        linedialog = QDialog()
        uic.loadUi("user_reg.ui", linedialog)
        linedialog.setWindowTitle("USER UI Register")
        linedialog.btnReg.clicked.connect(lambda : self.customerReg(linedialog))
        linedialog.exec_()

    def customerReg(self, linedialog):
        global waitCount
        phoneNum, ok = QInputDialog.getText(self, '예약할 연락처', '예약하실 연락처를 적어주세요')
        if ok and phoneNum.isdigit():
            headcount = linedialog.cbHeadCount.currentText()
            waitCount += 1
            Customer.Waitcustomer_info.append([str(waitCount), headcount, phoneNum])
            myWindows.waitinglist(headcount)
            linedialog.close()
            self.customerRegComplete(waitCount)
        else: QMessageBox.warning(self, '연락처 오류', '숫자만 입력해주세요.')
        
    def customerRegComplete(self, waitCount):
        regdialog = QDialog()
        uic.loadUi("user_reg_complete.ui", regdialog)
        regdialog.setWindowTitle("USER UI Complete")
        regdialog.entranceNum.setText(str(waitCount))
        regdialog.exec_()
        Control_TowerClass.user_newWindow.close()

    def customRegStatus(self, phoneNum):
        for info in Customer.Waitcustomer_info:
            if info[2] == phoneNum:
                Customer.regMode = True
                entranceNum = info[0]
                break
        if Customer.regMode == True:
            Control_TowerClass.user_newWindow.close()     
            statusdialog = QDialog()
            uic.loadUi("user_status.ui", statusdialog)
            statusdialog.setWindowTitle("USER UI Status")
            statusdialog.entranceNum.setText(entranceNum)
            statusdialog.displayNum.setText(str(int(entranceNum)-int(Customer.Waitcustomer_info[0][0])))
            statusdialog.exec_()
            Customer.regMode = False
            print(Customer.Waitcustomer_info)
        else: QMessageBox.warning(self, '연락처 불일치', '연락처를 다시 확인해주세요.')
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = Control_TowerClass()
    myWindows.show()
    sys.exit(app.exec_())