import sys
from PyQt6.QtWidgets import QApplication
from containers.Desktop import Desktop

app = QApplication(sys.argv)
gui = Desktop()
gui.setObjectName("desktop")

with open("src/styles.css", "r") as file:
    app.setStyleSheet(file.read())

gui.show()
app.exec()