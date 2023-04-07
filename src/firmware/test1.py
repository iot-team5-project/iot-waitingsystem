import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import uic
from PyQt6.QtCore import *
import socket
import time
import struct
import datetime


# ui 파일 연결
from_class = uic.loadUiType("/home/syh/Documents/amr_ws/ESP/test1/test1.ui")[0]

# 화면 클래스
class WindowClass(QMainWindow, from_class) :

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connect_mode = False

        self.timer = QTimer(self)
        self.timer2 = QTimer(self)

        # ip address format
        range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegularExpression("^" + range + "\\." + range + "\\." + \
                          range + "\\." + range + "$")


        self.ipEdit.setValidator(QRegularExpressionValidator(ipRegex, self))
        self.portEdit.setValidator(QIntValidator())
        self.setWindowTitle("TCP Client")
        self.ConnectBtn.clicked.connect(self.connect)

        self.table1btn.clicked.connect(self.clicktable1)
        self.stopbtn.clicked.connect(self.stoptimer)

        self.table2btn.clicked.connect(self.clicktable2)
        self.stopbtn_2.clicked.connect(self.stoptimer2)


        self.timer.timeout.connect(self.timeout)
        self.timer2.timeout.connect(self.timeout2)

    def timeout(self) :
        self.updateLED(34, 1)

    def timeout2(self) :
        self.updateLED(35, 1)


    def stoptimer(self) :
        self.timer.stop()

    def stoptimer2(self) :
        self.timer2.stop()


    def clicktable1(self) :
        self.timer.start(1000)

    def clicktable2(self) :
        self.timer2.start(1000)


    def updateLED(self, pin, status) :

        ## @ii -> 구조체 : integer 2개
        # data = struct.pack('@ii', pin, status)
        # test = struct.unpack("@ii", data)
        if self.connect_mode == True :
            data = self.format.pack(pin, status)
            req = self.sock.send(data)
            rev = self.format.unpack(self.sock.recv(self.format.size))
            if rev[0] == 34 :
                    self.sensorEdit.setText(str(rev[1]))
            elif rev[0] == 35 :
                    self.sensorEdit_2.setText(str(rev[1]))
    


    def connect(self):

        if self.connect_mode == False :
            self.connect_mode = True
            self.ConnectBtn.setText("Disconnect")
            ip = self.ipEdit.text()
            port = self.portEdit.text()

            self.sock = socket.socket()
            self.sock.connect((ip, int(port)))

            self.format = struct.Struct('@ii')
        elif self.connect_mode == True :
            self.connect_mode = False
            self.ConnectBtn.setText("Connect")
            self.sock.close()
            self.timer.stop()
            self.timer2.stop()

    

    #클래스 소멸자
    def __del__(self) :
        self.sock.close()
        self.connect_mode = False

# Python Main 함수
if __name__ == "__main__" :
    app = QApplication(sys.argv)    # 프로그램 실행
    myWindows = WindowClass()       # 화면 클래스 생성
    myWindows.show()                # 프로그램 화면 보이기
    sys.exit(app.exec())           # 프로그램을 종료까지 동작시킴