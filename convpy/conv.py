#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
convpy/conv.py
*************
Defines configuration-functions and the Classes "Config" and "Convpy".
"""

import datetime
import os
import sys
from shutil import rmtree

import functions
import converter


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-25"


class Config(object):
    """
    Config-Class:
    Representing a config file and content

    ARGS:
    * config: Path to JSON config-file
    """
    def __init__(self, config):
        self.path = os.path.dirname(config)
        self.config = self._read(config)

    def _read(self, file_path):
        """
        Config-Class non-public methode reading in a JSON config-file by its path

        ARGS:
        * file_path   : file path to JSON config

        RETURN:
            OK      > {DICT}: ...
            ERROR   > Exception & exits with error-code 1
        """
        try:
            return functions.read_json_file(file_path)
        except:
            print('[convPY:Error] Could not read config-file "' + file_path +'". Exit!')
            sys.exit(1)



class Confpy(object):
    """
    Confpy
    Representing a ConvPY Session aka the scenario driven Conversion you want to run :-D

    ARGS:
    * config: Path to main JSON config-file
    * engines: path to engines JSON config-file
    * scripts: path to scripts JSON config-file
    """
    def __init__(self, config, engines, scripts):
        self.main_config = config
        self.engines = engines
        self.scripts = scripts
        self.tmp_file = pathify(True, 'tmp/tmp.xml')
        self.tmp_dir = os.path.dirname(self.tmp_file)
        self.output = config.config['output-dir']
        self.scenario = False
        self.source = ''

        functions.create_dir(self.tmp_dir)


    def _create_output_file(self, content):
        """
        creates the output file and constructs this files name

        ARGS:
        * self: The actual configured convPY Instance
        * content: content to write into the output-file

        CREATES:
        * FILE

        TO-DO:
        * file and path handling sucks: extensions should be taken from tmp-file since thsi is
          the file beeing copyed
        * how to handle URL-Resources consitently?
        """

        #source = self.source
        outfile_name = ''

        if self.source.startswith('http'):
            outfile_name = ''.join(('http_resource_cpy.xml'))
        else:
            source_file = os.path.splitext(os.path.basename(self.source))
            #print source_file
            source_name = source_file[0]
            source_extension = source_file[1]

            outfile_name = ''.join((source_name, '_cpy', source_extension))

        functions.create_dir(self.output)
        functions.create_file(os.path.join(self.output, outfile_name), content)


    def _clean_tmp_dir(self):
        """
        cleans all the temporary data incl. temporary directory

        ARGS:
        * self: The actual configured convPY Instance
        """
        try:
            if self.tmp_dir != os.path.dirname(os.path.abspath(os.path.join(__file__, os.path.pardir))):
                rmtree(self.tmp_dir)
        except:
            print ('[convPY:WARNING] Could not clean up "' + self.tmp_dir +'". Maybe you should clean it manually!')
            sys.exit(0)


    def _work_the_flow(self, source):
        """
        main converison routine calling the different Converter Classes.
        Also tracks self.source

        ARGS:
        * self: The actual configured convPY Instance
        * source: the source being converted

        CREATES:
        * TEMPORARY FILE
        """
        self.source = source
        self._prepare(self.source)

        for step in self.scenario:
            if step['type'] == 'xslt':
                language = self.engines.config['Saxon']['xslt']['language']
                engine = os.path.join(self.engines.path, self.engines.config['Saxon']['xslt']['path'])
                #print ' '.join((language, engine, step['script'], self.tmpFile, self.tmpFile))
                converter.Saxon(language, engine).xslt(step['script'], self.tmp_file, self.tmp_file)
            elif step['type'] == 'xquery':
                language = self.engines['Saxon']['xquery']['language']
                engine = os.path.join(self.engines.path, self.engines.config['Saxon']['xquery']['path'])
                #engine = os.path.join(self.home, self.engines['Saxon']['xquery']['path'])
                converter.Saxon(language, engine).xquery(step['script'], self.tmp_file, self.tmp_file)
            else:
                converter.Call(step['language']).run(step['script'], self.tmp_file)


    def _output(self, write_output=True):
        """
        puts out the result on stdout and as output-file if spcified

        ARGS:
        * self: The actual configured convPY Instance
        * write_output:
            True: output will be written to file in specified path from config.json
            False: no output-file will be created

        RETURN:
        * STDOUT: the conversion result represented by tmp-file
        """
        output = functions.open_file(self.tmp_file)
        print output
        if write_output and self.output != 'None':
            self._create_output_file(output)


    def _prepare(self, source):
        """
        preparation Methode that creates the neccessary file-structure

        ARGS:
        * self: The actual configured convPY Instance
        * source: the source beeing converted

        CREATS:
        * TEMPORARY FILE
        """
        source = functions.retrieve(source)
        #if os.path.exists(self.tmp_file):
        #    os.remove(self.tmp_file)
        try:
            functions.create_file(self.tmp_file, source)
        except IOError:
            print ('[convPY:ERROR] Failed in creating temporary file "' + self.tmp_file +'". Exit!')
            sys.exit(1)


    def _scenarioise(self, scenario):
        """
        tries to synchronise a given scenario with ConvPY's scripts

        ARGS:
        * self: The actual configured convPY Instance
        * scenario: scenario which is going to be synchronised

        RETURNS:
        * {DICT}: synchronised Dictionary with expanded script paths
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


    def convert(self, source, write_output=True):
        """
        main conversion routine which creates Conversion-Instances, calls the Converter-Instances
        and ends ConvPY with sys.exit('0') if everything worked well

        ARGS:
        * self: The actual configured convPY Instance
        * flow: the givern conversion-workflow which should to be done
        
        TO-DO:
        * Not check the type but check if source is os.path.isdir()
          or os.path.isfile()
        * If os.path.isdir() create list of all files in dir with absolute path
        """
        #print type(source)
        if isinstance(source, str) or isinstance(source, unicode):
            self._work_the_flow(source)
            self._output(write_output)
        elif isinstance(source, list):
            for item in source:
                self._work_the_flow(item)
                self._output(write_output)
        else:
            sys.exit(1)

        self._clean_tmp_dir()
        sys.exit(0)


    def read_scenario(self, scenario):
        """
        ConvPY's public class reading in a given scenario.
        After synchronising the scenario it is saved as ConvPY's scenario-attribute

        ARGS:
        * self: The actual configured convPY Instance
        * scenario: given conversion scenario

        RETURN:
        * self.scenario: the synchronised scenario for the actual ConvPY-Instance
        """
        scenario_steps = []
        for step in scenario:
            scenario_steps.append(self._scenarioise(step))
        self.scenario = scenario_steps



def configure(config_file):
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


def pathify(homeify, *arg):
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
        home = os.path.dirname(os.path.abspath(os.path.join(__file__ , os.path.pardir)))
        #print 'homeify'
        #print os.path.join(home, path)
        return os.path.join(home, joined)
    else:
        #print 'relative'
        #print joined
        return os.path.abspath(joined)
