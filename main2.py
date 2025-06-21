from PySide6.QtWidgets import QCheckBox, QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt, Property
from PySide6.QtGui import QPainter, QColor, QMouseEvent


class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self._circle_pos_internal = 3
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)  # Убираем фокус-рамку

        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.stateChanged.connect(self.start_transition)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.toggle()  # Меняем состояние
        super().mouseReleaseEvent(event)

    def start_transition(self, value):
        start = self._circle_pos_internal
        end = self.width() - self.height() + 3 if value else 3

        self.animation.stop()
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Фон
        if self.isChecked():
            p.setBrush(QColor("#00cc66"))
        else:
            p.setBrush(QColor("#cccccc"))

        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)

        # Кружок
        p.setBrush(QColor("#ffffff"))
        p.drawEllipse(int(self._circle_pos_internal), 3, self.height() - 6, self.height() - 6)

    def get_circle_position(self):
        return self._circle_pos_internal

    def set_circle_position(self, pos):
        self._circle_pos_internal = pos
        self.update()

    circle_position = Property(float, get_circle_position, set_circle_position)


# Тест
if __name__ == "__main__":
    app = QApplication([])

    window = QWidget()
    layout = QVBoxLayout(window)

    toggle = ToggleSwitch()
    layout.addWidget(toggle)

    window.show()
    app.exec()
