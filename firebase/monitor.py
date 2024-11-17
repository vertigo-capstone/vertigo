from google.cloud import firestore

def main():
    # Firestore 초기화
    service_account_path = "firebase/vertigo-firebase.json"  # 서비스 계정 키 경로
    db = firestore.Client.from_service_account_json(service_account_path)

    # Firestore 데이터 읽기
    print("=== Firestore Data ===")
    docs = db.collection("vertigo").stream()  # 'vertigo' 컬렉션에서 데이터 가져오기
    for doc in docs:
        doc_data = doc.to_dict()
        print(f"Document ID: {doc.id}")
        print(f"Pitch: {doc_data.get('pitch', 'N/A')}")
        print(f"Roll: {doc_data.get('roll', 'N/A')}")
        print(f"Yaw: {doc_data.get('yaw', 'N/A')}")
        print("=======================")

    # 실시간 업데이트
    def on_snapshot(col_snapshot, changes, read_time):
        print("=== Real-Time Firestore Updates ===")
        for change in changes:
            if change.type.name in ["ADDED", "MODIFIED"]:
                doc_data = change.document.to_dict()
                print(f"Document ID: {change.document.id}")
                print(f"Pitch: {doc_data.get('pitch', 'N/A')}")
                print(f"Roll: {doc_data.get('roll', 'N/A')}")
                print(f"Yaw: {doc_data.get('yaw', 'N/A')}")
                print("===============================")

    # Firestore 실시간 리스너 연결
    collection_ref = db.collection("vertigo")
    collection_ref.on_snapshot(on_snapshot)

    print("Listening for Firestore updates...")

    # 프로그램이 종료되지 않도록 유지
    while True:
        pass

# 실행
if __name__ == "__main__":
    main()
