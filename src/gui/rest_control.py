import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import paho.mqtt.client as mqtt

rest_control = uic.loadUiType("rest_control.ui")[0]
user_basic = uic.loadUiType("user_basic.ui")[0]
user_reg = uic.loadUiType("user_reg.ui")[0]
user_reg_complete = uic.loadUiType("user_reg_complete.ui")[0]
user_status = uic.loadUiType("user_status.ui")[0]

WaitNewCustomer = False
waitCount = 0
regMode = False

class Control_TowerClass(QDialog, rest_control) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Restaurant Control Tower")
        self.btnUser.clicked.connect(self.customerWindow)
        # self.btnUser_2.clicked.connect(self.customerWindow)
        # self.btnUser_3.clicked.connect(self.customerWindow)

        #20230404 노태형추가 - MQTT 프로토콜
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect('192.168.0.120', 1883, 60)

    def customerWindow(self):
        window_2 = Customer()
        # uic.loadUi("user_reg.ui", window_2)
        # self.setWindowTitle("USER UI")
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

    # 20230404 노태형변경 - MQTT Message
    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker")
        client.subscribe("switch1_status")
        client.subscribe("switch2_status")

    # 20230405 노태형추가변경 - MQTT Receive Message
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        if topic == "switch1_status":
            self.switch1_label.setText("Switch 1: " + payload)
        elif topic == "switch2_status":
            self.switch2_label.setText("Switch 2: " + payload)

class Customer(QDialog, user_basic, user_reg, user_reg_complete, user_status) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("USER UI")
        
        if regMode == True:
            self.btnLine.setText("나의 줄 확인")
            self.btnLine.clicked.connect(self.customRegStatus)

        else:
            self.btnLine.clicked.connect(self.customMakeLine)

    def customMakeLine(self):
        linedialog = QDialog()
        uic.loadUi("user_reg.ui", linedialog)
        linedialog.setWindowTitle("USER UI Register")
        linedialog.btnReg.clicked.connect(lambda : self.customerReg(linedialog))
        linedialog.exec_()

    def customerReg(self, dialog):
        global WaitNewCustomer, waitCount
        headcount = dialog.cbHeadCount.currentText()
        WaitNewCustomer = True
        waitCount += 1
        myWindows.waitinglist(headcount)
        dialog.close()
        self.customerRegComplete(waitCount)

    def customerRegComplete(self, waitCount):
        regdialog = QDialog()
        global regMode
        uic.loadUi("user_reg_complete.ui", regdialog)
        regdialog.setWindowTitle("USER UI Complete")
        regdialog.entranceNum.setText(str(waitCount))
        regMode = True
        regdialog.exec_()

    def customRegStatus(self):
        statusdialog = QDialog()
        uic.loadUi("user_status.ui", statusdialog)
        statusdialog.setWindowTitle("USER UI Status")
        statusdialog.entranceNum.setText(str(waitCount))
        statusdialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = Control_TowerClass()
    myWindows.show()
    sys.exit(app.exec_())


