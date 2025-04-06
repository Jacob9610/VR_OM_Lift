import socket
import json
import RPi.GPIO as GPIO
import time
import threading

# ====== L298N DC Motor Pins (left motor) ======
IN1 = 17
IN2 = 27

# ====== ULN2003 Stepper Motor Pins (lift) ======
STEP_PINS = [5, 6, 13, 19]

# Half-step sequence for 28BYJ-48
SEQUENCE = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
for pin in STEP_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# ====== Functions ======
def move_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def move_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

def stop_dc():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

def step_motor(steps, direction='up', delay=0.001):
    seq = SEQUENCE if direction == 'up' else list(reversed(SEQUENCE))
    for _ in range(steps):
        for step in seq:
            for pin, val in zip(STEP_PINS, step):
                GPIO.output(pin, val)
            time.sleep(delay)
    # turn off coils
    for pin in STEP_PINS:
        GPIO.output(pin, 0)

# ====== Socket Server ======
HOST = '0.0.0.0'
PORT = 8000

print(f"Listening for commands on port {PORT}...")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connection from {addr}")
                data = conn.recv(1024).decode()
                if not data:
                    continue
                try:
                    cmd = json.loads(data)
                    print(f"Received command: {cmd}")

                    # === DC Motor Commands ===
                    if cmd.get("move") == "run":
                        move_forward()
                    elif cmd.get("move") == "reverse":
                        move_backward()
                    elif cmd.get("move") == "stop":
                        stop_dc()

                    # === Stepper Commands ===
                    elif cmd.get("lift") == "up":
                        threading.Thread(target=step_motor, args=(512, 'up')).start()
                    elif cmd.get("lift") == "down":
                        threading.Thread(target=step_motor, args=(512, 'down')).start()

                except json.JSONDecodeError:
                    print("Invalid JSON received")

except KeyboardInterrupt:
    print("Shutting down")
    GPIO.cleanup()
