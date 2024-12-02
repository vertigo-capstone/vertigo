import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, redirect, url_for, session

# Firebase Admin SDK 초기화
cred = credentials.Certificate('firebase-key.json')  # JSON 파일 경로
firebase_admin.initialize_app(cred)

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션을 위한 비밀 키 설정

# Firestore에서 센서 데이터를 가져오는 함수
def get_sensor_data():
    db = firestore.client()  # Firestore 클라이언트 생성

    # 'sensor' 컬렉션에서 각 문서 가져오기
    sensor_data = {}
    try:
        gyroscope_doc = db.collection('sensor').document('gyroscope').get()
        heart_doc = db.collection('sensor').document('heart').get()
        gps_doc = db.collection('sensor').document('GPS').get()

        if gyroscope_doc.exists:
            sensor_data['gyroscope'] = gyroscope_doc.to_dict()
        if heart_doc.exists:
            sensor_data['heart'] = heart_doc.to_dict()
        if gps_doc.exists:
            sensor_data['GPS'] = gps_doc.to_dict()

        print("Sensor data:", sensor_data)  # 데이터 확인
    except Exception as e:
        print("Error getting data:", e)

    return sensor_data


# 로그인 페이지
@app.route('/')
def login():
    return render_template('login.html', message="")

# 로그인 처리
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    # 로그인 정보 체크 (아이디와 비밀번호)
    if username == '1234' and password == '1234':  # 실제 아이디와 비밀번호로 수정
        session['username'] = username  # 세션에 사용자 정보 저장
        return redirect(url_for('dashboard'))  # 대시보드로 리다이렉트
    else:
        return render_template('login.html', message="로그인에 실패하였습니다.")  # 로그인 실패 메시지

# 대시보드 페이지
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))  # 로그인하지 않은 경우 로그인 페이지로 리다이렉트

    username = session['username']
    sensor_data = get_sensor_data()  # Firestore에서 센서 데이터 가져오기
    if sensor_data is None:
        sensor_data = {}  # 데이터가 없으면 빈 딕셔너리로 대체
    return render_template('dashboard.html', username=username, sensor_data=sensor_data)  # 대시보드에 데이터 출력

if __name__ == '__main__':
    app.run(debug=True)
