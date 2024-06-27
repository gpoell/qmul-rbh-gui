"""
The TactileSensor collects data from the Hall Effect sensor on the gripper.

Attributes:

    state <str>: defines the state of the sensor
    collect_data <float>: captures the data collected by the sensor
    collect_flag <bool>: flag indicating when to collect data based on sample

Methods:
    connect: tests the connection with the Esp32 server
    collect: collects a sample of data from the Hall Effect sensor
    read: reads data from Hall Effect sensor and emits to Console
"""

from PyQt6.QtCore import QObject, pyqtSignal as Signal
from components.EspClient import EspClient
from utils.datalog import write_csv

class TactileSensor(QObject):

    sig_tactile_data = Signal(tuple, name='tactileData')
    sig_console_msg = Signal(dict, name="consoleMessage")

    def __init__(self):
        super().__init__()
        self.state = 'idle'
        self.collect_data = []
        self.collect_flag = False

    def connect(self):
        """Continuously reads tactile sensor data and emits them to the Console"""
        
        # Connect to server, send command, and update state
        client = EspClient()
        client.connect()
        client.send_data("connect")
        self.state = "connected"

        # Read acknowledge bit response from server
        batch = client.receive_data(1)

		# Continuously process data until null bit terminator is received
        while batch != '':
            batch = client.receive_data(64)
            if not batch : break
            batch = batch.split(',')

            # Collect data when the collect button is pressed
            if self.collect_flag:
                self.collect_data.append([batch[0], batch[1], batch[2]])

            # Emit tactile sensor data
            self.sig_tactile_data.emit((batch[0], batch[1], batch[2]))

        # Close client connection and reset state
        client.close()
        self.state = "idle"


    def collect(self, sample=20):
        """Collects a sample (default=20) of tactile sensor data and stores it in CSV file"""

        if self.state != "connected":
            print("[WARNING]: Tactile Sensor must be reading data in order to collect data.")
            return
        
        # Start collecting data
        self.collect_flag = True

        # Wait for collected data to reach sample length
        while len(self.collect_data) < sample: continue

        # Stop collecting data
        self.collect_flag = False

        # Write data to CSV file
        write_csv(self.collect_data)

        # Reset collected data list
        self.collect_data = []

    def disconnect(self):
        """Sends command to stop reading data from sensor"""
        client = EspClient()
        client.connect()
        client.send_data("disconnect")
        client.close()