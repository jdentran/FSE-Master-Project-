import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# -----------------------
# MIDDLE SERVO PIN
# -----------------------
SORTER = 17
GPIO.setup(SORTER, GPIO.OUT)

sorter = GPIO.PWM(SORTER, 50)
sorter.start(0)

# -----------------------
# CALIBRATION VALUES
# -----------------------
NEUTRAL = 180    # YOUR true mechanical center
LEFT = 120       # Dark side (adjust if needed)
RIGHT = 240      # Pale side (adjust if needed)

# -----------------------
# Servo Move Function
# -----------------------
def move_sorter(angle):
    duty = 2.5 + (angle / 180.0) * 10
    sorter.ChangeDutyCycle(duty)
    time.sleep(0.5)
    sorter.ChangeDutyCycle(0)

print("Starting Middle Servo Test (Neutral = 180)...")

# -----------------------
# MAIN LOOP
# -----------------------
try:
    while True:
        # NEUTRAL (CENTER)
        print("Neutral (CENTER)")
        move_sorter(NEUTRAL)
        time.sleep(1)

        # LEFT (DARK)
        print("LEFT (Dark)")
        move_sorter(LEFT)
        time.sleep(1)

        # BACK TO NEUTRAL
        move_sorter(NEUTRAL)
        time.sleep(1)

        # RIGHT (PALE)
        print("RIGHT (Pale)")
        move_sorter(RIGHT)
        time.sleep(1)

except KeyboardInterrupt:
    sorter.stop()
    GPIO.cleanup()
    print("Program stopped.")