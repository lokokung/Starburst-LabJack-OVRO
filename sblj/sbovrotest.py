"""
    STARBURST OVRO Specific Abstraction Test Suite
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import unittest
from labjack import ljm
import sblj
import sbovro
import pickle

"""
TestOVROMethods Test Group Description:
    This is a group of unit tests that test each method offered by the
    sbovro module. This group only provides for basic functionality 
    testing.
    
    Test Count: 6
"""
class TestOVROMethods(unittest.TestCase):
    # Monkey patching methods for LJM Library and sblj in order to unit 
    # test effectively. The new method is injected in the setUp and 
    # removed in the tearDown to allow for running of individual test 
    # cases in this group.
        
    def connect(self):
        pass
        
    def errorCheck(self):
        pass
                        
    def eReadName(self, handle, name):
        return self.testValues[handle][name]
        
    def eReadNameString(self, handle, name):
        return self.testValues[handle][name]
        
    def eWriteName(self, handle, name, newVal):
        if handle is None:  
            handle = "Antenna"
        self.testValues[handle][name] = newVal
        
    def eWriteNameString(self, handle, name, newVal):
        self.testValues[handle][name] = newVal
        
    def setUp(self):
        # Dictionary of values that the mock LabJack will return for 
        # call with names corresponding to the keys of the dictionary.

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
            
        self.LOConstantNames = {value: name for name, 
                                value in vars(sblj.LOFreqConstants).items() 
                                if name.isupper()}
        
        self.o_connect = sblj.StarburstLJ.connect
        self.o_errorCheck = sblj.StarburstLJ.errorCheck
        self.o_eReadName = ljm.eReadName
        self.o_eReadNameString = ljm.eReadNameString
        self.o_eWriteName = ljm.eWriteName
        self.o_eWriteNameString = ljm.eWriteNameString
        
        sblj.StarburstLJ.connect = self.connect
        sblj.StarburstLJ.errorCheck = self.errorCheck
        ljm.eReadName = self.eReadName
        ljm.eReadNameString = self.eReadNameString
        ljm.eWriteName = self.eWriteName
        ljm.eWriteNameString = self.eWriteNameString
        
        self.ovroObj = sbovro.OVROStarburst("LONoise", "Antenna", "Antenna")
        self.ovroObj.ljLONoise.handle = "LONoise"
        self.ovroObj.ljA.handle = "Antenna"
        self.ovroObj.ljB.handle = "Antenna"
        
    def tearDown(self):
        sblj.StarburstLJ.connect = self.o_connect
        sblj.StarburstLJ.errorCheck = self.o_errorCheck
        ljm.eReadName = self.o_eReadName
        ljm.eReadNameString = self.o_eReadNameString
        ljm.eWriteName = self.o_eWriteName
        ljm.eWriteNameString = self.o_eWriteNameString
    
    """
    Test - test_getMonitorData_ReturnsCorrectValues:
        Given that we call getMonitorData when a single antenna and the 
            LO noise module is supplied with the values on the pins/register
            defined in testValues,
        Then the dictionary of dictionaries returned contains the correct 
            values in the correct places.
    """
    def test_getMonitorDataReturnsCorrectValues(self):
        dict = self.ovroObj.getMonitorData()
        
        # Assertions for generic LabJacks.
        for id in ["A", "B", "LONOISE"]:
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
        
        # Assertions for the antennas.
        for id in ["A", "B"]:
            self.assertEqual(dict[id]["HIPOW"], -24)
            self.assertEqual(dict[id]["HQPOW"], -24)
            self.assertEqual(dict[id]["VIPOW"], -24)
            self.assertEqual(dict[id]["VQPOW"], -24)
            self.assertEqual(dict[id]["HITEMP"], 211)
            self.assertEqual(dict[id]["HQTEMP"], 211)
            self.assertEqual(dict[id]["VITEMP"], 211)
            self.assertEqual(dict[id]["VQTEMP"], 211)
            self.assertEqual(dict[id]["VNSSEL"], 0)
            self.assertEqual(dict[id]["HNSSEL"], 0)
            self.assertEqual(dict[id]["HIATTEN"], 31.5)
            self.assertEqual(dict[id]["HQATTEN"], 31.5)
            self.assertEqual(dict[id]["VIATTEN"], 31.5)
            self.assertEqual(dict[id]["VQATTEN"], 31.5)
        
        # Assertions for the LO Noise module.
        self.assertEqual(dict["LONOISE"]["LOFREQ"][0], "LO_3_4GHZ")
        self.assertEqual(dict["LONOISE"]["LOFREQ"][1], 0)
        self.assertEqual(dict["LONOISE"]["NSSTAT"], 0)
    
    """
    Test - test_selectNoiseSource:
        Given that we select the noise source for the OVRO object,
        Then the noise source should be turned on in the LO Noise 
            module and all polarizations of all antennas should be 
            switched to the noise source.
    """
    def test_selectNoiseSource(self):
        self.ovroObj.selectNoiseSource()
        
        for key in ["A", "B"]:
            dict = self.ovroObj.getMonitorData()
            self.assertEqual(dict[key]["VNSSEL"], 1)
            self.assertEqual(dict[key]["HNSSEL"], 1)
            
        dict = self.ovroObj.getMonitorData()
        self.assertEqual(dict["LONOISE"]["NSSTAT"], 1)
    
    """
    Test - test_selectRFSource:
        Given that we select the RF source for the OVRO object,
        Then the noise source should be turned off in the LO Noise 
            module and all polarizations of all antennas should be 
            switched to the RF source.
    """
    def test_selectRFSource(self):
        self.ovroObj.selectRFSource()
        
        for key in ["A", "B"]:
            dict = self.ovroObj.getMonitorData()
            self.assertEqual(dict[key]["VNSSEL"], 0)
            self.assertEqual(dict[key]["HNSSEL"], 0)
            
        dict = self.ovroObj.getMonitorData()
        self.assertEqual(dict["LONOISE"]["NSSTAT"], 0)
        
    """
    Test - test_setToBand:
        Given that we set the band to band 1,
        Then the LO Frequency is at 3.4GHz, the vertical attenuators
            are at 10dB and the horizontal attenuators are at 12dB.
    """
    def test_setToBand(self):
    
        self.ovroObj.setToBand(1)
        dict = self.ovroObj.getMonitorData()
        
        with open(".bands", "r") as file:
            check = pickle.load(file)
            attens = check[1]["ATTEN"]
            lofrq = check[1]["LOFREQ"]
        
            self.assertEqual(dict["LONOISE"]["LOFREQ"][0], 
                             self.LOConstantNames[lofrq])
            self.assertEqual(dict["LONOISE"]["LOFREQ"][1], 0)
        
            for key in ["A", "B"]:
                dict = self.ovroObj.getMonitorData()
                self.assertEqual(dict[key]["VQATTEN"], attens["VQ"])
                self.assertEqual(dict[key]["VIATTEN"], attens["VI"])
                self.assertEqual(dict[key]["HQATTEN"], attens["HQ"])
                self.assertEqual(dict[key]["HIATTEN"], attens["HI"])
    
    """
    Test - test_setToBandNonexistantBandRaisesError:
        Given that we try setting to a band that does not exist,
        Then a InvalidBandError is raised.
    """
    def test_setToBandNonexistantBandRaisesError(self):
        self.assertRaises(sbovro.InvalidBandError, self.ovroObj.setToBand, 123)
        
    """
    Test - test_alterAntByDelta:
        Given that we decrement all attenuations by 10,
        Then the new attenuations is all 21.5.
    """
    def test_alterAntByDelta(self):
        self.ovroObj.alterAntByDelta(-10)
        
        for key in ["A", "B"]:
            dict = self.ovroObj.getMonitorData()
            self.assertEqual(dict[key]["VQATTEN"], 21.5)
            self.assertEqual(dict[key]["VIATTEN"], 21.5)
            self.assertEqual(dict[key]["HQATTEN"], 21.5)
            self.assertEqual(dict[key]["HIATTEN"], 21.5)
    

# Main Method
if __name__ == '__main__':
    testGroups = [TestOVROMethods]
    for tG in testGroups:
        print "\nTesting: " + str(tG.__name__)
        suite = unittest.TestLoader().loadTestsFromTestCase(
            tG)
        unittest.TextTestRunner(verbosity=2).run(suite)