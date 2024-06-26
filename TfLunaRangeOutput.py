######################################################
# Copyright (c) 2021 Maker Portal LLC
# Original Author: Joshua Hrisko
######################################################
#
# TF-Luna Mini LiDAR wired to a Raspberry Pi via UART
# --- testing the distance measurement from the TF-Luna
#
#
######################################################
# Modified by: James Brophy and Kaleb Nails
######################################################



import serial,time
import numpy as np
import csv
#
##########################
# TFLuna Lidar
##########################
#
ser = serial.Serial("/dev/serial0", 115200,timeout=0) # mini UART serial device
#
############################
# read ToF data from TF-Luna
############################
#
def read_tfluna_data():
    while True:
        counter = ser.in_waiting # count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = ser.read(9) # read 9 bytes
            ser.reset_input_buffer() # reset buffer

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                temperature = (temperature/8.0) - 256.0 # temp scaling and offset
                return distance/100.0,strength,temperature
distance_list = []
counter = 0
if ser.isOpen() == False:
    ser.open() # open serial port if not open
while counter<=200:
    
    distance,strength,temperature = read_tfluna_data() # read values
    distance_list.append(distance)
    print('Distance: {0:2.2f} m, Strength: {1:2.0f} / 65535 (16-bit), Chip Temperature: {2:2.1f} C'.\
                  format(distance,strength,temperature)) # print sample data
    time.sleep(.01)
    counter = counter +1
ser.close() # close serial port
print(distance_list)

filename ='output.csv'

with open(filename,mode='w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(distance_list)


