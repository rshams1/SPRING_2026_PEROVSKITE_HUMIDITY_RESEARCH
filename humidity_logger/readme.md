# Rapid Humidity Shift Chamber Logger

This project was built to study the effects of rapidly changing humidity during the spin-coating process of perovskite solar cells.

Humidity strongly affects perovskite crystallization. Instead of keeping humidity constant, this setup allows rapid shifts between humid and dry conditions during film formation. The goal is to study how different humidity ranges and transitions influence film formation and device performance.

To verify the actual humidity profile inside the chamber during each experiment, an Arduino and BME280 humidity sensor are used to record relative humidity in real time.

---

## Experimental Setup

The humidity chamber consists of:

- **18 × 18 × 18 inch acrylic enclosure** (1/4 inch thick walls)
- **Humidifier** used to increase humidity
- **Dry nitrogen (N₂)** used to rapidly reduce humidity
- **Arduino + BME280 humidity sensor** used to measure humidity inside the chamber

By adjusting humidifier output and N₂ flow, humidity inside the chamber can be rapidly shifted between different ranges during spin-coating experiments.

The humidity logger records the humidity vs time profile for each run so that experimental conditions can be verified and compared.

---

## Hardware

- Arduino Uno R4 Minima  
- BME280 humidity sensor (I2C)  
- Acrylic humidity chamber  
- Humidifier for humidity increase  
- Nitrogen gas line for humidity reduction  

### BME280 Wiring

SCL → A5  
SDA → A4  
VIN → 5V  
GND → GND  

---

## Software Overview

### Arduino Firmware

`humidity_logger.ino`

The Arduino reads relative humidity from the BME280 sensor and sends the value over serial.

Each humidity value is printed on its own line so it can be easily parsed by the Python script.

Example serial output:

43.21
43.10
42.95
42.87


---

### Python Logger

`humidity_logger.py`

The Python script performs the following:

- reads humidity data from the Arduino through the serial port
- records humidity values and elapsed time
- plots humidity vs time
- saves the data from each run to a CSV file

Each run is automatically saved using a timestamped filename.

Example:
RH_Run2026-03-13_16-42-51.csv


CSV contents:

| Time (s) | RH (%) |
|---------|--------|
| 0.00 | 42.8 |
| 0.50 | 43.1 |
| 1.00 | 43.0 |

---

## Python Dependencies

Install required libraries:

``` 
pip install pyserial
pip install pandas
pip install matplotlib
```



---

## Running the Logger

1. Upload the Arduino firmware to the board.
2. Connect the Arduino to your computer.
3. Update the Python script with the correct serial port.
4. Run the Python script.

The script will:

- collect humidity data for the selected runtime
- generate a humidity vs time plot
- automatically save the run data as a CSV file

---

## Purpose

During spin-coating experiments the chamber humidity does not change instantly when switching between humidified air and dry nitrogen.

This logging system was built to measure the actual humidity profile inside the chamber during experiments. The recorded humidity curves allow comparison between different humidity ranges and help verify experimental conditions.

The humidity data can then be correlated with perovskite film formation and device performance.

---

## Possible Future Improvements

- closed-loop humidity control using solenoid valves
- integration with spin-coater timing
- automated experiment logging
