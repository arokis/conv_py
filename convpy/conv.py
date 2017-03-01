#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
convpy/conv.py
*************
Defines the Class "Convpy".
This is where the magic happens.
"""

import datetime
import os
import sys
import magic
from shutil import rmtree

import iofd_handling as iofd
import converter


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-25"
__all__ = ['Convpy']


class Convpy(object):
    """
    Confpy
    Representing a ConvPY Session aka the scenario driven Conversion you want to run :-D

    ARGS:
    * config: Path to main JSON config-file
    * engines: path to engines JSON config-file
    * scripts: path to scripts JSON config-file
    """
    instance_amount = 0
    home = os.path.abspath(os.path.join(__file__ , os.path.pardir))
    

    def __init__(self, config, engines, scripts):
        Convpy.instance_amount += 1
        self.main_config = config
        self.engines = engines
        self.scripts = scripts
        self.tmp_file = iofd.pathify(True, 'tmp/tmp.tmp')
        self.tmp_dir = os.path.dirname(self.tmp_file)
        self.output = config.config['output-dir']
        self.output_file = ''
        self.scenario = False
        self.source = ''

        iofd.create_dir(self.tmp_dir)


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
        
        def mime_eval(mime, default):
            return {
                'application/xml': '.xml',
            }.get(mime, default)

        mime = magic.from_buffer(content, mime=True)
        #source = self.source
        outfile_name = ''

        if self.source.startswith('http'):
            outfile_name = ''.join(('http_resource_cpy.xml'))
        else:
            source_file = os.path.splitext(os.path.basename(self.source))
            #print source_file
            source_name = source_file[0]
            source_extension = mime_eval(mime, source_file[1])
            

            outfile_name = ''.join((source_name, '_cpy', source_extension))

        iofd.create_dir(self.output)
        iofd.create_file(os.path.join(self.output, outfile_name), content)


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

        TO-DO:
        * Function not smooth! It's crap ... need to make the workflow better
        * Its better to create the first tmp-file in _prepare() from the tmp-dir-path
        * Maybe better to create a tmp-dictionary to ceep track of counter and file
        """
        
        self.source = source

        self._prepare_source(self.source, self.tmp_file)

        self.output_file = self.tmp_file
        
        #print self.scenario
        tmp_nr = 0
        for step in self.scenario:
            outfile_name = str(tmp_nr)
            output_file = os.path.join(self.tmp_dir, ''.join((outfile_name, '.tmp'))) 
            
            #script_MIME = magic.from_file(step['script'], mime=True) 
            #print script_MIME

            if step['type'] == 'xslt':
                language = self.engines.config['Saxon']['xslt']['language']
                engine = os.path.join(self.engines.path, self.engines.config['Saxon']['xslt']['path'])
                #print ' '.join((language, engine, step['script'], self.tmpFile, self.tmpFile))
                converter.Saxon(language, engine).xslt(step['script'], self.output_file, output_file)
            elif step['type'] == 'xquery':
                language = self.engines['Saxon']['xquery']['language']
                engine = os.path.join(self.engines.path, self.engines.config['Saxon']['xquery']['path'])
                #engine = os.path.join(self.home, self.engines['Saxon']['xquery']['path'])
                converter.Saxon(language, engine).xquery(step['script'], self.output_file, output_file)
            else:
                in_param = ''.join( ('-i ' + self.output_file) )
                out_param = ''.join( ('-o ' + output_file) )
                converter.Call(step['language']).run(step['script'], in_param, out_param)
                #print step['language'], step['script'], parameter
            
            self.output_file = output_file
            tmp_nr += 1


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
        #print 'The actual source of output: ' + self.output_file
        
        output = iofd.open_file(self.output_file)
        
        print output
        
        #mime = magic.from_file(self.output_file, mime=True) 
        
        if write_output and self.output != 'None':
            self._create_output_file(output)
        #print 'Save ' + self.output_file


    def _prepare_source(self, source, target):
        """
        preparation Methode that creates the neccessary file-structure

        ARGS:
        * self: The actual configured convPY Instance
        * source: the source beeing converted

        CREATS:
        * TEMPORARY FILE
        """
        source = iofd.retrieve(source)
        try:
            iofd.create_file(target, source)
        except IOError:
            print ('[convPY:ERROR] Failed in creating temporary file "' + target +'". Exit!')
            sys.exit(1)


    def _scenarioise(self, scenario_step):
        """
        tries to synchronise a given scenario with ConvPY's scripts

        ARGS:
        * self: The actual configured convPY Instance
        * scenario: scenario which is going to be synchronised

        RETURNS:
        * {DICT}: synchronised Dictionary with expanded script paths
        """
        
        def scripts_param(scenario, key):
            try:
                return self.scripts.config[scenario][key]
            except KeyError:
                return False
        
        obj = {}
        if scenario_step.get('scenario'):
            #print 'CONVPY SCENARIO'
            scenario_name = scenario_step['scenario']
            scripts_path = self.scripts.path
            tmp_path = self.tmp_dir
            output_format = scripts_param(scenario_name, 'output')
            
            obj['name'] = scenario_name
            obj['type'] = scripts_param(scenario_name, 'type')
            obj['language'] = scripts_param(scenario_name, 'language')
            
            script = scripts_param(scenario_name, 'script')
            obj['script'] = os.path.join(scripts_path, script)
            obj['output'] = scripts_param(scenario_name, 'output')
            
        else:
            #print 'USER DEFINED SCENARIO'
            obj = scenario_step
        return obj


    def convert(self, source, scenario, write_output=True):
        """
        main conversion routine which creates Conversion-Instances, calls the Converter-Instances
        and ends ConvPY with sys.exit('0') if everything worked well

        ARGS:
        * self: The actual configured convPY Instance
        * source: a source that may be a single file, a directory or a python list
        * scenario: The given scenario which is going to be worked at
        * write_output: Flag to set the output-mode to True (create output-file) or False (don't create output-file)
        """
        #print ('{} {}'.format(source, self.tmp_file))
        self.scenario = [self._scenarioise(step) for step in scenario]

        if isinstance(source, list):
            #print ('List')
            for item in source:
                self._work_the_flow(item)
                self._output(write_output)
        elif os.path.isdir(source):
            #print ('DIR')
            dir_files = iofd.walk_dir(source)
            for item in dir_files:
                self._work_the_flow(item)
                self._output(write_output)
            #print dir_files
        elif os.path.isfile(source) or isinstance(source, unicode) or isinstance(source, str):
            #print ('File or URL-Resource')
            self._work_the_flow(source)
            self._output(write_output)
        else:
            print ('Nor DIR nor File nor List')
            sys.exit(1)
        
        self._clean_tmp_dir()
        sys.exit(0)

