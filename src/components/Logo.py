from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap

class Logo(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel(self)
        pixmap = QPixmap("src/images/qmul_logo.jpg")
        label.setPixmap(pixmap)

        mainbox = QHBoxLayout(self)
        mainbox.addWidget(label)