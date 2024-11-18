#include <SoftwareSerial.h>
#include <TinyGPS++.h>

// GPS와 연결된 소프트웨어 시리얼 포트 설정
SoftwareSerial gpsSerial(3, 4); // RX, TX 핀 설정

// TinyGPS++ 객체 생성
TinyGPSPlus gps;

void setup() {
  Serial.begin(9600);    // 기본 시리얼 포트 (USB 연결)
  gpsSerial.begin(9600); // GPS 모듈과의 시리얼 통신
  pinMode(A0, INPUT);    // 심박 센서 핀 설정
}

void loop() {
  // 심박 센서 데이터 읽기
  int heartRate = analogRead(A0);

  // GPS 데이터 읽기
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  // 심박 센서 값 시리얼 모니터에 출력
  Serial.print("Heart Rate (A0): ");
  Serial.print(heartRate);
  Serial.print(", ");

  // GPS 데이터가 완전히 수신되었을 때 출력
  if (gps.location.isUpdated()) {
    // 위도와 경도 출력 (단위: 도)
    double latitude = gps.location.lat();
    double longitude = gps.location.lng();
    
    Serial.print("Latitude: ");
    Serial.print(latitude, 6); // 위도 (소수점 6자리까지 출력)
    Serial.print(", Longitude: ");
    Serial.println(longitude, 6); // 경도 (소수점 6자리까지 출력)
  } else {
    Serial.println("Waiting for GPS data...");
  }

  delay(1000); // 1초 간격으로 데이터 전송
}
