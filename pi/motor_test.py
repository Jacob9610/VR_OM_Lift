import pigpio
import time

# GPIO pins (BCM numbering)
IN1 = 17  # L298N IN1
IN2 = 27  # L298N IN2

# Initialize pigpio and connect to the local daemon
pi = pigpio.pi()

if not pi.connected:
    print("Failed to connect to pigpio daemon. Is 'pigpiod' running?")
    exit()

# Initialize GPIOs
def gpio_init():
    pi.set_mode(IN1, pigpio.OUTPUT)
    pi.set_mode(IN2, pigpio.OUTPUT)
    pi.write(IN1, 0)
    pi.write(IN2, 0)

# Motor control
def motor_forward():
    print("Motor moving forward")
    pi.write(IN1, 1)
    pi.write(IN2, 0)

def motor_backward():
    print("Motor moving backward")
    pi.write(IN1, 0)
    pi.write(IN2, 1)

def motor_stop():
    print("Motor stopped")
    pi.write(IN1, 0)
    pi.write(IN2, 0)

# Run test
try:
    gpio_init()
    motor_forward()
    time.sleep(12)

    motor_backward()
    time.sleep(12)

    motor_stop()

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    motor_stop()
    pi.stop()  # Disconnect from pigpio daemon

