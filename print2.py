import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtPrintSupport import QPrinterInfo


class PrinterSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор принтера")

        layout = QVBoxLayout()

        self.label = QLabel("Выберите принтер:")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.printers = QPrinterInfo.availablePrinters()
        for printer in self.printers:
            self.combo.addItem(printer.printerName())
        layout.addWidget(self.combo)

        self.selected_label = QLabel("Выбранный принтер: ")
        layout.addWidget(self.selected_label)

        self.select_button = QPushButton("Подтвердить выбор")
        self.select_button.clicked.connect(self.show_selected_printer)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

    def show_selected_printer(self):
        selected_printer_name = self.combo.currentText()
        self.selected_label.setText(f"Выбранный принтер: {selected_printer_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrinterSelector()
    window.show()
    sys.exit(app.exec_())
