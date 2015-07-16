"""
    STARBURST OVRO Specific Abstraction
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import sblj
import copy

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
        bandLevel: band level to initialize the system to.
    Raises:
        UnknownDeviceError: occurs when device description such as 
                identifier, deviceType, or connectionType, do not point to a
                valid LabJack module.
"""
class OVROStarburst(object):
    def __init__(self, noiseLOID, dictOfAntennaIDs, bandLevel):
        self.noiseLOID = noiseLOID
        self.dictOfAntennaIDs = copy.copy(dictOfAntennaIDs)
        
        self.ljLONoise = sblj.LONoiseLJ(self.noiseLOID)
        
        self.ljDictOfAntennas = {}
        for key, value in self.dictOfAntennaIDs.items():
            self.ljDictOfAntennas[key] = sblj.AntennaLJ(value)
    
    def getMonitorData(self):
        varDump = {}
        varDump["LONOISE"] = self.ljLONoise.getParams()
        
        for key, lj in self.ljDictOfAntennas.items():
            varDump[key] = lj.getParams()
        
        return varDump