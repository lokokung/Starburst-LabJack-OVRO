"""
    STARBURST LabJack Control Wrapper Library Test Suite
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import unittest
from labjack import ljm
import sblj

"""
TestGenericLabJackMonitorVars Test Group Description:
    This group of tests makes sure that given that the LJM library correctly
    returns values on a LabJack with given names, that the getLJMonitorVar
    function returns the correct output. 
    
    Test Count: 8
"""
class TestGenericLabJackMonitorVars(unittest.TestCase):
    """
        Dictionary of values that the mock LabJack will return for call with 
        names corresponding to the keys of the dictionary.
    """
    mockLabJackValues = {'TEMPERATURE_DEVICE_K': 300,
                         'TEMPERATURE_AIR_K': 298,
                         'AIN4': 8,
                         'AIN5': 7.5,
                         'AIN6': 6,
                         'AIN7': 5,
                         'AIN9': -5,
                         'DEVICE_NAME_DEFAULT': 'MockLabJack'}
    
    """
        Monkey patching method for LJM Library in order to unit test 
        effectively. The new method is injected in the setUp and removed 
        in the tearDown to allow for running of individual test cases in 
        this group.
    """
    def eReadName(self, handle, name):
        return self.mockLabJackValues[name]
        
    def eReadNameString(self, handle, name):
        return self.mockLabJackValues[name]
    
    def setUp(self):
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
        Then getLJMonitorVar(["LJTEMP"]) returns 300,
        And a time stamp is returned.
    """
    def test_temperatureOfLabJack(self):
        dict = self.lj.getLJMonitorVar(["LJTEMP"])
        self.assertEqual(dict["LJTEMP"], 300)
        self.assertTrue(dict.has_key("TIMESTAMP"))
    
    """
    Test - test_temperatureOfEnvironment:
        Given that the mock LabJack environment has a temperature of 298,
        Then getLJMonitorVar(["LJAIRTEMP"]) returns 298,
        And a time stamp is returned.
    """
    def test_temperatureOfEnvironment(self):
        dict = self.lj.getLJMonitorVar(["LJAIRTEMP"])
        self.assertEqual(dict["LJAIRTEMP"], 298)
        self.assertTrue(dict.has_key("TIMESTAMP"))
    
    """
    Test - test_24V:
        Given that the AIN4 on the LabJack has a voltage of 8,
        Then getLJMonitorVar(["24V"]) returns 24,
        And a time stamp is returned.
    """
    def test_24V(self):
        dict = self.lj.getLJMonitorVar(["24V"])
        self.assertEqual(dict["24V"], 24)
        self.assertTrue(dict.has_key("TIMESTAMP"))
        
    """
    Test - test_15V:
        Given that the AIN5 on the LabJack has a voltage of 7.5,
        Then getLJMonitorVar(["15V"]) returns 15,
        And a time stamp is returned.
    """
    def test_15V(self):
        dict = self.lj.getLJMonitorVar(["15V"])
        self.assertEqual(dict["15V"], 15)
        self.assertTrue(dict.has_key("TIMESTAMP"))
        
    """
    Test - test_12V:
        Given that the AIN6 on the LabJack has a voltage of 6,
        Then getLJMonitorVar(["12V"]) returns 12,
        And a time stamp is returned.
    """
    def test_12V(self):
        dict = self.lj.getLJMonitorVar(["12V"])
        self.assertEqual(dict["12V"], 12)
        self.assertTrue(dict.has_key("TIMESTAMP"))
        
    """
    Test - test_5V:
        Given that the AIN7 on the LabJack has a voltage of 5,
        Then getLJMonitorVar(["5V"]) returns 5,
        And a time stamp is returned.
    """
    def test_5V(self):
        dict = self.lj.getLJMonitorVar(["5V"])
        self.assertEqual(dict["5V"], 5)
        self.assertTrue(dict.has_key("TIMESTAMP"))
        
    """
    Test - test_neg5V:
        Given that the AIN9 on the LabJack has a voltage of -5,
        Then getLJMonitorVar(["NEG5V"]) returns -5,
        And a time stamp is returned.
    """
    def test_neg5V(self):
        dict = self.lj.getLJMonitorVar(["NEG5V"])
        self.assertEqual(dict["NEG5V"], -5)
        self.assertTrue(dict.has_key("TIMESTAMP"))

    """
    Test - test_name:
        Given that the LabJack's name is "MockLabJack",
        Then getLJMonitorVar(["NAME"]) returns "MockLabJack",
        And a time stamp is returned.
    """
    def test_name(self):
        dict = self.lj.getLJMonitorVar(["NAME"])
        self.assertEqual(dict["NAME"], "MockLabJack")
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
                          lj.getLJMonitorVar)
                          
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
        Monkey patching method for LJM Library in order to unit test 
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
        dict = self.lj.getLJMonitorVar(["NAME"])
        self.assertEqual(dict["NAME"], "MockLabJack")
        
        self.lj.setLJName("NewName")
        
        dict = self.lj.getLJMonitorVar(["NAME"])
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
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(
        TestGenericLabJackName)
    unittest.TextTestRunner(verbosity=2).run(suite)
        
        


