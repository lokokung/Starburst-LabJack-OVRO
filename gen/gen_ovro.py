"""
    STARBURST OVRO Item Struct Decomposition
    (Based on gen_schedule_sf.py)
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import struct

"""
Method: gen_ovro_sf()
    Description:
        Writes the ovro stateframe items from the ovro dictionary created 
        when the getMonitorData() method is called. Optionally creates the 
        corresponding XML file. Regardless of whether the XML file is 
        created, the file name to the XML will be returned
        (/tmp/ovro_stateframe.xml). 
        
        Even if supplied an empty dictionary, this routine will return 
        something sensible.
    Arguments:
        ovro_dict: dictionary returned by calling ovro.getMonitorData().
    Returns:
        buf: binary data buffer.
        fmt: format string.
        xmlFile: xml file path.
"""
def gen_ovro(ovro_dict, mk_xml=False):
    # Set up file name, format string, and buffer.
    xmlFile = r'tmp/ovro_stateframe.xml'
    fmt = '<'
    buf = ''
    
    # Append XML for Data cluster.
    if mk_xml:
        xml = open(xmlFile, 'w+')
        xml.write('<Cluster>\n')
        xml.write('<Name>Data</Name>\n')
        xml.write('<NumElts>3</NumElts>\n')
    
    # ======================================================================    
    # Start of LO/Noise Module dump.
    # ======================================================================
    dict = ovro_dict.get("LONOISE", {})
    
    # Append XML for LONoiseModule cluster.
    if mk_xml:
        xml.write('<Cluster>\n')
        xml.write('<Name>LONoiseModule</Name>\n')
        xml.write('<NumElts>12</NumElts>')
    
    # Handle all generic LabJack properties
    append_fmt, append_buf = __generic_labjack(dict, xml, mk_xml)
    fmt += append_fmt
    buf += append_buf
    
    # Handle LO/Noise source LabJack properties
    append_fmt, append_buf = __lonoise_labjack(dict, xml, mk_xml)
    fmt += append_fmt
    buf += append_buf
    
    # ----------------------------------------------------------------------
    # End of LO/Noise Module parsing.
    if mk_xml:
        xml.write('</Cluster>\n')
        
    # ======================================================================    
    # Start of AntennaA Module dump.
    # ======================================================================
    dict = ovro_dict.get("A", {})
    
    # Append XML for LONoiseModule cluster.
    if mk_xml:
        xml.write('<Cluster>\n')
        xml.write('<Name>AntennaAModule</Name>\n')
        xml.write('<NumElts>24</NumElts>')
        
    # Handle all generic LabJack properties
    append_fmt, append_buf = __generic_labjack(dict, xml, mk_xml)
    fmt += append_fmt
    buf += append_buf
    
    # Handle Antenna A LabJack properties
    append_fmt, append_buf = __antenna_labjack(dict, xml, mk_xml)
    fmt += append_fmt
    buf += append_buf
    
    # ----------------------------------------------------------------------
    # End of AntennaA Module parsing.
    if mk_xml:
        xml.write('</Cluster>\n')
        
    # ======================================================================    
    # Start of AntennaB Module dump.
    # ======================================================================
    dict = ovro_dict.get("B", {})
    
    # Append XML for LONoiseModule cluster.
    if mk_xml:
        xml.write('<Cluster>\n')
        xml.write('<Name>AntennaBModule</Name>\n')
        xml.write('<NumElts>24</NumElts>')
        
    # Handle all generic LabJack properties
    append_fmt, append_buf = __generic_labjack(dict, xml, mk_xml)
    fmt += append_fmt
    buf += append_buf
    
    # Handle Antenna B LabJack properties
    append_fmt, append_buf = __antenna_labjack(dict, xml, mk_xml)
    fmt += append_fmt
    buf += append_buf
    
    # ----------------------------------------------------------------------
    # End of AntennaB Module parsing.
    if mk_xml:
        xml.write('</Cluster>\n')
        
    # ======================================================================
    # Wrap up end of parsing.
    if mk_xml:
        xml.write('</Cluster>')
        xml.close()
    # ======================================================================    
    
    return fmt, buf, xmlFile
    
def __generic_labjack(dict, xml, mk_xml):
    # Initialize
    fmt = ""
    buf = ""
    
    #----------------------------------------------------------------------
    # Name of LabJack (length 49 array of characters)
    # ----------------------------------------------------------------------
    
    # Define array dimensions
    fmt += 'I'
    buf += struct.pack('I', 49)
    item = dict.get("NAME", "")
    
    # Pack name as string of characters
    fmt += '49s'
    buf += struct.pack("49s", item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<Array>\n')
        xml.write('<Name>Name</Name>\n')
        xml.write('<Dimsize>49</Dimsize>\n')
        xml.write('<U8>\n')
        xml.write('<Name></Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</U8>\n')
        xml.write('</Array>\n')
        
    #----------------------------------------------------------------------
    # Serial Number of LabJack (unsinged int)
    # ----------------------------------------------------------------------
    
    # Pack serial number as unsigned int
    item = dict.get("SERIAL", 0)
    fmt += 'I'
    buf += struct.pack("I", item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<U32>\n')
        xml.write('<Name>SerialNumber</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</U32>\n')
        
    #----------------------------------------------------------------------
    # 24 Volt input of LabJack in volts (float)
    # ----------------------------------------------------------------------
    
    # Pack voltage as float
    item = dict.get("POW_24V", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Voltage.24v</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # 15 Volt input of LabJack in volts (float)
    # ----------------------------------------------------------------------
    
    # Pack voltage as float
    item = dict.get("POW_15V", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Voltage.15v</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # 12 Volt input of LabJack in volts (float)
    # ----------------------------------------------------------------------
    
    # Pack voltage as float
    item = dict.get("POW_12V", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Voltage.12v</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # 5 Volt input of LabJack in volts (float)
    # ----------------------------------------------------------------------
    
    # Pack voltage as float
    item = dict.get("POW_5V", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Voltage.5v</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # -5 Volt input of LabJack in volts (float)
    # ----------------------------------------------------------------------
    
    # Pack voltage as float
    item = dict.get("POW_N5V", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Voltage.Neg5v</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # 5 Volt (switched) input of LabJack in volts (float)
    # ----------------------------------------------------------------------
    
    # Pack voltage as float
    item = dict.get("POW_S5V", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Voltage.Switched5v</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # Temperature of the LabJack in Kelvin (float)
    # ----------------------------------------------------------------------
    
    # Pack temperature as float
    item = dict.get("LJTEMP", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Temp.labjack</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # Temperature of the Air Around LabJack in Kelvin (float)
    # ----------------------------------------------------------------------
    
    # Pack temperature as float
    item = dict.get("LJAIRTEMP", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Temp.air</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    return fmt, buf
    
def __lonoise_labjack(dict, xml, mk_xml):
    # Initialize
    fmt = ""
    buf = ""
    
    #----------------------------------------------------------------------
    # Status of Noise Source: 0 = off, 1 = on (unsigned int)
    # ----------------------------------------------------------------------
    
    # Pack temperature as unsigned int
    item = dict.get("NSSTAT", 0)
    try:
        item = int(item)
    except ValueError:
        item = 0
    fmt += 'I'
    buf += struct.pack('I', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<U32>\n')
        xml.write('<Name>NoiseSourceStatus</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</U32>\n')
        
    #----------------------------------------------------------------------
    # LO Frequency: 0 = 3.4GHz, 1 = 7.5GHz, 
    #               2 = 11.5GHz, 3 = 15.5GHz  (unsigned int)
    # ----------------------------------------------------------------------
    
    # Pack frequency as unsinged int
    item = dict.get("LOFREQ", 0)
    try:
        item = int(item[1])
    except ValueError:
        item = 0
    fmt += 'I'
    buf += struct.pack('I', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<U32>\n')
        xml.write('<Name>LOFrequency</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</U32>\n')
        
    return fmt, buf
    
def __antenna_labjack(dict, xml, mk_xml):
    # Initialize
    fmt = ""
    buf = ""
    
    #----------------------------------------------------------------------
    # Power to VQ component in dBm (float)
    # ----------------------------------------------------------------------
    
    # Pack power as float
    item = dict.get("VQPOW", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Power.vq</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # Power to VI component in dBm (float)
    # ----------------------------------------------------------------------
    
    # Pack power as float
    item = dict.get("VIPOW", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Power.vi</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # Power to HQ component in dBm (float)
    # ----------------------------------------------------------------------
    
    # Pack power as float
    item = dict.get("HQPOW", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Power.hq</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # Power to HI component in dBm (float)
    # ----------------------------------------------------------------------
    
    # Pack power as float
    item = dict.get("HIPOW", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Power.hi</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # Temperature of VQ component in Celsius (float)
    # ----------------------------------------------------------------------
    
    # Pack temperature as float
    item = dict.get("VQTEMP", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Temp.vq</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # Temperature of VI component in Celsius (float)
    # ----------------------------------------------------------------------
    
    # Pack temperature as float
    item = dict.get("VITEMP", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Temp.vi</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # Temperature of HQ component in Celsius (float)
    # ----------------------------------------------------------------------
    
    # Pack temperature as float
    item = dict.get("HQTEMP", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Temp.hq</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # Temperature of HI component in Celsius (float)
    # ----------------------------------------------------------------------
    
    # Pack temperature as float
    item = dict.get("HITEMP", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'f'
    buf += struct.pack('f', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<SGL>\n')
        xml.write('<Name>Temp.hi</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</SGL>\n')
        
    #----------------------------------------------------------------------
    # Attenuation setting for VQ component in dB (double)
    # ----------------------------------------------------------------------
    
    # Pack attenuation as double
    item = dict.get("VQATTEN", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'd'
    buf += struct.pack('d', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<DBL>\n')
        xml.write('<Name>Attenuation.vq</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</DBL>\n')
        
    #----------------------------------------------------------------------
    # Attenuation setting for VI component in dB (double)
    # ----------------------------------------------------------------------
    
    # Pack attenuation as double
    item = dict.get("VIATTEN", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'd'
    buf += struct.pack('d', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<DBL>\n')
        xml.write('<Name>Attenuation.vi</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</DBL>\n')
        
    #----------------------------------------------------------------------
    # Attenuation setting for HQ component in dB (double)
    # ----------------------------------------------------------------------
    
    # Pack attenuation as double
    item = dict.get("HQATTEN", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'd'
    buf += struct.pack('d', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<DBL>\n')
        xml.write('<Name>Attenuation.hq</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</DBL>\n')
        
    #----------------------------------------------------------------------
    # Attenuation setting for HI component in dB (double)
    # ----------------------------------------------------------------------
    
    # Pack attenuation as double
    item = dict.get("HIATTEN", 0)
    try:
        item = float(item)
    except ValueError:
        item = 0.0
    fmt += 'd'
    buf += struct.pack('d', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<DBL>\n')
        xml.write('<Name>Attenuation.hi</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</DBL>\n')
        
    #----------------------------------------------------------------------
    # Source Selection for Vertical Polarization:
    # 0 = antenna, 1 = noise source (unsigned int)
    # ----------------------------------------------------------------------
    
    # Pack selection as unsigned int
    item = dict.get("VNSSEL", 0)
    try:
        item = int(item)
    except ValueError:
        item = 0
    fmt += 'I'
    buf += struct.pack('I', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<U32>\n')
        xml.write('<Name>SourceSelection.v</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</U32>\n')
        
    #----------------------------------------------------------------------
    # Source Selection for Horizontal Polarization:
    # 0 = antenna, 1 = noise source (unsigned int)
    # ----------------------------------------------------------------------
    
    # Pack selection as unsigned int
    item = dict.get("HNSSEL", 0)
    try:
        item = int(item)
    except ValueError:
        item = 0
    fmt += 'I'
    buf += struct.pack('I', item)
    
    # Append to XML file
    if mk_xml:
        xml.write('<U32>\n')
        xml.write('<Name>SourceSelection.h</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</U32>\n')
        
    return fmt, buf