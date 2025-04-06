import RPi.GPIO as GPIO
import time

# ULN2003 stepper motor pins
IN1 = 5
IN2 = 6
IN3 = 13
IN4 = 19
pins = [IN1, IN2, IN3, IN4]

# Half-step sequence
sequence = [
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
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

def step_forward(steps, delay=0.001):
    for _ in range(steps):
        for step in sequence:
            for pin, val in zip(pins, step):
                GPIO.output(pin, val)
            time.sleep(delay)

def step_backward(steps, delay=0.001):
    for _ in range(steps):
        for step in reversed(sequence):
            for pin, val in zip(pins, step):
                GPIO.output(pin, val)
            time.sleep(delay)

try:
    print("Lifting fork (forward rotation)")
    step_forward(512)  # 1 full rotation
    time.sleep(1)

    print("Lowering fork (reverse rotation)")
    step_backward(512)
    time.sleep(1)

finally:
    GPIO.cleanup()
