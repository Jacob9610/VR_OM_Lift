import RPi.GPIO as GPIO
import time

# L298N left motor pins
IN1 = 17
IN2 = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

try:
    print("Left motor: FORWARD")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(2)

    print("Left motor: REVERSE")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(2)

    print("Stopping")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)

finally:
    GPIO.cleanup()
