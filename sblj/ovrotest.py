"""
    STARBURST OVRO Specific Abstraction Test Suite
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import unittest
from labjack import ljm
import ovro

class TestOVROGetMonitorData(unittest.TestCase):
    """
        Monkey patching methods for LJM Library and sblj in order to unit 
        test effectively. The new method is injected in the setUp and 
        removed in the tearDown to allow for running of individual test 
        cases in this group.
    """
    def newInit(self, identifier="ANY", connectionType="ETHERNET", 
                 deviceType="T7", handle=None):
        if not isinstance(deviceType, str):
            raise TypeError("Expected a string instead of " + 
                            str(type(deviceType)) + ".")
        if not isinstance(connectionType, str):
            raise TypeError("Expected a string instead of " + 
                            str(type(connectionType)) + ".")
        
        self.identifier = str(identifier)
        self.connectionType = connectionType
        self.deviceType = deviceType

        self.handle = self.identifier
        
        self.ljVariables = ["LJTEMP", "LJAIRTEMP", "POW_24V", "POW_15V", 
                            "POW_12V", "POW_5V", "POW_N5V", "NAME", 
                            "POW_S5V", "SERIAL"]
                        
    def eReadName(self, handle, name):
        return self.mockLabJackValues[handle][name]
        
    def eReadNameString(self, handle, name):
        return self.mockLabJackValues[handle][name]
        
    def eWriteName(self, handle, name, newVal):
        self.mockLabJackValues[handle][name] = newVal
        
    def eWriteNameString(self, handle, name, newVal):
        self.mockLabJackValues[handle][name] = newVal
        
    def setUp(self):
        """
            Dictionary of values that the mock LabJack will return for 
            call with names corresponding to the keys of the dictionary.
        """
        self.testValues = {
            'LONoise': {'TEMPERATURE_DEVICE_K': 300,
                        'TEMPERATURE_AIR_K': 298,
                        'AIN4': 8,
                        'AIN5': 7.5,
                        'AIN6': 6,
                        'AIN7': 5,
                        'AIN8': 5,
                        'AIN9': -5,
                        'EIO0': 0,
                        'EIO3': 0,
                        'EIO4': 0,
                        'DEVICE_NAME_DEFAULT': 'MockLabJack',
                        'SERIAL_NUMBER': 1000},
            'Antenna': {'TEMPERATURE_DEVICE_K': 300,
                        'TEMPERATURE_AIR_K': 298,
                        'AIN0': 1.2,
                        'AIN1': 1.2,
                        'AIN2': 1.2,
                        'AIN3': 1.2,
                        'AIN4': 8,
                        'AIN5': 7.5,
                        'AIN6': 6,
                        'AIN7': 5,
                        'AIN8': 5,
                        'AIN9': -5,
                        'AIN10': 1,
                        'AIN11': 1,
                        'AIN12': 1,
                        'AIN13': 1,
                        'EIO1': 0,
                        'EIO2': 0,
                        'CIO0': 0,
                        'CIO1': 0,
                        'CIO2': 0,
                        'CIO3': 0,
                        'FIO0': 1,
                        'FIO1': 1,
                        'FIO2': 1,
                        'FIO3': 1,
                        'FIO4': 1,
                        'FIO5': 1,
                        'DEVICE_NAME_DEFAULT': 'MockLabJack',
                        'SERIAL_NUMBER': 1000}
            }
        
        self.o_oldInit = sblj.StarburstLJ.__init__
        self.o_eReadName = ljm.eReadName
        self.o_eReadNameString = ljm.eReadNameString
        self.o_eWriteName = ljm.eWriteName
        self.o_eWriteNameString = ljm.eWriteNameString
        
        sblj.StarburstLJ.__init__ = self.newInit
        ljm.eReadName = self.eReadName
        ljm.eReadNameString = self.eReadNameString
        ljm.eWriteName = self.eWriteName
        ljm.eWriteNameString = self.eWriteNameString
        
    def tearDown(self):
        sblj.StarburstLJ.__init__ = self.o_oldInit
        ljm.eReadName = self.o_eReadName
        ljm.eReadNameString = self.o_eReadNameString
        ljm.eWriteName = self.o_eWriteName
        ljm.eWriteNameString = self.o_eWriteNameString
        
    def test_getMonitorDataReturnsCorrectValues(self):
        
        
if __name__ == '__main__':
    testGroups = [TestOVROGetMonitorData]
    for tG in testGroups:
        print "\nTesting: " + str(tG.__name__)
        suite = unittest.TestLoader().loadTestsFromTestCase(
            tG)
        unittest.TextTestRunner(verbosity=2).run(suite)