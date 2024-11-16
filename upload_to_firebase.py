import firebase_admin
from firebase_admin import credentials, firestore
import json
import time

cred = credentials.Certificate("firebase-key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()
json_file_path = "data.json"

def upload_data():
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            doc_ref = db.collection("your_collection_name").document(key)
            doc_ref.set(value)

        print("JSON 데이터를 Firestore에 업로드 완료!")

while True:
    upload_data()
    time.sleep(30)  # 30초 대기 후 다시 실행
