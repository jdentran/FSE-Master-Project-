import time
import RPi.GPIO as GPIO

# -------------------
# Servo Setup
# -------------------
servo_pin = 17  # GPIO17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz for servo
pwm.start(0)

def set_servo_angle(angle):
    """Move servo to a specific angle (0-180°)."""
    duty = 2 + (angle / 18)  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Stop sending signal

# -------------------
# Test Loop
# -------------------
try:
    while True:
        print("Moving to 0°")
        set_servo_angle(0)
        time.sleep(1)
        
        print("Moving to 90°")
        set_servo_angle(90)
        time.sleep(1)
        
        print("Moving to 180°")
        set_servo_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("Servo test finished")