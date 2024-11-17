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

# 넘어짐 감지 임계값
ACC_THRESHOLD = 9.5  # z축의 가속도가 9.5보다 작으면 넘어졌다고 판단
TILT_THRESHOLD = 30  # 기울기 각도 임계값 (roll 또는 pitch가 이 값을 넘으면 넘어짐)

def is_fallen(accel_vals, roll, pitch):
    # 가속도 값이 너무 작거나, 기울기가 너무 크면 넘어졌다고 판단
    accel_magnitude = np.sqrt(accel_vals[0]**2 + accel_vals[1]**2 + accel_vals[2]**2)
    if accel_magnitude < ACC_THRESHOLD or abs(roll) > TILT_THRESHOLD or abs(pitch) > TILT_THRESHOLD:
        return True
    return False

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

        # 넘어짐 감지
        if is_fallen(imu.AccelVals, sensorfusion.roll, sensorfusion.pitch):
            print("Fall detected!")
            data["fall_detected"] = True
        else:
            data["fall_detected"] = False

        file_path = '/home/vertigo/vertigo/gyro.json'
        # 데이터 파일에 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"'{file_path}'에 JSON 데이터를 저장했습니다.")

    except (OSError, ValueError) as e:
        print(f"Error: {e}. Retrying sensor setup in 5 seconds...")
        time.sleep(5)
        initialize_sensor()  # 센서를 다시 초기화

    time.sleep(1)
