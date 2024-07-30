"""
NAME
	client.py

DESCRIPTION
	This module provides classes and functions that establish wireless socket connections to a server (i.e. ESP32)

CLASSES
	WiFiClient
		
FUNCTIONS

"""

import socket
import yaml

class WiFiClient:
	def __init__(self, func):
		self._set_connection_config()
		self.func = func

	def __call__(self, *args, **kwargs):
		self._connect()
		status = self._send_data(kwargs['command'])
		if status == 400:
			self._close()
			raise ValueError("Server received a bad request.")
		if status == 404:
			self._close()
			raise ValueError("Server did not recognize command.")
		if status != 200:
			self._close()
			raise ValueError("Server experienced an issue.")
		while batch != '':
			batch = self.socket.recv(kwargs['buffSize']).decode('UTF-8')
			if not batch : break
			return self.func(*args, **kwargs)

		self._close()

	def _connect(self):
		"""Establishes connection with device using host and port details defined in settings.yaml"""
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.host, self.port))
		except Exception:
			raise Exception("Failed to connect to device. Check settings and ensure device is listening.")
	
	def _send_data(self, msg):
		"""Send command to server and return the status response"""
		try:
			self.socket.sendall(msg.encode("UTF-8"))
			self.socket.send("\0".encode("UTF-8"))
			self.socket.shutdown(1)
			status = self.socket.recv(64).decode('UTF-8')
			return int(status)
		except Exception as e:
			self.socket.close()
			raise e

	def _receive_data(self, batch, buffSize):
		"""Return batches of data until data is no longer available"""
		while batch != '':
			batch = self.socket.recv(buffSize).decode('UTF-8')
			if not batch : return
			yield batch
	
	def _close(self):
		"""Close the connection"""
		self.socket.shutdown(0)
		self.socket.close()

	def _set_connection_config(self):
		"""Set the host and port details defined in the settings.yaml"""
		with open('src/settings.yaml', 'r') as file:
			conf = yaml.safe_load(file)
			self.host = conf['client']['host']
			self.port = conf['client']['port']

	def send_command(self, command, buffSize=64, processDataFunc=None):
		"""Sends a command to the server and optionally processes the data using the provided callback"""
		self._connect()
		status = self._send_data(command)
		if status == 400:
			self._close()
			raise ValueError("Server received a bad request.")
		if status == 404:
			self._close()
			raise ValueError("Server did not recognize command.")
		if status != 200:
			self._close()
			raise ValueError("Server experienced an issue.")
		
		if processDataFunc:
			(processDataFunc(batch) for batch in self._receive_data(status, buffSize))
		
		self._close()