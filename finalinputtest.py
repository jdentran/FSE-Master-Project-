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
NEUTRAL_DUTY = 9.50   # Flat
RIGHT_DUTY   = 8.00   # Drop RIGHT (white)
LEFT_DUTY    = 11.00  # Drop LEFT (dark)

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
    while button.value:      # wait for release
        time.sleep(0.02)
    while not button.value:  # wait for press
        time.sleep(0.02)
    time.sleep(0.25)         # debounce delay

# -----------------------
# WAIT FOR START
# -----------------------
print("Press button to START system...")
wait_for_press()
print("System started.\n")

# -----------------------
# MAIN LOOP
# -----------------------
try:
    while True:

        # RESET SYSTEM
        print("RESETTING TO NEUTRAL")
        move_sorter(NEUTRAL_DUTY)
        move_flaps(180)

        # -------- 5 SECOND STABILIZED SAMPLING --------
        print("Stabilizing color detection (5 seconds)...")
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
            brightness = 0.299 * r_norm + 0.587 * g_norm + 0.114 * b_norm

            if c > 40 and brightness > 0.40:
                white_count += 1
            else:
                dark_count += 1

            time.sleep(0.1)

        # -------- FINAL DECISION --------
        if white_count > dark_count:
            print("FINAL DECISION: WHITE")
            move_sorter(RIGHT_DUTY)
        else:
            print("FINAL DECISION: DARK")
            move_sorter(LEFT_DUTY)

        # -------- FIRST BUTTON: DROP --------
        print("Press button to DROP...")
        wait_for_press()

        move_flaps(90)
        print("Flaps OPEN (DROPPED)")

        # -------- SECOND BUTTON: RESET --------
        print("Press button to RESET...")
        wait_for_press()

        move_flaps(180)
        print("Flaps CLOSED")

        move_sorter(NEUTRAL_DUTY)
        print("Sorter RESET COMPLETE\n")

        time.sleep(1)

except KeyboardInterrupt:
    sorter.stop()
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
    print("Program stopped safely.")
