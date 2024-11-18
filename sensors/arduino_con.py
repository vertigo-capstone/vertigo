import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# 아두이노가 연결된 포트 설정 (예: 'COM3' 또는 '/dev/ttyUSB0')
arduino_port = '/dev/ttyACM0'  # 실제 포트로 변경 필요
baud_rate = 9600               # 아두이노와 동일한 보드레이트 설정

# 시리얼 포트 초기화
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # 시리얼 포트 안정화 대기

# 데이터 저장용 리스트 초기화
heart_rate_data = []
time_data = []
start_time = time.time()

# 플로팅 설정
plt.style.use('seaborn')
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-', label='Heart Rate')
ax.set_xlim(0, 10)  # x축 초기 범위 (초)
ax.set_ylim(0, 1023)  # y축 범위 (심박 센서 데이터 범위)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Heart Rate (Analog Value)')
ax.legend()

# 애니메이션 업데이트 함수
def update(frame):
    global start_time

    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        try:
            heart_rate, gps_data = data.split(",", 1)
            heart_rate = int(heart_rate)
            current_time = time.time() - start_time

            # 데이터 추가
            heart_rate_data.append(heart_rate)
            time_data.append(current_time)

            # x축 범위를 조정하여 실시간 업데이트 유지
            if current_time > ax.get_xlim()[1]:
                ax.set_xlim(0, current_time + 10)

            # 플로팅 데이터 업데이트
            line.set_data(time_data, heart_rate_data)
            print(f"Heart Rate: {heart_rate}, GPS Data: {gps_data}")

        except ValueError:
            # 잘못된 데이터 형식 예외 처리
            print("Invalid data format received")
    
    return line,

# 애니메이션 설정
ani = FuncAnimation(fig, update, blit=True, interval=1)  # 1ms마다 업데이트

plt.show()

# 시리얼 닫기
ser.close()
