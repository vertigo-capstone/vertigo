import numpy as np
import serial
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import sys
import time
import smbus
from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman

#자이로 센서 포트 설정
address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
sensorfusion = kalman.Kalman()
imu.readSensor()
imu.computeOrientation()
sensorfusion.roll = imu.roll
sensorfusion.pitch = imu.pitch
sensorfusion.yaw = imu.yaw
count = 0
currTime = time.time()

# 아두이노와 연결된 시리얼 포트 설정 (예: COM3 또는 /dev/ttyUSB0 등)
arduino_port = '/dev/ttyACM0'  # Windows의 경우 'COM3' 또는 아두이노 포트를 설정
baud_rate = 9600  # 아두이노와 동일한 baud_rate 설정

# 시리얼 포트 열기
ser = serial.Serial(arduino_port, baud_rate)
ecg_data = np.array([])
at = None
ng = None
# 시리얼 데이터를 읽고 처리
try:
    while True:
        #자이로 센서
        imu.readSensor()
        imu.computeOrientation()
        newTime = time.time()
        dt = newTime - currTime
        currTime = newTime
        sensorfusion.computeAndUpdateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2], imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt)
        gyro_val = {
            "roll":sensorfusion.roll,
            "pitch":sensorfusion.pitch,
            "yaw":sensorfusion.yaw
        }
        # 시리얼 포트에서 한 줄을 읽음
        line = ser.readline().decode('utf-8').strip()
        print("읽은 데이터는 다음과 같습니다:", line)
        if line == (None or ""):
            pass
        elif line[0] == "h":
            ecg_data = np.append(ecg_data, int(line[1:]))
        elif line[0] == "a":
            at = float(line[1:])
        elif line[0] == "n":
            ng = float(line[1:])
        else:
            pass
        data = {"latitude":at, "longitude":ng}
        print(data)
        ecg_data = ecg_data.astype(int)
        print(ecg_data)
        with open("gyro_data.json", "w") as json_file:
            json.dump(gyro_val, json_file, indent=4)  # indent=4로 보기 좋게 포맷
        with open("gps_data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)  # indent=4로 보기 좋게 포맷
        np.save('ecg_data.npy', ecg_data)
        #loaded_data = np.load('ecg_data.npy')
        #print(loaded_data)
except IndexError as e:
    print(f"인덱스 오류 발생: {e}")
except KeyboardInterrupt:
    print("프로그램을 종료합니다.")
finally:
    ser.close()  # 시리얼 포트 닫기
