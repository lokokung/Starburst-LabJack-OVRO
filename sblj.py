"""
    STARBURST LabJack Control Wrapper Library
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

from labjack import ljm
import datetime

"""
Class: UnknownDeviceError extends Exception
    Description: 
        Custom error for handling in upper wrapper. Takes the LJMError 
        from the LabJack LJM Library and wraps it so that the device of 
        question can be easily identified. This error should indicates
        that the parameters passed to initiate a StarburstLJ object do 
        not correspond to any connected LabJacks.
"""
class UnknownDeviceError(Exception):
    def __init__(self, deviceType, connectionType, identifier, ljmError):
        self.deviceType = deviceType
        self.connectionType = connectionType
        self.identifier = identifier
        self.ljmError = ljmError
        
    def __str__(self):
        return ("Unable to connect to " + self.deviceType + " - " +
                self.identifier + " via " + self.connectionType + " due to " + 
                str(self.ljmError))

                
"""
Class: NoConnectionError extends Exception
    Description: 
        Custom error for checking that a giving StarburstLJ object has 
        a viable connection before trying to retrieve or send data.
"""                
class NoConnectionError(Exception):
    def __init__(self, identifier):
        self.identifier = identifier
        
    def __str__(self):
        return("There is no connection to device " + identifier)


"""
Class: StarburstLJ extends Object
    Description: 
        Custom object that represents a single generic LabJack unit 
        used in the Starburst project.
    Arguments: 
        identifier: string representation of an identification for designated
            LabJack. This can be a serial number, an ip address, or a name. Names
            cannot contain periods. Default value set to "ANY" to allow for any
            LabJack to be chosen.
        connectionType: string representation of how the LabJack is connected to 
            the computer. Can be "ETHERNET", "USB", "TCP", "ANY", or other 
            connection types supported by the LabJack LMJ library. (Refer to their
            documentation for details.) Default value set to "ETHERNET".
        deviceType: string representation of LabJack device. Can be "T7", "ANY", 
            or other types supported by the LabJack LMJ library. (Refer to their
            documentation for details.) Default value set to "T7".
        handle: LMJ handle object. The option to directly pass in the handle 
            object is used for unit testing. Otherwise, refrain from directly 
            passing the LMJ handle object.
    Raises:
        TypeError: occurs when given parameters are not strings.
        UnknownDeviceError: occurs when device description such as 
                identifier, deviceType, or connectionType, do not point to a
                valid LabJack module.
"""        
class StarburstLJ(object):
    """
        LabJack Parameters across generic modules:
            LJTEMP: Temperature of the CPU unit of the LabJack in Kelvin.
            LJAIRTEMP: Temperature of the surrounding environment 
                of the LabJack in Kelvin.
            24V: Voltage reading of the +24V input power in volts.
            15V: Voltage reading of the +15V input power in volts.
            12V: Voltage reading of the +12V input power in volts.
            5V: Voltage reading of the +5V input power in volts.
            NEG5V: Voltage reading of the -5V input power in volts.
            NAME: Name of LabJack device. (Can be used as identifier.)
    """
    ljVariables = ["LJTEMP", "LJAIRTEMP", "24V", "15V", "12V", "5V", 
                   "NEG5V", "NAME"]
    

    def __init__(self, identifier="ANY", connectionType="ETHERNET", 
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
        
        if handle is None: 
            self.handle = None
            self.connect()
        else: 
            self.handle = handle
    
    """
        Private getter methods to retrieve specific parameters. Do NOT use 
        these methods without its wrapper getLJMonitorVariables since these 
        are not error checked.
    """
    def __getLJTemp(self):
        temp = ljm.eReadName(self.handle, "TEMPERATURE_DEVICE_K")
        return temp
    def __getLJAirTemp(self):
        temp = ljm.eReadName(self.handle, "TEMPERATURE_AIR_K")
        return temp
    def __24V(self):
        volt = ljm.eReadName(self.handle, "AIN4") * 3
        return volt
    def __15V(self):
        volt = ljm.eReadName(self.handle, "AIN5") * 2
        return volt
    def __12V(self):
        volt = ljm.eReadName(self.handle, "AIN6") * 2
        return volt
    def __5V(self):
        volt = ljm.eReadName(self.handle, "AIN7")
        return volt
    def __N5V(self):
        volt = ljm.eReadName(self.handle, "AIN9")
        return volt
    def __getName(self):
        name = ljm.eReadNameString(self.handle, "DEVICE_NAME_DEFAULT")
        return name
        
    """
        Dictionary lookup for generic parameters (Placed here because the 
        corresponding methods that are pointed to must be defined first.)
    """
    ljVarDict = {'LJTEMP': __getLJTemp, 'LJAIRTEMP': __getLJAirTemp,
                 '24V': __24V, '15V': __15V, '12V': __12V, '5V': __5V,
                 'NEG5V': __N5V, 'NAME': __getName}
     
    """
    Method: connect()
        Description: 
            Connection method to establish connection with LabJack. Used in 
            in the initializer so that new StarburstLJ are connected by 
            default.
        Raises:
            UnknownDeviceError: occurs when device description such as 
                identifier, deviceType, or connectionType, do not point to a
                valid LabJack module.
    """
    def connect(self):
        try:
            self.handle = ljm.openS(self.deviceType, self.connectionType,
                                    self.identifier)
        except ljm.LJMError as e:
            self.handle = None
            raise UnknownDeviceError(self.deviceType, self.connectionType,
                                     self.identifier, e)
    
    """
    Method: disconnect()
        Description: 
            Disconnection method that closes all streams to the LabJack. After
            closing resources, the handle object is set to None to prevent 
            other methods from trying to hit the closed ports. The closed
            LabJack can be reconnected to using the connect() function above.
    """
    def disconnect(self):
        try:
            ljm.close(self.handle)
        except ljm.LJMError:
            pass
        finally:
            self.handle = None
    
    """
    Method: getLJMonitorVar(variables)
        Description: 
            Main query to LabJack modules for generic hardware 
            information. 
        Arguments: 
            variables: a list of keys from ljVarDict of which the 
                corresponding parameter should be measured and returned.
        Returns:
            varDump: a dictionary with each element from variables as a key 
                and the corresponding measurement as the value.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                LabJack unit.
    """
    def getLJMonitorVar(self, variables=ljVariables):
        if self.handle is not None:
            varDump = {'TIMESTAMP': str(datetime.datetime.utcnow())}
                       
            for var in variables:
                varDump[var] = StarburstLJ.ljVarDict[var](self)
            return varDump
        else:
            raise NoConnectionError(self.identifier)
            
    """
    Method: setLJName(name)
        Description:
            Used for setting an arbitrary name for the LabJack devices. This 
            name can then be used as an identifier for the LabJack. After 
            calling this method, a physical restart of the LabJack is 
            necessary in order for the changes to take place.
        Arguments:
            name: the new name that the LabJack should be assigned. Note that
                the LabJack itself limits the name to be at most 49 
                characters and cannot contain any periods. (This is checked
                before the name is assigned.)
        Raises:
            TypeError: occurs if name is not a string, has more than 49 
                characters, or includes periods.
            NoConnectionError: occurs when there is no connection to the
                LabJack unit.
    """
    def setLJName(self, name):
        name = str(name)
        if len(name) > 49 or "." in name:
            raise TypeError("Expected a string instead of " + 
                            str(type(name)) + 
                            " with less than 49 characters and no periods.")
        if self.handle is not None:
            ljm.eWriteNameString(self.handle, "DEVICE_NAME_DEFAULT",
                                 name)
        else:
            raise NoConnectionError(self.identifier)
        
        
class LONoiseLJ(StarburstLJ):
    def __init__(self, identifier="ANY", connectionType="ETHERNET", 
                 deviceType="T7", handle=None):
        super(LONoiseLJ, self).__init__(identifier, connectionType,
                                        deviceType, handle)
                                        
    