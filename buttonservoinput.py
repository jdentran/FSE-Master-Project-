import RPi.GPIO as GPIO
import time

# -------------------
# Pin Setup
# -------------------
BUTTON_PIN = 17      # Button input
SERVO_PIN = 18       # Servo PWM output

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up resistor
GPIO.setup(SERVO_PIN, GPIO.OUT)

# PWM for servo
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz for MG995
pwm.start(0)

# -------------------
# Servo control function
# -------------------
def set_servo_angle(angle):
    # Convert angle (0-180) to duty cycle (2-12)
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Time for servo to move
    pwm.ChangeDutyCycle(0)  # Stop sending signal

# -------------------
# Main loop
# -------------------
print("Press the button to rotate the servo 0° → 180°")

servo_moved = False

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)

        # Button pressed and servo hasn't moved yet
        if button_state == GPIO.LOW and not servo_moved:
            print("Button pressed! Rotating servo...")
            set_servo_angle(180)  # Move directly to 180°
            print("Servo reached 180°. Stopping.")
            servo_moved = True  # Prevent further movement

        time.sleep(0.05)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("Program terminated")