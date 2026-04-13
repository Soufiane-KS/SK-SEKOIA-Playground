import threading
import socket
from queue import Queue

class SyslogReceiver(threading.Thread):
    def __init__(self, port, queue, logger, stop_event):
        super().__init__()
        self.port = port
        self.queue = queue
        self.logger = logger
        self.stop_event = stop_event

    def run(self):
        self.logger(f"Starting Syslog Receiver on port {self.port}",level="info")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", self.port))

        while not self.stop_event.is_set():
            try:
                data, addr = sock.recvfrom(4096)
                self.logger(f"Received syslog message from {addr}",level="debug")
                line = data.decode("utf-8")
                self.queue.put(line)
            except Exception as e:
                self.logger(f"Error receiving syslog message: {e}",level="error")