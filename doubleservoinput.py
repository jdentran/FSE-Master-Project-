import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17
LEFT_SERVO = 18
RIGHT_SERVO = 19  # Example second pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LEFT_SERVO, GPIO.OUT)
GPIO.setup(RIGHT_SERVO, GPIO.OUT)

left_pwm = GPIO.PWM(LEFT_SERVO, 50)
right_pwm = GPIO.PWM(RIGHT_SERVO, 50)
left_pwm.start(0)
right_pwm.start(0)

def move_servo(pwm, start_angle, end_angle, step=2, delay=0.02):
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
current_angle = 180  # Start neutral (closed)

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)

        if last_button_state == GPIO.HIGH and button_state == GPIO.LOW:
            print("Button pressed! Flipping servos...")

            # Compute next angle
            next_angle = 90 if current_angle == 180 else 180

            # Move left servo
            move_servo(left_pwm, current_angle, next_angle)
            # Move right servo mirrored
            move_servo(right_pwm, 180 - current_angle, 180 - next_angle)

            current_angle = next_angle
            print(f"Left servo: {current_angle}°, Right servo: {180 - current_angle}°")

        last_button_state = button_state
        time.sleep(0.05)

except KeyboardInterrupt:
    left_pwm.stop()
    right_pwm.stop()
    GPIO.cleanup()
    print("Program terminated")