/*
Reads relative humidity from a BME280 sensor and sends the value over
the Arduino serial interface for data collection in Python.

Updated for a MOSFET control circuit using solenoid valves for automatic control of conditions inside chamber

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


State Machine Overview:

INITIAL
- Chamber conditions itself near the lower bound (~30% RH).
- If humidity is too low → humidify.
- If humidity is too high → dry.
- Once humidity is within startup window (28–32% RH) → go to HOLD.

HUMIDIFYING
- Opens wet solenoid valve.
- During startup conditioning: humidifies until chamber enters startup window.
- During experiment: humidifies from lower bound up to upper bound (30 → 40 RH).

DRYING
- Opens dry solenoid valve (N2 line).
- Lowers humidity until chamber enters startup window near lower bound.

HOLD
- Both valves closed.
- Chamber is stable near the lower bound.
- Waits for "START" command from Python to begin experiment.


Experiment Sequence:

1. Arduino powers on.
2. Chamber conditions itself to ~30% RH.
3. System enters HOLD state.
4. Python script sends "START".
5. Chamber humidifies from ~30 → 40 RH.
6. Valves close and system returns to HOLD.

Used for rapid humidity-shift chamber experiments studying
perovskite crystallization behavior.
*/

#include <Wire.h>
#include <Adafruit_sensor.h>
#include <Adafruit_BME280.h>

//Initialize to Sea level pressure in Tempe,AZ
#define SEALEVELPRESSURE_HPA 1015.24

Adafruit_BME280 bme;


// FSM states
enum States {
  INITIAL,
  HUMIDIFYING,
  DRYING,
  HOLD
};


// MOSFET Gate Pins for Arduino
const int WetSolenoidPin = 8;
const int DrySolenoidPin = 9;

// Experimental humidity bounds, change with each experiment
const float RH_Lower_Bound = 30.0;
const float RH_Upper_Bound = 40.0;

// Zones to initialize into the desired starting state
const float StartUpLow = RH_Lower_Bound - 2.0;
const float StartUpHigh = RH_Lower_Bound + 2.0;

States currentState = INITIAL;

// False = still just reaching the initial lower bound
// True = Experiment started
bool experimentStarted = false;







/*
Three functions to control FSM:
checkSerialCommand() -> Checks if Python communicates the start of experiment
updateState() -> State Transition logic function
applyOutputs() -> Actually controls the solenoids
*/

// Reads a command from Python script to signify if the experiment started
void checkSerialCommand() {
  if (Serial.available() > 0) {
    // Python script will be sending START with a \n modifier
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "START") {
      experimentStarted = true;
    }
  }
}

// Updates the FSM state based on humidity and experiment boolean
void updateState(float humidity) {
  switch (currentState) {
    case INITIAL:
      if (humidity < StartUpLow) {
        currentState = HUMIDIFYING;
      } else if (humidity > StartUpHigh) {
        currentState = DRYING;
      } else {
        currentState = HOLD;
      }
      break;

    case DRYING:
      // Dry until humidity is in startup zone near lower bound
      if (humidity >= StartUpLow && humidity <= StartUpHigh) {
        currentState = HOLD;
      }
      break;

    case HUMIDIFYING:
      if (!experimentStarted) {
        // Startup: humidify until humidity is near lower bound
        if (humidity >= StartUpLow && humidity <= StartUpHigh) {
          currentState = HOLD;
        }
      } else {
        // Experiment: Humidify until we get to the upper bound
        if
          if (humidity >= RH_Upper_Bound - 1) {
            currentState = HOLD;
            experimentStarted = false;
          }
      }
      break;

    case HOLD:
      // Wait here until Python sends START
      if (experimentStarted) {
        currentState = HUMIDIFYING;
      }
      break;
  }
}

// Sets solenoid outputs based on current state
void applyOutputs() {
  switch (currentState) {
    case INITIAL:
      digitalWrite(WetSolenoidPin, LOW);
      digitalWrite(DrySolenoidPin, LOW);
      break;

    case HUMIDIFYING:
      digitalWrite(WetSolenoidPin, HIGH);
      digitalWrite(DrySolenoidPin, LOW);
      break;

    case DRYING:
      digitalWrite(WetSolenoidPin, LOW);
      digitalWrite(DrySolenoidPin, HIGH);
      break;

    case HOLD:
      digitalWrite(WetSolenoidPin, LOW);
      digitalWrite(DrySolenoidPin, LOW);
      break;
  }
}




void setup() {
  //Starts Serial Log
  Serial.begin(9600);
  while (!Serial)
    ;

  pinMode(WetSolenoidPin, OUTPUT);
  pinMode(DrySolenoidPin, OUTPUT);

  digitalWrite(WetSolenoidPin, LOW);
  digitalWrite(DrySolenoidPin, LOW);

  //Starts the bme object from the 0x77 I2C address
  unsigned status = bme.begin(0x77);

  //Checks if BME280 is connected
  if (!status) {
    while (1) {
      // Stop forever if sensor is not found
    }
  }
}

void loop() {
  checkSerialCommand();

  float humidity = bme.readHumidity();

  updateState(humidity);
  applyOutputs();

  Serial.println(humidity);

  delay(500);
}
