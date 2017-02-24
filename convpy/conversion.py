#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
convpy/conversion.py
*************
Defines the Conversion Class for each Step in a Conversion-Scenario
IN WORK !
"""

import os
import functions


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-12"


class Conversion (object):

    def __init__(self, convpy):
        self.convpy = convpy
        self.name = False
        self.type = False
        self.desc = False
        self.script = False 
        self.language = False
        self.converter = False
        
    def info (self):
        print self.name
        print self.type
        print self.desc
        print self.script
        print self.converter
    
    
    def scenarioise (self, conversion):
        #self.path = os.path.dirname( scripts_config )
        #print scripts_path
        
        if conversion.get('scenario'):
            #print ('SCENARIO!')
            self.name = conversion['scenario']
            self.type = self.convpy.scripts[self.name]['type']
            self.desc = self.convpy.scripts[self.name]['desc']
            self.script = os.path.join(self.convpy.scripts_path, self.convpy.scripts[self.name]['script'])
            try: 
                self.language = self.convpy.scripts[self.name]['language']
            except KeyError:
                pass
        
        else:
            #print ('USERDEFINED!')
            self.name = conversion['name']
            self.type = conversion['type']
            self.desc = conversion['desc']
            self.script = os.path.abspath(conversion['script'])
            self.language = conversion['language']
            self.converter = ' '.join ( (conversion['language'], self.script) )
    
