"""
    STARBURST OVRO Specific Abstraction
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import sblj
import copy
import pickle

"""
Class: InvalidBandError extends Exception
    Description: 
        Custom error for indicating that an invalid band was selected.
"""                
class InvalidBandError(Exception):
    def __init__(self, band):
        self.band = band
        
    def __str__(self):
        return("Band " + str(band) + " is unavailable.")

"""
Class: OVROStarburst extends object
    Description:
        Custom object that represents the OVRO system of antennas and 
        necessary equipment. 
    Arguments:
        noiseLOID: identifier string for the LabJack corresponding to the
            LO and Noise Source system. 
        antennaA: identifier string for the LabJack corresponding to the 
            first antenna.
        antennaB: identifier string for the LabJack corresponding to the 
            second antenna.
    Raises:
        UnknownDeviceError: occurs when device description such as 
                identifier, deviceType, or connectionType, do not point to a
                valid LabJack module.
"""
class OVROStarburst(object):

    # Default dictionary for band levels.

    bandDictionary = {1: {"LOFREQ": 0,
                          "ATTEN": {"VQ": 10, "VI": 10, "HQ": 12, "HI": 12}, 
                          "DESCR": "Default band" } }
                                    
    def __init__(self, noiseLOID, antennaA=None, antennaB=None):
        self.noiseLOID = noiseLOID
        self.antennaA = antennaA
        self.antennaB = antennaB
        
        self.ljLONoise = sblj.LONoiseLJ(self.noiseLOID)
        if antennaA is not None:
            self.ljA = sblj.AntennaLJ(self.antennaA)
        if antennaB is not None:
            self.ljB = sblj.AntennaLJ(self.antennaB)
            
        try:
            with open(".bands", "r") as file:
                self.bands = pickle.load(file)
        except IOError:
            with open(".bands", "w") as file:
                pickle.dump(OVROStarburst.bandDictionary, file)
            self.bands = OVROStarburst.bandDictionary
    
    """
    Method: getMonitorData()
        Description:
            Query to the OVRO LabJacks to dump all data concerning the 
            system. The data is returned as a dictionary of dictionaries
            where the keys are "LONOISE" for the LO Noise module and 
            "A" and "B" for the corresponding antennas (A and B). The 
            dictionaries inside are keyed by the parameters described
            under the sblj.py for LONoiseLJ and AntennaLJ.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                at least one of the LabJack units.
    """
    def getMonitorData(self):
        varDump = {}
        varDump["LONOISE"] = self.ljLONoise.getParams()
        
        if self.antennaA is not None:
            varDump["A"] = self.ljA.getParams()
        if self.antennaB is not None:
            varDump["B"] = self.ljB.getParams()
        
        return varDump
    
    """
    Method: selectNoiseSource()
        Description:
            Turns on the Noise Source and switches all polarizations in all 
            antennas to the noise source.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                at least one of the LabJack units.
    """
    def selectNoiseSource(self):
        self.ljLONoise.setNoiseSourceOn()
        
        if self.antennaA is not None:
            self.ljA.selectNoiseSource()
        if self.antennaB is not None:
            self.ljB.selectNoiseSource()
    
    """
    Method: selectRFSource()
        Description:
            Turns off the Noise source and switches all polarizations in all 
            antennas to the RF signal source.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                at least one of the LabJack units.
    """
    def selectRFSource(self):
        self.ljLONoise.setNoiseSourceOff()
        
        if self.antennaA is not None:
            self.ljA.selectRFSource()
        if self.antennaB is not None:
            self.ljB.selectRFSource()
    
    """
    Method: setToBand(band, antennas)
        Description:
            Takes a band setting that is predefined and sets the LO frequency
            and attenuator settings.
        Parameters:
            band: band setting as defined in .bands file. (This can be edited
                using bands.py.)
            antennas: list of keys to antennas that the attenuation changes
                should apply to, valid keys are "A" and "B".
        Raises:
            InvalidBandError: occurs when the .bands setting does not have 
                values for a given band.
            NoConnectionError: occurs when there is no connection to the 
                at least one of the LabJack units.
            KeyError: occurs when a key in antennas does not match to any 
                AntennaLJ objects.
    """
    def setToBand(self, band, antennas=["A", "B"]):
        ref = {}
        try:
            ref = self.bands[band]
        except KeyError:
            raise InvalidBandError(band)
            
        self.ljLONoise.setLOFreq(ref["LOFREQ"])
        
        if "A" in antennas and self.antennaA is not None:
            for comp, val in ref["ATTEN"].items():
                self.ljA.setAttenuator(val, [comp])
        
        if "B" in antennas and self.antennaB is not None:
            for comp, val in ref["ATTEN"].items():
                self.ljB.setAttenuator(val, [comp])
    
    """
    Method: alterAntByDelta(delta, antennas)
        Description:
            Alters the attenuation of all polarization/components of the 
            given antennas by delta.
        Parameters:
            delta: amount to change the attenuations by.
            antennas: list of keys to antennas that the attenuation changes
                should apply to, valid keys are "A" and "B".
        Raises:
            InvalidBandError: occurs when the .bands setting does not have 
                values for a given band.
            NoConnectionError: occurs when there is no connection to the 
                at least one of the LabJack units.
            KeyError: occurs when a key in antennas does not match to any 
                AntennaLJ objects.
    """
    def alterAntByDelta(self, delta, antennas=["A", "B"]):
        if "A" in antennas and self.antennaA is not None:
            self.ljA.deltaAttenuator(delta)
        
        if "B" in antennas and self.antennaB is not None:
            self.ljB.deltaAttenuator(delta)
    
    """
    Method: endConnection()
        Description:
            Ends connections to all LabJacks in the system.
    """
    def endConnection(self):
        self.ljLONoise.disconnect()
        self.ljA.disconnect()
        self.ljB.disconnect()