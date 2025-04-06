import socket
import json
import RPi.GPIO as GPIO
import time
import threading

# ====== L298N DC Motor Pins (left + right motor) ======
IN1 = 17  # Left motor direction 1
IN2 = 27  # Left motor direction 2
IN3 = 23  # Right motor direction 1
IN4 = 24  # Right motor direction 2

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

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
for pin in STEP_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# PWM setup for speed control
LEFT_PWM = GPIO.PWM(IN1, 100)  # 100 Hz
RIGHT_PWM = GPIO.PWM(IN3, 100)
LEFT_PWM.start(0)
RIGHT_PWM.start(0)

# Stepper position tracking
current_step_pos = 0
MAX_LIFT_STEPS = 512

# ====== DC Motor Functions ======
def stop_dc():
    LEFT_PWM.ChangeDutyCycle(0)
    RIGHT_PWM.ChangeDutyCycle(0)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def drive(left_speed, right_speed):
    print(f"Driving: left={left_speed}, right={right_speed}")
    # Left motor
    if left_speed > 0:
        GPIO.output(IN2, GPIO.LOW)
        LEFT_PWM.ChangeDutyCycle(min(left_speed, 1.0) * 100)
    elif left_speed < 0:
        GPIO.output(IN2, GPIO.HIGH)
        LEFT_PWM.ChangeDutyCycle(min(abs(left_speed), 1.0) * 100)
    else:
        LEFT_PWM.ChangeDutyCycle(0)

    # Right motor
    if right_speed > 0:
        GPIO.output(IN4, GPIO.LOW)
        RIGHT_PWM.ChangeDutyCycle(min(right_speed, 1.0) * 100)
    elif right_speed < 0:
        GPIO.output(IN4, GPIO.HIGH)
        RIGHT_PWM.ChangeDutyCycle(min(abs(right_speed), 1.0) * 100)
    else:
        RIGHT_PWM.ChangeDutyCycle(0)

# ====== Stepper Motor Functions ======
def step_motor(steps, direction='up', delay=0.001):
    # Flip sequence to correct physical wiring
    seq = list(reversed(SEQUENCE)) if direction == 'up' else SEQUENCE
    for _ in range(steps):
        for step in seq:
            for pin, val in zip(STEP_PINS, step):
                GPIO.output(pin, val)
            time.sleep(delay)
    for pin in STEP_PINS:
        GPIO.output(pin, 0)

def safe_lift(direction, steps=256):
    global current_step_pos
    if direction == 'up' and current_step_pos + steps <= MAX_LIFT_STEPS:
        step_motor(steps, direction='up')
        current_step_pos += steps
    elif direction == 'down' and current_step_pos - steps >= 0:
        step_motor(steps, direction='down')
        current_step_pos -= steps
    else:
        print(f"Lift blocked: would exceed limits (position = {current_step_pos})")

def lift_to(position):
    global current_step_pos
    steps = position - current_step_pos
    if steps > 0:
        safe_lift('up', steps)
    elif steps < 0:
        safe_lift('down', -steps)

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
                    print(f"Received: {cmd}")

                    # Drive commands
                    if "drive" in cmd:
                        left = cmd["drive"].get("left_motor", 0)
                        right = cmd["drive"].get("right_motor", 0)
                        drive(left, right)

                    # Lift commands
                    elif cmd.get("lift") == "up":
                        threading.Thread(target=safe_lift, args=('up',)).start()
                    elif cmd.get("lift") == "down":
                        threading.Thread(target=safe_lift, args=('down',)).start()

                    # Simple named commands
                    elif cmd.get("command") == "forward":
                        drive(-1.0, -1.0)
                    elif cmd.get("command") == "backward":
                        drive(1.0, 1.0)
                    elif cmd.get("command") == "left":
                        drive(-0.4, -1.0)
                    elif cmd.get("command") == "right":
                        drive(-1.0, -0.4)
                    elif cmd.get("command") == "spin_left":
                        drive(1.0, -1.0)
                    elif cmd.get("command") == "spin_right":
                        drive(-1.0, 1.0)
                    elif cmd.get("command") == "stop":
                        stop_dc()
                    elif cmd.get("command") == "lift_up":
                        threading.Thread(target=safe_lift, args=('up',)).start()
                    elif cmd.get("command") == "lift_down":
                        threading.Thread(target=safe_lift, args=('down',)).start()
                    elif cmd.get("command") == "lift_zero":
                        threading.Thread(target=lift_to, args=(0,)).start()
                    elif cmd.get("command") == "lift_max":
                        threading.Thread(target=lift_to, args=(MAX_LIFT_STEPS,)).start()
                    elif cmd.get("command") == "forward_slow":
                        drive(-0.4, -0.4)
                    elif cmd.get("command") == "backward_slow":
                        drive(0.4, 0.4)
                    elif cmd.get("command") == "nudge_left":
                        drive(0.6, -0.6)
                        time.sleep(0.2)
                        stop_dc()
                    elif cmd.get("command") == "nudge_right":
                        drive(-0.6, 0.6)
                        time.sleep(0.2)
                        stop_dc()
                    elif cmd.get("command") == "all_stop":
                        stop_dc()

                except json.JSONDecodeError:
                    print("Invalid JSON received")

except KeyboardInterrupt:
    print("Shutting down...")
    GPIO.cleanup()
