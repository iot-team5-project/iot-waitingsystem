import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 버튼과 레이블을 담을 수 있는 수직, 수평 레이아웃 생성
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # 버튼 생성
        button1 = QPushButton("Button1")
        button2 = QPushButton("Button2")
        button3 = QPushButton("Button3")

        # 각 버튼에 대한 정보 설정
        button1.info = "Button1의 정보"
        button2.info = "Button2의 정보"
        button3.info = "Button3의 정보"

        # 버튼 클릭 시 정보 출력하는 함수 연결
        button1.clicked.connect(lambda: self.show_info(button1.info))
        button2.clicked.connect(lambda: self.show_info(button2.info))
        button3.clicked.connect(lambda: self.show_info(button3.info))

        # 버튼 수평 레이아웃에 추가
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)

        # 버튼 레이아웃과 공백 레이아웃을 수직 레이아웃에 추가
        main_layout.addLayout(button_layout)
        main_layout.addSpacing(20)

        # 버튼 정보를 출력하는 라벨 추가
        self.info_label = QLabel()
        main_layout.addWidget(self.info_label)

        # 수직 레이아웃을 윈도우에 추가
        self.setLayout(main_layout)

    def show_info(self, info):
        # 새로운 창을 생성하고 정보를 표시하는 라벨 추가
        info_window = QWidget()
        info_layout = QVBoxLayout()
        info_label = QLabel(info)
        info_layout.addWidget(info_label)
        info_window.setLayout(info_layout)
        info_window.setWindowTitle("버튼 정보")
        info_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
