import numpy as np
import serial
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 아두이노와 연결된 시리얼 포트 설정 (예: COM3 또는 /dev/ttyUSB0 등)
arduino_port = '/dev/ttyACM0'  # Windows의 경우 'COM3' 또는 아두이노 포트를 설정
baud_rate = 9600  # 아두이노와 동일한 baud_rate 설정

# 시리얼 포트 열기
ser = serial.Serial(arduino_port, baud_rate)
heart_i = np.array([])
at = None
ng = None
loc = "/home/vertigo/vertigo/sensors/information_data/location.json"
#json 쓰기 함수
def json_write(let_loc, let_data):
    with open(let_loc, "w") as json_file:
            json.dump(let_data, json_file, indent=4)  # indent=4로 보기 좋게 포맷
#시리얼 읽기 함수
def ser_read(let_ser):
    let_line = ser.readline().decode('utf-8').strip()
    return let_line
# 시리얼 데이터를 읽고 처리
try:
    while True:
        line = ser_read(loc)
        print("읽은 데이터는 다음과 같습니다:", line)
        if line == (None or ""):
            pass
        elif line[0] == "h":
            heart_i = np.append(heart_i, int(line[1:]))
        elif line[0] == "a":
            at = float(line[1:])
        elif line[0] == "n":
            ng = float(line[1:])
        else:
            pass
        data = {"latitude":at, "longitude":ng}
        print(data)
        heart_i = heart_i.astype(int)
        print(heart_i)
        json_write(loc, data)
except KeyboardInterrupt:
    print("프로그램을 종료합니다.")
finally:
    ser.close()  # 시리얼 포트 닫기
