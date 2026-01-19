from machine import I2C, Pin
from BMX055 import BMX055
import time

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
bmx = BMX055(i2c)

while True:
    ax, ay, az = bmx.read_accel()
    gx, gy, gz = bmx.read_gyro()
    mx, my, mz = bmx.read_mag()

    print("ACC:", ax, ay, az)
    print("GYR:", gx, gy, gz)
    print("MAG:", mx, my, mz)
    print()

    time.sleep(0.1)
