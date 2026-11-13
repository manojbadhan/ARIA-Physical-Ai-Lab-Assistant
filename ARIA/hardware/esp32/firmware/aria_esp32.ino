// ESP32: heartbeat + LED command over serial JSON lines. {"cmd":"led","on":1}
#include <ArduinoJson.h>
const int LED_PIN = 2;
unsigned long last = 0;
void setup() { Serial.begin(115200); pinMode(LED_PIN, OUTPUT); }
void loop() {
  if (Serial.available()) {
    StaticJsonDocument<128> d;
    if (!deserializeJson(d, Serial.readStringUntil('\n')) && String((const char*)d["cmd"]) == "led")
      digitalWrite(LED_PIN, d["on"] ? HIGH : LOW);
  }
  if (millis() - last > 1000) { last = millis(); Serial.println("{\"device\":\"esp32\",\"status\":\"ok\"}"); }
}
