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

"""
Method: clrScreen()
    Description: 
        Method that clears the screen on the shell prompt.
"""
def clrScreen():
    tmp = sp.call('cls', shell = True)

"""
Method: welcomeScreen()
    Description:
        Method that produces a welcome message at the top of the 
        shell prompt.
"""
def welcomeScreen():
    clrScreen()
    print SEPARATOR
    print "This script is used to help add, delete, or modify"
    print "default band settings. Select one of the following"
    print "options by typing in the number next to the" 
    print "option."
    print SEPARATOR

"""
Method: listBands()
    Description:
        Method that lists all existing band settings in the .bands file.
"""
def listBands():
    with open(".bands", "r") as file:
        dict = pickle.load(file)
        for key, val in dict.items():
            print SEPARATOR
            print "Band " + str(key) + ": " + val["DESCR"]
            print "LO Frequency: " + LOFREQS[val["LOFREQ"]]
            print "VQ Attenuation: " + str(val["ATTEN"]["VQ"])
            print "VI Attenuation: " + str(val["ATTEN"]["VI"])
            print "HQ Attenuation: " + str(val["ATTEN"]["HQ"])
            print "HI Attenuation: " + str(val["ATTEN"]["HI"])
        print SEPARATOR
        optionScreen()

"""
Method: addBand()
    Description:
        Method that prompts the user in order to help either modify an 
        existing band setting or to create a new one. 
"""
def addBand():
    dict = None
    with open(".bands", "r") as file:
        dict = pickle.load(file)
        clrScreen()
        print SEPARATOR
        print "Follow the instructions below to add or modify"
        print "a band."
        print SEPARATOR
        
        band = None
        while band is None:
            band = raw_input("Please enter a valid band number: ")
            try:
                band = int(band)
            except:
                band = None
            
            if band in dict.keys():
                overwriteFlag = None
                while overwriteFlag is None:
                    overwriteFlag = raw_input("Band number already in use, " +
                                               "overwrite? (y/n) ")
                    if overwriteFlag == "n":
                        band = None
                    elif overwriteFlag != "y":
                        overwriteFlag = None
                    else:
                        pass
        
        bandDescr = raw_input("Give a description for this band.\n")
        
        loFreq = None
        print SEPARATOR
        print "Select a LO frequency by typing the corresponding"
        print "number:"
        print "(0) 3.4GHz"
        print "(1) 7.5GHz"
        print "(2) 11.5GHz"
        print "(3) 15.5GHz"
        
        while loFreq is None:
            loFreq = raw_input("Please choose a LO frequency: ")
            try:
                loFreq = int(loFreq)
            except:
                loFreq = None
                print "Please pick one of the given LO frequencies."
            
            if loFreq < 0 or loFreq > 3:
                loFreq = None
                print "Please pick one of the given LO frequencies."
        
        print SEPARATOR
        vq = getDouble("VQ")
        print SEPARATOR
        vi = getDouble("VI")
        print SEPARATOR
        hq = getDouble("HQ")
        print SEPARATOR
        hi = getDouble("HI")
        
        dict[band] = formatData(bandDescr, loFreq, vq, vi, hq, hi)
        
    with open(".bands", "w") as file:
        pickle.dump(dict, file)
        
    done = None
    while done is None:
        done = raw_input("Successfully saved band," + 
                         " return to main menu? (y/n) ")
        if done == "y":
            welcomeScreen()
            optionScreen()
        elif done != "n":
            done = None
        else:
            pass
"""
Method: removeBand()
    Description: 
        Method to assist users in removing old or invalid band settings. 
        Has a built in confirmation in order to make sure that deletions
        only occur if meant to be.
"""
def removeBand():
    dict = None
    with open(".bands", "r") as file:
        dict = pickle.load(file)
        clrScreen()
        print SEPARATOR
        print "Follow the instructions below to remove a band."
        print SEPARATOR
        
        band = None
        while band is None:
            band = raw_input("Please enter a valid band number: ")
            try:
                band = int(band)
            except:
                band = None
                print "The given band number does not exist."
            if band not in dict.keys():
                band = None
                print "The given band number does not exist."
        
    confirm = None
    while confirm is None:
        confirm = raw_input("Are you sure you want to delete band " + 
                            str(band) + "? (y/n) ")
        if confirm == "y":  
            del dict[band]
            with open(".bands", "w") as file:
                pickle.dump(dict, file)
            
            done = None
            while done is None:
                done = raw_input("Successfully removed band," + 
                                " return to main menu? (y/n) ")
                if done == "y":
                    welcomeScreen()
                    optionScreen()
                elif done != "n":
                    done = None
                else:
                    pass
            
        elif confirm != "n":
            confirm = None
        else:
            welcomeScreen()
            optionScreen()

"""
Method: getDouble(polarComp)
    Description:
        Helper method to get attenuation values for the different 
        component.
    Arguments:
        polarComp: string to indicate which polarization/component that
            the returned value is used for.
"""
def getDouble(polarComp):
    val = None
    while val is None:
        val = raw_input("Attenuation level for " + polarComp +
                        " in dB: ")
        try:
            val = float(val)
        except:
            val = None
            print "Please enter a valid attenuation value."
            
        if val < 0 or val > 31.5:
            val = None
            print "Please enter a valid attenuation value."
            
    return val
"""
Method: formatData()
    Description:
        Helper method to format all the data that is collected in addBand()
        into the standard dictionary format to add into the .bands setting 
        file.
"""            
def formatData(bandDescr, loFreq, vq, vi, hq, hi):
    dict = {"LOFREQ": loFreq,
            "ATTEN": {"VQ": vq,
                      "VI": vi,
                      "HQ": hq,
                      "HI": hi}, 
            "DESCR": bandDescr}
    return dict

"""
Method: exit()
    Description:
        Method that does nothing but makes it easier to understand the code
        when reading through.
"""
def exit():
    pass
"""
Method: optionScreen()
    Description:
        Method that generates the main menu. This method is also in charge of 
        getting the chosen option and redirecting to the correct procedures
        using a map.
"""
def optionScreen():
    functionMap = {1: listBands,
                   2: addBand,
                   3: removeBand,
                   4: exit}
    
    print "\n(1): List current band settings."
    print "(2): Add/Modify new band setting."
    print "(3): Remove band setting."
    print "(4): Exit."
    
    val = None
    while val is None:
        try:
            val = int(raw_input(""))
            if val < 1 or val > 5:
                print "Invalid input!"
        except:
            print "Invalid input!"
    
    functionMap[val]()
    
"""
Main Method
"""    
if __name__ == '__main__':
    welcomeScreen()
    optionScreen()