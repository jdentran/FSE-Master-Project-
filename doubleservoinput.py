import RPi.GPIO as GPIO
import time
import board
import digitalio

# ---------------------------
# GPIO Setup
# ---------------------------
GPIO.setmode(GPIO.BCM)

# Servo pins
SERVO_LEFT = 18
SERVO_RIGHT = 19

GPIO.setup(SERVO_LEFT, GPIO.OUT)
GPIO.setup(SERVO_RIGHT, GPIO.OUT)

left = GPIO.PWM(SERVO_LEFT, 50)
right = GPIO.PWM(SERVO_RIGHT, 50)

left.start(0)
right.start(0)

# Button setup
button = digitalio.DigitalInOut(board.D17)
button.switch_to_input(pull=digitalio.Pull.DOWN)

# Track flap state
is_open = False
last_state = False  # for edge detection

# ---------------------------
# Move servos identically
# ---------------------------
def move_flaps(target_angle):
    """
    Both servos move to the exact same angle.
    """
    duty = 2.5 + (target_angle / 180) * 10
    left.ChangeDutyCycle(duty)
    right.ChangeDutyCycle(duty)
    time.sleep(0.3)  # movement time
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)

print("System ready. Press button to toggle flaps.")

# ---------------------------
# Main loop
# ---------------------------
try:
    while True:
        current_state = button.value

        # Detect rising edge (button press)
        if current_state and not last_state:
            if is_open:
                # CLOSE flaps → both to 180°
                move_flaps(180)
                is_open = False
                print("Flaps CLOSED")
            else:
                # OPEN flaps → both to 90°
                move_flaps(90)
                is_open = True
                print("Flaps OPEN")

            time.sleep(0.25)  # debounce

        last_state = current_state
        time.sleep(0.02)

except KeyboardInterrupt:
    left.stop()
    right.stop()
    GPIO.cleanup()
    print("Program stopped.")