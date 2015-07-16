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
        NoiseLOID: identifier string for the LabJack corresponding to the
            LO and Noise Source system. 
        dictOfAntennaIDs: dictionary with the keys being a way to reference
            the different antennas and the values being an identifier string
            to the LabJack corresponding to the antenna.
    Raises:
        UnknownDeviceError: occurs when device description such as 
                identifier, deviceType, or connectionType, do not point to a
                valid LabJack module.
"""
class OVROStarburst(object):

    """
        Default dictionary for band levels.
    """
    bandDictionary = {1: {"LOFREQ": 0,
                          "ATTEN": [(10, ["VQ", "VI"]),
                                    (12, ["HQ", "HI"]) ], 
                          "DESCR": "Default band" } }
                                    
    def __init__(self, noiseLOID, dictOfAntennaIDs):
        self.noiseLOID = noiseLOID
        self.dictOfAntennaIDs = copy.copy(dictOfAntennaIDs)
        
        self.ljLONoise = sblj.LONoiseLJ(self.noiseLOID)
        
        self.ljDictOfAntennas = {}
        for key, value in self.dictOfAntennaIDs.items():
            self.ljDictOfAntennas[key] = sblj.AntennaLJ(value)
            
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
            the given keys from dictOfAntennaIDs for the Antennas. The 
            dictionaries inside are keyed by the parameters described
            under the sblj.py for LONoiseLJ and AntennaLJ.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                at least one of the LabJack units.
    """
    def getMonitorData(self):
        varDump = {}
        varDump["LONOISE"] = self.ljLONoise.getParams()
        
        for key, lj in self.ljDictOfAntennas.items():
            varDump[key] = lj.getParams()
        
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
        
        for lj in self.ljDictOfAntennas.values():
            lj.selectNoiseSource()
    
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
        
        for lj in self.ljDictOfAntennas.values():
            lj.selectRFSource()
    
    """
    Method: setToBand(band, antennas)
        Description:
            Takes a band setting that is predefined and sets the LO frequency
            and attenuator settings.
        Parameters:
            band: band setting as defined in .bands file. (This can be edited
                using bands.py.)
            antennas: list of keys to antennas that the attenuation changes
                should apply to.
        Raises:
            InvalidBandError: occurs when the .bands setting does not have 
                values for a given band.
            NoConnectionError: occurs when there is no connection to the 
                at least one of the LabJack units.
            KeyError: occurs when a key in antennas does not match to any 
                AntennaLJ objects.
    """
    def setToBand(self, band, antennas=None):
        if antennas is None:
            antennas = self.ljDictOfAntennas.keys()
            
        ref = {}
        try:
            ref = self.bands[band]
        except KeyError:
            raise InvalidBandError(band)
            
        self.ljLONoise.setLOFreq(ref["LOFREQ"])
        
        for lj in antennas:
            for val, list in ref["ATTEN"]:
                self.ljDictOfAntennas[lj].setAttenuator(val, list)
    
    """
    Method: alterAntByDelta(delta, antennas)
        Description:
            Alters the attenuation of all polarization/components of the 
            given antennas by delta.
        Parameters:
            delta: amount to change the attenuations by.
            antennas: list of keys to antennas that the attenuation changes
                should apply to.
        Raises:
            InvalidBandError: occurs when the .bands setting does not have 
                values for a given band.
            NoConnectionError: occurs when there is no connection to the 
                at least one of the LabJack units.
            KeyError: occurs when a key in antennas does not match to any 
                AntennaLJ objects.
    """
    def alterAntByDelta(self, delta, antennas=None):
        if antennas is None:
            antennas = self.ljDictOfAntennas.keys()
        
        for lj in antennas:
            self.ljDictOfAntennas[lj].deltaAttenuator(delta)
    
    """
    Method: endConnection()
        Description:
            Ends connections to all LabJacks in the system.
    """
    def endConnection(self):
        self.ljLONoise.disconnect()
        for lj in self.ljDictOfAntennas.values():
            lj.diconnect()