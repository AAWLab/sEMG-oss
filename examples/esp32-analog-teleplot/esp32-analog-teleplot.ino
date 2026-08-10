const int EMG_PIN = 34;
const unsigned long SAMPLE_INTERVAL_US = 1000; // About 1000 samples per second.

unsigned long nextSampleAt = 0;

void setup() {
  Serial.begin(115200);
  delay(300);

  analogReadResolution(12);
  analogSetPinAttenuation(EMG_PIN, ADC_11db);

  nextSampleAt = micros();
}

void loop() {
  unsigned long now = micros();
  if ((long)(now - nextSampleAt) < 0) {
    return;
  }
  nextSampleAt += SAMPLE_INTERVAL_US;

  int raw = analogRead(EMG_PIN);
  float voltage = raw * (3.3f / 4095.0f);

  Serial.print(">emg:");
  Serial.println(raw);
  Serial.print(">emg_v:");
  Serial.println(voltage, 3);
}
