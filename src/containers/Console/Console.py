from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class Console(QWidget):
    def __init__(self):
        super().__init__()

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("display-box")
        self.text = ''

        layout = QVBoxLayout(self)
        layout.addWidget(self.textEdit)

    def update(self, data):
        self.textEdit.insertPlainText(data)
        self.textEdit.insertPlainText("\n")