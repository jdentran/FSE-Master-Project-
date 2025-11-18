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

# Setup PWM for servo
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
pwm.start(0)

def set_servo_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.4)
    pwm.ChangeDutyCycle(0)

print("Press the button to move the servo...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button pressed
            print("Button pressed! Moving servo...")
            set_servo_angle(0)
            time.sleep(0.3)
            set_servo_angle(90)
            time.sleep(0.3)
            set_servo_angle(180)
            time.sleep(0.3)
            print("Servo movement complete.")
        
        time.sleep(0.1)  # Prevent CPU hogging

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()