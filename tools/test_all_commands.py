import socket
import json
import time

PI_IP = "10.143.230.242"  # 🔁 Replace with your Pi IP if needed
PORT = 8000

commands = [
    "forward",
    "stop",
    "backward",
    "stop",
    "left",
    "stop",
    "right",
    "stop",
    "spin_left",
    "stop",
    "spin_right",
    "stop",
    "forward_slow",
    "stop",
    "backward_slow",
    "stop",
    "nudge_left",
    "nudge_right",
    "lift_up",
    "lift_down",
    "lift_zero",
    "lift_max",
    "all_stop"
]

def send_command(cmd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((PI_IP, PORT))
        message = json.dumps({ "command": cmd })
        s.sendall(message.encode())
        print(f"Sent: {message}")

print("🚀 Starting test sequence...")
for cmd in commands:
    send_command(cmd)
    time.sleep(5)  # ⏱️ 5-second visual delay
print("✅ Test sequence complete.")
