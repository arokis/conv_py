#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
convpy/conv.py
*************
Defines configuration-functions and the Classes "Config" and "Convpy".
"""

import json 
import os
import sys
import urllib2
from shutil import rmtree

import functions
import converter 

__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-25"


class Config (object):
    def __init__ (self, config):
        self.path = os.path.dirname(config)
        self.config = read_config(config)


class Confpy (object):
    def __init__ (self, config, engines, scripts):
        self.main_config = config
        self.engines = engines
        self.scripts = scripts
        self.tmpFile = pathify(True, config.config['tmp-file'])
        self.output = config.config['output-dir']

    def prepare (self, source):
        """
        preparation Methode that creates the neccessary file-structure of ConvPY

        ARGS:
        * data: the givern conversion-workflow which should to be done
        * convpy: The actual configured convPY Instance
        
        TO-DO:
        - "pathify" Saxon-Class (Converter.py) -> and make the Classes smooth ... they are a mess right now
        - make Conversion-Class smooth !
        """
        source = functions.retrieve(source)
        preset(source, self.tmpFile)

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
                 
            step = self.scenarioise(step)
            #print step
            
            if step['type'] == 'xslt':
                language = self.engines.config['Saxon']['xslt']['language']
                engine = os.path.join(self.engines.path, self.engines.config['Saxon']['xslt']['path'])
                #print ' '.join((language, engine, step['script'], self.tmpFile, self.tmpFile))
                converter.Saxon(language, engine).xslt(step['script'], self.tmpFile, self.tmpFile)
            elif step['type'] == 'xquery':
                language = self.engines['Saxon']['xquery']['language']
                engine = os.path.join(self.engines.path, self.engines.config['Saxon']['xquery']['path'])
                #engine = os.path.join(self.home, self.engines['Saxon']['xquery']['path'])
                converter.Saxon(language, engine).xquery(step['script'], self.tmpFile, self.tmpFile)
            else:
                converter.Call(step['language']).run(step['script'], self.tmpFile)
    

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


    def scenarioise (self, scenario):
        """
        ...

        ARGS:
        * scenario   : ...

        RETURN:
        * {DICT}: ...
        """
        #print convpy.tmpFile
        obj = {}
        
        if scenario.get('scenario'):
            #print 'CONVPY SCENARIO'
            scenario_name = scenario['scenario']
            obj['name'] = scenario_name
            try:
                #print convpy.scripts.config[scenario_name]
                obj['script'] = os.path.join(self.scripts.path, self.scripts.config[scenario_name]['script'])
                obj['type'] = self.scripts.config[scenario_name]['type']
                try:
                    obj['language'] = self.scripts.config[scenario_name]['language']
                except:
                    obj['language'] = False   
            except:
                #print 'NICHT DRIN'
                pass
        else:
            #print 'USER DEFINED SCENARIO'
            obj = scenario
        return obj



def configure (config_file):
    """
    configures ConvPY with homepath and reads engines and scipts configs

    ARGS:
    * config_file: path to config.json 

    RETURN:
    {CONVPY OBJECT} that is configured with main-config, engines and scenario-scripts
    """
    config_path = pathify(True, config_file)
    main_config = Config(config_path)

    scripts_config = pathify(True, main_config.config['scripts']['path'], main_config.config['scripts']['config'])
    engines_config = pathify(True, main_config.config['engines']['path'], main_config.config['engines']['config'])
    
    scripts = Config(scripts_config)
    engines = Config(engines_config)
    return Confpy(main_config, engines, scripts)


def pathify (homeify, *arg):
    """
    ...

    ARGS:
    * homeify   : ...
    * *arg      : ... 

    RETURN:
    * STR: ...
    """
    joined = ''.join(arg)
    if homeify == True:
        home = os.path.dirname( os.path.abspath( os.path.join( __file__ , os.path.pardir) ) )
        #print 'homeify'
        #print os.path.join(home, path)
        return os.path.join(home, joined)
    else:
        #print 'relative'
        #print joined
        return os.path.abspath(joined)


def preset (data, tmp_file):
    """
    starts convPY's workflow by creating the essential file-system for temporary file
    
    ARGS:
    * data      : ...
    * tmp_file  : ... 

    RETURN:
        OK      > File-structure: ...
        Error   > Exception & exits with error-code 1
    """

    def create_tmp_essentials (tmp_file, data):
        os.makedirs( os.path.dirname( tmp_file ) )
        functions.create_file( tmp_file, data )

    tmp_file = tmp_file
    tmp_dir = os.path.dirname( tmp_file )
    try:
        if not os.path.exists( tmp_dir ):
            create_tmp_essentials(tmp_file, data)
        else:
            functions.clean_tmp(tmp_file)
            create_tmp_essentials(tmp_file, data)
    except:
        print ('[convPY:ERROR] Failed in creating essential file "' + tmp_file +'". Exit!')
        sys.exit(1)


def read_config (file_path):
    """
    ...

    ARGS:
    * file_path   : ...

    RETURN:
        OK      > {DICT}: ...
        ERROR   > Exception & exits with error-code 1
    """
    try:
        return functions.read_JSON_file(file_path)
    except:
        print ('[convPY:Error] Could not read config-file "' + file_path +'". Exit!')
        sys.exit(1)