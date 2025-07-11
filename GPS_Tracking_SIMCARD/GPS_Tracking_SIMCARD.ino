#include <TinyGPS++.h>
#include <SoftwareSerial.h>

TinyGPSPlus gps;

// GPS on SoftwareSerial — TX from GPS to D4, RX from Arduino to D5
SoftwareSerial gpsSerial(4, 5);  // GPS TX → D4, GPS RX ← D5

String server = "http://192.168.1.11:5000/gps";

void setup() {
  Serial.begin(9600);           // SIM7600 on hardware UART
  gpsSerial.begin(9600);        // GPS module

  Serial.println("🛰️ GPS Tracker booting...");

  delay(3000);
  checkCommand("AT", "OK");
  checkCommand("AT+CGATT=1", "OK");
  checkCommand("AT+CSTT=\"telstra.internet\"", "OK");   // Update with your working APN
  checkCommand("AT+CIICR", "OK");
  checkCommand("AT+CIFSR", ".");
}

void loop() {
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  if (gps.location.isValid()) {
    float lat = gps.location.lat();
    float lon = gps.location.lng();
    String timestamp = "Fallback-" + String(millis());
    String speed = String(gps.speed.kmph(), 2);
    String sats  = String(gps.satellites.value());

    Serial.println("🧭 Location acquired:");
    Serial.println("Lat: " + String(lat, 6));
    Serial.println("Lon: " + String(lon, 6));
    Serial.println("Speed: " + speed);
    Serial.println("Sats: " + sats);

    String json = "{";
    json += "\"latitude\":\"" + String(lat, 6) + "\",";
    json += "\"longitude\":\"" + String(lon, 6) + "\",";
    json += "\"timestamp\":\"" + timestamp + "\",";
    json += "\"speed\":\"" + speed + "\",";
    json += "\"satellites\":\"" + sats + "\"";
    json += "}";

    sendHTTP(json);
    delay(15000);
  }
}

void sendHTTP(String json) {
  Serial.println("📡 Starting HTTP POST...");
  checkCommand("AT+HTTPTERM", "OK");
  checkCommand("AT+HTTPINIT", "OK");
  checkCommand("AT+HTTPPARA=\"CID\",1", "OK");
  checkCommand("AT+HTTPPARA=\"URL\",\"" + server + "\"", "OK");
  checkCommand("AT+HTTPPARA=\"CONTENT\",\"application/json\"", "OK");

  Serial.println("📦 Payload:");
  Serial.println(json);

  Serial.println("AT+HTTPDATA=" + String(json.length()) + ",10000");
  delay(500);
  Serial.println(json);
  delay(1500);

  Serial.println("AT+HTTPACTION=1");
  delay(3000);
  String resp = readResponse(4000);
  Serial.println("📥 HTTP Response:");
  Serial.println(resp);

  checkCommand("AT+HTTPTERM", "OK");
}

bool checkCommand(String command, String expected) {
  Serial.println(command);
  String resp = readResponse(2000);
  Serial.println("🔧 " + command + " → " + resp);
  return resp.indexOf(expected) != -1;
}

String readResponse(unsigned long timeout_ms) {
  String response = "";
  unsigned long start = millis();
  while (millis() - start < timeout_ms) {
    while (Serial.available()) {
      response += (char)Serial.read();
    }
  }
  return response;
}