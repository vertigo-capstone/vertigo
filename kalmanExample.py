import os
import sys
import time
import smbus
import numpy as np
import json
from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
sensorfusion = kalman.Kalman()

def initialize_sensor():
    try:
        imu.begin()
        imu.readSensor()
        imu.computeOrientation()
        sensorfusion.roll = imu.roll
        sensorfusion.pitch = imu.pitch
        sensorfusion.yaw = imu.yaw
        return True
    except OSError as e:
        print(f"Sensor initialization error: {e}")
        return False

# 초기 센서 설정 시도
if not initialize_sensor():
    print("Initial sensor setup failed. Retrying in 5 seconds...")
    time.sleep(5)

currTime = time.time()

while True:
    try:
        imu.readSensor()
        imu.computeOrientation()
        newTime = time.time()
        dt = newTime - currTime
        currTime = newTime

        sensorfusion.computeAndUpdateRollPitchYaw(
            imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2],
            imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2],
            imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt
        )

        # yaw 값이 유효하지 않은 경우 예외 발생
        if sensorfusion.yaw is None:
            raise ValueError("Yaw value is None, indicating a read or initialization issue.")

        data = {"roll": sensorfusion.roll, "pitch": sensorfusion.pitch, "yaw": sensorfusion.yaw}
        print(data)

    except (OSError, ValueError) as e:
        print(f"Error: {e}. Retrying sensor setup in 5 seconds...")
        time.sleep(5)
        initialize_sensor()  # 센서를 다시 초기화

    time.sleep(1/8000)
