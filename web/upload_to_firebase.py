import json
import os
import time
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 프로젝트 초기화


def initialize_firebase():
    # 절대 경로 설정
    key_path = "./firebase/vertigo-firebase.json"
    # key_path = os.path.join(base_path)

    # firebase-key.json 파일 확인
    if not os.path.exists(key_path):
        raise FileNotFoundError(
            f"'firebase-key.json' 파일이 경로에 없습니다: {key_path}")

    # Firebase Admin SDK 초기화
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

# Firestore에 데이터 업로드


# def upload_data_to_firestore():
    # 절대 경로 설정
    data_path = "web/sensor_data.json"
    # data_path = os.path.join(base_path, 'sensor_data.json')

    # data.json 파일 확인
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"'sensor_data.json' 파일이 경로에 없습니다: {data_path}")

    # JSON 파일 읽기
    with open(data_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Firestore에 데이터 업로드
    db = firestore.client()
    for collection_name, documents in data.items():
        collection_ref = db.collection(collection_name)
        for doc_id, doc_data in documents.items():
            collection_ref.document(doc_id).set(doc_data)
            print(f"Firestore에 업로드 완료: 컬렉션={collection_name}, 문서={doc_id}")


def main():
    try:
        print("Firebase 초기화 중...")
        initialize_firebase()

        while True:
            print("Firestore 데이터 업로드 중...")
            upload_data_to_firestore()
            print("10초 대기 중...")
            time.sleep(5)  # 5초 대기

    except KeyboardInterrupt:
        print("\n프로그램이 사용자 요청에 의해 종료되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == '__main__':
    main()
