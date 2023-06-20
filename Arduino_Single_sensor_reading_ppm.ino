/*
This is for CO-B4 162381201
*/
#include <Wire.h>              // include Arduino wire library (required for I2C devices)
#include <Adafruit_BMP280.h>   // include Adafruit library for BMP280 sensor
#define BMP280_I2C_ADDRESS  0x76
Adafruit_BMP280  bmp280;
#include <SPI.h>
#include <SD.h>
float t;
float V1;
float V2;
float sensorVal_1;
float sensorVal_2;

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
}
void loop() {
  t = millis()/1000.0;
  // make a string for assembling the data to log:
  //String dataString = "";

  // read three sensors and append to the string:
//  for (int analogPin = 0; analogPin < 5; analogPin++) {
//    int sensor = (analogRead(A(analogPin)))*(5/1023);
//    dataString += String(sensor);
//    if (analogPin < 4) {
//      dataString += ",";
//    }
//  }

  sensorVal_1 = analogRead(A0);
  sensorVal_2 = analogRead(A1);
//Depending on 5.0V or3.3V change the vlotage value 
  V1 = sensorVal_1 * (5.0/1023.0);
  V2 = sensorVal_2 * (5.0/1023.0);
  PPM = ((Alpha3OP1 - 0.352) + * (Alpha3OP2 - 0.361)) / 0.439 * 1000;

    // print to the serial port too:
    //Serial.println(dataString);
    Serial.println(PPM) ;
}
