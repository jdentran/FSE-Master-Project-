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

# Sorter servo
SORTER = 17
GPIO.setup(SORTER, GPIO.OUT)
sorter = GPIO.PWM(SORTER, 50)
sorter.start(0)

# Button to start detection
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
# SORTER SERVO DUTY CYCLES
# -----------------------
NEUTRAL_DUTY = 9.5    # flat
RIGHT_DUTY   = 8.0    # drop RIGHT (white)
LEFT_DUTY    = 11.0   # drop LEFT (dark)

# -----------------------
# FUNCTIONS
# -----------------------
def move_sorter(duty):
    sorter.ChangeDutyCycle(duty)
    time.sleep(0.5)
    sorter.ChangeDutyCycle(0)

# -----------------------
# WAIT FOR BUTTON
# -----------------------
print("Press button to start detection...")

while not button.value:
    time.sleep(0.05)

print("Button pressed! Starting color detection...")

# -----------------------
# MAIN LOOP
# -----------------------
try:
    while True:

        # Reset to flat
        print("Resetting to NEUTRAL")
        move_sorter(NEUTRAL_DUTY)
        time.sleep(1)

        # Read color
        r, g, b, c = sensor.color_raw
        if c == 0:
            print("No object detected.")
            continue

        r_norm = r / c
        g_norm = g / c
        b_norm = b / c
        brightness = 0.299 * r_norm + 0.587 * g_norm + 0.114 * b_norm

        # Decide color
        if c > 40 and brightness > 0.40:
            print("Detected: WHITE clothing")
            move_sorter(RIGHT_DUTY)
        else:
            print("Detected: DARK clothing")
            move_sorter(LEFT_DUTY)

        # Stabilize before next item
        print("Waiting 5 seconds...")
        time.sleep(5)

except KeyboardInterrupt:
    sorter.stop()
    GPIO.cleanup()
    print("Program stopped.")