import json
import random
import time

# 임의의 값을 생성하는 함수
def generate_random_value():
    return str(random.randint(1, 100))  # 예시로 1부터 100까지의 임의의 정수 값을 생성

# JSON 파일 경로
file_path = 'C:/Users/user/Desktop/Firebase/sensor_data.json'

# JSON 파일을 읽고 데이터 수정 후 덮어쓰기
def update_json_file():
    try:
        # JSON 파일 읽기
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # 각 "value" 부분을 임의의 값으로 변경
        data['sensor']['gyroscope']['roll'] = generate_random_value()
        data['sensor']['gyroscope']['pitch'] = generate_random_value()
        data['sensor']['gyroscope']['yaw'] = generate_random_value()
        data['sensor']['heart']['rate'] = generate_random_value()
        data['sensor']['GPS']['latitude'] = generate_random_value()
        data['sensor']['GPS']['longitude'] = generate_random_value()
        
        # 수정된 데이터를 다시 JSON 파일에 덮어쓰기
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print("JSON 파일이 성공적으로 업데이트되었습니다!")

    except FileNotFoundError:
        print(f"{file_path} 파일을 찾을 수 없습니다.")
    except json.JSONDecodeError:
        print(f"{file_path} 파일을 읽는 데 문제가 발생했습니다.")
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")

while True:
    update_json_file()
    time.sleep(5) #5초 대기

