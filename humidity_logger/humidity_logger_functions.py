"""
Humidity logging script for rapid humidity-shift chamber experiments.

Reads relative humidity values from an Arduino + BME280 sensor over serial,
logs humidity vs time, plots the humidity profile, and saves experiment data
to a timestamped CSV file for later analysis.

Used for my Spring 2026 Research project on studying the effects of Rapid Humidity Shifts
on MAPI(Methylammonium Lead Iodide) perovskite solar cells
"""

import serial
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import math
from datetime import datetime


# Returns the Humidity valuves from the BME 280 and the time when those values were taken
# comport is the dedicated port for the arduino
# baudrate is the Serial frequency, which from the C++ code we have chosen 9600
# Allows for Live Monitoring of RH Values if given a target_low and target_high 
# Added Functionality for sample period, samples at given value in seconds
def RH_List(comport, baudrate, runtime, target_low=None, target_high=None,sample_period=0.5):
    RH_values = []
    T_values = []
    

    # Creates a arduino object that is connected with the serial output 
    # Samples at the defined frqeuency from the selected comport
    # Waits until requested bytes are read, or 1 second
    arduino = serial.Serial(comport, baudrate, timeout=1)

    time.sleep(2)
    print("Serial is connected to Arduino!")

    target_reached = False
    latest_RH = None

    starttime = time.time()
    next_sample_time = 0.0


    while True:
        elapsedtime = time.time() - starttime
        if elapsedtime >= runtime:
            break

        # Reads raw data from serial port, and decodes into a strong
        raw_data = arduino.readline().decode('utf-8', errors='ignore').strip()


        if raw_data != "":
            try:
                RH = float(raw_data)
                latest_RH = RH
            except ValueError:
                print(f"Skipped non-numeric line: {raw_data}")
                continue

            
            
            
            # Makes a optional choice of live monitoring
            # Provides a alert if RH exceeds or is lower than target_low or target_high
            if latest_RH is not None and elapsedtime >= next_sample_time:
                RH_values.append(latest_RH)
                T_values.append(round(next_sample_time, 2))

                if target_low is not None and target_high is not None:
                    if latest_RH < target_low:
                        status = "TOO LOW"
                        target_reached = False
                    elif latest_RH > target_high:
                        status = "TOO HIGH"
                        target_reached = False
                    else:
                        status = "IN TARGET"
                        if not target_reached:
                            print("\n*** TARGET RH REACHED ***\n")
                            target_reached = True

                    print(f"Time: {next_sample_time:.2f}s | RH: {latest_RH:.2f}% | {status}")
                else:
                    print(f"Time: {next_sample_time:.2f}s | RH: {latest_RH:.2f}%")

                next_sample_time += sample_period


    arduino.close()

    return RH_values, T_values


# Returns the average rate of humidity change in RH% per second
def RH_change(RH_v,seconds):
    if RH_v == []:
        return None
    return (max(RH_v)-min(RH_v)) / seconds


# Plots Humidity vs Time Graph
def plotRH(T_values,RH_values):
    RH_smooth = exponential_smoothing(RH_values, alpha=0.1)
    RH_filtered = deadband_filter(RH_smooth, threshold=0.25)

    plt.plot(T_values,RH_filtered, marker = 'o', color = 'blue')
    plt.xlabel("Time(s)")
    plt.ylabel("RH Value(%)")
    plt.title("Chamber Humidity vs Time Graph")
    plt.grid(True)
    plt.show()

# Smooths Noisy humidity reading
def exponential_smoothing(data, alpha=0.2):
    smoothed = [data[0]]
    for i in range(1, len(data)):
        smoothed.append(alpha * data[i] + (1 - alpha) * smoothed[i-1])
    return smoothed

# Implements a deadband to filter out changes of less than the threshold
def deadband_filter(data, threshold=0.05):
    filtered = [data[0]]

    for i in range(1, len(data)):
        if abs(data[i] - filtered[-1]) < threshold:
            filtered.append(filtered[-1])  # hold value
        else:
            filtered.append(data[i])

    return filtered

# Exports Humidity vs Time values into a CSV using Pandas
def saveValues(T_values, RH_values):
    values = {"Time (s)": T_values, "RH (%)": RH_values}
    df = pd.DataFrame(values)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "Data")

   

    os.makedirs(folder, exist_ok=True)


    filename = "RH_Run_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    filepath = os.path.join(folder, filename)

    df.to_csv(filepath, index=False)



def main():
    RH_Values, T_values = RH_List("/dev/cu.usbmodem101", 9600,10,40,57.5)
    plotRH(T_values,RH_Values)
    saveValues(T_values,RH_Values)

if __name__ == '__main__':
    main()


