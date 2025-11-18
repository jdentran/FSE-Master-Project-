import RPi.GPIO as GPIO
import time

# -------------------
# Pin Setup
# -------------------
BUTTON_PIN = 17      # Button input
SERVO_PIN = 18       # Servo PWM output

GPIO.setmode(GPIO.BCM)

# Button with pull-up resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# PWM for servo
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
pwm.start(0)

def set_servo_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.4)
    pwm.ChangeDutyCycle(0)

print("Press the button to flip the hamper.")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button pressed
            print("Button pressed! Flipping hamper...")
            set_servo_angle(0)    # Start position
            time.sleep(0.3)
            set_servo_angle(90)   # Mid flip
            time.sleep(0.3)
            set_servo_angle(180)  # End position
            time.sleep(0.3)
        else:
            # Do nothing when button not pressed
            time.sleep(0.1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("Program terminated")