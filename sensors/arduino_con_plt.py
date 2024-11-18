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

# 실시간 그래프 설정
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-', label="Heart Rate")
ax.set_xlim(0, 100)  # x축 범위 설정
ax.set_ylim(0, 800)  # y축 범위 설정 (심박수에 맞게 조정)
ax.set_xlabel('Time')
ax.set_ylabel('Heart Rate')
ax.legend()

# 업데이트 함수 정의
def update(frame):
    global heart_i
    line_data = ser.readline().decode('utf-8').strip()
    if line_data and line_data[0] == "h":
        heart_i = np.append(heart_i, int(line_data[1:]))
        heart_i = heart_i[-100:]  # 최대 100개의 데이터만 유지 (그래프가 너무 길어지지 않도록)
        line.set_data(np.arange(len(heart_i)), heart_i)
        ax.set_xlim(0, max(100, len(heart_i)))  # x축을 데이터 길이에 맞게 조정
    return line,

# 애니메이션 설정
ani = FuncAnimation(fig, update, interval=100)

try:
    plt.show()  # 그래프 표시
except KeyboardInterrupt:
    print("프로그램을 종료합니다.")
finally:
    ser.close()  # 시리얼 포트 닫기
