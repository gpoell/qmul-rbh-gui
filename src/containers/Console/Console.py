from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class Console(QWidget):
    def __init__(self):
        super().__init__()

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("display-box")
        self.text = []

        layout = QVBoxLayout(self)
        layout.addWidget(self.textEdit)

    def update_data(self, data):
        for i in range(50):
            self.text.append(data)
        text = "\n".join(self.text)
        self.textEdit.setPlainText(text)
        