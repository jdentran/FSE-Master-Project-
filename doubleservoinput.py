import RPi.GPIO as GPIO
import time
import board
import digitalio

GPIO.setmode(GPIO.BCM)

# Servo pins
SERVO1 = 18  # left servo
SERVO2 = 19  # right servo
BUTTON = board.D22

GPIO.setup(SERVO1, GPIO.OUT)
GPIO.setup(SERVO2, GPIO.OUT)

servo1 = GPIO.PWM(SERVO1, 50)
servo2 = GPIO.PWM(SERVO2, 50)

servo1.start(0)
servo2.start(0)

# Button setup
button = digitalio.DigitalInOut(BUTTON)
button.switch_to_input(pull=digitalio.Pull.DOWN)

is_open = False
last_state = False

# -----------------------
# Move servos in opposite directions
# -----------------------
def move_flaps(left_angle):
    right_angle = 270 - left_angle  # simple inversion: 90->180, 180->90

    duty1 = 2.5 + (left_angle / 180.0) * 10
    duty2 = 2.5 + (right_angle / 180.0) * 10

    servo1.ChangeDutyCycle(duty1)
    servo2.ChangeDutyCycle(duty2)
    time.sleep(0.3)
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)

print("Ready. Press button to toggle flaps.")

# -----------------------
# Main loop
# -----------------------
try:
    while True:
        current_state = button.value

        # Detect rising edge
        if current_state and not last_state:
            if is_open:
                move_flaps(180)  # close flaps
                is_open = False
                print("Flaps CLOSED")
            else:
                move_flaps(90)   # open flaps
                is_open = True
                print("Flaps OPEN")

            time.sleep(0.25)  # debounce

        last_state = current_state
        time.sleep(0.02)

except KeyboardInterrupt:
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
    print("Program stopped.")
