#include <Arduino.h>
#include <filters.h>
#include "pins.h"
#include "constants.h"
#include "utils.h"
#include <LiquidCrystal.h>
#include <NoDelay.h>

double x[nbPoints] = {231, 238, 245, 267, 306, 382, 600, 989};
double y[nbPoints] = {0, 1, 2, 5, 10, 20, 50, 100};
double coeffs[2];
uint8_t calibrationIndex = 0;

String options[] = {"Peser", "Compter", "Mise a zero", "Etalonnage", "Gramme <-> Once"};
float coinWeights[] = {3.85, 1.8, 4.4, 5.7, 6.55};

Filter f(cutoff_freq, sampling_time, order);
Filter f2(cutoff_freq * 10, sampling_time / 10, order);

int readButtons();
void handleButtonPress(int button);
void clearLine(int line);

int getCurrentAnalog();
float getWeight();
String getCount();

void updateButtons();
void updatePwmOutput();
void updateWeight();
void updateCount();

void displayMenu();
void displayWeight();
void displayCount();
void displayTare();
void displayCalibration();
void displayUnit();

void setupPWM16();
void analogWrite16(uint8_t pin, uint16_t val);

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

uint8_t buttonState = Btn::NONE;
uint8_t lastButtonState = Btn::NONE;
uint8_t selectedOption = 0;
float tareValue = 0;
Mode currentMode = Mode::MENU;
Coin countSelectedCoin = Coin::FIVE;
Unit currentUnit = Unit::GRAM;
// create queue for the last 5 weights
float lastWeights[5] = {0, 0, 0, 0, 0};

noDelay updatePwmOutputTimer(5, updatePwmOutput);
noDelay updateWeightTimer(300, updateWeight);
noDelay updateCountTimer(30, updateCount);
noDelay updateButtonsTimer(10, updateButtons);

void setup()
{
  Serial.begin(115200);
  pinMode(hallSensorPin, INPUT);
  pinMode(currentReadingPin, INPUT);
  pinMode(pwmOutputPin, OUTPUT);

  setupPWM16();
  lcd.begin(16, 2);
  lcd.print("Gantt Gang");
  delay(1000);
  lcd.clear();
  displayMenu();

  getCoefs(coeffs, x, y);
}

void loop()
{
  updatePwmOutputTimer.update();
  updateButtonsTimer.update();

  switch (currentMode)
  {
  case Mode::MENU:
    if (buttonState != lastButtonState && buttonState != Btn::NONE)
    {
      displayMenu();
    }
    break;

  case Mode::WEIGHT:
    if (buttonState != lastButtonState && buttonState != Btn::NONE)
    {
      displayWeight();
    }
    updateWeightTimer.update();
    break;

  case Mode::COUNT:
    if (buttonState != lastButtonState && buttonState != Btn::NONE)
    {
      displayCount();
    }
    updateCountTimer.update();
    break;

  case Mode::TARER:
    if (buttonState != lastButtonState && buttonState != Btn::NONE)
    {
      displayTare();
    }
    break;

  case Mode::ETALONNAGE:
    if (buttonState != lastButtonState && buttonState != Btn::NONE)
    {
      displayCalibration();
    }
    break;

  case Mode::UNIT:
    if (buttonState != lastButtonState && buttonState != Btn::NONE)
    {
      displayUnit();
    }
    break;

  default:
    break;
  }

  lastButtonState = buttonState;
}

void handleButtonPress(int button)
{
  switch (button)
  {
  case Btn::UP:
    if (currentMode == Mode::MENU)
    {
      selectedOption = (selectedOption + (options->length() - 1)) % options->length();
    }
    else if (currentMode == Mode::COUNT)
    {
      countSelectedCoin = static_cast<Coin>((countSelectedCoin + 4) % 5);
    }
    break;

  case Btn::DOWN:
    if (currentMode == Mode::MENU)
    {
      selectedOption = (selectedOption + 1) % options->length();
    }
    else if (currentMode == Mode::COUNT)
    {
      countSelectedCoin = static_cast<Coin>((countSelectedCoin + 1) % 5);
    }
    break;

  case Btn::SELECT:
    if (currentMode == Mode::MENU)
    {
      currentMode = static_cast<Mode>(selectedOption + 1);
      if (currentMode == Mode::WEIGHT)
      {
        updateWeight();
      }
    }
    else if (currentMode == Mode::ETALONNAGE)
    {
      if (calibrationIndex < (nbPoints - 1))
      {
        int current = getCurrentAnalog();
        x[calibrationIndex] = current;
        calibrationIndex++;
      }
      else
      {
        getCoefs(coeffs, x, y);
        calibrationIndex = 0;
        currentMode = Mode::MENU;
      }
    }
    else
    {
      currentMode = Mode::MENU;
    }
    break;

  case Btn::NONE:
  case Btn::LEFT:
  case Btn::RIGHT:
  default:
    break;
  }
}

void updateButtons()
{
  buttonState = readButtons();

  if (buttonState != lastButtonState && buttonState != Btn::NONE)
  {
    handleButtonPress(buttonState);
  }
}

void displayMenu()
{
  lcd.clear();
  lcd.setCursor(0, 0);

  for (int i = 0; i < 2; ++i)
  {
    int optionIndex = (selectedOption + i) % options->length();
    lcd.print((i == 0) ? ">" : " ");
    lcd.print(options[optionIndex]);
    lcd.setCursor(0, i + 1);
  }
}

void displayWeight()
{
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Masse: ");
  clearLine(1);
}

void updateWeight()
{
  lcd.setCursor(0, 1);
  float weight = getWeight();

  String  weightStr = String(weight, 1);
  uint8_t nbDigits = weightStr.indexOf('.');
  if (nbDigits == 2)
  {
    weightStr = " " + weightStr;
  }
  else if (nbDigits == 1)
  {
    weightStr = "  " + weightStr;
  }

  lcd.print(weightStr);
  lcd.print((currentUnit == Unit::GRAM) ? " g" : " oz");
}

void displayCount()
{
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Quantite: ");
  lcd.setCursor(0, 1);
  switch (countSelectedCoin)
  {
  case Coin::FIVE:
    lcd.print("0.05$");
    break;
  case Coin::TEN:
    lcd.print("0.10$");
    break;
  case Coin::TWENTY_FIVE:
    lcd.print("0.25$");
    break;
  case Coin::ONE:
    lcd.print("1.00$");
    break;
  case Coin::TWO:
    lcd.print("2.00$");
    break;
  default:
    break;
  }
  lcd.print(" -> ");
}

void updateCount()
{
  lcd.setCursor(9, 1);
  lcd.print("       ");
  lcd.setCursor(9, 1);
  lcd.print(getCount());
}

void displayTare()
{
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Mise a zero");
  lcd.setCursor(0, 1);
  lcd.print("effectuee");
  tareValue += getWeight();
  Serial.println("Tared! : " + String(tareValue));
}

void displayCalibration()
{
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Deposer: " + String(y[calibrationIndex], 0) + " g");
  lcd.setCursor(0, 1);
  lcd.print("puis -> SELECT");
}

void displayUnit()
{
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Nouvelle unite:");
  currentUnit = static_cast<Unit>((currentUnit + 1) % 2);
  lcd.setCursor(0, 1);
  lcd.print((currentUnit == Unit::GRAM) ? "Gramme" : "Once");
}

int getCurrentAnalog()
{
  int rawCurrent = analogRead(currentReadingPin);
  // int current = f2.filterIn(rawCurrent);
  return rawCurrent;
}

float getWeight()
{
  int current = getCurrentAnalog();

  float weight = coeffs[0] * current + coeffs[1];

  if (currentUnit == Unit::POUND)
  {
    weight *= 0.035274;
  }
  return weight - tareValue;
}

String getCount()
{
  float weight = getWeight();
  float coinWeight = coinWeights[static_cast<int>(countSelectedCoin)];
  // if the number is not a multiple of the coin weight, we return a string error
  int count = weight / coinWeight;

  if (fmod(weight, coinWeight) > 0.55 || count < 0)
  {
    return "N/A";
  }

  return String(count);
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
  int pwmOutput = Kp * error + Ki * integral + Kd * derivative;
  pwmOutput = constrain(pwmOutput, 0, 65536);

  analogWrite16(pwmOutputPin, pwmOutput);

  prevError = error;
}
