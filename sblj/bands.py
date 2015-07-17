"""
    STARBURST OVRO Band Manipulation Program
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import pickle
import subprocess as sp
from sblj import LOFreqConstants

SEPARATOR = "=================================================="

LOFREQS = {value: name for name, value in vars(LOFreqConstants).items() 
           if name.isupper()}

def clrScreen():
    tmp = sp.call('cls', shell = True)
    
def welcomeScreen():
    clrScreen()
    print SEPARATOR
    print "This script is used to help add, delete, or modify"
    print "default band settings. Select one of the following"
    print "options by typing in the number next to the" 
    print "option."
    print SEPARATOR
    
def listBands():
    with open(".bands", "r") as file:
        dict = pickle.load(file)
        for key, val in dict.items():
            print SEPARATOR
            print "Band " + str(key) + ":"
            print "LO Frequency: " + LOFREQS[val["LOFREQ"]]
            print "VQ Attenuation: "
    
def optionScreen():
    functionMap = {1: listBands}
    
    print "\n(1): List current band settings."
    print "(2): Add new band setting."
    print "(3): Modify existing band setting."
    print "(4): Remove band setting."
    print "(5): Exit."
    
    val = None
    while val is None:
        try:
            val = int(raw_input(""))
        except:
            print "Invalid input!\n"
    
    functionMap[val]()
    
"""
Main Method
"""    
if __name__ == '__main__':
    welcomeScreen()
    optionScreen()