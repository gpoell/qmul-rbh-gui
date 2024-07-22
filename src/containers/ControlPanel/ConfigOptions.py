from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel
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

        self.modeLabel = QLabel("Collection Mode")
        self.modeLabel.setObjectName("configOptionLabel")
        self.modeSelection = QComboBox()
        self.modeSelection.addItems(self.modes)
        self.modeSelection.activated.connect(self.emit_mode)

        self.classifierLabel = QLabel("Model Labels")
        self.classifierLabel.setObjectName("configOptionLabel")
        self.classifierSelection = QComboBox()
        self.classifierSelection.addItems(self.classifiers)
        self.classifierSelection.activated.connect(self.emit_classifier)

        configBox1 = QHBoxLayout()
        configBox1.addWidget(self.modeLabel)
        configBox1.addWidget(self.modeSelection)
        
        configBox2 = QHBoxLayout()
        configBox2.addWidget(self.classifierLabel)
        configBox2.addWidget(self.classifierSelection)
        
        mainbox = QVBoxLayout(self)
        mainbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainbox.addLayout(configBox1)
        mainbox.addLayout(configBox2)

    def emit_classifier(self, index):
        data = self.classifiers[index].lower()
        self.sigTactileClassifier.emit(data)

    def emit_mode(self, index):
        data = self.modes[index].lower()
        self.sigTactileMode.emit(data)

    def _set_config(self):
        """Sets the configuration modes and object options based on the gripper settings"""
        with open('src/settings.yaml', 'r') as file:
            conf = yaml.safe_load(file)
            self.modes = [mode.upper() for mode in conf['gripper']['modes']]
            self.classifiers = [classifier.upper() for classifier in conf['gripper']['classifiers']]