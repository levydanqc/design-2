int stablePosition = 400;
double error, integral = 0, prevError = 0, prevprevError = 0;
// double Kp = 0.0479325;
// double Ki = 0.363425;
// double Kd = 0.000040035;
// double Kd2 = 0.0000000032005;
double Kp = 8;
double Ki = .1;
double Kd = 0;
double Kd2 = 0;
    
const float cutoff_freq   = 1.5915;  //Cutoff frequency in Hz
const float sampling_time = 0.01; //Sampling time in seconds.
IIR::ORDER  order  = IIR::ORDER::OD1; // Order (OD1 to OD4)


enum Mode
{
    SELECT_MODE,
    WEIGHT_CHANGE,
    COUNT_CHANGE
};

enum Coin
{
    FIVE,
    TEN,
    TWENTY_FIVE,
    ONE,
    TWO
};