#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
convpy/converter.py
*************
Defines the Converter-Classes of ConvPY
"""

import subprocess
import os
import json


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-12"


class Converter (object):
    def __init__(self, call):
        self.process = list()
        #self.call = call
        self.process.append(call)

    def _process (self, call):
        subprocess.check_output(call, shell=True)

    def info (self):
        print ('Simple Converison with ' + self.process)



class Saxon (Converter):
    def __init__(self, call, engine_path):
        Converter.__init__(self, call)
        #self.engine_path = engine_path
        self.process.append(engine_path)

    def info (self):
        print ('SAXON: via ' + self.call + ' using ' + self.engine_path + ' with CALL:')
        print ' '.join((self.engine_path, self.call))

    def xslt (self, script, source, output, params=False):
        self.script = ''.join(('-xsl:', script))
        self.process.append(self.script)
        
        self.source = ''.join(('-s:', source))
        self.process.append(self.source)
        
        self.output = ''.join(('-o:', output))
        self.process.append(self.output)
        
        if params != False:
            self.process.append(params)
        self._process(' '.join(self.process))
        #print ' '.join(self.process)

    def xquery (self, script, source, output, params=False):
        self.script = ''.join(('-xq:', script))
        self.process.append(self.script)
        
        self.source = ''.join(('-s:', source))
        self.process.append(self.source)
        
        self.output = ''.join(('-o:', output))
        self.process.append(self.output)
        
        if params != False:
            self.process.append(params)
        #self._process(call)
        print ' '.join(self.process)


class Call (Converter):
    def __init__(self, call):
        Converter.__init__(self, call)

    def info (self):
        print ('I am a ' + self.process[0] + ' Call!')

    def run (self, script, source, output=False):
        self.script = os.path.abspath(script)
        self.process.append(self.script)

        self.source = os.path.abspath(source)
        self.process.append(self.source)

        #self.output = os.path.abspath(output)
        #call =  ( ' '.join( (self.call, self.script, self.source) ) )
        #subprocess.check_output(call, shell=True)
        self._process(' '.join(self.process))
        #print ' '.join(self.process)
