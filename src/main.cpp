#include <Arduino.h>
#include <filters.h>
#include "pins.h"
#include "constants.h"
#include "utils.h"
#include <LiquidCrystal.h>
#include <NoDelay.h>

double x[nbPoints] = {299, 306, 333, 373, 445, 667, 1007};
double y[nbPoints] = {1, 2, 5, 10, 20, 50, 100};
double coeffs[2];
uint8_t calibrationIndex = 0;

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

void setupPWM16();
void analogWrite16(uint8_t pin, uint16_t val);

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

uint8_t buttonState = Btn::NONE;
uint8_t lastButtonState = Btn::NONE;
uint8_t selectedOption = 0;
uint16_t tareValue = 0;
Mode currentMode = Mode::MENU;
Coin countSelectedCoin = Coin::FIVE;

String options[] = {"Peser", "Compter", "Mise a zero", "Etalonnage"};
float coinWeights[] = {3.95, 1.75, 4.4, 6.27, 6.92};

noDelay updatePwmOutputTimer(5, updatePwmOutput);
noDelay updateWeightTimer(500, updateWeight);
noDelay updateCountTimer(500, updateCount);
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
      selectedOption = (selectedOption + 3) % 4;
    }
    else if (currentMode == Mode::COUNT)
    {
      countSelectedCoin = static_cast<Coin>((countSelectedCoin + 4) % 5);
    }
    break;

  case Btn::DOWN:
    if (currentMode == Mode::MENU)
    {
      selectedOption = (selectedOption + 1) % 4;
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
    }
    else if (currentMode == Mode::ETALONNAGE)
    {
      if (calibrationIndex < (nbPoints - 1))
      {
        x[calibrationIndex] = getCurrentAnalog();
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
    int optionIndex = (selectedOption + i) % 4;
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
  lcd.print(String(weight, 2));
  lcd.print(" g");
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
  tareValue = getCurrentAnalog();
}

void displayCalibration()
{
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Deposer: " + String(y[calibrationIndex], 0) + " g");
  lcd.setCursor(0, 1);
  lcd.print("puis -> SELECT");
}

int getCurrentAnalog()
{
  int rawCurrent = analogRead(currentReadingPin);
  float current = f2.filterIn(rawCurrent);
  return current;
}

float getWeight()
{
  int current = getCurrentAnalog() - tareValue;

  float weight = coeffs[0] * current + coeffs[1];
  
  return weight;
}

String getCount()
{
  float weight = getWeight();
  float coinWeight = coinWeights[static_cast<int>(countSelectedCoin)];
  // if the number is not a multiple of the coin weight, we return a string error
  int count = weight / coinWeight;

  if (fmod(weight, coinWeight) > 0.3 || count < 0)
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