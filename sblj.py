"""
    STARBURST LabJack Control Wrapper Library
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

from labjack import ljm
import datetime
import sbljconstants as const
import copy
import math

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
Class: InvalidLOFreqError extends Exception
    Description:
        Custom error for checking that a given LO setting is valid when trying
        to change.
"""
class InvalidLOFreqError(Exception):
    def __str__(self):
        return("Please refer to sbljconstant.py for LO frequency constants," +
               " or documentation for usage.")
"""
Class: StarburstLJ extends Object
    Description: 
        Custom object that represents a single generic LabJack unit 
        used in the Starburst project.
    Arguments: 
        identifier: string representation of an identification for designated
            LabJack. This can be a serial number, an ip address, or a name. 
            Names cannot contain periods. Default value set to "ANY" to allow 
            for any LabJack to be chosen.
        connectionType: string representation of how the LabJack is connected 
            to the computer. Can be "ETHERNET", "USB", "TCP", "ANY", or other 
            connection types supported by the LabJack LMJ library. (Refer to 
            their documentation for details.) Default value set to "ETHERNET".
        deviceType: string representation of LabJack device. Can be "T7", 
            "ANY", or other types supported by the LabJack LMJ library. 
            (Refer to their documentation for details.) Default value set 
            to "T7".
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
        LabJack Parameters across generic modules:
            LJTEMP: Temperature of the CPU unit of the LabJack in Kelvin.
            LJAIRTEMP: Temperature of the surrounding environment 
                of the LabJack in Kelvin.
            24V: Voltage reading of the +24V input power in volts.
            15V: Voltage reading of the +15V input power in volts.
            12V: Voltage reading of the +12V input power in volts.
            5V: Voltage reading of the +5V input power in volts.
            S5V: Voltage reading of switched +5V input power in volts.
            NEG5V: Voltage reading of the -5V input power in volts.
            NAME: Name of LabJack device. (Can be used as identifier.)
        """
        self.ljVariables = ["LJTEMP", "LJAIRTEMP", "24V", "15V", "12V", "5V", 
                            "NEG5V", "NAME", "S5V"]
    
    """
        Private getter methods to retrieve specific parameters. Do NOT use 
        these methods without its wrapper getParamsiables since these 
        are not error checked.
    """
    def __getLJTemp(self):
        temp = ljm.eReadName(self.handle, "TEMPERATURE_DEVICE_K")
        return temp
    def __getLJAirTemp(self):
        temp = ljm.eReadName(self.handle, "TEMPERATURE_AIR_K")
        return temp
    def __get24V(self):
        volt = ljm.eReadName(self.handle, "AIN4") * 3
        return volt
    def __get15V(self):
        volt = ljm.eReadName(self.handle, "AIN5") * 2
        return volt
    def __get12V(self):
        volt = ljm.eReadName(self.handle, "AIN6") * 2
        return volt
    def __get5V(self):
        volt = ljm.eReadName(self.handle, "AIN7")
        return volt
    def __getN5V(self):
        volt = ljm.eReadName(self.handle, "AIN9")
        return volt
    def __getName(self):
        name = ljm.eReadNameString(self.handle, "DEVICE_NAME_DEFAULT")
        return name
    def __getS5V(self):
        volt = ljm.eReadName(self.handle, "AIN8")
        return volt
        
    """
        Dictionary lookup for parameters (Placed here because the 
        corresponding methods that are pointed to must be defined first.)
    """
    ljVarDict = {'LJTEMP': __getLJTemp, 'LJAIRTEMP': __getLJAirTemp,
                 '24V': __get24V, '15V': __get15V, '12V': __get12V, 
                 '5V': __get5V, 'NEG5V': __getN5V, 'NAME': __getName,
                 'S5V': __getS5V}
     
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
    Method: getParams(variables)
        Description: 
            Main query to LabJack modules for hardware information. 
        Arguments: 
            variables: a list of keys from ljVarDict of which the 
                corresponding parameter should be measured and returned.
        Returns:
            varDump: a dictionary with each element from variables as a key 
                and the corresponding measurement as the value.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                LabJack unit.
            KeyError occurs when designated key is non-existent.
    """
    def getParams(self, variables=None):
        if self.handle is not None:
            varDump = {'TIMESTAMP': str(datetime.datetime.utcnow())}
            if variables is None:
                variables = self.ljVariables
            
            for var in variables:
                varDump[var] = self.ljVarDict[var](self)
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
        

"""
Class: LONoiseLJ extends StarburstLJ
    Description:
        Custom object that represents a LO/Noise Source LabJack control unit
        used in the Starburst project.
    Arguments:
        (Same as those of StarburstLJ. Refer to the description above.)
    Raises:
        (Same as those of StarburstLJ. Refer to the description above.)
"""        
class LONoiseLJ(StarburstLJ):   
    def __init__(self, identifier="ANY", connectionType="ETHERNET", 
                 deviceType="T7", handle=None):
        super(LONoiseLJ, self).__init__(identifier, connectionType,
                                        deviceType, handle)
        
        """
        LabJack Parameters across LO/Noise Source modules
            LOFREQ: Current set LO setting.
            NSSTATUS: On/Off status of noise source (0=off, 1=on).
        """        
        self.ljLOVariables = ["LOFREQ", "NSSTAT"]
        self.ljVariables.extend(self.ljLOVariables)
        self.LOConstantNames = {value: name for name, 
                                value in vars(const.LOFreqConst).items() 
                                if name.isupper()}
                                        
    """
        Private getter methods to retrieve specific parameters. Do NOT use 
        these methods without its wrapper getParamsiables since these 
        are not error checked.
    """
    def __getLOFreq(self):
        rightBit = ljm.eReadName(self.handle, "EIO3")
        leftBit = ljm.eReadName(self.handle, "EIO4")
        
        setting = leftBit * 2 + rightBit
        freqName = self.LOConstantNames[setting]
        return freqName
    def __getNSStatus(self):
        status = ljm.eReadName(self.handle, "EIO0")
        return status
        
    """
        Dictionary lookup for parameters (Placed here because the 
        corresponding methods that are pointed to must be defined first.)
    """
    ljLOVarDict = {'LOFREQ': __getLOFreq, 'NSSTAT': __getNSStatus}

    """
        Private LO frequency setting methods. Do NOT call these methods 
        directly, instead, use the setLOFreq method. These methods are
        not error checked. 
    """
    def __setFreq(self, leftBit, rightBit):
        ljm.eWriteName(self.handle, "EIO3", rightBit)
        ljm.eWriteName(self.handle, "EIO4", leftBit)   
    def __3_4GHZ(self):
        self.__setFreq(0, 0)
    def __7_5GHZ(self):
        self.__setFreq(0, 1)  
    def __11_5GHZ(self):
        self.__setFreq(1, 0)
    def __15_5GHZ(self):
        self.__setFreq(1, 1)
    
    """
        Dictionary lookup for LO settings and corresponding methods.
    """
    ljLODict = {const.LOFreqConst.LO_3_4GHZ: __3_4GHZ, 
                const.LOFreqConst.LO_7_5GHZ: __7_5GHZ,
                const.LOFreqConst.LO_11_5GHZ: __11_5GHZ, 
                const.LOFreqConst.LO_15_5GHZ: __15_5GHZ}
    
    """
    Method: setLOFreq(freq)
        Description:
            Sets the LO frequency to the desired level.
        Arguments:
            freq: a frequency option defined in sbljconstants.py. Please refer
                there for the constant values.
        Raises:
            InvalidLOFreqError: occurs when freq is not a defined frequency 
                option from sbljconstants.py.
            NoConnectionError: occurs when there is no connection to the
                LabJack unit.
            
    """
    def setLOFreq(self, freq):
        if self.handle is not None:
            try:
                LONoiseLJ.ljLODict[freq](self)
            except KeyError:
                raise InvalidLOFreqError()
        else:
            raise NoConnectionError(self.identifier)
       
       
    """
    Method: setNoiseSourceOn
        Description:
            Turns the noise source on the LO/Noise Source board on entirely.
        Raises:
            NoConnectionError: occurs when there is no connection to the
                LabJack unit.
    """
    def setNoiseSourceOn(self):
        if self.handle is not None:
            ljm.eWriteName(self.handle, "EIO0", 1)
        else:
            raise NoConnectionError(self.identifier)
    
    """
    Method: setNoiseSourceOff
        Description:
            Turns the noise source on the LO/Noise Source board off entirely.
        Raises:
            NoConnectionError: occurs when there is no connection to the
                LabJack unit.
    """
    def setNoiseSourceOff(self):
        if self.handle is not None:
            ljm.eWriteName(self.handle, "EIO0", 0)
        else:
            raise NoConnectionError(self.identifier)
            
    """
    Method: getParams(variables)
        Description: 
            Main query to LabJack modules for hardware information. 
        Arguments: 
            variables: a list of keys from ljVarDict of which the 
                corresponding parameter should be measured and returned.
        Returns:
            varDump: a dictionary with each element from variables as a key 
                and the corresponding measurement as the value.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                LabJack unit.
            KeyError occurs when designated key is non-existent.
    """
    def getParams(self, variables=None):
        if self.handle is not None:
            if variables is None:
                variables = self.ljVariables
                
            cpy = copy.copy(variables)
            varDump = {}
        
            for var in self.ljLOVariables:
                if var in cpy:
                    varDump[var] = self.ljLOVarDict[var](self)
                    cpy.remove(var)
                
            varDump.update(super(LONoiseLJ, self).getParams(cpy))
            return varDump
            
        else:
            raise NoConnectionError(self.identifier)
            

"""
Class: AntennaLJ extends StarburstLJ
    Description:
        Custom object that represents a Antenna LabJack control unit
        used in the Starburst project.
    Arguments:
        (Same as those of StarburstLJ. Refer to the description above.)
    Raises:
        (Same as those of StarburstLJ. Refer to the description above.)
"""            
class AntennaLJ(StarburstLJ):
    def __init__(self, identifier="ANY", connectionType="ETHERNET", 
                 deviceType="T7", handle=None):
        super(AntennaLJ, self).__init__(identifier, connectionType,
                                        deviceType, handle)
        
        """
        LabJack Parameters across Antenna modules
            VQPOW: IF Power to the Q component of the Vertical polarization 
                given in dBm.
            VIPOW: IF Power to the I component of the Vertical polarization
                given in dBm.
            HQPOW: IF Power to the Q component of the Horizontal polarization
                given in dBm.
            HIPOW: IF Power to the I component of the Horizontal polarization
                given in dBm.
            VQTEMP: Temperature of Q component of the Vertical polarization
                given in degrees Celsius.
            VITEMP: Temperature of I component of the Vertical polarization
                given in degrees Celsius.
            HQTEMP: Temperature of Q component of the Horizontal polarization
                given in degrees Celsius.
            HITEMP: Temperature of I component of the Horizontal polarization
                given in degrees Celsius.
            VQATTEN: Attenuation settings for the Q of Vertical polarization
                given in dB.
            VIATTEN: Attenuation settings for the I of Vertical polarization
                given in dB.
            HQATTEN: Attenuation settings for the Q of Horizontal polarization
                given in dB.
            HIATTEN: Attenuation settings for the I of Horizontal polarization
                given in dB.
            VNSSEL: Noise source selection for Vertical polarization 
                (0=antenna, 1=noise source).
            HNSSEL: Noise source selection for Horizontal polarization 
                (0=antenna, 1=noise source).
            
        """        
        self.ljAVariables = ["VQPOW", "VIPOW", "HQPOW", "HIPOW",
                             "VQTEMP", "VITEMP", "HQTEMP", "HITEMP",
                             "VQATTEN", "VIATTEN", "HQATTEN", "HIATTEN",
                             "VNSSEL", "HNSSEL"]
        self.ljVariables.extend(self.ljAVariables)
        
        """
        Ghost copy of attenuations for each component
        """
        self.vqAtt = 31.5
        self.viAtt = 31.5
        self.hqAtt = 31.5
        self.hiAtt = 31.5
        
        self.setAttenuator(31.5)
        
    """
        Private attenuator methods. Do NOT call these methods directly, 
        instead, use the setAttenuator methods to do so. (These methods
        are not error checked.)
    """
    def __setUpAttenuations(self, val):
        attDict = {1: "FIO1", 2: "FIO2", 3: "FIO3", 4: "FIO4", 5: "FIO5"}
        
        if val > 31:
            newVal = 63
        else:
            newVal = math.ceil(val * 2)
            
        temp = newVal / 2.0
            
        if newVal % 2 == 1:
            ljm.eWriteName(self.handle, "FIO0", 1)
            newVal = (newVal - 1) / 2
        
        for i in range(1, 6):
            ljm.eWriteName(self.handle, attDict[i], newVal % 2)
            newVal /= 2
            
        return temp
            
    def __turnOffAllLatches(self):
        ljm.eWriteName(self.handle, "CIO0", 0)
        ljm.eWriteName(self.handle, "CIO1", 0)
        ljm.eWriteName(self.handle, "CIO2", 0)
        ljm.eWriteName(self.handle, "CIO3", 0)
    def __VQAttenLatch(self, newVal):
        ljm.eWriteName(self.handle, "CIO0", 1)
        self.__turnOffAllLatches()
        self.vqAtt = newVal
    def __VIAttenLatch(self, newVal):
        ljm.eWriteName(self.handle, "CIO1", 1)
        self.__turnOffAllLatches()
        self.viAtt = newVal
    def __HQAttenLatch(self, newVal):
        ljm.eWriteName(self.handle, "CIO2", 1)
        self.__turnOffAllLatches()
        self.hqAtt = newVal
    def __HIAttenLatch(self, newVal):
        ljm.eWriteName(self.handle, "CIO3", 1)
        self.__turnOffAllLatches()
        self.hiAtt = newVal
        
    """
        Dictionary for attenuator method setups.
    """
    attDict = {'VQ': __VQAttenLatch, 
               'VI': __VIAttenLatch,  
               'HQ': __HQAttenLatch, 
               'HI': __HIAttenLatch}
        
    """
        Private getter methods to retrieve specific parameters. Do NOT use 
        these methods without its wrapper getParamsiables since these 
        are not error checked.
    """
    def __getVQPow(self):
        pow = ljm.eReadName(self.handle, "AIN3")
        pow = 24 - 40 * pow
        return pow
    def __getVIPow(self):
        pow = ljm.eReadName(self.handle, "AIN2")
        pow = 24 - 40 * pow
        return pow
    def __getHQPow(self):
        pow = ljm.eReadName(self.handle, "AIN1")
        pow = 24 - 40 * pow
        return pow
    def __getHIPow(self):
        pow = ljm.eReadName(self.handle, "AIN0")
        pow = 24 - 40 * pow
        return pow
    def __getVQTemp(self):
        temp = ljm.eReadName(self.handle, "AIN13")
        temp = 478 * temp - 267
        return temp
    def __getVITemp(self):
        temp = ljm.eReadName(self.handle, "AIN12")
        temp = 478 * temp - 267
        return temp
    def __getHQTemp(self):
        temp = ljm.eReadName(self.handle, "AIN11")
        temp = 478 * temp - 267
        return temp
    def __getHITemp(self):
        temp = ljm.eReadName(self.handle, "AIN10")
        temp = 478 * temp - 267
        return temp
    def __getVQAtt(self):
        return self.vqAtt
    def __getVIAtt(self):
        return self.viAtt
    def __getHQAtt(self):
        return self.hqAtt
    def __getHIAtt(self):
        return self.hiAtt
    def __getVNoiseSel(self):
        sel = ljm.eReadName(self.handle, "EIO2")
        return sel
    def __getHNoiseSel(self):
        sel = ljm.eReadName(self.handle, "EIO1")
        return sel
        
    """
        Dictionary lookup for parameters (Placed here because the 
        corresponding methods that are pointed to must be defined first.)
    """
    ljAVarDict = {'VQPOW': __getVQPow, 'VIPOW': __getVIPow, 
                  'HQPOW': __getHQPow, 'HIPOW': __getHIPow,
                  'VQTEMP': __getVQTemp, 'VITEMP': __getVITemp,
                  'HQTEMP': __getHQTemp, 'HITEMP': __getHITemp,
                  'VQATTEN': __getVQAtt, 'VIATTEN': __getVIAtt,
                  'HQATTEN': __getHQAtt, 'HIATTEN': __getHIAtt,
                  'VNSSEL': __getVNoiseSel, 'HNSSEL': __getHNoiseSel}
    
    """
    Method: getParams(variables)
        Description: 
            Main query to LabJack modules for hardware information. 
        Arguments: 
            variables: a list of keys from ljVarDict of which the 
                corresponding parameter should be measured and returned.
        Returns:
            varDump: a dictionary with each element from variables as a key 
                and the corresponding measurement as the value.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                LabJack unit.
            KeyError occurs when designated key is non-existent.
    """
    def getParams(self, variables=None):
        if self.handle is not None:
            if variables is None:
                variables = self.ljVariables
                
            cpy = copy.copy(variables)
            varDump = {}
        
            for var in self.ljAVariables:
                if var in cpy:
                    varDump[var] = self.ljAVarDict[var](self)
                    cpy.remove(var)
                
            varDump.update(super(AntennaLJ, self).getParams(cpy))
            return varDump
            
        else:
            raise NoConnectionError(self.identifier)
    
    """
    Method setAttenuator(val, list)
        Description:
            Sets attenuators to the smallest 0.5 increment larger than val.
                This is capped at 31.5dB due to hardware.
        Arguments:
            val: value to set attenuators to.
            list: list of which attenuators to set.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                LabJack unit.
            KeyError occurs when designated attenuator is non-existent.
            
    """
    def setAttenuator(self, val, list=["VQ","VI","HQ","HI"]):
        if self.handle is not None:
            newVal = self.__setUpAttenuations(val)
                           
            for input in list:
                self.attDict[input](self, newVal)
                
        else:
            raise NoConnectionError(self.identifier)
    
    """
    Method selectNoiseSource(list)
        Description: 
            Selects noise source as input for the polarizations in list.
        Arguments:
            list: list of polarizations to select noise source for.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                LabJack unit.
    """
    def selectNoiseSource(self, list=["H","V"]):
        if self.handle is not None:
            if "H" in list:
                ljm.eWriteName(self.handle, "EIO1", 1)
            if "V" in list:
                ljm.eWriteName(self.handle, "EIO2", 1)
        else:
            raise NoConnectionError(self.identifier)
    
    """
    Method selectRFSource(list)
        Description: 
            Selects RF as input for the polarizations in list.
        Arguments:
            list: list of polarizations to select RF for.
        Raises:
            NoConnectionError: occurs when there is no connection to the 
                LabJack unit.
    """
    def selectRFSource(self, list=["H","V"]):
        if self.handle is not None:
            if "H" in list:
                ljm.eWriteName(self.handle, "EIO1", 0)
            if "V" in list:
                ljm.eWriteName(self.handle, "EIO2", 0)
        else:
            raise NoConnectionError(self.identifier)