import json
import time

asdf = time.time()
data = {
    "trash0": "name",
    "trash1": 30,
    "trash2": "New York",
    "trash3": False,
    "data": asdf
}

# JSON 파일로 저장
with open('data.json', 'w') as json_file: #파일 경로 지정할 것
    json.dump(data, json_file, indent=4)  # indent는 읽기 쉽게 들여쓰기를 추가
