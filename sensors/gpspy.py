import serial
import json
import time

# 아두이노의 시리얼 포트를 설정합니다. (예: COM3, /dev/ttyUSB0 등)
ser = serial.Serial('/dev/ttyACM0', 9600)  # 시리얼 포트 이름과 BaudRate 설정

# 파일 이름 설정
output_file = "gps_data.json"

# GPS 데이터가 시리얼로 출력될 때마다 JSON 파일로 저장
try:
    while True:
        if ser.in_waiting > 0:  # 데이터가 수신되었을 때
            data = ser.readline().decode('utf-8').strip()
            
            try:
                # JSON 데이터로 변환
                gps_data = json.loads(data)
                
                # JSON 파일에 저장
                with open(output_file, 'w') as f:
                    json.dump(gps_data, f, indent=4)
                
                print(f"GPS Data Saved: {gps_data}")
            except json.JSONDecodeError:
                # JSON 포맷이 아닌 데이터가 들어오면 무시
                print("Invalid JSON data received")
        
        time.sleep(1)  # 1초마다 확인

except KeyboardInterrupt:
    print("Program interrupted")
finally:
    ser.close()  # 시리얼 포트 닫기