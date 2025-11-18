import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

p = GPIO.PWM(17, 50)
p.start(0)

while True:
    p.ChangeDutyCycle(2)   # hard left
    time.sleep(1)
    p.ChangeDutyCycle(12)  # hard right
    time.sleep(1)