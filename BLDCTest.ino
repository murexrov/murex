#define CW_CWW_PIN 10
#define PWM_PIN 11

long pwm = 0;

void setup() {
  Serial.begin(115200);
  pinMode(CW_CWW_PIN, OUTPUT);
  pinMode(PWM_PIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    //input speed, must be int between -255 and 255
    //-255 = max speed backward; 0 = stop; 255 = max speed forward
    pwm=Serial.parseInt();
    if (pwm<0 && pwm>=-255) {
      digitalWrite(CW_CWW_PIN, LOW);
      //actual pwm: 0 = max speed; 255 = stop
      analogWrite(PWM_PIN, 255+pwm);
    }
    else if (pwm>=0 && pwm<=255) {
      digitalWrite(CW_CWW_PIN, HIGH);
      //actual pwm: 0 = max speed; 255 = stop
      analogWrite(PWM_PIN, 255-pwm);
    }
    else {
      Serial.println("INVALID SPEED");
    }
    delay(200);
  }
}
