'''This is a script to automatically control the fans of my Raspberry Pi mini-PC build.
If you find this useful somehow, feel free to use the code.
Copyrights: MrMadsenMalmo 2015
'''

import re
from sys import exit
import os

try:
    import RPi.GPIO as GPIO
except ImportError:
    exit("Could not locate RPi library")



class FanControl:
    def setPins(self):
        """Set up the pins, as of now I will use GPIO.BCM"""
        
        GPIO.cleanup()
    
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        self.fanAuto = 26  # This will be used to determine whether auto mode is wanted or not
        
        self.tempLights = [18, 23, 24]  # 18 = low, 23 = med, 24 = hot
        
        GPIO.setup(self.fanAuto, GPIO.IN)  # reads from the fanAuto pin
        GPIO.setup(self.tempLights, GPIO.OUT)  # sets these pins to output
        
        print "Pins are set"
    
    def getTemp(self):
        os.system("/opt/vc/bin/vcgencmd measure_temp >> readTemp.txt")
        
        with open(readTemp.txt) as file:
            content = file.read()
            
            self.temperature = re.search("temp\=([\d\.]+)\'C", content, re.VERBOSE|re.MULTILINE)
            return self.temperature
        
    
    def setTemp(self, mode=False):
        """Set the temperatures (temp) either automatically or manually with user input"""

        if mode:
            validInput = False

            while not validInput:
                try:
                    self.temp1 = int(raw_input("Input first temp. level:  "))
                    self.temp2 = int(raw_input("Input second temp. level:  "))
                    self.temp3 = int(raw_input("Input third temp. level:  "))
                except ValueError:
                    print "Invalid input, try again."
                    continue

                validInput = True
                print "Temperatures set."
                print "Temp 1:", self.temp1
                print "Temp 2:", self.temp2
                print "Temp 3:", self.temp3
        else:
            self.temp1 = 35
            self.temp2 = 45
            self.temp3 = 60
            
            print "Temperatures set."
            print "Temp 1:", self.temp1
            print "Temp 2:", self.temp2
            print "Temp 3:", self.temp3
    
    def __init__(self):
        useDefault = raw_input("Would you like to set the temperatures manually? y/n\n")

        if len(useDefault.strip()) == 0 or useDefault.strip().lower() == "n":
            self.setTemp()
        else:
            self.setTemp(True)
            
        self.setPins()
        
        self.tempTemp = self.getTemp()
        print self.tempTemp

Control = FanControl()