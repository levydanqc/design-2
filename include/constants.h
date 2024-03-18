int stablePosition = 400;
double error, integral = 0, prevError = 0;
double Kp = 8;
double Ki = .1;
double Kd = 0;

const float cutoff_freq   = 1.5915;  //Cutoff frequency in Hz
const float sampling_time = 0.01; //Sampling time in seconds.
IIR::ORDER  order  = IIR::ORDER::OD1; // Order (OD1 to OD4)

#define nbPoints 8

enum Mode
{
    MENU,
    WEIGHT,
    COUNT,
    TARER,
    ETALONNAGE
};

enum Coin
{
    FIVE,
    TEN,
    TWENTY_FIVE,
    ONE,
    TWO
};

enum Btn
{
    RIGHT,
    UP,
    DOWN,
    LEFT,
    SELECT,
    NONE
};