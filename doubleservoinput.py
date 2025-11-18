import RPi.GPIO as GPIO
import time
import board
import digitalio

GPIO.setmode(GPIO.BCM)

# Servo pins
SERVO_LEFT = 18
SERVO_RIGHT = 19  # second servo

GPIO.setup(SERVO_LEFT, GPIO.OUT)
GPIO.setup(SERVO_RIGHT, GPIO.OUT)

# Setup PWM for both servos
left = GPIO.PWM(SERVO_LEFT, 50)
right = GPIO.PWM(SERVO_RIGHT, 50)

left.start(0)
right.start(0)

# Button pin
button = digitalio.DigitalInOut(board.D17)
button.switch_to_input(pull=digitalio.Pull.DOWN)

# Track the flap state
is_open = False

def set_angle(pwm, angle):
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)
    pwm.ChangeDutyCycle(0)

while True:
    if button.value:
        if is_open:
            # CLOSE flaps
            # LEFT = 180°, RIGHT = 0° (mirrored)
            set_angle(left, 180)
            set_angle(right, 0)
            is_open = False
        else:
            # OPEN flaps
            # LEFT = 90°, RIGHT = 90° (mirrored same)
            set_angle(left, 90)
            set_angle(right, 90)
            is_open = True
        
        time.sleep(0.4)