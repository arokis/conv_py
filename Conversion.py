# Conversion.py
# *************
# Defines the Conversion Class for each Step in a Conversion-Scenario
# IN WORK !

import os
#import Config
import functions

class Conversion (object):

    def __init__(self):
        self.name = False
        self.type = False
        self.desc = False
        self.script = False 
        self.converter = False
        
    def info (self):
        print self.name
        print self.type
        print self.desc
        print self.script
        print self.converter
    
    
    def scenarioise (self, conversion, scripts):
        #self.path = os.path.dirname( scripts_config )
        #print scripts_path
        
        if conversion.get('scenario'):
            #print ('SCENARIO!')
            self.name = conversion['scenario']
            self.type = scripts[self.name]['type']
            self.desc = scripts[self.name]['desc']
            self.script = scripts[self.name]['script']
        else:
            #print ('USERDEFINED!')
            self.name = conversion['name']
            self.type = conversion['type']
            self.desc = conversion['desc']
            self.script = os.path.abspath(conversion['script'])
            self.language = conversion['language']
            self.converter = ' '.join ( (conversion['language'], self.script) )
    
