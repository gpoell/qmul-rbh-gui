"""
NAME
	client.py

DESCRIPTION
	This module provides classes and functions that establish wireless socket connections to a server (i.e. ESP32).

CLASSES
	WiFiClient
	TactileSensor
	L9110HMotor
		
"""

import socket
import yaml
from utils.datalog import processTactileData
from PyQt6.QtCore import QObject, pyqtSignal as Signal


class WiFiClient:
	"""
	Used as a decorator for functions to standardize how the client connects to the server, sends commands,
	receives and processes server data, and closes the client connection once complete.

	PARAMETERS
		command <string>: command to be sent to the server
		buffersize <int>: the size of the buffer to receive from the server (default = 64)

	METHODS
			_setConnection
			_connect
			_sendCommand
			_receiveData
			_close
	"""
	def __init__(self, **kwargs):
		self._setConnection()
		self.command = kwargs['command']
		self.buffersize = kwargs['buffersize']

	def __call__(self, func):
		"""
		Returns a decorated function that performs the client communication and executes the function
		wrapped by the decorated class while processing the server data.
		"""
		def wrapper(*args, **kwargs):
			try:
				self._connect()
				batch = self._sendCommand(self.command)
				self._receiveData(func, *args)
			except Exception:
				raise Exception
			finally:
				self._close()
		return wrapper

	def _connect(self):
		"""
		Establishes connection with the server the using host and port details defined in settings.yaml
		and sets the socket property to retain the communication thread.
		"""
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.host, self.port))
		except Exception:
			raise Exception("Failed to connect to device. Check settings and ensure device is listening.")
	
	def _sendCommand(self, msg):
		"""Sends the message argument to server and returns an integer status response"""
		try:
			self.socket.sendall(msg.encode("UTF-8"))
			self.socket.send("\0".encode("UTF-8"))
			self.socket.shutdown(1)
			status = self.socket.recv(64).decode('UTF-8')
			status = int(status)
			return status
		except Exception:
			self._close()
			raise Exception("Failed to send command to the server")

	def _receiveData(self, func, *args):
		"""
		Processes the function argument while reading batches of data from the server.
		
		Parameters
			func: a function reference that processes the batches of data
			*args: additional arguments required for the function (used to pass back self)

		"""
		batch = True
		while batch != '':
			batch = self.socket.recv(self.buffersize).decode('UTF-8')
			if not batch : return
			func(*args, batch)
	
	def _close(self):
		"""Closes the connection to the server."""
		self.socket.shutdown(0)
		self.socket.close()

	def _setConnection(self):
		"""Sets the host and port details defined in the settings.yaml"""
		with open('src/settings.yaml', 'r') as file:
			conf = yaml.safe_load(file)
			self.host = conf['client']['host']
			self.port = conf['client']['port']


class TactileSensor(QObject):
	"""
	The TactileSensor contains methods for reading, calibrating, and collecting data from the Hall Effect sensor on the gripper.

	METHODS
		read
		collect
		_collectTactileData
		disconnect
		calibrate
	"""

	sig_tactile_data = Signal(tuple, name='tactileData')
	sig_console_msg = Signal(dict, name="consoleMessage")

	def __init__(self):
		super().__init__()
		self.state = 'idle'
		self.tactileData = []
		self.collectFlag = False

	@WiFiClient(command="connect", buffersize=64)
	def read(self, batch):
		"""
		Reads data from the tactile sensor and emits it to the console.

		PARAMETERS
			batch: string of 4 tactile data values (X, Y, Z, buffer message padding)
		"""

		# Split the data, remove the buffer message padding, and format the values to 2 decimal precision
		batch = batch.split(',')
		if len(batch) < 4: return
		del batch[-1]
		batch = [f"{float(num):.2f}" for num in batch]

		# Emit tactile sensor data
		self.sig_tactile_data.emit((batch[0], batch[1], batch[2]))

	@WiFiClient(command="collect", buffersize=64)
	def _collectTactileData(self, batch):
		"""Collects a sample of tactile data from the gripper."""
		
		# Split the data, remove the buffer message padding, and format the values to 2 decimal precision
		batch = batch.split(',')
		if len(batch) < 4: return
		del batch[-1]
		batch = [f"{float(num):.2f}" for num in batch]
		
		self.tactileData.append(batch)

	def collect(self, settings):
		"""
		Processes the collected tactile data by writing it to a csv file
		or using the data model to classify the object.
		"""
		# Collect the sample of tactile data
		self._collectTactileData()
		
		# Process the collected data based on the GUI mode and classifier
		# settings = self.settings['gripper']['tactile']
		processTactileData(settings, self.tactileData)

		# Reset tactile data list
		self.tactileData = []

	@WiFiClient(command="disconnect", buffersize=64)
	def disconnect(self, batch):
		"""Sends command to disconnect the active client reading data from the gripper."""
		self.console_message["header"] = "info"
		self.console_message["body"] = f"Response from server: {batch}."

	@WiFiClient(command="calibrate", buffersize=64)
	def calibrate(self, batch):
		"""Sends command calibrate the tactile sensors on the gripper."""
		self.console_message["header"] = "info"
		self.console_message["body"] = f"Response from server: {batch}."


class L9110HMotor(QObject):
	"""
	The L9110HMotor contains methods for opening and closing the gripper.

	METHODS
		open
		close
	"""
	sig_console_msg = Signal(dict, name="consoleMessage")

	def __init__(self):
		super().__init__()
		self.state = 'idle'

	@WiFiClient(command="open", buffersize=64)
	def open(self, batch):
		"""
		Sends command to open the gripper and logs responses to the console.
		"""
		self.console_message["header"] = "info"
		self.console_message["body"] = f"Response from server: {batch}."

	@WiFiClient(command="close", buffersize=64)
	def close(self, batch):
		"""
		Sends command to close the gripper and logs responses to the console.
		"""
		self.console_message["header"] = "info"
		self.console_message["body"] = f"Response from server: {batch}."