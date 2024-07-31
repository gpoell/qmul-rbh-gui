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
from utils.datalog import write_csv, classify_object
from statistics import fmean
from math import fsum

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

            # Validate message size and split on delimiter
            if not batch : break
            batch = batch.split(',')
            if len(batch) < 3: continue
            
            # Format batch messages with 2 decimal precision
            batch = [f"{float(num):.2f}" for num in batch]
            
            # Collect data when the collect button is pressed
            if self.collect_flag:
                self.collect_data.append([batch[0], batch[1], batch[2]])

            # Emit tactile sensor data
            self.sig_tactile_data.emit((batch[0], batch[1], batch[2]))

        # Close client connection and reset state
        client.close()
        self.state = "idle"


    def collect(self, config={"samples": 20, "mode": "collect", "classifier": ""}):
        """Collects a sample of tactile sensor data and stores it in CSV file"""

        # Establish connection and send command
        client = EspClient()
        client.connect()
        client.send_data("collect") # send sample size?

        # Read acknowledge bit response from server
        batch = client.receive_data(1)
        
        # Capture data to write to the csv file
        data = []

        while batch != '':
            batch = client.receive_data(64)
            if not batch : break
            batch = batch.split(',')
            if len(batch) < 3: continue
            batch = [f"{float(num):.2f}" for num in batch]
            data.append([batch[0], batch[1], batch[2]])
        
        # Close client connection
        client.close()

        # Compute Absolute and Magnitude Values of Tactile Data
        data = self._absMagnitudeData(data)

        # Collect data or test against classification model
        if config["mode"] == "collect": write_csv(data, config['classifier'])
        if config["mode"] == "classify":
            avg_data = self._average_tactile_features(data)
            prediction = classify_object(avg_data)
            print(prediction) # future change to emit to console

    def disconnect(self):
        """Sends command to stop reading data from sensor"""
        client = EspClient()
        client.connect()
        client.send_data("disconnect")
        client.close()

    def calibrate(self):
        """Sends command to calibrate tactile sensor."""
        client = EspClient()
        client.connect()
        client.send_data("calibrate")
        client.close()

    def _average_tactile_features(self, data):
        """Returns the average feature values of a uniform tactile data set"""
        feature_length = len(data[0])
        avg_features = []
        for i in range(feature_length):
            avg_features.append(round(fmean([float(sample[i]) for sample in data]), 2))
        return avg_features
    
    def _absMagnitudeData(self, data):
        """Returns a new list appending the absolute and magnitude of the tactile values"""
        result = data
        for index, row in enumerate(result):
            absData = [abs(float(val)) for val in row]
            magnitude = round(fsum(val**2 for val in absData) ** 0.5, 2)
            result[index] = row + absData + [magnitude]
        return result