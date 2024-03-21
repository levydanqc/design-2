#include <Arduino.h>
#include <curveFitting.h>

int readButtons()
{
  int adcKeyIn = analogRead(0);
  if (adcKeyIn < 50)
    return Btn::RIGHT;
  if (adcKeyIn < 250)
    return Btn::UP;
  if (adcKeyIn < 450)
    return Btn::DOWN;
  if (adcKeyIn < 650)
    return Btn::LEFT;
  if (adcKeyIn < 850)
    return Btn::SELECT;
  return Btn::NONE;
}

void setupPWM16()
{
  // Set PB1/2 as outputs.
  DDRB |= (1 << DDB5) | (1 << DDB6);

  TCCR1A =
      (1 << COM1A1) | (1 << COM1B1) |
      // Fast PWM mode.
      (1 << WGM11);
  TCCR1B =
      // Fast PWM mode.
      (1 << WGM12) | (1 << WGM13) |
      // No clock prescaling (fastest possible
      // freq).
      (1 << CS10);
  OCR1B = 0;
  // Set the counter value that corresponds to
  // full duty cycle. For 15-bit PWM use
  // 0x7fff, etc. A lower value for ICR1 will
  // allow a faster PWM frequency.
  ICR1 = 0xffff;
}

/* 16-bit version of analogWrite(). Works only on pins 9 and 10. */
void analogWrite16(uint8_t pin, uint16_t val)
{
  switch (pin)
  {
  case 12:
    OCR1B = val;
    break;
  }
}

void getCoefs(double *coeffs, double *x, double *y)
{
  fitCurve(1, nbPoints, x, y, 2, coeffs);

  Serial.print("Coeffs: ");
  Serial.print(coeffs[0], 4);
  Serial.print(", ");
  Serial.println(coeffs[1], 4);
}