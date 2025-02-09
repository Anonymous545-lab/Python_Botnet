import socket
import webbrowser
import logging

class Bot:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        logging.basicConfig(level=logging.INFO)

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            logging.info("Connected to server")
        except Exception as e:
            logging.error(f"Connection error: {e}")
            self.sock.close()

    def receive_command(self):
        try:
            return self.sock.recv(1024).decode()
        except Exception as e:
            logging.error(f"Receive error: {e}")
            return None

    def execute_command(self, command):
        try:
            if command == "open_youtube":
                webbrowser.open("https://www.youtube.com")
                logging.info("YouTube opened")
            else:
                logging.warning(f"Unknown command: {command}")
        except Exception as e:
            logging.error(f"Command execution error: {e}")

    def close(self):
        self.sock.close()
        logging.info("Connection closed")

if __name__ == "__main__":
    bot = Bot("192.168.8.143", 9999)
    bot.connect()
    while True:
        command = bot.receive_command()
        if command:
            if command.lower() == "exit":
                break
            bot.execute_command(command)
    bot.close()
