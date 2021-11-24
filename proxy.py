# SamTheDog0's Proxy Server

import socket
import threading


class Proxy:
    """ A simple proxy server"""
    def __init__(self, port, dest_ip, dest_port):
        self.RUNNING = True
        self.port = port
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.processes = []

        # Initialising Socket:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", self.port))

    def run(self):
        """ Accepts connections and spawns threads to handle them"""
        self.sock.listen()
        while self.RUNNING:
            try:
                client_conn, addr = self.sock.accept()

                server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_conn.connect((self.dest_ip, self.dest_port))

                self.processes.append(Forward(client_conn, server_conn))
                self.processes.append(Forward(server_conn, client_conn))

                self.processes = [i for i in self.processes if i.RUNNING]
            except Exception as e:
                print(e)

    def __del__(self):
        self.sock.close()
        for i in self.processes:
            i.RUNNING = False


class Forward:
    def __init__(self, from_sock, to_sock):
        self.RUNNING = True
        self.from_sock = from_sock
        self.to_sock = to_sock

        self.main_process = threading.Thread(name='Forward_Process', target=self.server)
        self.main_process.start()

    def server(self):
        while self.RUNNING:
            try:
                packet = self.from_sock.recv(99999)
                if packet != b"":
                    self.to_sock.send(packet)
                else:
                    self.RUNNING = False
            except Exception as e:
                print(e)
                self.RUNNING = False
