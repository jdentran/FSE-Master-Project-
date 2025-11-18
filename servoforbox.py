import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17
SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def move_servo(start_angle, end_angle, step=2, delay=0.02):
    if start_angle < end_angle:
        angles = range(start_angle, end_angle + 1, step)
    else:
        angles = range(start_angle, end_angle - 1, -step)
    
    for angle in angles:
        duty = 2 + (angle / 18)
        pwm.ChangeDutyCycle(duty)
        time.sleep(delay)
    pwm.ChangeDutyCycle(0)

print("Press the button to flip the hamper 90° each time.")

last_button_state = GPIO.input(BUTTON_PIN)
current_angle = 0  # Start neutral at 0°

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)

        # Detect button press (edge)
        if last_button_state == GPIO.HIGH and button_state == GPIO.LOW:
            print("Button pressed! Flipping servo...")
            next_angle = 90 if current_angle == 0 else 0
            move_servo(current_angle, next_angle)
            current_angle = next_angle
            print(f"Servo now at {current_angle}°")

        last_button_state = button_state
        time.sleep(0.05)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("Program terminated")