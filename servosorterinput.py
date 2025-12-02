import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# -----------------------
# SERVO PIN
# -----------------------
SORTER = 17
GPIO.setup(SORTER, GPIO.OUT)

sorter = GPIO.PWM(SORTER, 50)  # 50Hz
sorter.start(0)

# -----------------------
# CALIBRATED DUTY CYCLES
# -----------------------
NEUTRAL_DUTY = 9.50   # flat plank
RIGHT_DUTY   = 8.00   # left side rises → drop right
LEFT_DUTY    = 11.00  # right side rises → drop left

# -----------------------
def move_duty(duty):
    sorter.ChangeDutyCycle(duty)
    time.sleep(0.5)    # allow MG995 to move
    sorter.ChangeDutyCycle(0)

print("Starting Tilt Platform Test (Neutral = 9.50)...")

try:
    while True:

        # -------- FLAT (NEUTRAL) --------
        print("FLAT (NEUTRAL)")
        move_duty(NEUTRAL_DUTY)
        time.sleep(1.5)

        # -------- DROP TO RIGHT --------
        print("DROP → RIGHT (Left side UP)")
        move_duty(RIGHT_DUTY)
        time.sleep(1.5)

        # -------- BACK TO FLAT --------
        print("RETURN TO FLAT")
        move_duty(NEUTRAL_DUTY)
        time.sleep(1.5)

        # -------- DROP TO LEFT --------
        print("DROP → LEFT (Right side UP)")
        move_duty(LEFT_DUTY)
        time.sleep(1.5)

except KeyboardInterrupt:
    sorter.stop()
    GPIO.cleanup()
    print("Program stopped.")