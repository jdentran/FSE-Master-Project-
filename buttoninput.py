import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)

print("Press the button...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == 1:
            print("Button pressed!")
        else:
            print("Button not pressed.")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()