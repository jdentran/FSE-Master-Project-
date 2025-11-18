import RPi.GPIO as GPIO
import time
import board
import digitalio

GPIO.setmode(GPIO.BCM)

# Servo pins
SERVO_LEFT = 18
SERVO_RIGHT = 19

GPIO.setup(SERVO_LEFT, GPIO.OUT)
GPIO.setup(SERVO_RIGHT, GPIO.OUT)

left = GPIO.PWM(SERVO_LEFT, 50)     # normal servo
right = GPIO.PWM(SERVO_RIGHT, 50)   # reversed servo
left.start(0)
right.start(0)

button = digitalio.DigitalInOut(board.D17)
button.switch_to_input(pull=digitalio.Pull.DOWN)

is_open = False
last_state = False

def angle_to_duty(angle):
    """Normal servo conversion."""
    return 2.5 + (angle / 180.0) * 10

def set_servo_mirrored(left_angle):
    """
    Moves left servo normally, moves right servo as a MIRROR
    using reversed duty cycle instead of reversed angle.
    This keeps both movements synchronized.
    """
    # Normal servo movement
    left_duty = angle_to_duty(left_angle)

    # Mirrored reversed servo movement (perfect inversion)
    # 2.5 → 12.5 becomes 12.5 → 2.5
    right_duty = 15 - left_duty

    # send signals
    left.ChangeDutyCycle(left_duty)
    right.ChangeDutyCycle(right_duty)

    time.sleep(0.3)

    # stop driving to avoid jitter
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)

print("Ready. Press button to toggle flaps (perfect mirrored control).")

try:
    while True:
        current_state = button.value

        if current_state and not last_state:  # edge detect
            if is_open:
                # CLOSE → left = 180, right auto-mirrors
                set_servo_mirrored(180)
                is_open = False
            else:
                # OPEN → left = 90, right mirrors perfectly
                set_servo_mirrored(90)
                is_open = True

            time.sleep(0.25)

        last_state = current_state
        time.sleep(0.02)

except KeyboardInterrupt:
    left.stop()
    right.stop()
    GPIO.cleanup()
    print("Stopped.")