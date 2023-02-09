#include <Servo.h>

#define CW_CWW_PIN 10
#define PWM_PIN 11

void setup() {
  pinMode(CW_CWW_PIN, OUTPUT);
  pinMode(PWM_PIN, OUTPUT);
}

void loop() {
  digitalWrite(CW_CWW_PIN, HIGH);
  analogWrite(PWM_PIN, 200);
}
