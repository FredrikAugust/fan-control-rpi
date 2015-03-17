'''This is a script to automatically control the fans of my Raspberry Pi mini-PC build.
If you find this useful somehow, feel free to use the code.
Copyrights: MrMadsenMalmo 2015
'''

import re
# import RPi.GPIO as GPIO  # This import will fail unless you have the RPi lib installed, obviously



class FanControl:
    def setTemp(self):
        validInput = False
        
        while not validInput:
            try:
                self.temp1 = int(raw_input("Input first temp. level:  "))
                self.temp2 = int(raw_input("Input second temp. level:  "))
                self.temp3 = int(raw_input("Input third temp. level:  "))
            except(ValueError):
                print "Invalid input, try again."
                continue
            
            validInput = True
            print "Temperatures set."
    
    def __init__(self):
        useDefault = raw_input("Would you like to set the temperatures manually? y/n\n")
        
        if len(useDefault.strip()) == 0:
            self.temp1 = 35
            self.temp2 = 45
            self.temp3 = 60
        else:
            self.setTemp()
            
FanControl1 = FanControl()