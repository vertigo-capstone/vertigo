import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import collections

# 아두이노 포트 및 시리얼 속도 설정
arduino_port = '/dev/ttyACM0'
baud_rate = 9600

# 시리얼 연결 초기화
ser = serial.Serial(arduino_port, baud_rate)

# 데이터를 계속 받을 수 있도록 하는 deque (고정된 길이 유지)
data_list = collections.deque(maxlen=100)

# 실시간 플로팅을 위한 함수
def update_plot(frame):
    if ser.in_waiting > 0:  # 수신 대기 데이터가 있는지 확인
        data = ser.readline().decode('utf-8').strip()  # 수신된 데이터를 디코딩하고 줄 바꿈 제거
        try:
            value = float(data)  # 데이터를 실수로 변환
            data_list.append(value)  # 데이터를 deque에 추가
        except ValueError:
            pass  # 잘못된 데이터가 오면 무시

    ax1.clear()  # 이전 플롯을 지우기
    ax1.plot(data_list, label="Heart Rate")  # 새로운 데이터로 플로팅
    ax1.set_title('Heart Rate Monitoring')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Heart Rate')
    ax1.legend()

# Subplot 설정
fig, ax1 = plt.subplots()

# 애니메이션 설정
ani = animation.FuncAnimation(fig, update_plot, interval=100, blit=False)

# 종료시 시리얼 포트 닫기
def on_close(event):
    ser.close()

fig.canvas.mpl_connect('close_event', on_close)

plt.show()
