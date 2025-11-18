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

# PWM for servo
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
pwm.start(0)

def set_servo_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Adjust speed if needed
    pwm.ChangeDutyCycle(0)

print("Press the button to flip the hamper once.")

# Track if servo has already moved
servo_moved = False

try:
    while True:
        if not servo_moved and GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed! Rotating servo 0° → 180°...")
            for angle in range(0, 181, 5):  # Step through 0 → 180°
                set_servo_angle(angle)
            print("Servo finished rotation. It will stay at 180°.")
            servo_moved = True  # Prevent further movement

        time.sleep(0.05)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("Program terminated")