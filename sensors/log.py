import serial
import time

# 아두이노와 연결된 포트와 보드레이트 설정
arduino_port = '/dev/ttyACM0'  # 아두이노가 연결된 포트
baud_rate = 9600               # 아두이노와 동일한 통신 속도

# 시리얼 포트 열기
ser = serial.Serial(arduino_port, baud_rate)

# 심박수 데이터 수집 및 처리 함수
def process_heart_rate():
    heart_rate_data = []
    while True:
        if ser.in_waiting > 0:  # 데이터가 시리얼 포트에 있으면
            line = ser.readline()  # 한 줄 읽기
            try:
                signal_value = int(line.strip())  # 줄 끝의 개행문자 제거하고 정수로 변환
                heart_rate_data.append(signal_value)
                
                # 일정 간격으로 심박수를 출력 (예시: 10개의 데이터 평균을 출력)
                if len(heart_rate_data) > 10:
                    heart_rate_data = heart_rate_data[-10:]  # 최근 10개의 값만 유지
                    avg_signal = sum(heart_rate_data) / len(heart_rate_data)
                    print(f"최근 심박수 신호 평균: {avg_signal:.2f}")
                    
                    # 예시: 특정 임계값 이상일 때 발작 가능성 체크
                    if avg_signal > 600:  # 임계값 (예시)
                        print("발작 징후: 심박수 신호가 비정상적으로 높습니다!")
            
            except ValueError:
                continue  # 잘못된 값이 들어오면 무시하고 계속 진행

        time.sleep(0.1)  # 0.1초 대기

# 실시간 심박수 데이터 처리 시작
process_heart_rate()
