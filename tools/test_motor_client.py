import socket
import json

# Replace with your Pi's actual IP address
PI_IP = "10.143.230.242"
PORT = 8000

def send_command(command: dict):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((PI_IP, PORT))
            s.send(json.dumps(command).encode())
            print(f"Sent: {command}")
    except Exception as e:
        print(f"Error: {e}")

# Example command
if __name__ == "__main__":
    # send_command({"move": "run"})       # Run forward
    # send_command({"move": "stop"})    # Stop
    send_command({"lift": "up"})      # Lift fork
    # send_command({"lift": "down"})    # Lower fork