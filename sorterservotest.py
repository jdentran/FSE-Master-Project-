import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# -----------------------
# MIDDLE SERVO PIN
# -----------------------
SORTER = 17   # Your MG995 signal pin

GPIO.setup(SORTER, GPIO.OUT)

sorter = GPIO.PWM(SORTER, 50)   # 50Hz for servo
sorter.start(0)

# -----------------------
# Servo Move Function
# -----------------------
def move_sorter(angle):
    duty = 2.5 + (angle / 180.0) * 10
    sorter.ChangeDutyCycle(duty)
    time.sleep(0.5)
    sorter.ChangeDutyCycle(0)

print("Starting Middle Servo Test...")

# -----------------------
# MAIN LOOP
# -----------------------
try:
    while True:
        # NEUTRAL
        print("Neutral")
        move_sorter(90)
        time.sleep(1)

        # LEFT (DARK)
        print("LEFT (Dark)")
        move_sorter(30)
        time.sleep(1)

        # BACK TO NEUTRAL
        move_sorter(90)
        time.sleep(1)

        # RIGHT (PALE)
        print("RIGHT (Pale)")
        move_sorter(150)
        time.sleep(1)

except KeyboardInterrupt:
    sorter.stop()
    GPIO.cleanup()
    print("Program stopped.")