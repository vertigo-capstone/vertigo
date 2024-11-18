#include <TinyGPS++.h>  // TinyGPS++ 라이브러리 포함
#include <ArduinoJson.h>

TinyGPSPlus gps;  // TinyGPS++ 객체 생성
int cnt = 0;
int cnt_max = 4096;

void setup() {
  Serial.begin(9600);   // 시리얼 모니터와 연결 (9600 baud)
  Serial1.begin(9600);  // GPS 모듈과 연결된 하드웨어 시리얼 포트 (Serial1)
  Serial.println("Init GPS...");
  pinMode(A0, INPUT);
}

void loop() {
  int heartRate = analogRead(A0);
  cnt += 1;
  if (cnt == cnt_max) {
    cnt = 0;
  }
  while (Serial1.available()) {  // Serial1에서 데이터를 읽기
    char c = Serial1.read();    // 읽은 데이터를 저장
    gps.encode(c);  // GPS 데이터 처리 (NMEA 문장)
  }
  if (cnt == 2) {
  Serial.print("Heart Rate (A0):");
  Serial.print(heartRate);
  Serial.println(", ");
  }
  // 데이터가 유효할 때만 출력
  if (gps.location.isValid()) {
    if (cnt == 1) {
      // JsonDocument 사용
      JsonDocument jsonDoc;  // JsonDocument 객체 생성 (크기 자동 관리)

      // GPS 데이터를 JSON 객체에 추가
      jsonDoc["latitude"] = gps.location.lat();  // 위도
      jsonDoc["longitude"] = gps.location.lng();  // 경도

      // JSON 객체를 문자열로 변환하여 출력
      char jsonBuffer[256];
      serializeJson(jsonDoc, jsonBuffer);
      Serial.println(jsonBuffer);

      Serial.print("위도는: ");
      Serial.print(gps.location.lat(), 6);  // 위도 출력 (소수점 6자리)
      Serial.print(" , ");
      Serial.print("경도는: ");
      Serial.println(gps.location.lng(), 6);  // 경도 출력 (소수점 6자리)
    }
  }
  else {
    if (cnt == 1) {
      Serial.println("GPS 신호를 찾는 중...");
    }
  }
}
