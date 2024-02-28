#include <Arduino.h>
#include <filters.h>
#include "pins.h"
#include "constants.h"
#include <LiquidCrystal.h>

// Low-pass filter
Filter f(cutoff_freq, sampling_time, order);
Filter f2(cutoff_freq*10, sampling_time/10, order);

void setupPWM16();
int readButtons();
void handleButtonPress(int button);
void printMenu();
void clearLine(int line);
float measureMagneticField();
int getCurrentAnalog();
float getWeight();
String showCoinsCount(Coin coin);
void analogWrite16(uint8_t pin, uint16_t val);
void updatePwmOutput();

LiquidCrystal lcd(8, 9, 4, 5, 6, 7); // Initialize the LCD

int buttonState;
int lastButtonState = btnNONE;
Coin selectedCoin;
Mode currentMode = Mode::SELECT_MODE;
Mode lastMode = Mode::SELECT_MODE;
Mode cursor = Mode::WEIGHT_CHANGE;

void setup()
{
  Serial.begin(115200);
  pinMode(hallSensorPin, INPUT);
  pinMode(currentReadingPin, INPUT);
  pinMode(pwmOutputPin, OUTPUT);

  setupPWM16();
  lcd.begin(16, 2); // Set up the LCD's number of columns and rows
  lcd.print("Gantt Gang");
  delay(1000);
  lcd.clear();
  printMenu();
}

void loop()
{
  getWeight();
  updatePwmOutput();
  lastMode = currentMode;

  buttonState = readButtons();
  if (buttonState != lastButtonState)
  {
    handleButtonPress(buttonState);
    lastButtonState = buttonState;
  }

  if (lastMode != currentMode)
  {
    lcd.clear();
    lcd.setCursor(0, 0);
    switch (currentMode)
    {
    case WEIGHT_CHANGE:
      lcd.print("Peser piece(s)");
      // TODO: Implement weight coin logic
      break;

    case COUNT_CHANGE:
      lcd.print("Compter piece(s)");
      lcd.setCursor(0, 1);
      switch (selectedCoin)
      {
      case FIVE:
        lcd.print("0.05$");
        break;
      case TEN:
        lcd.print("0.10$");
        break;
      case TWENTY_FIVE:
        lcd.print("0.25$");
        break;
      case ONE:
        lcd.print("1.00$");
        break;
      case TWO:
        lcd.print("2.00$");
        break;
      }
      lcd.print(" -> ");
      showCoinsCount(selectedCoin);
      // TODO : show the number of coins

      break;

    case SELECT_MODE:
    default:
      printMenu();
      break;
    }
  }
}

int readButtons()
{
  int adcKeyIn = analogRead(0); // read the value from the sensor
  if (adcKeyIn < 50)
    return btnRIGHT;
  if (adcKeyIn < 150)
    return btnUP;
  if (adcKeyIn < 300)
    return btnDOWN;
  if (adcKeyIn < 500)
    return btnLEFT;
  if (adcKeyIn < 750)
    return btnSELECT;
  return btnNONE;
}

void handleButtonPress(int button)
{
  switch (button)
  {
  case btnUP:
  case btnDOWN:
    if (currentMode == SELECT_MODE)
    {
      cursor = (cursor == Mode::WEIGHT_CHANGE) ? Mode::COUNT_CHANGE : Mode::WEIGHT_CHANGE;
    }
    else if (currentMode == COUNT_CHANGE)
    {
      clearLine(1);
      selectedCoin = static_cast<Coin>((selectedCoin + (button == btnUP ? 1 : selectedCoin == 0 ? 4
                                                                                                : -1)) %
                                       5);
    }
    break;

  case btnSELECT:
    if (currentMode == SELECT_MODE)
    {
      currentMode = cursor;
    }
    else
    {
      currentMode = SELECT_MODE;
    }
    break
  case btnNONE:
  default:
    break;
  }
}

void printMenu()
{
  lcd.setCursor(0, 0);
  if (cursor == Mode::WEIGHT_CHANGE)
  {
    lcd.print("=> Peser");
    lcd.setCursor(0, 1);
    lcd.print("   Compter");
  }
  else
  {
    lcd.print("   Peser");
    lcd.setCursor(0, 1);
    lcd.print("=> Compter");
  }
}

void clearLine(int line)
{
  lcd.setCursor(0, line);
  lcd.print("                ");
}

void updatePwmOutput()
{
  int rawDist = analogRead(hallSensorPin);
  float dist = f.filterIn(rawDist);
  int error = dist - stablePosition;

  integral += error;
  double derivative = error - prevError;
  double derivative2 = derivative - prevprevError;
  int pwmOutput = Kp * error + Ki * integral + Kd * derivative + Kd2 * derivative2;
  pwmOutput = constrain(pwmOutput, 0, 65536);

  analogWrite16(pwmOutputPin, pwmOutput);

  prevprevError = prevError;
  prevError = error;
  // Serial.println(String(int(dist)) + ", " + String(pwmOutput));
}

int getCurrentAnalog()
{
  int rawCurrent = analogRead(currentReadingPin);
  float current = f2.filterIn(rawCurrent);
  return current;
}

float getWeight()
{
  int current = getCurrentAnalog();
  float weight;
  if (current < 350)
  {
    weight = (0.1255 * current - 36.484) + 3;
  } else
  {
    weight = 0.1387 * current - 41.066;
  }
  // Serial.println(String(current) + ", " + String(weight));
  // Serial.println(weight);
  Serial.println(weight);
  return weight;
}

String strCoinWeight(Coin coin)
{
  switch (coin)
  {
  case FIVE:
    return "8.00 g";
  case TEN:
    return "7.00 g";
  case TWENTY_FIVE:
    return "6.00 g";
  case ONE:
    return "5.00 g";
  case TWO:
    return "4.00 g";
  }
  return "error";
}

String showCoinsCount(Coin coin)
{
  switch (coin)
  {
  case FIVE:
    // if weight can be divided by weights[coin]
    // return weight / weight of coin
    // else return "error"
    break;
  case TEN:
    break;
  case TWENTY_FIVE:
    break;
  case ONE:
    break;
  case TWO:
    break;
  }
  return "error";
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