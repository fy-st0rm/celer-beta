import socket
import pyaudio
import threading

# Constants
BUFFER   = 1024
FORMAT   = pyaudio.paInt16
CHANNELS = 2
RATE     = 44100

class Client:
	def __init__(self):
		self.ip = ""
		self.port = 0
		self.running = True
	
	def __create_cli(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print(f"[INFO]Connecting to {self.ip}:{self.port}")
		self.client.connect((self.ip, self.port))
	
	def __pyaudio_init(self):
		self.p_cli = pyaudio.PyAudio()
		self.istream = self.p_cli.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = BUFFER)
		self.ostream = self.p_cli.open(format = FORMAT, channels = CHANNELS, rate = RATE, output = True)
	
	def __listen(self):
		while self.running:
			audio = self.client.recv(BUFFER)
			if audio:
				self.ostream.write(audio)

	def __record(self):
		while self.running:
			try:
				audio = self.istream.read(BUFFER)
				if audio:
					self.client.send(audio)
			except KeyboardInterrupt:
				self.running = False
			except Exception as e:
				print(f"[ERROR]: {e}")

	def __username(self):
		username = input("Username> ")
		self.client.send(username.encode('utf-8'))

	def __server(self):
		running = True
		while running:
			indata = input("Server ip> ")
			try:
				indata = indata.split(":")
				self.ip = str(indata[0])
				self.port = int(indata[1])
				running = False
			except:
				print("[SERVER_IP]:[SERVER_PORT]")

	
	def close(self):
		self.istream.stop_stream()
		self.istream.close()
		self.ostream.stop_stream()
		self.ostream.close()
		self.p_cli.terminate()

		print("[INFO]: Disconnected from the server.")

	def run(self):
		self.__server()
		self.__create_cli()
		self.__username()
		self.__pyaudio_init()
		print(f"[INFO]: Connected to the {self.ip}:{self.port}")

		listen_thread = threading.Thread(target = self.__listen)
		listen_thread.start()

		self.__record()

if __name__ == "__main__":
	client = Client()
	client.run()
	client.close()
