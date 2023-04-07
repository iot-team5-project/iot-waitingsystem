import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import socket
import struct

rest_control = uic.loadUiType("rest_control.ui")[0]
user_basic = uic.loadUiType("user_basic.ui")[0]
table_state = uic.loadUiType("table_state.ui")[0]

waitCount = 0
# Must input your Server IP
IP = '192.168.0.129'
PORT = 80

#g, gram
WEIGHT = 1000

class Table_StateClass(QDialog, table_state) :
    def __init__(self, tableNum) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Table State view")
        self.tableNum.setText(str(tableNum))
        
        if Control_TowerClass.statusTable[tableNum] == [0]:
            self.tableStateLabel.setText("고객 대기 중")
            self.tableStateBack.setStyleSheet("background-color: #01DF01")
        elif Control_TowerClass.statusTable[tableNum] == [1]:
            self.tableStateLabel.setText("테이블 이용 중")
            self.tableStateBack.setStyleSheet("background-color: #F7D358")
        elif Control_TowerClass.statusTable[tableNum] == [2]:
            self.tableStateLabel.setText("조리 완료")
            self.tableStateBack.setStyleSheet("background-color: #DF7401")
        elif Control_TowerClass.statusTable[tableNum] == [3]:
            self.tableStateLabel.setText("청소 중")
            self.tableStateBack.setStyleSheet("background-color: #2ECCFA")
        elif Control_TowerClass.statusTable[tableNum] == [4]:
            self.tableStateLabel.setText("호출 중")
            self.tableStateBack.setStyleSheet("background-color: #FA5858")
        self.btnCook.clicked.connect(lambda: self.cookComplete(tableNum))
        

    def cookComplete(self, tableNum):
        Control_TowerClass.statusTable[tableNum] = [2]
        Control_TowerClass.table_newWindow.close()

class Control_TowerClass(QDialog, rest_control) :
    user_newWindow = None

    # 점포 내 테이블
    table_newWindow = None
    statusTable=[['admin'], [0], [0], [0], [1], [2], [3], [4]]

    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Restaurant Control Tower")
        #SET TIMER FOR REALTIME
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)

        # 손님 추가
        self.btnUser.clicked.connect(self.customerWindow)
        self.btnTable1.clicked.connect(lambda: self.tableStateWindow(1))
        self.btnTable2.clicked.connect(lambda: self.tableStateWindow(2))
        self.btnTable3.clicked.connect(lambda: self.tableStateWindow(3))
        self.btnTable4.clicked.connect(lambda: self.tableStateWindow(4))
        self.btnTable5.clicked.connect(lambda: self.tableStateWindow(5))
        self.btnTable6.clicked.connect(lambda: self.tableStateWindow(6))
        self.btnTable7.clicked.connect(lambda: self.tableStateWindow(7))
        # self.btnAdmin.clicked.connect(self.addTable)
        self.WaitingList.cellDoubleClicked.connect(self.selectCustomer)

        #region 20230407_thro Sensor TCP/IP
        #BUTTON COMMAND
        
        self.table1btn.clicked.connect(self.clicktable1)
        self.stopbtn.clicked.connect(self.stoptimer1)
        
        self.table2btn.clicked.connect(self.clicktable2)
        self.stopbtn_2.clicked.connect(self.stoptimer2)

        # SENSOR UNIT INIT #timer2 = TABLE1, #timer3 = TABLE2
        self.connect_mode = False

        # If you want Debug with Offline mode, you must comment out 'self.connecting()'
        if __debug__:
            print('DEBUG MODE, NOT CONNECTED SERVER')
        else:
            self.connecting()

        self.timer2 = QTimer(self)
        self.timer3 = QTimer(self)

        self.timer2.timeout.connect(self.timeout2)
        self.timer3.timeout.connect(self.timeout3)

        if __debug__:     
            print('Init')
        #endregion

    #region 임용재 예약손님 확인창
    def selectCustomer(self, row):
        infodialog = QDialog()
        ##################################################################
        # UI_file : customerInfo.ui                                      #
        # trigger : Have a Waiting List                                  #
        # Show Data : str(waitCount), headcount, phoneNum                #
        # Select Function : Entrance - adminCustomerEntrance()           #
        #                   Check - Dialog Close                         #
        #                   Delete - adminCustromerDelete()              #
        ##################################################################
        uic.loadUi("customerInfo.ui", infodialog)
        infodialog.setWindowTitle("Admin Customer Info")
        selectItem = self.WaitingList.item(row, 0)
        
        def adminCustomerEntrance():
            for tableInfo in Control_TowerClass.statusTable:
                if Customer.Waitcustomer_info == []:
                    break
                elif tableInfo == [0]:
                    index = Control_TowerClass.statusTable.index([0])
                    Control_TowerClass.statusTable[index] = [1]
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

    #endregion

    def updateDateTime(self):
        now = QDateTime.currentDateTime()
        dateTimeStr = now.toString("yyyy년 MM월 dd일 hh:mm:ss")
        self.currentTime.setText(dateTimeStr)
    #region 임용재 Table Status 
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
                label.setText("조리 완료")
                back.setStyleSheet("background-color: #DF7401")
            elif statusT[i] == [3]:
                label.setText("청소 중")
                back.setStyleSheet("background-color: #2ECCFA")
            elif statusT[i] == [4]:
                label.setText("호출 중")
                back.setStyleSheet("background-color: #FA5858")
    #endregion
    #region 20230407_thro Server Connect 현재 조정 중
    def connecting(self):
        if __debug__:
            print('connecting')

        if self.connect_mode == False :
            self.connect_mode = True
            if __debug__:
                print("Connected")

            self.sock = socket.socket()
            self.sock.connect((IP, int(PORT)))

            self.format = struct.Struct('@ii')
        elif self.connect_mode == True :
            self.connect_mode = False
            if __debug__:
                print("DisConnected")
            self.sock.close()
            self.timer2.stop()
            self.timer3.stop()
    if __debug__:
        def timeout2(self) :
            self.updateWeight(1, 1)

        def timeout3(self) :
            self.updateWeight(2, 1)

        def updateWeight(self, table, weight) :
            if __debug__:
                print('Update')
            ## @ii -> 구조체 : integer 2개
            # data = struct.pack('@ii', pin, status)
            # test = struct.unpack("@ii", data)
            if self.connect_mode == True :
                data = self.format.pack(table, weight)
                req = self.sock.send(data)
                rev = self.format.unpack(self.sock.recv(self.format.size))
                if rev[0] == 1 :
                        self.sensorEdit.setText(str(rev[1]))
                elif rev[0] == 2 :
                        self.sensorEdit_2.setText(str(rev[1]))

    # 현재 조정 주우우우우우우우우우우우우웅
    else:
        def updateWeight(self, table, weight) :
            if __debug__:
                print('Converting')
            ## @ii -> 구조체 : integer 2개
            # data = struct.pack('@ii', pin, status)
            # test = struct.unpack("@ii", data)
            if self.connect_mode == True :
                data = self.format.pack(table, weight)
                req = self.sock.send(data)
                rev = self.format.unpack(self.sock.recv(self.format.size))
                if rev[0] == 1 :
                    self.weightTopercent(str(rev[1]))
                    self.timeLabel1.setText(str(rev[1]))
                elif rev[0] == 2 :
                    self.weightTopercent(str(rev[1]))
                    self.timeLabel2.setText(str(rev[1]))

    def weightTopercent(self, weight):
        (WEIGHT - weight) / 100  
           
        

    def stoptimer1(self) :
        self.timer2.stop()

    def clicktable1(self) :
        if __debug__:
            print('Clicked')
        self.timer2.start(1000)

    def stoptimer2(self) :
        self.timer3.stop()

    def clicktable2(self) :
        if __debug__:
            print('Clicked')
        self.timer3.start(1000)

    #클래스 소멸자
    def __del__(self) :
        self.sock.close()
        self.connect_mode = False
    #endregion
        
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


#region 임용재 Customer Class
##################################################################
# UI_file : user_basic.ui                                        #
# trigger : Clicked User Button                                  #
# Function : btnVal - phoneVal(self)                             #
#            btnLine - customMakeline(self)                      #
##################################################################
class Customer(QDialog, user_basic) :
    regMode = False
    Waitcustomer_info = []
    delinfo = None
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("USER UI")
        self.btnVal.clicked.connect(self.phoneVal)
        self.btnLine.clicked.connect(self.customMakeline)
    
    def phoneVal(self):
        phoneNum, ok = QInputDialog.getText(self, '줄서기 예약 확인', '예약하신 연락처를 적어주세요')
        if ok and phoneNum.isdigit():
            self.customRegStatus(phoneNum)
        else: QMessageBox.warning(self, '연락처 오류', '숫자만 입력해주세요.')

    ##################################################################
    # UI_file : user_reg.ui                                          #
    # trigger : Clicked btnVal button                                #
    # Input Data : How Many Peoples, PhoneNumber                     #
    # Output Data : Waiting Number                                   #
    ##################################################################
    def customMakeline(self):
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

    ##################################################################
    # UI_file : user_status.ui                                       #
    # trigger : Clicked btnLine button                               #
    # input Data : Phone Number                                      #
    # Output Data : Check the Waiting Number                         #
    ##################################################################
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
#endregion
    
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = Control_TowerClass()
    myWindows.show()
    myWindows.currentTime.textChanged.connect(myWindows.confirmTable)
    # myWindows.currentTime.textChanged.connect(myWindows.confirmTable)
    sys.exit(app.exec_())