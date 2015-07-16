"""
    STARBURST LabJack Control Wrapper Library Test Suite
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import unittest
from labjack import ljm
import sblj
    
"""
TestGenericLabJackGetParams Test Group Description:
    This group of tests makes sure that given that the LJM library correctly
    returns values on a LabJack with given names, that the getParams
    function returns the correct output. 
    
    Test Count: 10
"""
class TestGenericLabJackGetParams(unittest.TestCase):    
    """
        Monkey patching methods for LJM Library in order to unit test 
        effectively. The new method is injected in the setUp and removed 
        in the tearDown to allow for running of individual test cases in 
        this group.
    """
    def eReadName(self, handle, name):
        return self.mockLabJackValues[name]
        
    def eReadNameString(self, handle, name):
        return self.mockLabJackValues[name]
    
    def setUp(self):
        """
            Dictionary of values that the mock LabJack will return for 
            call with names corresponding to the keys of the dictionary.
        """
        self.mockLabJackValues = {'TEMPERATURE_DEVICE_K': 300,
                                  'TEMPERATURE_AIR_K': 298,
                                  'AIN4': 8,
                                  'AIN5': 7.5,
                                  'AIN6': 6,
                                  'AIN7': 5,
                                  'AIN8': 5,
                                  'AIN9': -5,
                                  'DEVICE_NAME_DEFAULT': 'MockLabJack',
                                  'SERIAL_NUMBER': 1000}
                         
        self.lj = sblj.StarburstLJ("ANY","ANY","ANY","MOCK")
        
        self.o_eReadName = ljm.eReadName
        self.o_eReadNameString = ljm.eReadNameString
        
        ljm.eReadName = self.eReadName
        ljm.eReadNameString = self.eReadNameString
        
    def tearDown(self):
        ljm.eReadName = self.o_eReadName
        ljm.eReadNameString = self.o_eReadNameString
    
    """
    Test - test_temperatureOfLabJack:
        Given that the mock LabJack has a temperature of 300,
        Then getParams(["LJTEMP"]) returns 300,
        And a time stamp is returned.
    """
    def test_temperatureOfLabJack(self):
        dict = self.lj.getParams(["LJTEMP"])
        self.assertEqual(dict["LJTEMP"], 300)
        self.assertTrue(dict.has_key("TIMESTAMP"))
    
    """
    Test - test_temperatureOfEnvironment:
        Given that the mock LabJack environment has a temperature of 298,
        Then getParams(["LJAIRTEMP"]) returns 298,
        And a time stamp is returned.
    """
    def test_temperatureOfEnvironment(self):
        dict = self.lj.getParams(["LJAIRTEMP"])
        self.assertEqual(dict["LJAIRTEMP"], 298)
        self.assertTrue(dict.has_key("TIMESTAMP"))
    
    """
    Test - test_24V:
        Given that the AIN4 on the LabJack has a voltage of 8,
        Then getParams(["24V"]) returns 24,
        And a time stamp is returned.
    """
    def test_24V(self):
        dict = self.lj.getParams(["POW_24V"])
        self.assertEqual(dict["POW_24V"], 24)
        self.assertTrue(dict.has_key("TIMESTAMP"))
        
    """
    Test - test_15V:
        Given that the AIN5 on the LabJack has a voltage of 7.5,
        Then getParams(["15V"]) returns 15,
        And a time stamp is returned.
    """
    def test_15V(self):
        dict = self.lj.getParams(["POW_15V"])
        self.assertEqual(dict["POW_15V"], 15)
        self.assertTrue(dict.has_key("TIMESTAMP"))
        
    """
    Test - test_12V:
        Given that the AIN6 on the LabJack has a voltage of 6,
        Then getParams(["12V"]) returns 12,
        And a time stamp is returned.
    """
    def test_12V(self):
        dict = self.lj.getParams(["POW_12V"])
        self.assertEqual(dict["POW_12V"], 12)
        self.assertTrue(dict.has_key("TIMESTAMP"))
        
    """
    Test - test_5V:
        Given that the AIN7 on the LabJack has a voltage of 5,
        Then getParams(["5V"]) returns 5,
        And a time stamp is returned.
    """
    def test_5V(self):
        dict = self.lj.getParams(["POW_5V"])
        self.assertEqual(dict["POW_5V"], 5)
        self.assertTrue(dict.has_key("TIMESTAMP"))
        
    """
    Test - test_neg5V:
        Given that the AIN9 on the LabJack has a voltage of -5,
        Then getParams(["NEG5V"]) returns -5,
        And a time stamp is returned.
    """
    def test_neg5V(self):
        dict = self.lj.getParams(["POW_N5V"])
        self.assertEqual(dict["POW_N5V"], -5)
        self.assertTrue(dict.has_key("TIMESTAMP"))
    
    """
    Test - test_s5V:
        Given that the AIN8 on the LabJack has a voltage of 5,
        Then getParams(["S5V"]) returns 5,
        And a time stamp is returned.
    """
    def test_s5V(self):
        dict = self.lj.getParams(["POW_S5V"])
        self.assertEqual(dict["POW_S5V"], 5)
        self.assertTrue(dict.has_key("TIMESTAMP"))
    
    """
    Test - test_name:
        Given that the LabJack's name is "MockLabJack",
        Then getParams(["NAME"]) returns "MockLabJack",
        And a time stamp is returned.
    """
    def test_name(self):
        dict = self.lj.getParams(["NAME"])
        self.assertEqual(dict["NAME"], "MockLabJack")
        self.assertTrue(dict.has_key("TIMESTAMP"))
        
    """
    Test - test_serial:
        Given that the LabJack's serial is 1000,
        Then getParams(["SERIAL"]) returns 1000,
        And a time stamp is returned.
    """
    def test_serial(self):
        dict = self.lj.getParams(["SERIAL"])
        self.assertEqual(dict["SERIAL"], 1000)
        self.assertTrue(dict.has_key("TIMESTAMP"))
    
    
"""
TestGenericLabJackConnections Test Group Description:
    This group of tests makes sure that exceptions are thrown when connections
    to LabJacks are not made or cannot be made.
    
    Test Count: 3
"""
class TestGenericLabJackConnections(unittest.TestCase):
    
    """
    Test - test_throwExceptionWhenLabJackNotExist:
        Given that one tries to connect to a LabJack that does not exist,
        Then an UnknownDeviceError is thrown.
    """
    def test_throwExceptionWhenLabJackNotExist(self):
        self.assertRaises(sblj.UnknownDeviceError, 
                          sblj.StarburstLJ, "FakeName")
    
    """
    Test - test_throwExceptionWhenDisconnect:
        Given that one disconnected from a StarburstLJ object,
        Then calling getters on that object results in NoConnectionError.
    """
    def test_throwExceptionWhenDisconnect(self):
        lj = sblj.StarburstLJ("","","","FAKE")
        lj.disconnect()
        self.assertRaises(sblj.NoConnectionError, 
                          lj.getParams)
                          
    """
    Test - test_throwExceptionWhenInvalidParam:
        Given that either the deviceType or connectionType is not a string,
        Then a TypeError is thrown.
    """
    def test_throwExceptionWhenInvalidParam(self):
        self.assertRaises(TypeError, sblj.StarburstLJ, 
                          "FAKE", 10, "ANY")
        self.assertRaises(TypeError, sblj.StarburstLJ, 
                          "FAKE", "ANY", 10)                  
                          

"""
TestGenericLabJackName Test Group Description:
    This group of tests makes sure that we write a name to the LabJack modules.
    
    Test Count: 4
"""
class TestGenericLabJackName(unittest.TestCase):
    """
        Monkey patching methods for LJM Library in order to unit test 
        effectively. The new method is injected in the setUp and removed 
        in the tearDown to allow for running of individual test cases in 
        this group.
    """
    def eReadNameString(self, handle, name):
        return self.ljName
        
    def eWriteNameString(self, handle, name, newName):
        self.ljName = newName
        
    def setUp(self):
        self.lj = sblj.StarburstLJ("ANY","ANY","ANY","MOCK")
        self.ljName = "MockLabJack"
        
        self.o_eReadNameString = ljm.eReadNameString
        self.o_eWriteNameString = ljm.eWriteNameString
        
        ljm.eReadNameString = self.eReadNameString
        ljm.eWriteNameString = self.eWriteNameString
        
    def tearDown(self):
        ljm.eReadNameString = self.o_eReadNameString
        ljm.eWriteNameString = self.o_eWriteNameString
        
    """
    Test - test_writeNameToLabJack:
        Given that the we change the LabJack's name to "NewName", 
        Then the change is reflected when we check it.
    """
    def test_writeNameToLabJack(self):
        dict = self.lj.getParams(["NAME"])
        self.assertEqual(dict["NAME"], "MockLabJack")
        
        self.lj.setLJName("NewName")
        
        dict = self.lj.getParams(["NAME"])
        self.assertEqual(dict["NAME"], "NewName")
        
    """
    Test - test_nameTooLong:
        Given that a name that exceeds 49 character is used,
        Then a TypeError will be thrown.
    """
    def test_nameTooLong(self):
        self.assertRaises(TypeError, self.lj.setLJName,
                          "ThisNameHasMoreThan49CharactersSoItShouldCauseFail")
    
    """
    Test - test_nameWithPeriods:
        Given that a name has periods,
        Then a TypeError will be thrown.
    """
    def test_nameWithPeriods(self):
        self.assertRaises(TypeError, self.lj.setLJName,
                          "This.Name.Has.Periods")
    
    """
    Test - test_throwExceptionWhenDisconnect
        Given that one disconnected from a StarburstLJ object,
        Then calling setLJName results in NoConnectionError. 
    """
    def test_throwExceptionWhenDisconnect(self):
        self.lj.disconnect()
        self.assertRaises(sblj.NoConnectionError, 
                          self.lj.setLJName, "Name")


"""
TestGenericLabJackReboot Test Group Description:
    This group of tests makes sure that the reboot function across
    generic LabJack's works.
    
    Test Count: 1
"""
class TestGenericLabJackReboot(unittest.TestCase):
    """
        Monkey patching methods for LJM Library in order to unit test 
        effectively. The new method is injected in the setUp and removed 
        in the tearDown to allow for running of individual test cases in 
        this group.
    """
    def eWriteName(self, handle, name, newVal):
        if name is "SYSTEM_REBOOT":
            self.reboot = newVal
        
    def setUp(self):
        self.reboot = 0
        self.lj = sblj.StarburstLJ("", "", "", "MOCK")
        
        self.o_eWriteName = ljm.eWriteName
        
        ljm.eWriteName = self.eWriteName
        
    def tearDown(self):
        ljm.eWriteName = self.o_eWriteName
        
    def test_rebootChangesRebootValue(self):
        self.lj.reboot()
        
        self.assertEqual(self.reboot, 0x4C4A0000)
                          

"""
TestLONoiseLabJackModule Test Group Description:
    This group of tests makes sure that we can get/set the LO frequency 
    and that the settings are correct. 
    
    Test Count: 4
"""
class TestLONoiseLabJackModule(unittest.TestCase):
    """
        Monkey patching methods for LJM Library in order to unit test 
        effectively. The new method is injected in the setUp and removed 
        in the tearDown to allow for running of individual test cases in 
        this group.
    """
    def eReadName(self, handle, name):
        return self.mockLabJackValues[name]
        
    def eReadNameString(self, handle, name):
        return self.mockLabJackValues[name]
        
    def eWriteName(self, handle, name, newVal):
        self.mockLabJackValues[name] = newVal
        
    def eWriteNameString(self, handle, name, newVal):
        self.mockLabJackValues[name] = newVal
    
    def setUp(self):
        """
            Dictionary of values that the mock LabJack will return for 
            call with names corresponding to the keys of the dictionary.
        """
        self.mockLabJackValues = {'TEMPERATURE_DEVICE_K': 300,
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
                                  'SERIAL_NUMBER': 1000}
        
        self.lj = sblj.LONoiseLJ("","","","MOCK")
        
        self.o_eReadName = ljm.eReadName
        self.o_eReadNameString = ljm.eReadNameString
        self.o_eWriteName = ljm.eWriteName
        self.o_eWriteNameString = ljm.eWriteNameString
        
        ljm.eReadName = self.eReadName
        ljm.eReadNameString = self.eReadNameString
        ljm.eWriteName = self.eWriteName
        ljm.eWriteNameString = self.eWriteNameString
        
    def tearDown(self):
        ljm.eReadName = self.o_eReadName
        ljm.eReadNameString = self.o_eReadNameString
        ljm.eWriteName = self.o_eWriteName
        ljm.eWriteNameString = self.o_eWriteNameString
    
    """
    Test - test_allLOFreqAreCorrespondinglyCorrect:
        Given that we set the LO level,
        Then, the two bits that communicate with the daughter board are set 
            accordingly and getting the variables match our constant names.
    """
    def test_allLOFreqAreCorrespondinglyCorrect(self):
        """
            Testing 3.4GHz.
        """
        self.lj.setLOFreq(sblj.LOFreqConstants.LO_3_4GHZ)
        dict = self.lj.getParams(["LOFREQ"])
        
        self.assertEqual(self.mockLabJackValues["EIO4"], 0)
        self.assertEqual(self.mockLabJackValues["EIO3"], 0)
        self.assertEqual("LO_3_4GHZ", dict["LOFREQ"])
        
        """
            Testing 7.5GHz.
        """
        self.lj.setLOFreq(sblj.LOFreqConstants.LO_7_5GHZ)
        dict = self.lj.getParams(["LOFREQ"])
        
        self.assertEqual(self.mockLabJackValues["EIO4"], 0)
        self.assertEqual(self.mockLabJackValues["EIO3"], 1)
        self.assertEqual("LO_7_5GHZ", dict["LOFREQ"])
        
        """
            Testing 11.5GHz.
        """
        self.lj.setLOFreq(sblj.LOFreqConstants.LO_11_5GHZ)
        dict = self.lj.getParams(["LOFREQ"])
        
        self.assertEqual(self.mockLabJackValues["EIO4"], 1)
        self.assertEqual(self.mockLabJackValues["EIO3"], 0)
        self.assertEqual("LO_11_5GHZ", dict["LOFREQ"])
        
        """
            Testing 15.5GHz.
        """
        self.lj.setLOFreq(sblj.LOFreqConstants.LO_15_5GHZ)
        dict = self.lj.getParams(["LOFREQ"])
        
        self.assertEqual(self.mockLabJackValues["EIO4"], 1)
        self.assertEqual(self.mockLabJackValues["EIO3"], 1)
        self.assertEqual("LO_15_5GHZ", dict["LOFREQ"])
    
    """
    Test - test_onOffNoiseSource:
        Given that we turn on/off the noise source, 
        Then the corresponding register is changed accordingly
    """
    def test_onOffNoiseSource(self):
        self.lj.setNoiseSourceOn()
        self.assertEqual(self.mockLabJackValues["EIO0"], 1)
        
        self.lj.setNoiseSourceOff()
        self.assertEqual(self.mockLabJackValues["EIO0"], 0)
    
    """
    Test - test_getParamsReturnsCorrectValues:
        Given that the LMJ library calls work, 
        Then we can get parameters relating to both the generic and 
            LO/Noise Source modules.
    """
    def test_getParamsReturnsCorrectValues(self):
        dict = self.lj.getParams()
        
        """
            Check a couple default values, then check that 
            noise source status and LO level is returned 
            from the call.
        """
        self.assertEqual(dict["NAME"], "MockLabJack")
        self.assertEqual(dict["LJTEMP"], 300)
        
        self.assertEqual(dict["LOFREQ"], "LO_3_4GHZ")
        self.assertEqual(dict["NSSTAT"], 0)
    
    """
    Test - test_throwExceptionWhenDisconnectOrInvalid:
        Given that we call getParams with an invalid key,
        Then a KeyError is raised.
        
        Given that we are not connected to a LabJack module,
        Then when we call getParams, a NoConnectionError is raised.
    """
    def test_throwExceptionWhenDisconnectOrInvalid(self):
        self.assertRaises(KeyError, self.lj.getParams, ["FAKEKEY"])
        
        self.lj.disconnect()
        self.assertRaises(sblj.NoConnectionError, self.lj.getParams)
    

"""
TestAntennaLabJackModule Test Group Description:
    This group of tests makes sure that the methods for the AntennaLJ
    work properly.
    
    Test Count: 4
"""    
class TestAntennaLabJackModule(unittest.TestCase):
    """
        Monkey patching methods for LJM Library in order to unit test 
        effectively. The new method is injected in the setUp and removed 
        in the tearDown to allow for running of individual test cases in 
        this group.
    """
    def eReadName(self, handle, name):
        return self.mockLabJackValues[name]
        
    def eReadNameString(self, handle, name):
        return self.mockLabJackValues[name]
        
    def eWriteName(self, handle, name, newVal):
        self.mockLabJackValues[name] = newVal
        
    def eWriteNameString(self, handle, name, newVal):
        self.mockLabJackValues[name] = newVal
    
    def setUp(self):
        """
            Dictionary of values that the mock LabJack will return for 
            call with names corresponding to the keys of the dictionary.
        """
        self.mockLabJackValues = {'TEMPERATURE_DEVICE_K': 300,
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
                                  "CIO0": 0,
                                  "CIO1": 0,
                                  "CIO2": 0,
                                  "CIO3": 0,
                                  "FIO0": 1,
                                  "FIO1": 1,
                                  "FIO2": 1,
                                  "FIO3": 1,
                                  "FIO4": 1,
                                  "FIO5": 1,
                                  'DEVICE_NAME_DEFAULT': 'MockLabJack',
                                  'SERIAL_NUMBER': 1000}
        
        self.o_eReadName = ljm.eReadName
        self.o_eReadNameString = ljm.eReadNameString
        self.o_eWriteName = ljm.eWriteName
        self.o_eWriteNameString = ljm.eWriteNameString
        
        ljm.eReadName = self.eReadName
        ljm.eReadNameString = self.eReadNameString
        ljm.eWriteName = self.eWriteName
        ljm.eWriteNameString = self.eWriteNameString
        
        self.lj = sblj.AntennaLJ("","","","MOCK")
        
    def tearDown(self):
        ljm.eReadName = self.o_eReadName
        ljm.eReadNameString = self.o_eReadNameString
        ljm.eWriteName = self.o_eWriteName
        ljm.eWriteNameString = self.o_eWriteNameString
    
    """
    Test - test_getParamsReturnsCorrectValues:
        Given that the LMJ library calls work, 
        Then we can get parameters relating to both the generic and 
            AntennaLJ modules.
    """
    def test_getParamsReturnsCorrectValues(self):
        dict = self.lj.getParams()
        
        self.assertEqual(dict["NAME"], "MockLabJack")
        self.assertEqual(dict["LJTEMP"], 300)
        
        self.assertEqual(dict["HIPOW"], -24)
        self.assertEqual(dict["HQPOW"], -24)
        self.assertEqual(dict["VIPOW"], -24)
        self.assertEqual(dict["VQPOW"], -24)
        self.assertEqual(dict["HITEMP"], 211)
        self.assertEqual(dict["HQTEMP"], 211)
        self.assertEqual(dict["VITEMP"], 211)
        self.assertEqual(dict["VQTEMP"], 211)
        self.assertEqual(dict["VNSSEL"], 0)
        self.assertEqual(dict["HNSSEL"], 0)
        self.assertEqual(dict["HIATTEN"], 31.5)
        self.assertEqual(dict["HQATTEN"], 31.5)
        self.assertEqual(dict["VIATTEN"], 31.5)
        self.assertEqual(dict["VQATTEN"], 31.5)
        
        for i in range(0, 6):
            self.assertEqual(self.mockLabJackValues["FIO" + str(i)], 1)
    
    """
    Test - test_setAttenuatorSetsValueCorrectly:
        Given that we set the attenuators to certain values,
        Then the attenuators should be set to the first 0.5 increment 
            larger than the given value if the value is less than 31.5
    """
    def test_setAttenuatorSetsValueCorrectly(self):
        """
            Check that we are always rounding up.
        """
        self.lj.setAttenuator(10.01, ["VQ"])
        dict = self.lj.getParams()
        self.assertEqual(dict["VQATTEN"], 10.5)
        
        """
            Check that we do not round if not necessary.
        """
        self.lj.setAttenuator(9, ["HQ"])
        dict = self.lj.getParams()
        self.assertEqual(dict["HQATTEN"], 9)
        
        """
            Check that large values cap at 31.5
        """
        self.lj.setAttenuator(100, ["HI"])
        dict = self.lj.getParams()
        self.assertEqual(dict["HIATTEN"], 31.5)
        
        """
            Check that 0.5 works.
        """
        self.lj.setAttenuator(0.5, ["VI"])
        dict = self.lj.getParams()
        self.assertEqual(dict["VIATTEN"], 0.5)
    
    """
    Test - test_rfNoiseSourceSelection:
        Given that we change to either RF or Noise Source,
        Then this is reflected in the pin-out values on the LabJacks.
    """
    def test_rfNoiseSourceSelection(self):
        """
            Select noise source.
        """
        self.lj.selectNoiseSource()
        dict = self.lj.getParams()
        self.assertEqual(dict["VNSSEL"], 1)
        self.assertEqual(dict["HNSSEL"], 1)
        
        """
            Select RF source.
        """
        self.lj.selectRFSource()
        dict = self.lj.getParams()
        self.assertEqual(dict["VNSSEL"], 0)
        self.assertEqual(dict["HNSSEL"], 0)
    
    """
    Test - test_throwExceptionWhenDisconnectOrInvalid:
        Given that we call getParams with an invalid key,
        Then a KeyError is raised.
        
        Given that we are not connected to a LabJack module,
        Then when we call getParams, a NoConnectionError is raised.
    """
    def test_throwExceptionWhenDisconnectOrInvalid(self):
        self.assertRaises(KeyError, self.lj.getParams, ["FAKEKEY"])
        
        self.lj.disconnect()
        self.assertRaises(sblj.NoConnectionError, self.lj.getParams)
        
        
"""
Main Method
"""    
if __name__ == '__main__':
    testGroups = [TestGenericLabJackGetParams, TestGenericLabJackConnections,
                  TestGenericLabJackReboot, TestGenericLabJackName, 
                  TestLONoiseLabJackModule, TestAntennaLabJackModule]
    for tG in testGroups:
        print "\nTesting: " + str(tG.__name__)
        suite = unittest.TestLoader().loadTestsFromTestCase(
            tG)
        unittest.TextTestRunner(verbosity=2).run(suite)