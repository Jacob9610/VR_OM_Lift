import RPi.GPIO as GPIO
import time

# L298N right motor pins
IN3 = 23
IN4 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

try:
    print("Right motor: FORWARD")
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(2)

    print("Right motor: REVERSE")
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(2)

    print("Stopping")
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

finally:
    GPIO.cleanup()
