#include <QTRSensors.h>

#define NUM_SENSORS   8     // number of sensors used
#define TIMEOUT       2500  // waits for 2500 microseconds for sensor outputs to go low
#define EMITTER_PIN   2     // emitter is controlled by digital pin 2

const int analogInPin0 = A0; //left encoder input
const int analogInPin1 = A1; //right encoder input
const int OutPin0 = A2; // out pin for left encoder
const int OutPin1 = A3;  // out pin for right encoder
const int RadioEnablePin = 8; // radio pin
const int Jumper = A5; // pin number the jumper is conected to

// sensors 0 through 7 are connected to digital pins 3 through 10, plus 12 respectively
QTRSensorsRC qtrrc((unsigned char[]) {
  3, 4, 5, 6, 7, 9, 10, 12
}, NUM_SENSORS, TIMEOUT, EMITTER_PIN);
unsigned int sensorValues[NUM_SENSORS];

int sensorValue0 = 0;
int sensorValue1 = 0;
int count0 = 0;
int count1 = 0;
int val = 0;


bool lastValue0 = false;
bool lastValue1 = false;
bool Value0 = false;
bool Value1 = false;
bool newValue0 = false;
bool newValue1 = false;
bool lineFlag = false; // if line jumper not fitted line will be flase.

void setup() {
  count0 = 0;
  count1 = 0;

  // define output pins for encoder input, output plus radio enable.
  pinMode(13, OUTPUT);   // initialize pin 13 as digital output (LED)
  pinMode(RadioEnablePin, OUTPUT); // initialize pin to control the radio
  pinMode(OutPin0, OUTPUT); // initialize pin 2 as an output to signal change of A0 status
  pinMode(OutPin1, OUTPUT); // initialize pin 3 as an output to signal change of A1 status
  pinMode(Jumper, INPUT_PULLUP);

  // Enable radio and start the serial link

  digitalWrite(RadioEnablePin, HIGH); // turn on the radio if set to HIGH, LOW is off.
  Serial.begin(115200);    // start the serial port at 115200 baud
  delay(1);

  // setup & calibrat line following sensors if jumper is fitted
 
  if (digitalRead(Jumper)) {
    Serial.println("line following selected");
    Serial.println("Starting Line Calibration");
    delay(500);
    pinMode(13, OUTPUT);
    digitalWrite(13, HIGH);    // turn on Arduino's LED to indicate we are in calibration mode
    for (int i = 0; i < 400; i++)  // make the calibration take about 10 seconds
    {
      qtrrc.calibrate();       // reads all sensors 10 times at 2500 us per read (i.e. ~25 ms per call)
    }
    digitalWrite(13, LOW);     // turn off Arduino's LED to indicate we are through with calibration

    // print the calibration minimum values measured when emitters were on
    
    for (int i = 0; i < NUM_SENSORS; i++)
    {
      Serial.print(qtrrc.calibratedMinimumOn[i]);
      Serial.print(' ');
    }
    Serial.println();

    // print the calibration maximum values measured when emitters were on
    for (int i = 0; i < NUM_SENSORS; i++)
    {
      Serial.print(qtrrc.calibratedMaximumOn[i]);
      Serial.print(' ');
    }
    Serial.println();
    Serial.println();
    delay(1000);
    lineFlag = true;
    Serial.println("finished line calibration");
  }
  else {
    Serial.println("Motor Counters started");
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if (!lineFlag) {
    // read the analog in value:
    sensorValue0 = analogRead(analogInPin0);
    sensorValue1 = analogRead(analogInPin1);


    if (sensorValue0 > 600) {

      Value0 = true;
    }
    else {
      Value0 = false;
    }

    if (sensorValue1 > 700) {

      Value1 = true;
    }
    else {
      Value1 = false;
    }

    if (Value0 != lastValue0) {

      count0 = count0 + 1;
      lastValue0 = Value0;
      newValue0 = true;
    }

    if (Value1 != lastValue1) {

      count1 = count1 + 1;
      lastValue1 = Value1;
      newValue1 = true;
    }
    if (newValue0 || newValue1) {
      Serial.println(String(count0) + " " + String(count1));

    }
    if (newValue0) {
      //Serial.println(String(count0) + " " + String(count1));
      //Serial.println("l: " + String(sensorValue0) +" r: " + String(sensorValue1));
      //Serial.println("Sensor left: " + String(sensorValue0) +" Sensor right: " + String(sensorValue1));
      newValue0 = false;
      if (digitalRead(OutPin0)) {
        digitalWrite(OutPin0, LOW);
      }
      else {
        digitalWrite(OutPin0, HIGH);

      }
    }


    if (newValue1) {
      //Serial.println(String(count0) + " " + String(count1));
      //Serial.println("l: " + String(sensorValue0) +" r: " + String(sensorValue1));
      //Serial.println("Sensor left: " + String(sensorValue0) +" Sensor right: " + String(sensorValue1));
      newValue1 = false;
      if (digitalRead(OutPin1)) {
        digitalWrite(OutPin1, LOW);
      }
      else {
        digitalWrite(OutPin1, HIGH);

      }
    }

    delayMicroseconds(1);
  }
  else {
    // read calibrated sensor values and obtain a measure of the line position from 0 to 5000
    // To get raw sensor values, call:
    //  qtrrc.read(sensorValues); instead of unsigned int position = qtrrc.readLine(sensorValues);
    unsigned int position = qtrrc.readLine(sensorValues);

    // print the sensor values as numbers from 0 to 1000, where 0 means maximum reflectance and
    // 1000 means minimum reflectance, followed by the line position
    /*
    for (unsigned char i = 0; i < NUM_SENSORS; i++)
    {
      Serial.print(sensorValues[i]);
      Serial.print('\t');
    }
    */
    //Serial.println(); // uncomment this line if you are using raw values
    Serial.println(position); // comment this line out if you are using raw values

    delay(10);

  }
}

