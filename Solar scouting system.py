# import all the necessary libraries 

from machine import Pin, I2c, ADC       # pin modules control pins on raspberry pi 
                                        # I2c to control communication protocol 
                                        # Anolgue to digital converter: to control signals coming form the solar panel 
import utime        # to control the time in the programm 
import icd_api      # to control the LCD
from pico_i2c_Lcd import i2cLcd   # to control the LCD

import threading 

# set the i2c for the lcd screen 
i2c = I2c(0, scl=Pin(1), sda=Pin(0), freq = 4000000)
                        
# create an adress for the lcd 
lcd = I2cLcd(i2c, 0x27, 2, 16)

# set up the ADC to pin 26
adc = ADC(Pin(26))
verf = 3.3                   # The maximum voltage the adc can read 
adc_resolution = 65535           # The range of value or differnet levels the adc can read/output 

# list to store the timestamp and voltage data or reading 
timestamp = []
voltage = []

# Function to calculate voltage 
def calculate_voltage ():
    raw_value = adc.read_u16()                            # getting raw_value from adc (a number between 0 and 65,535)
    voltage = (raw_value / adc_resolution)*verf           # converting the raw_value to voltage (a number between 0 and 3.3)
    return voltage

def main():
    while True:
        voltage = calculated_voltage          # store the calculated voltage from solar panel 
        lcd.clear()                           # Clear the lcd 
        lcd.putstr("voltage:{:2f}v")          # to show data on lcd 
                                     # get the current timestamp 
        timestamp = utime.localtime()
        timestamp_str = "{:04b}-{:02b}-{:02b} {:02b}:{:02b}:{:02b}".format(timestamp[0], timestamp[1], timestamp[2],
                                                                           timestamp[3], timestamp[4], timestamp[5])
        print("timestamp: {}, voltage: {:.2f}v".format(timestamp_str, voltage))
        
        # store voltage reading in a csv file
        
        data_file = open("voltage_data_csv", "w")
        data_file.write("timestamp, voltage\n")
        
        # Write the voltage and timestamp to the file at a regular interval
        
        interval = 100 
        
        def every_interval():
            data_file.write("{}, {:.2f}\n.formart(timestamp_str, voltage)")
            data_file.flush()       # ensure data is written to the file
            
        # Start the interval
        def start_interval():
            every_interval()  # Initial call
            threading.Timer(interval / 1000, start_interval).start()

        # Start the interval loop
        start_interval()
        
        # wait for 1 second b4 reading the voltage
        utime.sleep(1)
        
        led = Pin(5, Pin.out)
        
        # turn on the LED
        led.value(1)
        
        utime.sleep(2)
         
        # turn off the led
        led.value(0)
        
        utime.sleep(2)
main()  # call the "main" function for the programm to run

try:
    main()
except KeyboardInterrupt:
    data_file.close()   # close the datafiles when the programm is interrupted
    print("data_file closed")