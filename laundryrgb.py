import time
import board
import busio
import adafruit_tcs34725

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)
sensor.integration_time = 400
sensor.gain = 60

while True: 
    r, g, b, c = sensor.color_raw
    if c == 0:
        continue
    r_norm = r / c
    g_norm = g / c
    b_norm = b / c

    brightness = 0.299 * r_norm + 0.587 * g_norm + 0.114 * b_norm

    rgb = (int(r_norm * 255), int(g_norm * 255), int(b_norm * 255))

    print("R:", r, "G:", g, "B:", b, "C:", c,)
    print("Color Temperature:", sensor.color_temperature, "K")
    print("Lux:", sensor.lux)
    print("Normalized RGB:", rgb)

    if c > 100 and brightness > 0.55:
        print("Light / White Clothing Detected")
    else:
        print("Dark / Colored Clothing Detected")
    print("-----------------------------")
    time.sleep(1)
    