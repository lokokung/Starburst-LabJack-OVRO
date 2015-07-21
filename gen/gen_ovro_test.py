"""
    STARBURST OVRO Item Struct Decomposition Test Suite
    (Based on gen_schedule_sf.py)
    Author: Lokbondo Kung
    Email: lkkung@caltech.edu
"""

import unittest
import struct
import numpy as np
import xml.etree.ElementTree as etree
import copy
import gen_ovro as go
import os
import sys

class TestGenerateOVROBinary(unittest.TestCase):
    # Redefine methods already used in Starburst pipeline so that the 
    # tests can be ran without unnecessary dependencies. 
    
    # handle_cluster copied from read_xml2.py
    def handle_cluster(self, child):
        '''This element of the XML tree is the head of a Cluster.  Step through
        each element of the branch and return the keys, the empty dictionary, 
        and the fmt string.  This routine is reentrant'''
        # Clusters have a name, a NumElts, and one or more objects
        c = list(child)
        fmt = ''
        if c[0].tag == "Name":
            keys = [c[0].text]
            mydict = {}    # Start an empty dictionary
            c.pop(0)
        else:
            print 'Illegal format for item',child
            return None, None
        if c[0].tag == "NumElts":
            n = int(c[0].text)
            c.pop(0)
        else:
            print 'Illegal format for item',child
            return None, None
        # Loop through all items in the cluster
        for i in range(n):
            datatype = c[0].tag
            if datatype == "Array":
                ch = c[0]
                key, arr, dims, fmt1 = self.handle_array(ch)
                keys += key
                fmt += fmt1
                mydict.update({key[0]:arr}) 
                c.pop(0)
            elif datatype == "Cluster":
                ch = c[0]
                key, newdict, fmt1 = self.handle_cluster(ch)
                if not key is None:
                    keys += key
                fmt += fmt1
                mydict.update({key[0]:newdict})
                c.pop(0)
            else:
                ch = c[0]
                key, fmt1 = self.handle_item(ch)
                keys += key
                fmt += fmt1
                mydict.update({key[0]:0})
                c.pop(0)
        return keys, mydict, fmt
    
    # handle_array copied from read_xml2.py
    def handle_array(self, child):
        '''This element of the XML tree is an Array.  Step through the items 
           of the array (which may contain clusters, other arrays, etc.) and return the keys, array, dimensions of the array, and fmt string.  
           This routine is reentrant.
        '''
        # Arrays have a name and one or more dimension statements, then one or more objects
        c = list(child)
        if c[0].tag == "Name":
            keys = [c[0].text]
            c.pop(0)
        else:
            print 'Illegal format for item',child
            return None, None, None, None
        # Handle up to four levels of dimension
        d1, d2, d3, d4 = 1, 1, 1, 1
        if c[0].tag == "Dimsize":
            d1 = int(c[0].text)
            fmt = 'I'
            c.pop(0)
        else:
            print 'Illegal format for item',child
            return None, None
        if c[0].tag == "Dimsize":
            d2 = int(c[0].text)
            fmt += 'I'
            c.pop(0)
        if d2 != 1:
            if c[0].tag == "Dimsize":
                d3 = int(c[0].text)
                fmt += 'I'
                c.pop(0)
            if d3 != 1:
                if c[0].tag == "Dimsize":
                    d4 = int(c[0].text)
                    fmt += 'I'
                    c.pop(0)
        dims = [d1, d2, d3, d4]
        datatype = c[0].tag
        dtype_dict = {'U8':'s','B8':'B','U16':'H','U32':'I','I16':'h',
                      'I32':'i','SGL':'f','DBL':'d'}
        fmt += str(d1*d2*d3*d4)+dtype_dict.get(datatype,'[')
        if datatype == "Cluster":
            ch = list(c[0])
            key, mydict, fmt1 = handle_cluster(ch)
            keys += key
            fmt += fmt1+']'
            arr = [mydict]  # Return cluster dictionary as 1-element list place holder
            c.pop(0)
        else:
            arr = dims   # Return list of dims as place holder
        return keys, arr, dims, fmt
    
    # handle_item copied from read_xml2.py
    def handle_item(self, c):
        '''This element of the XML tree is a simple, single item.  
           Simply return its key and fmt string.
        '''
        dtype_dict = {'U8':'s','B8':'B','U16':'H','U32':'I','I16':'h',
                      'I32':'i','SGL':'f','DBL':'d'}
        fmt = dtype_dict.get(c.tag,'*')
        if c[0].tag == "Name":
            key = [c[0].text]
        else:
            print 'Illegal format for item',c
            return None, None
        return key, fmt
    
    # xml_read adapted from read_xml2.py
    def xml_read(self, fileName):
        if fileName is not None:
            f = open(fileName)
            tree = etree.parse(f)
            f.close()

            root = tree.getroot()
            try:
                # Stateframe version number is supposed to be included 
                # in the second element of the stateframe cluster 
                # (after the timestamp)
                version = float(root[3][1].text)
            except:
                # It seems not to be there, so set version to 3.0
                version = 3.0

            keys, mydict, fmt = self.handle_cluster(root)
            return keys, mydict, fmt, version
        return None
        
    # handle_key copied from read_xml2.py
    def handle_key(self, keys, dictlist, fmt, off):
        key = keys.pop(0)
        if key is None:
            #Skip any "None" key
            return keys, dictlist, fmt, off
        mydict = dictlist.pop()      # Get the inner-most dict for processing
        try:
            val = mydict[key]
        except:
            # We must be done with this dictionary, so go back and try again
            # Note that dictlist is one item shorter than before
            keys = [key] + keys  # Put key back in list
            return keys, dictlist, fmt, off
        valtype = type(val)
        if valtype == int or valtype == float:
            # This is just a single value
            f = fmt[0]
            fmt = fmt[len(f):]
            try:
                mydict[key] = [f, off] # Assign fmt, offset pair as value to 
                                       # key. Increment off by number of bytes 
                                       # taken by f            
                off += struct.calcsize(f)
            except:
                print key, fmt
            dictlist.append(mydict)   # Put original dictionary back
        elif valtype == list:
            # This is an array of values
            if type(val[0]) == int:
                # This is a simple array of numbers
                dims = val  # List of dimensions from XML file
                arrsiz = 1  # Total array size (product of dimensions)
                ndim = 0    # Number of dimensions 
                for dim in dims:
                   arrsiz *= dim
                   if dim != 1:
                       # Count only non-unity dimensions
                       ndim += 1
                dims = dims[:ndim]
                # Read dimensions of array
                while fmt[0] == 'I':
                    f = fmt[0]
                    fmt = fmt[len(f):]
                    # Skip dimension variables
                    # Increment off by number of bytes taken by f
                    off += struct.calcsize(f)
                f = fmt[:len(str(arrsiz))+1]
                fmt = fmt[len(f):]
                if f[-1] == 's':
                    mydict[key] = [f, off] # If f is 'string', do not save dims
                else:
                    mydict[key] = [f, off, dims] # Assign fmt, offset and dims 
                                                 # as value to key. Increment 
                                                 # off by number of bytes 
                                                 # taken by f (to prepare for 
                                                 # next iteration)
                off += struct.calcsize(f)
                dictlist.append(mydict)    # Put original dictionary back
            else:
                # This is something more complicated (e.g. an array of dicts)
                if type(val[0]) == dict:
    #                dims = []   # List of dimensions
                    arrsiz = 1  # Total array size (product of dimensions)
                    dictarr = []
                    # Read dimensions of array
                    while fmt[0] == 'I':
                        f = fmt[0]
                        fmt = fmt[len(f):]
                        # Skip dimension variables
                        # Increment off by number of bytes taken by f
                        off += struct.calcsize(f)
    #                    dims.append(vals[0])
    #                    arrsiz *= vals[0]
                    # Extract array size (number just before '[')
                    arrsiz = int(fmt[:fmt.index('[')])  
                    
                    newfmt = fmt[fmt.index('[')+1:fmt.index(']')]
                    fmt = fmt[fmt.index(']')+1:]  
                    
                    for j in range(arrsiz):
                        newdictarr = [copy.deepcopy(val[0])]
                        tmpfmt = newfmt
                        tmpkeys = copy.deepcopy(keys)
                        while tmpfmt != '':
                            tmpkeys, newdictarr, tmpfmt, off = handle_key(
                                tmpkeys, newdictarr, tmpfmt, off)
                        while len(newdictarr) > 1:
                            newdictarr.pop()  # Remove all but the original 
                                              # dictionary
                        
                        # Dictionary is all filled in, and only one copy 
                        # remains.  Copy it to dictarray being assembled
                        dictarr.append(copy.deepcopy(newdictarr.pop()))
                    keys = tmpkeys
                mydict[key] = dictarr    # Assign array of dicts to mydict key
                dictlist.append(mydict)  # Put original dictionary back
        elif valtype == dict:
            # This is a dictionary.
            dictlist.append(mydict)  # Put original dictionary back
            dictlist.append(val)     # Add new dictionary
        else:
            print 'Unknown value type',valtype
        return keys, dictlist, fmt, off
    
    # xml_ptrs copied from read_xml2.py
    def xml_ptrs(self, filename=None):
        inkeys, indict, infmt, version = self.xml_read(filename)   
        # Pre-processing step
        keys = copy.deepcopy(inkeys)
        mydict = copy.deepcopy(indict)
        fmt = infmt
        keys.pop(0)
        dictlist = [mydict]  # A list of dictionaries.  
                             # The one at the end is the one 
                             # currently being manipulated
        off = 0
        while fmt != '':
            keys, dictlist, fmt, off = self.handle_key(keys, dictlist, 
                                                       fmt, off)
        mydict = dictlist.pop()   # Should be the original, but now 
                                  # updated dictionary
        if dictlist != []:
            mydict = dictlist.pop() # Should be the original, but now updated
                                    # dictionary
        return mydict, version
        
    # extract copied from stateframe.py
    def extract(self, data, k):
        '''Helper function that extracts a value from data, based on stateframe
           info pair k (k[0] is fmt string, k[1] is byte offset into data)
        '''
        if len(k) == 3:
           k[2].reverse()
           val = np.array(struct.unpack_from(k[0],data,k[1]))
           val.shape = k[2]
           k[2].reverse()
        else:
           val = struct.unpack_from(k[0],data,k[1])[0]
        return val

    def setUp(self):
        # Setup the values to be returned.
        self.data = {"LONOISE": {"NAME": "LONoiseMod",
                                 "LJTEMP": 300,
                                 "LJAIRTEMP": 298,
                                 "POW_24V": 24,
                                 "POW_15V": 15,
                                 "POW_12V": 12,
                                 "POW_5V": 5,
                                 "POW_N5V": -5,
                                 "POW_S5V": 5,
                                 "SERIAL": 1000,
                                 "LOFREQ": ("LO_3_4GHZ", 0),
                                 "NSSTAT": 0 },
                     "A":       {"NAME": "AntennaA",
                                 "LJTEMP": 300,
                                 "LJAIRTEMP": 298,
                                 "POW_24V": 24,
                                 "POW_15V": 15,
                                 "POW_12V": 12,
                                 "POW_5V": 5,
                                 "POW_N5V": -5,
                                 "POW_S5V": 5,
                                 "SERIAL": 2000,
                                 "HIPOW": 0,
                                 "HQPOW": 1,
                                 "VIPOW": 2,
                                 "VQPOW": 3,
                                 "HITEMP": 100,
                                 "HQTEMP": 101,
                                 "VITEMP": 102,
                                 "VQTEMP": 103,
                                 "VNSSEL": 1,
                                 "HNSSEL": 1,
                                 "HIATTEN": 31.5,
                                 "HQATTEN": 31.5,
                                 "VIATTEN": 31.5,
                                 "VQATTEN": 31.5 },
                     "B":       {"NAME": "AntennaB",
                                 "LJTEMP": 300,
                                 "LJAIRTEMP": 298,
                                 "POW_24V": 24,
                                 "POW_15V": 15,
                                 "POW_12V": 12,
                                 "POW_5V": 5,
                                 "POW_N5V": -5,
                                 "POW_S5V": 5,
                                 "SERIAL": 3000,
                                 "HIPOW": 0,
                                 "HQPOW": -1,
                                 "VIPOW": -2,
                                 "VQPOW": -3,
                                 "HITEMP": 200,
                                 "HQTEMP": 201,
                                 "VITEMP": 202,
                                 "VQTEMP": 203,
                                 "VNSSEL": 0,
                                 "HNSSEL": 0,
                                 "HIATTEN": 0,
                                 "HQATTEN": 0,
                                 "VIATTEN": 0,
                                 "VQATTEN": 0 } }
        
        # Setup maps between the data set and the returned dictionary names.
        self.nameMap = {"Temp.labjack": "LJTEMP",
                        "Temp.air": "LJAIRTEMP",
                        "Voltage.24v": "POW_24V",
                        "Voltage.15v": "POW_15V",
                        "Voltage.12v": "POW_12V",
                        "Voltage.5v": "POW_5V",
                        "Voltage.Neg5v": "POW_N5V",
                        "Voltage.Switched5v": "POW_S5V",
                        "Name": "NAME",
                        "SerialNumber": "SERIAL",
                        "NoiseSourceStatus": "NSSTAT",
                        "LOFrequency": "LOFREQ",
                        "Power.vq": "VQPOW",
                        "Power.vi": "VIPOW",
                        "Power.hq": "HQPOW",
                        "Power.hi": "HIPOW",
                        "Temp.vq": "VQTEMP",
                        "Temp.vi": "VITEMP",
                        "Temp.hq": "HQTEMP",
                        "Temp.hi": "HITEMP",
                        "Attenuation.vq": "VQATTEN",
                        "Attenuation.vi": "VIATTEN",
                        "Attenuation.hq": "HQATTEN",
                        "Attenuation.hi": "HIATTEN",
                        "SourceSelection.v": "VNSSEL",
                        "SourceSelection.h": "HNSSEL" }
                        
    """
    Test - test_XMLFileIsGenerated:
        Given that gen_ovro is called to create the XML file for parsing,
        Then the XML file exists at the location returned.
    """
    def test_XMLFileIsGenerated(self):
        fmt, buf, xmlFile = go.gen_ovro(self.data, True)
        self.assertTrue(os.path.exists(xmlFile))
    
    """
    Test - test_sensibleEvenIfDictionaryIsEmpty:
        Given that gen_ovro is passed an empty dictionary, 
        Then the buffer string generated is not an empty string.
    """
    def test_sensibleEvenIfDictionaryIsEmpty(self):
        fmt, buf, xmlFile = go.gen_ovro({})
        self.assertTrue(sys.getsizeof(buf) != 0)
    
    """
    Test - test_stringBufferRevertsToActualValues:
        Given that self.data is defined and passed to gen_ovro,
        Then the buffer generated decodes to the values in self.data.
    """
    def test_stringBufferRevertsToActualValues(self):
        fmt, buf, xmlFile = go.gen_ovro(self.data, True)
        dict, version = self.xml_ptrs(xmlFile)
        
        # Test the LO/Noise Module values
        testDic = dict["LONoiseModule"]
        for key, value in testDic.items():
            if key == "Name":
                val1 = self.extract(buf, value)
                val1 = val1.replace('\x00', '')
                val2 = self.data["LONOISE"][self.nameMap[key]]
                self.assertEqual(val1, val2)
            elif key == "LOFrequency":
                val1 = self.extract(buf, value)
                val2 = self.data["LONOISE"][self.nameMap[key]][1]
                self.assertEqual(val1, val2)
            else:
                val1 = self.extract(buf, value)
                val2 = self.data["LONOISE"][self.nameMap[key]]
                self.assertEqual(val1, val2)
                
        # Test the AntennaA Module values
        testDic = dict["AntennaAModule"]
        for key, value in testDic.items():
            if key == "Name":
                val1 = self.extract(buf, value)
                val1 = val1.replace('\x00', '')
                val2 = self.data["A"][self.nameMap[key]]
                self.assertEqual(val1, val2)
            else:
                val1 = self.extract(buf, value)
                val2 = self.data["A"][self.nameMap[key]]
                self.assertEqual(val1, val2)
                
        # Test the AntennaB Module values
        testDic = dict["AntennaBModule"]
        for key, value in testDic.items():
            if key == "Name":
                val1 = self.extract(buf, value)
                val1 = val1.replace('\x00', '')
                val2 = self.data["B"][self.nameMap[key]]
                self.assertEqual(val1, val2)
            else:
                val1 = self.extract(buf, value)
                val2 = self.data["B"][self.nameMap[key]]
                self.assertEqual(val1, val2)
        
        
# Main Method
if __name__ == '__main__':
    testGroups = [TestGenerateOVROBinary]
    for tG in testGroups:
        print "\nTesting: " + str(tG.__name__)
        suite = unittest.TestLoader().loadTestsFromTestCase(
            tG)
        unittest.TextTestRunner(verbosity=2).run(suite)