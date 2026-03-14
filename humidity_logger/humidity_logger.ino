/*
Reads relative humidity from a BME280 sensor and sends the value over
the Arduino serial interface for data collection in Python.

Hardware:
Arduino Uno R4
BME280 humidity sensor (I2C)

Connections:
SCL -> A5
SDA -> A4
VIN -> 5V
GND -> GND

Output format:
One humidity value per line (RH %)
Sampling at 2Hz

Used for rapid humidity-shift chamber experiments studying
perovskite crystallization behavior.
*/


#include <Wire.h>
#include <Adafruit_sensor.h>
#include <Adafruit_BME280.h>


//Initialize to Sea level pressure in Tempe,AZ
#define SEALEVELPRESSURE_HPA 1015.24

Adafruit_BME280 bme;



void setup() {
  //Starts Serial Log
  Serial.begin(9600);
  while (!Serial);
  
  //Starts the bme object from the 0x77 I2C address
  unsigned status;
  status = bme.begin(0x77);


  //Checks if BME280 is connected
  if (!status) {
    Serial.println("BME280 Sensor not found");
    while(1);
  }

  Serial.println("BME280 initialized.");


}

void loop() {
  Serial.println(bme.readHumidity());
  delay(500);


}


