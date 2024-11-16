import serial
import json
import matplotlib.pyplot as plt
import numpy as np

# 아두이노와 연결된 시리얼 포트 설정 (예: /dev/ttyUSB0)
arduino_port = '/dev/ttyACM0'
baud_rate = 9600  # 아두이노와 동일한 속도 설정

# 시리얼 포트 열기
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

# 그래프를 초기화
plt.ion()  # interactive mode 활성화
fig, ax = plt.subplots()
x_data = []  # 시간 또는 샘플 번호
y_data = []  # 센서 값

# 그래프의 축 레이블 설정
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Sensor Value')

# 그래프의 범위 설정
ax.set_ylim(0, 1023)  # 센서 값 범위 (예시: 0~1023)

# 그래프 초기화
line, = ax.plot(x_data, y_data, 'r-')  # 초기 선 그리기

# 시간 변수
time_elapsed = 0

# 실시간 데이터 수집 및 플로팅
while True:
    if ser.in_waiting > 0:
        # 시리얼 데이터 읽기 (바이트 단위로 읽기)
        byte_data = ser.readline()

        if byte_data:
            try:
                # 바이트 데이터를 문자열로 디코딩
                decoded_data = byte_data.decode('utf-8', errors='ignore').strip()

                if decoded_data:
                    # JSON 형식으로 파싱
                    json_data = json.loads(decoded_data)
                    sensor_value = json_data.get("sensor_value", None)

                    if sensor_value is not None:
                        # 데이터 리스트에 추가
                        x_data.append(time_elapsed)
                        y_data.append(sensor_value)

                        # 그래프 업데이트
                        line.set_xdata(x_data)
                        line.set_ydata(y_data)

                        # x축 범위 업데이트 (최대 1000개 데이터로 제한)
                        if len(x_data) > 1000:
                            x_data = x_data[-1000:]
                            y_data = y_data[-1000:]

                        ax.relim()  # 데이터에 맞게 축의 범위 재계산
                        ax.autoscale_view(True, True, True)

                        # 화면 업데이트
                        plt.pause(0.01)

                        # 시간 증가
                        time_elapsed += 1

            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"Error decoding data: {e}, Raw data: {byte_data}")
    
    plt.pause(0.01)  # 그래프 갱신을 위한 짧은 대기
