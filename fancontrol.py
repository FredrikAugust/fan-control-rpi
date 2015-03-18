'''This is a script to automatically control the fans of my Raspberry Pi mini-PC build.
If you find this useful somehow, feel free to use the code.
Copyrights: MrMadsenMalmo 2015
'''

import re
from sys import exit
import os
from time import sleep
import datetime

try:
    import RPi.GPIO as GPIO
except ImportError:
    exit("Could not locate RPi library")


def clearScreen():
    os.system("clear")



class FanControl:
    def powerLights(self, temperature):
        """Simple program that flashes each light, turns off all the lights,
        and then lights up a light depending on the temperature of the Raspberry Pi
        """

        for light in self.tempLights:
            GPIO.output(light, 1)
            sleep(1)
            GPIO.output(light, 0)

        if temperature >= self.temp1 and self.temp1 < self.temp2:
            GPIO.output(self.tempLights[0], 1)
        elif temperature >= self.temp2 and self.temp2 < self.temp3:
            GPIO.output(self.tempLights[1], 1)
        elif temperature >= self.self.temp3:
            GPIO.output(self.tempLights[2], 1)

    def fanPower(self, temperature):
        """This turns on or off the fan depending on the heat of the Raspberry Pi
        The fan is running a 5v current, so I will use a transistor that is controlled
        with a 3.3v current + 1k ohm resistor.
        """

        self.fanPin = 4

        if temperature >= self.temp3:
            GPIO.output(self.fanPin, 1)
        else:
            GPIO.output(self.fanPin, 0)


    def setPins(self):
        """Set up the pins, as of now I will use GPIO.BCM"""
        
        GPIO.setwarnings(False)
        
        GPIO.cleanup()
    
        GPIO.setmode(GPIO.BCM)
        
        self.fanAuto = 26  # This will be used to determine whether auto mode is wanted or not
        self.tempLights = [18, 23, 24]  # 18 = low, 23 = med, 24 = hot
        
        GPIO.setup(self.fanAuto, GPIO.IN)  # reads from the fanAuto pin
        
        for tempLight in self.tempLights:
            GPIO.setup(tempLight, GPIO.OUT)  # sets these pins to output
        
        print "Pins are set"
    
    def getTemp(self):
        """Create a file from the result of a command that gets the system temp
        Then reads it using with 'with'
        """
        
        os.system("/opt/vc/bin/vcgencmd measure_temp >> readTemp.txt")
        
        with open("readTemp.txt") as file:
            content = file.read()
            
            self.temperature = re.search("temp\=(?P<temp>[\d\.]+)\'C", content, re.VERBOSE|re.MULTILINE)
            return float(self.temperature.group('temp'))
        
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
            self.temp2 = 40
            self.temp3 = 50
            
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



class Program:
    def Main(self):
        clearScreen()

        self.temperatureControl = FanControl()
        prevTemp = 0

        while True:
            self.currentTemp = self.temperatureControl.getTemp()

            if self.currentTemp != prevTemp:
                self.temperatureControl.powerLights(self.currentTemp)
                self.temperatureControl.fanPower(self.currentTemp)

                print "Fan speed and lights updated"

            print "Temperature:", self.currentTemp  # for debugging purposes, will probably not be here in finished product

            prevTemp = self.currentTemp  # This is so it wont call the functions each time

            sleep(10)



program = Program()  # Instanciate main class
program.Main()  # Start the program