"""
Humidity logging script for rapid humidity-shift chamber experiments.

Reads relative humidity values from an Arduino + BME280 sensor over serial,
logs humidity vs time, plots the humidity profile, and saves experiment data
to a timestamped CSV file for later analysis.

Used for my Spring 2026 Research project on studying the effects of Rapid Humidity Shifts
on MAPI(Methylammonium Phosphate Iodide) perovskite solar cells
"""

import serial
import time
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


# Returns the Humidity valuves from the BME 280 and the time when those values were taken
# comport is the dedicated port for the arduino
# baudrate is the Serial frequency, which from the C++ code we have chosen 9600
def RH_List(comport, baudrate,runtime):
    RH_values = []
    T_values = []
    starttime = time.time()
    elapsedtime = 0

    # Creates a arduino object that is connected with the serial output 
    # Samples at the defined frqeuency from the selected comport
    # Waits until requested bytes are read, or 1 second

    arduino = serial.Serial(comport,baudrate, timeout=1) 

    # Gives 2 seconds to establish connection

    time.sleep(2) 
    print("Serial is connected to Arduino!")

    
    while elapsedtime < runtime:
        # Reads raw data from serial port, and decodes into a strong
        raw_data = arduino.readline().decode('utf-8')
        raw_data = raw_data.strip()


        current_time = time.time()
        elapsedtime = current_time - starttime

        # Appends RH and time values at the same time to sync entries
        if raw_data != "":
            RH = float(raw_data)
            RH_values.append(RH)
            T_values.append(elapsedtime)

    arduino.close()
    
    return RH_values, T_values


# Calculates the change in RH in a given time
def RH_change(RH_v,seconds):
    if RH_v == []:
        return None
    return (max(RH_v)-min(RH_v)) / seconds


# Plots Humidity vs Time Graph
def plotRH(T_values,RH_values):
    plt.plot(T_values,RH_values, marker = 'o', color = 'blue')
    plt.xlabel("Time(s)")
    plt.ylabel("RH Value(%)")
    plt.title("Chamber Humidity vs Time Graph")
    plt.grid(True)
    plt.show()


# Exports Humidity vs Time values into a CSV using Pandas
def saveValues(T_values,RH_values):
    values = {"Time (s)": T_values, "RH (%)": RH_values}
    df = pd.DataFrame(values)
    filename = "RH_Run" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    df.to_csv(filename, index = False)

