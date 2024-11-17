#include <TinyGPS++.h>  // Include TinyGPS++ library
#include <ArduinoJson.h> // Include ArduinoJson library (if you need it later)

TinyGPSPlus gps;  // Create a TinyGPS++ object
int cnt_max = 1000000;  // Loop interval control (higher value for slower updates)
unsigned long lastUpdateTime = 0;  // Time control for printing GPS data
unsigned long updateInterval = 1000;  // Time interval to update GPS info (1 second)

int heartPin = A0;  // Analog pin connected to the heart rate sensor
int heartData = 0;   // Variable to store the heart sensor value

void setup() {
  Serial.begin(9600);   // Start Serial Monitor communication (9600 baud)
  Serial1.begin(9600);  // Start communication with GPS module (Serial1)
  Serial.println("Initializing GPS and Heart Sensor...");
}

void loop() {
  // Read data from GPS and decode it
  while (Serial1.available()) {
    char c = Serial1.read();  // Read a character from Serial1 (GPS data)
    gps.encode(c);            // Pass character to GPS object for decoding
  }

  // Read heart sensor data (analog value from A0 pin)
  heartData = analogRead(heartPin);  // Read analog value from the heart sensor

  // Send GPS and heart rate data to Serial Monitor
  if (gps.location.isValid()) {
    unsigned long currentTime = millis();
    if (currentTime - lastUpdateTime >= updateInterval) {
      lastUpdateTime = currentTime;  // Update the last time printed

      // Print latitude and longitude (GPS data)
      Serial.print("Latitude: ");
      Serial.print(gps.location.lat(), 6);  // Print latitude with 6 decimal places
      Serial.print(" , ");
      Serial.print("Longitude: ");
      Serial.print(gps.location.lng(), 6);  // Print longitude with 6 decimal places

      // Print heart rate data
      Serial.print(" , ");
      Serial.print("Heart Rate: ");
      Serial.println(heartData);  // Print heart sensor analog data
    }
  } else {
    // If GPS signal is lost, notify via Serial Monitor
    unsigned long currentTime = millis();
    if (currentTime - lastUpdateTime >= updateInterval) {
      lastUpdateTime = currentTime;
      Serial.println("Waiting for GPS signal...");
    }
  }

  // Add a small delay for stability
  delay(100);
}