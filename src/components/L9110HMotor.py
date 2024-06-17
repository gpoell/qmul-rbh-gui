from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot
from components.EspClient import EspClient

class L9110HMotor:

    def __init__(self, host, port):
        self.client = EspClient(host, port)
        self.state = 'inactive'

    def move(self, direction):
        self.state = 'active'
        print(self.state)
        self.client.connect()
        self.client.send_data(direction)
        batch = self.client.receive_data()
        while batch != '':
            batch = self.client.receive_data()
            if not batch : break
            print(f"{direction} motor...")
        self.client.close()
        self.state = 'inactive'
        print(self.state)