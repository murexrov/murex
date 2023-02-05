#include <Servo.h>

Servo motor1;
int potentio1;
int speed1;

void setup() {
  //change motor pin here; default=3
  motor1.attach(3);
  Serial.begin(9600);
}

void loop() {
  //change potentiometer pin here; default=A0
  potentio1=analogRead(A0);
  speed1=map(potentio1,0,1023,0,180);
  motor1.write(speed1);
  Serial.println(speed1);
}
