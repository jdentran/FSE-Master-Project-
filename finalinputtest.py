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

# Button to start detection / drop flaps
BUTTON = board.D22
button = digitalio.DigitalInOut(BUTTON)
button.switch_to_input(pull=digitalio.Pull.DOWN)
is_open = False
last_state = False

# -----------------------
# TCS34725 SETUP
# -----------------------
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)
sensor.integration_time = 400
sensor.gain = 60

# -----------------------
# SORTER SERVO DUTY CYCLES
# -----------------------
NEUTRAL_DUTY = 9.50   # flat plank
RIGHT_DUTY   = 8.00   # left side rises → drop right (white)
LEFT_DUTY    = 11.00   # right side rises → drop left (dark)

# -----------------------
# FUNCTIONS
# -----------------------
def move_sorter(duty):
    sorter.ChangeDutyCycle(duty)
    time.sleep(0.5)
    sorter.ChangeDutyCycle(0)

def move_flaps(left_angle):
    right_angle = 270 - left_angle
    duty1 = 2.5 + (left_angle / 180.0) * 10
    duty2 = 2.5 + (right_angle / 180.0) * 10
    servo1.ChangeDutyCycle(duty1)
    servo2.ChangeDutyCycle(duty2)
    time.sleep(0.3)
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)

# -----------------------
# WAIT FOR BUTTON TO START
# -----------------------
print("Press button to start sorting...")
while not button.value:
    time.sleep(0.05)
print("Button pressed! System starting...")

try:
    while True:

        # FLAT SORTER BEFORE DETECTION
        print("FLAT (NEUTRAL)")
        move_sorter(NEUTRAL_DUTY)
        time.sleep(0.5)

        # DETECT COLOR
        r, g, b, c = sensor.color_raw
        if c == 0:
            continue  # skip if no reading
        r_norm = r / c
        g_norm = g / c
        b_norm = b / c
        brightness = 0.299 * r_norm + 0.587 * g_norm + 0.114 * b_norm

        if c > 40 and brightness > 0.40:
            clothing = "white"
            print("Detected: WHITE clothing")
            move_sorter(RIGHT_DUTY)
        else:
            clothing = "dark"
            print("Detected: DARK clothing")
            move_sorter(LEFT_DUTY)

        # 3SHORT DELAY TO LET SORTER STABILIZE
        print("Waiting 5 seconds to stabilize before dropping...")
        time.sleep(5)

        # WAIT FOR BUTTON TO DROP FLAPS
        print("Press button to drop flaps...")
        while True:
            current_state = button.value
            if current_state and not last_state:
                if is_open:
                    move_flaps(180)  # close flaps
                    is_open = False
                    print("Flaps CLOSED")
                else:
                    move_flaps(90)   # open flaps
                    is_open = True
                    print("Flaps OPEN")
                time.sleep(0.25)
            last_state = current_state
            if is_open:  # flap has moved, break to reset sorter
                break
            time.sleep(0.02)

        # RETURN SORTER TO NEUTRAL
        print("Returning sorter to NEUTRAL")
        move_sorter(NEUTRAL_DUTY)
        time.sleep(1)

except KeyboardInterrupt:
    sorter.stop()
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
    print("Program stopped.")
