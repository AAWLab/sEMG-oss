const int EMG_PIN = A0;
const unsigned long SAMPLE_INTERVAL_US = 1000; // About 1000 samples per second.

unsigned long nextSampleAt = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
  nextSampleAt = micros();
}

void loop() {
  unsigned long now = micros();
  if ((long)(now - nextSampleAt) < 0) {
    return;
  }
  nextSampleAt += SAMPLE_INTERVAL_US;

  int raw = analogRead(EMG_PIN);
  Serial.print(">emg:");
  Serial.println(raw);
}
