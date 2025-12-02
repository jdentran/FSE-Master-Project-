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
# ★★★ CALIBRATION VALUES ★★★
# YOU WILL TUNE THESE
# -----------------------
NEUTRAL_DUTY = 7.5   # FLAT plank (start here)
RIGHT_DUTY   = 6.2   # LEFT side UP → drops RIGHT
LEFT_DUTY    = 8.8   # RIGHT side UP → drops LEFT

# -----------------------
def move_duty(duty):
    sorter.ChangeDutyCycle(duty)
    time.sleep(0.5)
    sorter.ChangeDutyCycle(0)

print("Starting Tilt Platform Test...")

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