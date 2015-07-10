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
    
    Test Count: 7
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
                         'AIN9': -5}
    
    """
    Monkey patching method for LJM Library in order to unit test effectively.
    The new method is injected in the setUp and removed in the tearDown to 
    allow for running of individual test cases in this group.
    """
    def eReadName(self, handle, name):
        return self.mockLabJackValues[name]
    
    def setUp(self):
        self.lj = sblj.StarburstLJ("ANY","ANY","ANY","MOCK")
        
        self.o_eReadName = ljm.eReadName
        ljm.eReadName = self.eReadName
        
    def tearDown(self):
        ljm.eReadName = self.o_eReadName
    
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
TestGenericLabJackConnections Test Group Description:
    This group of tests makes sure that exceptions are thrown when connections
    to LabJacks are not made or cannot be made.
    
    Test Count: 1
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
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(
        TestGenericLabJackConnections)
    unittest.TextTestRunner(verbosity=2).run(suite)
        
        


