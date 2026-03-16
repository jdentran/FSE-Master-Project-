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
    time.sleep(0.02)
    pwm.ChangeDutyCycle(0)

print("Press the button to rotate servo fully.")

last_button_state = GPIO.input(BUTTON_PIN)

try:
    while True:
        current_button_state = GPIO.input(BUTTON_PIN)

        # Detect button press (edge detection)
        if last_button_state == GPIO.HIGH and current_button_state == GPIO.LOW:
            print("Button pressed! Rotating servo...")
            # Move servo from 0° → 180° progressively
            for angle in range(0, 181, 5):
                set_servo_angle(angle)
            print("Servo reached end position.")

        last_button_state = current_button_state
        time.sleep(0.05)  # small delay to reduce CPU usage

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("Program terminated")