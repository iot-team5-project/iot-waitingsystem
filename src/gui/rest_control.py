import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

rest_control = uic.loadUiType("rest_control.ui")[0]
user_basic = uic.loadUiType("user_basic.ui")[0]

waitCount = 0

class Control_TowerClass(QDialog, rest_control) :
    user_newWindow = None
    statusTable=[['admin'], [0], [0], [0], [1], [2], [3], [1]]
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Restaurant Control Tower")
        self.btnUser.clicked.connect(self.customerWindow)
        self.btnAdmin.clicked.connect(self.addTable)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)

    def updateDateTime(self):
        now = QDateTime.currentDateTime()
        dateTimeStr = now.toString("yyyy년 MM월 dd일 hh:mm:ss")
        self.currentTime.setText(dateTimeStr)

    def addTable(self):
        for tableInfo in Control_TowerClass.statusTable:
            if Customer.Waitcustomer_info == []:
                break
            elif tableInfo == [0]:
                index = Control_TowerClass.statusTable.index([0])
                Control_TowerClass.statusTable[index] = [1]
                myWindows.WaitingList.removeRow(0)
                del Customer.Waitcustomer_info[0]                    
            
    def confirmTable(self):
        statusT=Control_TowerClass.statusTable
        for i in range(1, 8):
            label = getattr(self, f"statusLabel{i}")
            back = getattr(self, f"backLabel{i}")
            if statusT[i] == [0]:
                label.setText("고객 대기 중")
                back.setStyleSheet("background-color: #01DF01")
            elif statusT[i] == [1]:
                label.setText("테이블 이용 중")
                back.setStyleSheet("background-color: #F7D358")
            elif statusT[i] == [2]:
                label.setText("청소 중")
                back.setStyleSheet("background-color: #2ECCFA")
            elif statusT[i] == [3]:
                label.setText("호출 중")
                back.setStyleSheet("background-color: #FA5858")
        
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

class Customer(QDialog, user_basic) :
    regMode = False
    Waitcustomer_info = []
    delinfo = None
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
                Customer.delinfo = info
                break
        for row in range(myWindows.WaitingList.rowCount()):
            item = myWindows.WaitingList.item(row, 0)
            if item and item.text() == entranceNum:
                customerWait = myWindows.WaitingList.item(row, 0).row()
                
        if Customer.regMode == True:
            Control_TowerClass.user_newWindow.close()     
            statusdialog = QDialog()
            uic.loadUi("user_status.ui", statusdialog)
            statusdialog.setWindowTitle("USER UI Status")
            statusdialog.entranceNum.setText(entranceNum)
            statusdialog.displayNum.setText(str(customerWait+1))
            statusdialog.btnCancel.clicked.connect(lambda : self.customListDelete(statusdialog, customerWait))
            statusdialog.exec_()
            Customer.regMode = False
        else: QMessageBox.warning(self, '연락처 불일치', '연락처를 다시 확인해주세요.')
        
    def customListDelete(self, statusdialog, customerWait):
        bookedCancel = QMessageBox.question(self, '예약취소', '예약을 취소하시겠습니까?', QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
        if bookedCancel == QMessageBox.Yes:
            myWindows.WaitingList.removeRow(customerWait)
            Customer.Waitcustomer_info.remove(Customer.delinfo)
            statusdialog.close()
        else:
            pass
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = Control_TowerClass()
    myWindows.show()
    myWindows.currentTime.textChanged.connect(myWindows.confirmTable)
    sys.exit(app.exec_())
    