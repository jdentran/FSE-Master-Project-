import RPi.GPIO as GPIO
import time

# -------------------
# Pin Setup
# -------------------
BUTTON_PIN = 17      # Button input
SERVO_PIN = 18       # Servo PWM output

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
pwm.start(0)

def set_servo_angle(angle):
    duty = 2 + (angle / 18)  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)           # Adjust speed
    pwm.ChangeDutyCycle(0)

print("Press the button to flip the hamper.")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button pressed
            print("Button pressed! Moving servo to full position...")

            # Move servo progressively from current to end
            for angle in range(0, 181, 5):  # 0° → 180°, step 5°
                set_servo_angle(angle)

            print("Servo reached final position. Waiting for next button press.")

            # Wait for button release before next press
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.1)

        else:
            # Do nothing when button not pressed
            time.sleep(0.1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("Program terminated")