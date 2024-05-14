import socket

class RbhSocket:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.conn = False
		self.data = ''

	def connect(self):
		self.socket.connect((self.host, self.port))
		self.conn = True
	
	def send_data(self, msg):
		self.socket.sendall(msg.encode("UTF-8"))
		self.socket.shutdown(1)

	def receive_data(self):
		# Check first message for status
		batch = self.socket.recv(64).decode('UTF-8')
		# Collect batches of data
		while batch != '':
			self.data += self.socket.recv(2048).decode("UTF-8")
		# Organize data
		self.data = self.data.split(',')
		del self.data[-1]
		### Close Connection ###
		self.close()
		self.conn = False
	
	def close(self):
		self.socket.shutdown(0)
		self.socket.close()

	def collect_sensor_data(self):
		self.send_data("collect")
		self.receive_data()
		
	def get_data(self):
		print(self.data)
		print(len(self.data))