#include <Servo.h>

Servo servo;

const int SERVO_PIN = 9;
int currentAngle = 0;

void setup() {
  servo.attach(SERVO_PIN);
  servo.write(0);      // make sure it starts stopped
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    if (line.length() > 0) {
      // Expect "<desired_angle>,<current_angle>" format
      int desiredAngle = line.toInt();

      if (desiredAngle > currentAngle) {
        while (desiredAngle > currentAngle) {
          currentAngle++;
          servo.write(currentAngle);
          delay(5);
        }
      } else if (desiredAngle < currentAngle) {
        while (desiredAngle < currentAngle) {
          currentAngle--;
          servo.write(currentAngle);
          delay(5);
        }
      }        
    }
  }

}
