import RPi.GPIO as GPIO
import time
import board
import busio
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
RIGHT_DUTY   = 8.00   # drop RIGHT (white)
LEFT_DUTY    = 11.00  # drop LEFT (dark)

# -----------------------
# FUNCTIONS
# -----------------------
def move_duty(duty):
    sorter.ChangeDutyCycle(duty)
    time.sleep(0.5)    # allow servo to move
    sorter.ChangeDutyCycle(0)

# -----------------------
# MAIN LOOP
# -----------------------
print("Waiting for clothing detection...")

try:
    while True:

        # Reset to neutral
        print("Resetting to NEUTRAL")
        move_duty(NEUTRAL_DUTY)
        time.sleep(0.5)

        # Read color
        r, g, b, c = sensor.color_raw
        if c == 0:
            print("No clothing detected, skipping...")
            continue

        r_norm = r / c
        g_norm = g / c
        b_norm = b / c
        brightness = 0.299 * r_norm + 0.587 * g_norm + 0.114 * b_norm

        # Decide color and move sorter
        if c > 40 and brightness > 0.40:
            print("Detected: WHITE clothing → dropping RIGHT")
            move_duty(RIGHT_DUTY)
        else:
            print("Detected: DARK clothing → dropping LEFT")
            move_duty(LEFT_DUTY)

        # Wait a short moment before next reading
        time.sleep(1)

except KeyboardInterrupt:
    sorter.stop()
    GPIO.cleanup()
    print("Program stopped.")