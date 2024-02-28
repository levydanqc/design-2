#include <Arduino.h>
#include <NewPing.h>
#define sensor A15 // Sharp IR GP2Y0A41SK0F (4-30cm, analog)

const int trigPin = 45;
const int echoPin = 44;
long microsecondsToMillimeters(long microseconds);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  /*
    SONAR
  */
  // long duration, mm;
  // pinMode(trigPin, OUTPUT);

  // digitalWrite(trigPin, LOW);
  // delayMicroseconds(2000);
  // digitalWrite(trigPin, HIGH);
  // delayMicroseconds(1000);
  // digitalWrite(trigPin, LOW);
  // pinMode(echoPin, INPUT);
  // duration = pulseIn(echoPin, HIGH);
  // // inches = microsecondsToInches(duration);

  // // cm = microsecondsToCentimeters(duration);
  // mm = microsecondsToMillimeters(duration);
  // // Serial.print(inches);
  // // Serial.print("in, ");
  // // Serial.print(cm);
  // // Serial.print("cm, ");
  // Serial.print(mm);
  // Serial.println(" mm");
  // // Serial.println();
  // delay(100);
  /*
  END OF SONAR
  */

  /*
    IR
  */
  // 5v
  float volts = analogRead(sensor) * 0.0048828125; // value from sensor * (5/1024)
  int distance = 13 * pow(volts, -1);              // worked out from datasheet graph
  delay(100);                                     // slow down serial port

  if (distance <= 30)
  {
    Serial.println(distance); // print the distance
  }
  /*
  END OF IR
  */
}

long microsecondsToInches(long microseconds)
{
  return microseconds / 74 / 2;
}
long microsecondsToCentimeters(long microseconds)
{
  return microseconds / 29 / 2;
}
long microsecondsToMillimeters(long microseconds)
{
  return microseconds / 2.9 / 2;
}