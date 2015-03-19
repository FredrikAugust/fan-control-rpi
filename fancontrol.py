'''This is a script to automatically control the fans of my Raspberry Pi mini-PC build.
If you find this useful somehow, feel free to use the code.
Copyrights: MrMadsenMalmo 2015
'''

import re
from sys import exit
from time import sleep, strftime, strftime
import os
from time import strftime

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

        if temperature < self.temp2:
            GPIO.output(self.tempLights[0], 1)
        elif temperature >= self.temp2 and temperature < self.temp3:
            GPIO.output(self.tempLights[1], 1)
        elif temperature >= self.temp3:
            GPIO.output(self.tempLights[2], 1)

    def fanPower(self, temperature):
        """This turns on or off the fan depending on the heat of the Raspberry Pi
        The fan is running a 5v current, so I will use a transistor that is controlled
        with a 3.3v current + 1k ohm resistor.
        """

        if temperature >= self.temp3:
            GPIO.output(self.fanPin, 1)
        else:
            GPIO.output(self.fanPin, 0)


    def setPins(self):
        """Set up the pins, as of now I will use GPIO.BCM"""
        
        GPIO.setwarnings(False)
        
        GPIO.cleanup()
    
        GPIO.setmode(GPIO.BCM)
        
        self.tempLights = [0, 0, 0]  # low, med, hot
        self.fanPin = 0  # This will turn on and off the transistor that controls the fan
        self.autoPin = 0  # This will determine whether to use auto mode or not
        
        GPIO.setup(self.fanPin, GPIO.OUT)
        GPIO.setup(self.autoPin, GPIO.IN)
        
        for tempLight in self.tempLights:
            GPIO.setup(tempLight, GPIO.OUT)  # sets these pins to output
        
        print "Pins are set"

        sleep(1)
    
    def getTemp(self):
        """Create a file from the result of a command that gets the system temp
        Then reads it using with 'with'
        """

        os.system("vcgencmd measure_temp >> currentTemp.txt")
        
        with open("currentTemp.txt", "r+") as file:
            self.tempP = file.read()
            file.truncate(0)

        self.temperature = re.search("temp\=(?P<temp>[\d\.]+)\'C", self.tempP, re.VERBOSE|re.MULTILINE)
        return float(self.temperature.group('temp'))
        
    def printTemp(self):
        print "Temperatures set."
        print "Temp 1:", self.temp1
        print "Temp 2:", self.temp2
        print "Temp 3:", self.temp3

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
                printTemp()
                
                sleep(1)
        else:
            self.temp1 = 35
            self.temp2 = 40
            self.temp3 = 50
            
            printTemp()

            sleep(1)
    
    def __init__(self):
        useDefault = raw_input("Would you like to set the temperatures manually? y/n\n")

        self.autoOn = False

        if len(useDefault.strip()) == 0 or useDefault.strip().lower() == "n":
            self.setTemp()
        else:
            self.setTemp(True)
            
        self.setPins()



class Program:
    def Main(self):
        clearScreen()

        self.temperatureControl = FanControl()

        with open("log.log", "r") as f:
            tempContent = f.readline()
            
            prevTemp = int(re.search("\:\s(?P<temp>[\d]+)\'C", tempContent, re.VERBOSE).group("temp"))

        while True:
            if GPIO.input(self.temperatureControl.autoPin):
                try:
                    clearScreen()
                    self.currentTemp = self.temperatureControl.getTemp()

                    if self.currentTemp != prevTemp:
                        self.temperatureControl.powerLights(self.currentTemp)
                        self.temperatureControl.fanPower(self.currentTemp)
                    
                        print "Fan speed and lights updated"

                        with open("log.log", "a") as f:
                            f.write("\n[{}]: {}'C".format(strftime("%d.%m.%Y %H:%M"), self.currentTemp))

                    print "Temperature:", self.currentTemp  # for debugging purposes, will probably not be here in finished product

                    prevTemp = self.currentTemp  # This is so it wont call the functions each time

                    sleep(10)

                except KeyboardInterrupt:
                    GPIO.cleanup()
                    os.system("rm currentTemp.txt")
                    exit("You terminated the process")
            else:
                print "Auto-mode not activated"
                sleep(10)


program = Program()  # Instanciate main class
program.Main()  # Start the program
