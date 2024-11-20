import numpy as np
import serial
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# 아두이노와 연결된 시리얼 포트 설정
arduino_port = '/dev/ttyACM0'  #포트 주소
baud_rate = 9600  # 아두이노와 동일한 baud_rate로 설정
# 시리얼 포트 열기
heart_i = np.array([])
at = None
ng = None
loc = "/home/vertigo/vertigo/sensors/information_data/gps_data.json"
#json 쓰기 함수
def json_write(let_loc, let_data):
    with open(let_loc, "w") as json_file:
            json.dump(let_data, json_file, indent=4)  # indent=4로 보기 좋게 포맷
#시리얼 읽기 함수
def ser_read(let_ser):
    let_line = let_ser.readline().decode('utf-8').strip()
    return let_line
# 시리얼 데이터를 읽고 처리
def processing_heart(let_line, let_heart_i):
    if let_line == (None or ""):
        pass
    elif let_line[0] == "h":
        let_heart_i = np.append(let_heart_i, int(line[1:]))
    let_heart_i = let_heart_i.astype(int)
    print(let_heart_i)
try:
    while True:
        line = ser_read(serial.Serial(arduino_port, baud_rate))
        print("읽은 데이터는 다음과 같습니다:", line)
        processing_heart(line, heart_i)
        if line == (None or ""):
            pass
        elif line[0] == "a":
            at = float(line[1:])
        elif line[0] == "n":
            ng = float(line[1:])
        else:
            pass
        data = {"latitude":at, "longitude":ng}
        print(data)
        json_write(loc, data)
except KeyboardInterrupt:
    print("프로그램을 종료합니다.")
finally:
    serial.Serial(arduino_port, baud_rate).close()  # 시리얼 포트 닫기