import sys
from PyQt5.QtCore import QTimer, Qt, QPoint, QRect
from PyQt5.QtGui import QColor, QPainter, QLinearGradient, QPainterPath
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

        # Set stylesheet for QProgressBar
        stylesheet = """
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                background-color: #FFFFFF;
                text-align: center;
            }
        """
        self.progressBar.setStyleSheet(stylesheet)

    def updateProgressBar(self):
        self.value += 1
        if self.value > 100:
            self.value = 0
        self.progressBar.setValue(self.value)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.progressBar.rect()

        # Draw background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(230, 230, 230))
        painter.drawRect(rect)

        # Draw progress bar
        gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        if self.progressBar.value() <= 33:
            color1 = QColor(255, 92, 92)
            color2 = QColor(220, 0, 0)
        elif self.progressBar.value() <= 66:
            color1 = QColor(255, 221, 135)
            color2 = QColor(255, 172, 70)
        else:
            color1 = QColor(123, 229, 135)
            color2 = QColor(16, 156, 22)
        gradient.setColorAt(0, color1)
        gradient.setColorAt(1, color2)
        painter.setBrush(gradient)

        width = rect.width() * self.progressBar.value() / self.progressBar.maximum()
        height = rect.height() / 3

        points = []
        for i in range(10):
            x = rect.left() + width * i / 10
            y = rect.bottom() - height if i % 2 == 0 else rect.top()
            points.append(QPoint(x, y))

        path = QPainterPath()
        path.moveTo(points[0])
        for i in range(len(points) - 1):
            point1, point2 = points[i], points[i + 1]
            control_point = QPoint((point1.x() + point2.x()) / 2, (point1.y() + point2.y()) / 2)
            path.quadTo(control_point, point2)
        painter.drawPath(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyCustomWidget()
    widget.show()
    sys.exit(app.exec_())
