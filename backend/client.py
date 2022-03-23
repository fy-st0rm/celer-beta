import socket
import pyaudio
import threading

# Constants
IP       = "127.0.0.1"
PORT     = 6969
BUFFER   = 1024
FORMAT   = pyaudio.paInt16
CHANNELS = 2
RATE     = 44100

class Client:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.running = True
	
	def __create_cli(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
	
	def close(self):
		self.istream.stop_stream()
		self.istream.close()
		self.ostream.stop_stream()
		self.ostream.close()
		self.p_cli.terminate()

		print("[INFO]: Disconnected from the server.")

	def run(self):
		self.__create_cli()
		self.__pyaudio_init()
		print(f"[INFO]: Connected to the {self.ip}:{self.port}")

		listen_thread = threading.Thread(target = self.__listen)
		listen_thread.start()

		self.__record()

if __name__ == "__main__":
	client = Client(IP, PORT)
	client.run()
	client.close()
