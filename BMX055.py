# BMX055.py
# MicroPython driver for BMX055 (Accel + Gyro + Mag)
# Author: Teru & Copilot

from machine import I2C
import time

class BMX055:
    # I2C addresses
    ACC_ADDR = 0x18
    GYR_ADDR = 0x68
    MAG_ADDR = 0x10

    # -------------------------
    # Constructor
    # -------------------------
    def __init__(self, i2c: I2C):
        self.i2c = i2c
        self.init_accel()
        self.init_gyro()
        self.init_mag()

    # -------------------------
    # Accelerometer
    # -------------------------
    def init_accel(self):
        self._write(self.ACC_ADDR, 0x0F, 0x03)  # ±2g
        self._write(self.ACC_ADDR, 0x10, 0x08)  # BW = 7.81Hz
        self._write(self.ACC_ADDR, 0x11, 0x00)  # Normal mode
        time.sleep_ms(10)

    def read_accel(self):
        data = self._read(self.ACC_ADDR, 0x02, 6)

        x = ((data[1] << 8) | (data[0] & 0xF0)) >> 4
        y = ((data[3] << 8) | (data[2] & 0xF0)) >> 4
        z = ((data[5] << 8) | (data[4] & 0xF0)) >> 4

        # sign correction (12bit)
        if x > 2047: x -= 4096
        if y > 2047: y -= 4096
        if z > 2047: z -= 4096

        return x, y, z

    # -------------------------
    # Gyroscope
    # -------------------------
    def init_gyro(self):
        self._write(self.GYR_ADDR, 0x0F, 0x04)  # ±125 dps
        self._write(self.GYR_ADDR, 0x10, 0x07)  # ODR = 100Hz
        self._write(self.GYR_ADDR, 0x11, 0x00)  # Normal mode
        time.sleep_ms(10)

    def read_gyro(self):
        data = self._read(self.GYR_ADDR, 0x02, 6)

        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]

        # sign correction (16bit)
        if x > 32767: x -= 65536
        if y > 32767: y -= 65536
        if z > 32767: z -= 65536

        return x, y, z

    # -------------------------
    # Magnetometer
    # -------------------------
    def init_mag(self):
        self._write(self.MAG_ADDR, 0x4B, 0x83)  # Soft reset
        time.sleep_ms(10)

        self._write(self.MAG_ADDR, 0x4C, 0x00)  # Normal mode, ODR 10Hz
        self._write(self.MAG_ADDR, 0x4E, 0x84)  # Enable XYZ
        self._write(self.MAG_ADDR, 0x51, 0x04)  # XY repetitions = 9
        self._write(self.MAG_ADDR, 0x52, 0x0F)  # Z repetitions = 15
        time.sleep_ms(10)

    def read_mag(self):
        data = self._read(self.MAG_ADDR, 0x42, 6)

        x = ((data[1] << 8) | (data[0] & 0xF8)) >> 3
        y = ((data[3] << 8) | (data[2] & 0xF8)) >> 3
        z = ((data[5] << 8) | (data[4] & 0xFE)) >> 1

        # sign correction
        if x > 4095: x -= 8192
        if y > 4095: y -= 8192
        if z > 16383: z -= 32768

        return x, y, z

    # -------------------------
    # Low-level I2C helpers
    # -------------------------
    def _write(self, addr, reg, val):
        self.i2c.writeto_mem(addr, reg, bytes([val]))

    def _read(self, addr, reg, length):
        return self.i2c.readfrom_mem(addr, reg, length)
