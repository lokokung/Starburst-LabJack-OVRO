"""
    STARBURST OVRO Item Struct Decomposition
    (Based on gen_schedule_sf.py)
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import struct
import numpy as np
import shutil

# NUMBER OF ELEMENTS IN CLUSTERS:
Nelements = 7
Nelements_starburst = 4
Nelements_lonoise = 12
Nelements_antenna = 24

# Version # for Subarray2 stateframe and for 
# Starburst-specific stateframe - MUST BE DEFINED HERE
version = 3               # Version Date: 3/31/15
starburst_version = 1     # Version Date: 3/7/15
version_date = '3.31.15'  # Most recent update (used to write backup file)

"""
Method: gen_starburst_sf()
    Description:
        Writes the Starburst OVRO stateframe items from the stateframe
        dictionary. Optionally creates the corresponding XML file. Regardless 
        of whether the XML file is created, the file name to the XML will be 
        returned (/tmp/ovro_stateframe.xml). 
        
        Even if supplied an empty dictionary, this routine will return 
        something sensible.
    Arguments:
        sf_dict: stateframe dictionary.
    Returns:
        buf: binary data buffer.
        fmt: format string.
        xmlFile: xml file path.
"""
def gen_starburst_sf(sf_dict, mk_xml=False):
    
    # Set up file name, format string, and buffer.
    xmlFile = r'tmp/schedule2_stateframe.xml'
    fmt = '<'
    buf = ''
    xml = None
    
    # Append XML for data cluster
    if mk_xml:
        xml = open(xmlFile, "w")
        xml.write('<Cluster>\n')
        xml.write('<Name>Dat2</Name>\n')
        xml.write('<NumElts>' + str(Nelements) + '</NumElts>\n')
        
    # ======================================================================    
    # Start of data dump.
    # ======================================================================
    append_fmt, append_buf = __general_stateframe(sf_dict, xml, mk_xml)
    fmt += append_fmt
    buf += append_buf
    
    # ======================================================================    
    # Start of Starburst cluster dump.
    # ======================================================================
    append_fmt, append_buf = __starburst_stateframe(sf_dict, xml, mk_xml)
    fmt += append_fmt
    buf += append_buf
    
    # Append for end of data cluster
    if mk_xml:
        xml.write('</Cluster>\n')
        xml.close()
        
        # Make backup copy of XML file
        backup_file = ('starburst/schedule2_stateframe_v' + 
                       str(version) + '_' + version_date + '.xml')
        shutil.copyfile(xmlFile, backup_file) 

        # Print size of buf
        print 'schedule2 size =', len(buf)
        print 'Modify acc.ini to reflect this if this is a change in size'

    return fmt, buf, xmlFile
    
def __generic_labjack(dict, xml, mk_xml):
    # Initialize
    fmt = ""
    buf = ""
    
    # DEFAULTS - Generic LabJacks:
    default_serial = 0
    default_name = ""
    default_volts = 0
    default_temp = 0
    
    #----------------------------------------------------------------------
    # Name of LabJack (length 49 array of characters)
    # ----------------------------------------------------------------------
    
    # Define array dimensions
    fmt += 'I'
    buf += struct.pack('I', 49)
    item = dict.get("NAME", default_name)
    
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
    item = dict.get("SERIAL", default_serial)
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
    item = dict.get("POW_24V", default_volts)
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
    item = dict.get("POW_15V", default_volts)
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
    item = dict.get("POW_12V", default_volts)
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
    item = dict.get("POW_5V", default_volts)
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
    item = dict.get("POW_N5V", default_volts)
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
    item = dict.get("POW_S5V", default_volts)
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
    item = dict.get("LJTEMP", default_temp)
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
    item = dict.get("LJAIRTEMP", default_temp)
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
    
    # DEFAULTS - Generic LabJacks:
    default_status = 0
    default_freq = ("", 0)
    
    #----------------------------------------------------------------------
    # Status of Noise Source: 0 = off, 1 = on (unsigned int)
    # ----------------------------------------------------------------------
    
    # Pack temperature as unsigned int
    item = dict.get("NSSTAT", default_status)
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
    item = dict.get("LOFREQ", default_freq)
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
    
    # DEFAULTS - Generic LabJacks:
    default_pow = 0
    default_atten = 31.5
    default_temp = 0
    default_vsel = 0
    default_hsel = 0
    
    #----------------------------------------------------------------------
    # Power to VQ component in dBm (float)
    # ----------------------------------------------------------------------
    
    # Pack power as float
    item = dict.get("VQPOW", default_pow)
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
    item = dict.get("VIPOW", default_pow)
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
    item = dict.get("HQPOW", default_pow)
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
    item = dict.get("HIPOW", default_pow)
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
    item = dict.get("VQTEMP", default_temp)
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
    item = dict.get("VITEMP", default_temp)
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
    item = dict.get("HQTEMP", default_temp)
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
    item = dict.get("HITEMP", default_temp)
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
    item = dict.get("VQATTEN", default_atten)
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
    item = dict.get("VIATTEN", default_atten)
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
    item = dict.get("HQATTEN", default_atten)
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
    item = dict.get("HIATTEN", default_atten)
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
    item = dict.get("VNSSEL", default_vsel)
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
    item = dict.get("HNSSEL", default_hsel)
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

# Copied from gen_schedule_sf    
def __general_stateframe(sf_dict, xml, mk_xml):
    # Initialize
    fmt = ""
    buf = ""
    
    # DEFAULTS - General
    default_tstamp = 0.0
    default_scan_state = 0
    default_phase_tracking = 0
    default_uvw = np.array([[0.0,0.0,0.0]]*16)
    default_delay = np.zeros(16)
    default_az = np.zeros(15)
    default_el = np.zeros(15)
    default_chi = np.zeros(15)
    default_track_flag = np.array([False]*16)
        
    # 1 - Schedule_Timestamp (double) [s, in LabVIEW format]
    # To be compatible with other timestamps in the stateframe, this
    # will be in LabVIEW format, which is s since 1904/01/01 (don't ask).
    # It is the time (should be exact second, no microseconds) for
    # which the UVW coordinates and Delays are calculated.
    item = sf_dict.get('timestamp',default_tstamp)
    fmt += 'd'
    buf += struct.pack('d',item)
    if mk_xml:
        xml.write('<DBL>\n')
        xml.write('<Name>Timestamp</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</DBL>\n')
    
    # 2 - Schedule version (double) [N/A]
    # Version of the schedule2 stateframe.
    item = version
    fmt += 'd'
    buf += struct.pack('d',item)
    if mk_xml:
        xml.write('<DBL>\n')
        xml.write('<Name>Version</Name>\n')
        xml.write('<Val>'+str(item)+'</Val>\n')
        xml.write('</DBL>\n')

    # 3 - Scan_State (unsigned integer bool)
    # Flag (=1 to indicate that DPP should be recording data, =0 otherwise)
    item = sf_dict.get('scan_state',default_scan_state)
    fmt += 'i'
    buf += struct.pack('i',item)
    if mk_xml:
        xml.write('<I32>\n')
        xml.write('<Name>ScanState</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</I32>\n')

    # 4 - Phase_Tracking (unsigned integer bool)
    # Flag (=1 to indicate that uvw coordinates are valid, =0 otherwise)
    item = sf_dict.get('phase_tracking',default_phase_tracking)
    fmt += 'I'
    buf += struct.pack('I',item)
    if mk_xml:
        xml.write('<U32>\n')
        xml.write('<Name>PhaseTracking</Name>\n')
        xml.write('<Val></Val>\n')
        xml.write('</U32>\n')

    # 5 - UVW (3 x 16 array of doubles) [ns]
    # u, v, w coordinates for each antenna, relative to antenna 1.
    # Default is array of zeros (=> not tracking phase center)
    item = sf_dict.get('uvw',default_uvw)
    # Write dimensions into data stream
    fmt += 'II'
    buf += struct.pack('II',3,16)
    fmt += str(3*16)+'d'
    for i in range(16):
        buf += struct.pack('3d',item[i,0],item[i,1],item[i,2])
    if mk_xml:
       xml.write('<Array>\n')
       xml.write('<Name>UVW</Name>\n')
       xml.write('<Dimsize>3</Dimsize><Dimsize>16</Dimsize>\n<DBL>\n<Name></Name>\n<Val></Val>\n</DBL>\n')
       xml.write('</Array>\n')

    # 6 - Delay (length 16 x 2 array of doubles) [ns]
    # Geometric delay (-w coordinate) for each antenna, relative to antenna 1,
    # for current time (stateframe timestamp), and again for current time plus
    # 1 s (delay1).
    # Default is array of zeros (=> not tracking phase center)
    # Write dimensions into data stream
    fmt += 'II'
    buf += struct.pack('II',16,2)
    item = sf_dict.get('delay',default_delay)
    fmt += '32d'
    for i in item:
        buf += struct.pack('d',i)
    item = sf_dict.get('delay1',default_delay)
    for i in item:
        buf += struct.pack('d',i)
    if mk_xml:
       xml.write('<Array>\n')
       xml.write('<Name>Delay</Name>\n')
       xml.write('<Dimsize>16</Dimsize><Dimsize>2</Dimsize>\n<DBL>\n<Name></Name>\n<Val></Val>\n</DBL>\n')
       xml.write('</Array>\n')
       
    return fmt, buf
       
def __starburst_stateframe(sf_dict, xml, mk_xml):
    # Initialize
    fmt = ""
    buf = ""
    
    # Append XML for Starburst cluster.
    if mk_xml:
        xml.write('<Cluster>\n')
        xml.write('<Name>Starburst</Name>\n')
        xml.write('<NumElts>' + str(Nelements_starburst) + '</NumElts>\n')
    
    # ======================================================================    
    # Start of LO/Noise Module dump.
    # ======================================================================
    dict = sf_dict.get("starburst", {}).get("LONOISE", {})
    
    # Append XML for LONoiseModule cluster.
    if mk_xml:
        xml.write('<Cluster>\n')
        xml.write('<Name>LONM</Name>\n')
        xml.write('<NumElts>' + str(Nelements_lonoise) + '</NumElts>')
    
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
    dict = sf_dict.get("starburst", {}).get("A", {})
    
    # Append XML for LONoiseModule cluster.
    if mk_xml:
        xml.write('<Cluster>\n')
        xml.write('<Name>DCMA</Name>\n')
        xml.write('<NumElts>' + str(Nelements_antenna) + '</NumElts>')
        
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
    dict = sf_dict.get("starburst", {}).get("B", {})
    
    # Append XML for LONoiseModule cluster.
    if mk_xml:
        xml.write('<Cluster>\n')
        xml.write('<Name>DCMB</Name>\n')
        xml.write('<NumElts>' + str(Nelements_antenna) + '</NumElts>')
        
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
    # Include Starburst Version
    # ======================================================================
    item = starburst_version
    fmt += 'I'
    buf += struct.pack('I',item)
    if mk_xml:
        xml.write('<U32>\n')
        xml.write('<Name>Version</Name>\n')
        xml.write('<Val>' + str(item) + '</Val>\n')
        xml.write('</U32>\n')
        
    # ======================================================================
    # Wrap up end of Starburst cluster.
    if mk_xml:
        xml.write('</Cluster>')
    # ======================================================================    
    
    return fmt, buf