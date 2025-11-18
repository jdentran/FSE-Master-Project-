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

# PWM setup
left = GPIO.PWM(SERVO_LEFT, 50)
right = GPIO.PWM(SERVO_RIGHT, 50)

left.start(0)
right.start(0)

# Button setup using digitalio (pull-down)
button = digitalio.DigitalInOut(board.D17)
button.switch_to_input(pull=digitalio.Pull.DOWN)

# Track state
is_open = False
last_state = False  # for edge detection

# ---------------------------
# Move servo to angle
# ---------------------------
def set_angle(pwm, angle):
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)
    pwm.ChangeDutyCycle(0)

print("System ready. Press button to toggle flaps.")

# ---------------------------
# MAIN LOOP
# ---------------------------
try:
    while True:
        current_state = button.value   # True = pressed

        # Detect rising edge (button press)
        if current_state and not last_state:
            print("Button pressed!")

            if is_open:
                # CLOSE: left → 180°, right → 0° (mirrored closed)
                set_angle(left, 180)
                set_angle(right, 0)
                is_open = False
                print("Closed position.")
            else:
                # OPEN: both → 90°
                set_angle(left, 90)
                set_angle(right, 90)
                is_open = True
                print("Open position.")

            time.sleep(0.3)  # debounce delay

        last_state = current_state
        time.sleep(0.02)

except KeyboardInterrupt:
    left.stop()
    right.stop()
    GPIO.cleanup()
    print("Program stopped.")