import RPi.GPIO as GPIO
import time
import board
import busio
import digitalio
import adafruit_tcs34725

# -----------------------
# GPIO SETUP
# -----------------------
GPIO.setmode(GPIO.BCM)

# Middle sorter servo
SORTER = 17
GPIO.setup(SORTER, GPIO.OUT)
sorter = GPIO.PWM(SORTER, 50)
sorter.start(0)

# Double flap servos
SERVO1 = 18
SERVO2 = 19
GPIO.setup(SERVO1, GPIO.OUT)
GPIO.setup(SERVO2, GPIO.OUT)
servo1 = GPIO.PWM(SERVO1, 50)
servo2 = GPIO.PWM(SERVO2, 50)
servo1.start(0)
servo2.start(0)

# Button
BUTTON = board.D22
button = digitalio.DigitalInOut(BUTTON)
button.switch_to_input(pull=digitalio.Pull.DOWN)

# -----------------------
# TCS34725 SETUP
# -----------------------
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)
sensor.integration_time = 400
sensor.gain = 60

# -----------------------
# SERVO DUTY CYCLES
# -----------------------
NEUTRAL_DUTY = 9.5
RIGHT_DUTY = 7.5   # Slightly more extreme
LEFT_DUTY = 11.5   # Slightly more extreme

# -----------------------
# FLAP LOGIC
# -----------------------
FLAPS_OPEN = 180
FLAPS_CLOSED = 90

# -----------------------
# SERVO FUNCTIONS
# -----------------------
def move_sorter(duty):
    sorter.ChangeDutyCycle(duty)
    time.sleep(0.6)

def move_flaps(left_angle):
    right_angle = 270 - left_angle
    duty1 = 2.5 + (left_angle / 180.0) * 10
    duty2 = 2.5 + (right_angle / 180.0) * 10
    servo1.ChangeDutyCycle(duty1)
    servo2.ChangeDutyCycle(duty2)
    time.sleep(0.6)

# -----------------------
# BUTTON DEBOUNCE
# -----------------------
def wait_for_press():
    while button.value:
        time.sleep(0.02)
    while not button.value:
        time.sleep(0.02)
    time.sleep(0.25)

# -----------------------
# MAIN PROGRAM
# -----------------------
print("System initialized. Press button to RESET system.")
wait_for_press()

while True:
    #   BUTTON PRESS #1 RESET
    print("Resetting system...")
    move_sorter(NEUTRAL_DUTY)
    move_flaps(FLAPS_CLOSED)
    print("System is now in NEUTRAL state (flaps closed).")
    
    # Wait for next stage
    print("Press button to START RGB detection.")
    wait_for_press()

    # BUTTON PRESS #2: START RGB 
    print("Stabilizing RGB detection for 5 seconds...")
    end_time = time.time() + 5
    white_count = 0
    dark_count = 0

    while time.time() < end_time:
        r, g, b, c = sensor.color_raw
        if c == 0:
            continue
        r_norm = r / c
        g_norm = g / c
        b_norm = b / c
        brightness = 0.299*r_norm + 0.587*g_norm + 0.114*b_norm

        if c > 40 and brightness > 0.40:
            white_count += 1
        else:
            dark_count += 1
        time.sleep(0.1)

    # Final decision
    if white_count > dark_count:
        clothing = "white"
        print("FINAL DECISION: WHITE")
        move_sorter(RIGHT_DUTY)
    else:
        clothing = "dark"
        print("FINAL DECISION: DARK")
        move_sorter(LEFT_DUTY)

    # BUTTON PRESS #3 
    print("Press button to DROP flaps.")
    wait_for_press()
    move_flaps(FLAPS_OPEN)
    print("Flaps OPEN, clothes dropped.")

    print("System is now in DROPPED state. Press button to RESET again when ready.\n")
    wait_for_press()  # Wait for manual reset to start next cycle
