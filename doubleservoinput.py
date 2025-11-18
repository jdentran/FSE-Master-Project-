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

# Calibration offsets (degrees). Start at 0; tweak if needed.
left_offset = 0     # add/subtract to fine-tune left servo
right_offset = 0    # add/subtract to fine-tune right servo

# Track state
is_open = False
last_state = False  # for edge detection

# ---------------------------
# Move servo to angle (with offset clamp 0-180)
# ---------------------------
def set_angle(pwm, angle, offset=0):
    a = int(angle + offset)
    if a < 0: a = 0
    if a > 180: a = 180
    duty = 2.5 + (a / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.25)
    pwm.ChangeDutyCycle(0)

print("System ready. Press button to toggle flaps (mirrored).")

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
                # CLOSE: Left->180 (closed), Right -> mirror(180) = 0 (closed mirrored)
                left_target = 180
            else:
                # OPEN: Left->90 (open), Right -> mirror(90) = 90
                left_target = 90

            # compute mirrored right target
            right_target = 180 - left_target

            # apply offsets and move both servos
            set_angle(left, left_target, left_offset)
            set_angle(right, right_target, right_offset)

            is_open = not is_open
            time.sleep(0.3)  # debounce

        last_state = current_state
        time.sleep(0.02)

except KeyboardInterrupt:
    left.stop()
    right.stop()
    GPIO.cleanup()
    print("Program stopped.")