#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
convpy.py
*************
Defines ConvPY itself as a Class and its conversion-functionalities
"""

import os
import json
import sys

import functions
import conversion
import converter 


#home = os.path.dirname( os.path.abspath( __file__ ) )
#default_config = os.path.join(home, 'config/config.json')

class ConvPY(object):

    def _homeify (self, path):
        return os.path.join(self.home, path)
    

    def _readJSON (self, path):
        path = path
        if os.path.isfile(path):
            with open(path, 'r') as data:
                return json.load(data)
    

    def __init__ (self, config):
        self.home = os.path.dirname( os.path.abspath( __file__ ) )
        self.config = self._readJSON( os.path.join(self.home, config) )
        self.tmpFile = self._homeify(self.config['tmp-file'])


    def configure(self):
        self.scenarios_path = self._homeify( self.config['scenarios']['path'] )
        self.scenarios_config = os.path.join(self.scenarios_path, self.config['scenarios']['config'])
        self.scenarios = self._readJSON( self.scenarios_config )

        self.engines_path =  self._homeify( self.config['engines']['path'] )
        self.engines_config =  os.path.join(self.engines_path, self.config['engines']['config']) 
        self.engines = self._readJSON(self.engines_config)

        self.scripts_path = self._homeify( self.config['scripts']['path'] )
        self.scripts_config = os.path.join(self.scripts_path, self.config['scripts']['config'])
        self.scripts = self._readJSON( self.scripts_config )
        

    def convert (self, workflow):
        """
        main conversion routine which creates Conversion-Instances and call the Converter-Instances

        ARGS:
        * flow: the givern conversion-workflow which should to be done
        * convpy: The actual configured convPY Instance
        
        TO-DO:
        - "pathify" Saxon-Class (Converter.py) -> and make the Classes smooth ... they are a mess right now
        - make Conversion-Class smooth !
        """
        for step in workflow:
            conv = conversion.Conversion(self)
            conv.scenarioise(step)
            #print convpy.scripts_path
            #conv.info()
            
            if conv.type == 'xslt':
                language = self.engines['Saxon']['xslt']['language']
                engine = os.path.join(self.home, self.engines['Saxon']['xslt']['path'])
                converter.Saxon(language, engine).xslt(conv.script)
            elif conv.type == 'xquery':
                language = self.engines['Saxon']['xquery']['language']
                engine = os.path.join(self.home, self.engines['Saxon']['xquery']['path'])
                converter.Saxon(language, engine).xquery()
            else:
                converter.Call(conv.language).run(conv.script)


    def finish (self, clean=False, output_file=False):
        """
        convPY's result:  
        * return last conversion's output from tmp-file and clean-up
        
        ARGS:
        * tmp_file [STRING]: The temporary files going to be cleaned up
        * output_file [STRING]: An optional output directory
        * clean [BOOLEAN]: If True clean up, if False don't and keep all tmp-files and directories

        TO-DO:
        * save last conversion's output from tmp-file in user-defined output-folder
        """
        output = functions.open_file (self.tmpFile)
        if output_file != False:
            functions.create_file(output_file, output)
        print(output)
        if clean == True:
            functions.clean_tmp(self.tmpFile)
        sys.exit(0)


    def prepare (self, data):
        data = functions.retrieve(data)
        functions.preset(data, self.tmpFile)

    """
    def extensions (self):
        ext = dict()
        for conversion in self.conversions:
            for extension in self.conversions[conversion]['extensions']:
                ext[extension] = conversion
        return ext
    """
    """
    def custom (self, config):
        self.config = self._readJSON( config )
        print os.path.abspath(self.config['scenarios']) 
        self.scenarios = self._readJSON( self.config['scenarios'] )
        self.engines = self._readJSON( self.config['engines'] )
        self.conversions = self._readJSON( self.config['conversions'] )
        self.tmpFile = self.config['tmp-file']
    """
