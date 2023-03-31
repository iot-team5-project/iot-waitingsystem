import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QVBoxLayout


class MyCustomWidget(QWidget):
    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        layout.addWidget(self.progressBar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(100)  # 0.1초마다 업데이트

        self.value = 0

    def updateProgressBar(self):
        self.value += 1
        if self.value > 100:
            self.value = 0
        self.progressBar.setValue(self.value)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        rect = self.progressBar.rect()
        rect.setWidth(rect.width() * self.progressBar.value() / self.progressBar.maximum())

        if self.progressBar.value() <= 33:
            painter.setBrush(QColor(255, 92, 92))
        elif self.progressBar.value() <= 66:
            painter.setBrush(QColor(255, 221, 135))
        else:
            painter.setBrush(QColor(123, 229, 135))

        painter.drawRect(rect)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyCustomWidget()
    widget.show()
    sys.exit(app.exec_())
