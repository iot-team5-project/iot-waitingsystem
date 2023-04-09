import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import time 
import datetime

rest_control = uic.loadUiType("rest_control.ui")[0]
user_basic = uic.loadUiType("user_basic.ui")[0]
table_state = uic.loadUiType("table_state.ui")[0]

waitCount = 0

class Time_Run(QThread) :
    update = pyqtSignal()

    def __init__(self) :
        super().__init__()
        self.running = True

    def run(self):
        while self.running == True:
            self.update.emit()
            time.sleep(1)
    # def stop(self):
    #     self.running = False

class Table_StateClass(QDialog, table_state) :
    def __init__(self, tableNum) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Table State view")
        self.tableNum.setText(str(tableNum))
        self.btnCook.clicked.connect(lambda: self.cookComplete(tableNum))
        self.btnFinish.clicked.connect(lambda: self.tableOut(tableNum))
        self.btnClean.clicked.connect(lambda: self.cleanComplete(tableNum))
        self.btnCall.clicked.connect(lambda: self.tableCall(tableNum))
        myWindows.currentTime.textChanged.connect(lambda : self.selectTableState(tableNum))

    def selectTableState(self, tableNum):
        if Control_TowerClass.statusTable[tableNum][0] == 0:
            self.tableStateLabel.setText("고객 대기 중")
            self.tableStateBack.setStyleSheet("background-color: #01DF01")
            self.timeLabel.hide()
        elif Control_TowerClass.statusTable[tableNum][0] == 1:
            self.tableStateLabel.setText("테이블 이용 중")
            self.tableStateBack.setStyleSheet("background-color: #F7D358")
            self.timeLabel.show()
            self.timeLabel.setText("남은시간: "+str(datetime.timedelta(seconds=Control_TowerClass.statusTable[tableNum][1])))
        elif Control_TowerClass.statusTable[tableNum][0] == 2:
            self.tableStateLabel.setText("조리가 완료되었습니다.\n"+str(tableNum)+"번 테이블로 음식을 가져다주세요")
            self.tableStateBack.setStyleSheet("background-color: #DF7401")
            self.timeLabel.setText("남은시간: "+str(datetime.timedelta(seconds=Control_TowerClass.statusTable[tableNum][1])))
        elif Control_TowerClass.statusTable[tableNum][0] == 3:
            self.tableStateLabel.setText(str(tableNum)+"번 테이블 청소가 필요합니다.\n청소를 완료 후 청소 완료 버튼을 눌러주세요")
            self.tableStateBack.setStyleSheet("background-color: #2ECCFA")
            self.timeLabel.hide()
        elif Control_TowerClass.statusTable[tableNum][0] == 4:
            self.tableStateLabel.setText(str(tableNum)+"번 테이블에서 호출 중 입니다.")
            self.tableStateBack.setStyleSheet("background-color: #FA5858")
            self.timeLabel.setText("남은시간: "+str(datetime.timedelta(seconds=Control_TowerClass.statusTable[tableNum][1])))    

    def cookComplete(self, tableNum):
        Control_TowerClass.statusTable[tableNum][0] = 2
        Control_TowerClass.table_newWindow.close()

    def tableOut(self, tableNum):
        Control_TowerClass.statusTable[tableNum][0] = 3
        Control_TowerClass.table_newWindow.close()

    def cleanComplete(self, tableNum):
        Control_TowerClass.statusTable[tableNum][0] = 0
        Control_TowerClass.statusTable[tableNum][1] = 7200
        Control_TowerClass.table_newWindow.close()

    def tableCall(self, tableNum):
        if Control_TowerClass.statusTable[tableNum][0] == 4:
            Control_TowerClass.statusTable[tableNum][0] = 1
        elif Control_TowerClass.statusTable[tableNum][0] == 1:
            Control_TowerClass.statusTable[tableNum][0] = 4

class Control_TowerClass(QDialog, rest_control) :
    
    user_newWindow = None
    table_newWindow = None
    statusTable=[['admin'], [0, 7200], [0, 7200], [0, 7200], [1, 7200], [2, 7200], [3, 7200], [4, 7200]]
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Restaurant Control Tower")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.btnUser.clicked.connect(self.customerWindow)
        self.btnTable1.clicked.connect(lambda: self.tableStateWindow(1))
        self.btnTable2.clicked.connect(lambda: self.tableStateWindow(2))
        self.btnTable3.clicked.connect(lambda: self.tableStateWindow(3))
        self.btnTable4.clicked.connect(lambda: self.tableStateWindow(4))
        self.btnTable5.clicked.connect(lambda: self.tableStateWindow(5))
        self.btnTable6.clicked.connect(lambda: self.tableStateWindow(6))
        self.btnTable7.clicked.connect(lambda: self.tableStateWindow(7))
        self.timer120()
        self.WaitingList.cellDoubleClicked.connect(self.selectCustomer)
        
    def selectCustomer(self, row):
        infodialog = QDialog()
        uic.loadUi("customerInfo.ui", infodialog)
        infodialog.setWindowTitle("Admin Customer Info")
        selectItem = self.WaitingList.item(row, 0)
        
        def adminCustomerEntrance():
            for tableInfo in Control_TowerClass.statusTable:
                if Customer.Waitcustomer_info == []:
                    break
                elif tableInfo[0] == 0:
                    index = Control_TowerClass.statusTable.index([0, 7200])
                    Control_TowerClass.statusTable[index][0] = 1
                    myWindows.WaitingList.removeRow(selectItem.row())
                    Customer.Waitcustomer_info.remove(tempInfo)
                    infodialog.close()
                    break

        def adminCustomerDelete():
            bookedCancel = QMessageBox.question(self, '예약취소', '예약을 취소하시겠습니까?', QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
            if bookedCancel == QMessageBox.Yes:
                myWindows.WaitingList.removeRow(selectItem.row())
                Customer.Waitcustomer_info.remove(tempInfo)
                infodialog.close()
    
        for info in Customer.Waitcustomer_info:
            if info[0] == selectItem.text():
                tempInfo = info
                infodialog.infoLabel.setText("|| 대기번호: "+ info[0] +" || 인원수: " + info[1] +"명"+" || \n"+"연락처: "+ info[2])
                infodialog.btnEntrance.clicked.connect(adminCustomerEntrance)
                infodialog.btnDelete.clicked.connect(adminCustomerDelete)
        infodialog.btnConfirm.clicked.connect(infodialog.close)
        infodialog.exec_()

    def updateDateTime(self):
        now = QDateTime.currentDateTime()
        dateTimeStr = now.toString("yyyy년 MM월 dd일 hh:mm:ss")
        self.currentTime.setText(dateTimeStr)

    def timer120(self):
        def minusTime():
            statusT = Control_TowerClass.statusTable
            for i in range(1, 8):
                if statusT[i][0] == 1 or statusT[i][0] == 2 or statusT[i][0] == 4:
                    statusT[i][1] -= 1
        self.stopWatch = Time_Run()
        self.stopWatch.start()
        self.stopWatch.update.connect(minusTime)

    def confirmTable(self):
        statusT = Control_TowerClass.statusTable
        for i in range(1, 8):
            label = getattr(self, f"statusLabel{i}")
            back = getattr(self, f"backLabel{i}")
            time = getattr(self, f"timeLabel{i}")
            if statusT[i][0] == 0:
                label.setText("고객 대기 중")
                back.setStyleSheet("background-color: #01DF01")
                time.hide()
            elif statusT[i][0] == 1:
                label.setText("테이블 이용 중")
                back.setStyleSheet("background-color: #F7D358")
                time.show()
                time.setText(str(datetime.timedelta(seconds=statusT[i][1])))
            elif statusT[i][0] == 2:
                label.setText("조리 완료")
                back.setStyleSheet("background-color: #DF7401")
                time.setText(str(datetime.timedelta(seconds=statusT[i][1])))
            elif statusT[i][0] == 3:
                label.setText("청소 중")
                back.setStyleSheet("background-color: #2ECCFA")
                time.hide()
            elif statusT[i][0] == 4:
                label.setText("호출 중")
                back.setStyleSheet("background-color: #FA5858")
                time.setText(str(datetime.timedelta(seconds=statusT[i][1])))
  
    def customerWindow(self):
        Control_TowerClass.user_newWindow = Customer()
        Control_TowerClass.user_newWindow.show()

    def tableStateWindow(self, tableNum):
        Control_TowerClass.table_newWindow = Table_StateClass(tableNum)
        Control_TowerClass.table_newWindow.show()

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

    def phoneVal(self):
        phoneNum, ok = QInputDialog.getText(self, '줄서기 예약 확인', '예약하신 연락처를 적어주세요')
        if ok and phoneNum.isdigit():
            self.customRegStatus(phoneNum)
        else: QMessageBox.warning(self, '연락처 오류', '숫자만 입력해주세요.')

    def customRegStatus(self, phoneNum):
        for phoneInfo in Customer.Waitcustomer_info:
            if phoneInfo[2] == phoneNum:
                Customer.regMode = True
                Customer.delinfo = phoneInfo
                break
        for row in range(myWindows.WaitingList.rowCount()):
            item = myWindows.WaitingList.item(row, 0)
            if item and item.text() == phoneInfo[0]:
                customerWait = myWindows.WaitingList.item(row, 0).row()
                
        if Customer.regMode == True:
            Control_TowerClass.user_newWindow.close()     
            statusdialog = QDialog()
            uic.loadUi("user_status.ui", statusdialog)
            statusdialog.setWindowTitle("USER UI Status")
            statusdialog.entranceNum.setText(phoneInfo[0])
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