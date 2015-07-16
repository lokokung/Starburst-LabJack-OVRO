"""
    STARBURST OVRO Specific Abstraction Test Suite
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import unittest
from labjack import ljm
import sblj
import ovro

class TestOVROGetMonitorData(unittest.TestCase):
    """
        Monkey patching methods for LJM Library and sblj in order to unit 
        test effectively. The new method is injected in the setUp and 
        removed in the tearDown to allow for running of individual test 
        cases in this group.
    """
    def connect(self):
        pass
        
    def setAttenuator(self, level, list=None):
        pass
                        
    def eReadName(self, handle, name):
        return self.testValues[handle][name]
        
    def eReadNameString(self, handle, name):
        return self.testValues[handle][name]
        
    def eWriteName(self, handle, name, newVal):
        self.testValues[handle][name] = newVal
        
    def eWriteNameString(self, handle, name, newVal):
        self.testValues[handle][name] = newVal
        
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
        
        self.o_connect = sblj.StarburstLJ.connect
        self.o_setAttenuator = sblj.AntennaLJ.setAttenuator
        self.o_eReadName = ljm.eReadName
        self.o_eReadNameString = ljm.eReadNameString
        self.o_eWriteName = ljm.eWriteName
        self.o_eWriteNameString = ljm.eWriteNameString
        
        sblj.StarburstLJ.connect = self.connect
        sblj.AntennaLJ.setAttenuator = self.setAttenuator
        ljm.eReadName = self.eReadName
        ljm.eReadNameString = self.eReadNameString
        ljm.eWriteName = self.eWriteName
        ljm.eWriteNameString = self.eWriteNameString
        
        self.ovroObj = ovro.OVROStarburst("LONoise", {"Antenna": "Antenna"}, 1)
        self.ovroObj.ljLONoise.handle = "LONoise"
        self.ovroObj.ljDictOfAntennas["Antenna"].handle = "Antenna"
        
    def tearDown(self):
        sblj.StarburstLJ.connect = self.o_connect
        sblj.AntennaLJ.setAttenuator = self.o_setAttenuator
        ljm.eReadName = self.o_eReadName
        ljm.eReadNameString = self.o_eReadNameString
        ljm.eWriteName = self.o_eWriteName
        ljm.eWriteNameString = self.o_eWriteNameString
    
    """
    Test - test_getMonitorDataReturnsCorrectValues:
        Given that we call getMonitorData when a single antenna and the 
            LO noise module is supplied with the values on the pins/register
            defined in testValues,
        Then the dictionary of dictionaries returned contains the correct 
            values in the correct places.
    """
    def test_getMonitorDataReturnsCorrectValues(self):
        dict = self.ovroObj.getMonitorData()
        
        """
            Assertions for generic LabJacks.
        """
        for id in ["Antenna", "LONOISE"]:
            self.assertEqual(dict[id]["NAME"], "MockLabJack")
            self.assertEqual(dict[id]["LJTEMP"], 300)
            self.assertEqual(dict[id]["LJAIRTEMP"], 298)
            self.assertEqual(dict[id]["POW_24V"], 24)
            self.assertEqual(dict[id]["POW_15V"], 15)
            self.assertEqual(dict[id]["POW_12V"], 12)
            self.assertEqual(dict[id]["POW_5V"], 5)
            self.assertEqual(dict[id]["POW_N5V"], -5)
            self.assertEqual(dict[id]["POW_S5V"], 5)
            self.assertEqual(dict[id]["SERIAL"], 1000)
        
        """
            Assertions for the antenna.
        """
        self.assertEqual(dict["Antenna"]["HIPOW"], -24)
        self.assertEqual(dict["Antenna"]["HQPOW"], -24)
        self.assertEqual(dict["Antenna"]["VIPOW"], -24)
        self.assertEqual(dict["Antenna"]["VQPOW"], -24)
        self.assertEqual(dict["Antenna"]["HITEMP"], 211)
        self.assertEqual(dict["Antenna"]["HQTEMP"], 211)
        self.assertEqual(dict["Antenna"]["VITEMP"], 211)
        self.assertEqual(dict["Antenna"]["VQTEMP"], 211)
        self.assertEqual(dict["Antenna"]["VNSSEL"], 0)
        self.assertEqual(dict["Antenna"]["HNSSEL"], 0)
        self.assertEqual(dict["Antenna"]["HIATTEN"], 31.5)
        self.assertEqual(dict["Antenna"]["HQATTEN"], 31.5)
        self.assertEqual(dict["Antenna"]["VIATTEN"], 31.5)
        self.assertEqual(dict["Antenna"]["VQATTEN"], 31.5)
        
        """
            Assertions for the LO Noise module.
        """
        self.assertEqual(dict["LONOISE"]["LOFREQ"], "LO_3_4GHZ")
        self.assertEqual(dict["LONOISE"]["NSSTAT"], 0)
        
if __name__ == '__main__':
    testGroups = [TestOVROGetMonitorData]
    for tG in testGroups:
        print "\nTesting: " + str(tG.__name__)
        suite = unittest.TestLoader().loadTestsFromTestCase(
            tG)
        unittest.TextTestRunner(verbosity=2).run(suite)