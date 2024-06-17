from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot
from components.EspClient import EspClient

class TactileSensor(QObject):

    signal = Signal(tuple, name='tactileData')
    console_msg = Signal(str, name="consoleMessage")

    def __init__(self, host, port):
        super().__init__()
        self.client = EspClient(host, port)
        self.collect_data = []
        self.collect_flag = False

    def connect(self):
        self.client.connect()
        self.client.send_data("collect")
        batch = self.client.receive_data()
		# Receive Data Batches
        while batch != '':
            batch = self.client.receive_data()
            if not batch : break
            batch = batch.split(',')
            if self.collect_flag: self.collect_data.append([batch[0], batch[1], batch[2]])
            self.signal.emit((batch[0], batch[1], batch[2]))
        self.client.close()

    def collect(self, sample=20):
        self.collect_flag = True
        self.console_msg.emit("------COLLECTED--------")
        while len(self.collect_data) < sample: continue
        self.collect_flag = False
        self.console_msg.emit("------COLLECTED--------")
        for i in self.collect_data:
            print(i)
        print(len(self.collect_data))
        self.write_csv(self.collect_data)
        self.collect_data = []

    def write_csv(self, data):

        path = "data/tactile_sensor_data.csv"
        object = 'cherry'

        with open(path, 'a+') as f:
            for value in data:
                f.write(f"{value[0]},{value[1]},{value[2]},{object}")
                f.write("\n")
            f.close()