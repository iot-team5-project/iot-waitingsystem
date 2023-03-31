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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), self.palette().color(self.backgroundRole()))
        painter.setBrush(self.progressBar.palette().color(self.progressBar.foregroundRole()))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.progressBar.geometry(), 5, 5)

    def updateProgressBar(self):
        self.value += 1
        if self.value > 100:
            self.value = 0
        self.progressBar.setValue(self.value)

        palette = self.palette()
        progress_palette = self.progressBar.palette()

        if self.value <= 33:
            palette.setColor(self.backgroundRole(), QColor(255, 92, 92))
            progress_palette.setColor(self.progressBar.foregroundRole(), QColor(255, 92, 92))
        elif self.value <= 66:
            palette.setColor(self.backgroundRole(), QColor(255, 221, 135))
            progress_palette.setColor(self.progressBar.foregroundRole(), QColor(255, 221, 135))
        else:
            palette.setColor(self.backgroundRole(), QColor(123, 229, 135))
            progress_palette.setColor(self.progressBar.foregroundRole(), QColor(123, 229, 135))

        self.setPalette(palette)
        self.progressBar.setPalette(progress_palette)
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyCustomWidget()
    widget.show()
    sys.exit(app.exec_())
