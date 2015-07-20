"""
    STARBURST LabJack Control Wrapper Library Constants
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

class GenericLabJackConstants(object):
    LJTEMP = 100
    LJAIRTEMP = 101
    POW_24V = 102
    POW_15V = 103
    POW_12V = 104
    POW_5V = 105
    POW_S5V = 106
    POW_N5V = 107
    NAME = 108
    
class LONoiseLabJackConstants(GenericLabJackConstants):
    LOFREQ = 200
    NSSTAT = 201