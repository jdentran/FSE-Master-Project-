import RPi.GPIO as GPIO
import time

# Pin setup
BUTTON_PIN = 17
SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up resistor
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_servo_angle(angle):
    duty = 2 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Time for servo to move
    pwm.ChangeDutyCycle(0)

print("Press the button to rotate servo 0° → 180°")

try:
    while True:
        # Wait for button press
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed! Rotating servo...")
            set_servo_angle(180)  # Move directly to 180°
            
            # Wait until button released to allow next press
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.05)
            
            print("Servo at 180°. Waiting for next button press.")
        else:
            time.sleep(0.05)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("Program terminated")