from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal as Signal
import yaml

class ConfigOptions(QWidget):

    sigTactileMode = Signal(str, name="tactileMode")
    sigTactileClassifier = Signal(str, name="tactileClassifier")

    def __init__(self):
        super().__init__()
        self.modes = []
        self.classifiers = []
        self._set_config()

        self.modeSelection = QComboBox()
        self.modeSelection.addItems(self.modes)
        self.modeSelection.activated.connect(self.emit_mode)

        self.classifierSelection = QComboBox()
        self.classifierSelection.addItems(self.classifiers)
        self.classifierSelection.activated.connect(self.emit_classifier)

        mainbox = QHBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainbox.addWidget(self.modeSelection)
        mainbox.addWidget(self.classifierSelection)

    def emit_classifier(self, index):
        data = self.classifiers[index]
        self.sigTactileClassifier.emit(data)

    def emit_mode(self, index):
        data = self.modes[index]
        self.sigTactileMode.emit(data)

    def _set_config(self):
        """Sets the configuration modes and object options based on the gripper settings"""
        with open('src/settings.yaml', 'r') as file:
            conf = yaml.safe_load(file)
            self.modes = conf['gripper']['modes']
            self.classifiers = conf['gripper']['classifiers']