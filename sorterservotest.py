import RPi.GPIO as GPIO
import time
import sys
import termios
import tty

GPIO.setmode(GPIO.BCM)

SORTER = 17
GPIO.setup(SORTER, GPIO.OUT)

sorter = GPIO.PWM(SORTER, 50)
sorter.start(0)

# -----------------------
# STARTING DUTY (will be tuned)
# -----------------------
duty = 7.5   # starting guess

def move(d):
    sorter.ChangeDutyCycle(d)
    time.sleep(0.25)
    sorter.ChangeDutyCycle(0)

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

print("\n--- SERVO CALIBRATION MODE ---")
print("A = move LEFT")
print("D = move RIGHT")
print("S = SAVE as NEUTRAL")
print("Q = quit\n")

try:
    while True:
        print(f"\rCurrent Duty: {duty:.2f}   ", end="")
        move(duty)

        key = getch()

        if key.lower() == 'a':
            duty -= 0.05
        elif key.lower() == 'd':
            duty += 0.05
        elif key.lower() == 's':
            print(f"\n✅ SAVED NEUTRAL DUTY = {duty:.2f}")
        elif key.lower() == 'q':
            break

        # SAFETY LIMITS
        duty = max(5.5, min(9.5, duty))

except KeyboardInterrupt:
    pass

sorter.stop()
GPIO.cleanup()
print("\nProgram stopped.")