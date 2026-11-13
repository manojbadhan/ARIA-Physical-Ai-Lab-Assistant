// Arduino: same protocol, plain text. Sends "ok" every second, toggles LED on 'L'.
void setup() { Serial.begin(115200); pinMode(LED_BUILTIN, OUTPUT); }
unsigned long last = 0;
void loop() {
  if (Serial.available() && Serial.read() == 'L') digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  if (millis() - last > 1000) { last = millis(); Serial.println("ok"); }
}
