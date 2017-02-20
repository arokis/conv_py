import subprocess
import os
import json

import Config
convpy = Config.ConvPY('config/config.json')

class Converter (object):
    def __init__(self, path, script, source, output):
        self.script = os.path.abspath(script)
        self.source = os.path.abspath(source)
        self.output = os.path.abspath(output) 

    def _process (self, call):
        subprocess.check_output(call, shell=True)

    def info (self):
        print ('Simple Converison from ' + self.source + ' to ' + self.output)



class Saxon (Converter):
    def __init__(self, path, engine, script, source=convpy.tmpFile, output=convpy.tmpFile):
        Converter.__init__(self, path, script, source, output)
        self.engine = engine

    def info (self):
        print ('SAXON: via ' + self.language + ' from ' + self.path + ' using ' + self.script + ' on ' + self.source)
        print self.engine

    def xslt (self):
        self.language = self.engine['xslt']['language']
        self.path = os.path.abspath(self.engine['xslt']['path']) 
        #self.path = os.path.abspath(self.engine['xslt']['path'])
        script = ''.join( ( self.engine['xslt']['script-param'], self.script ) )
        source = ''.join( ( self.engine['xslt']['source-param'], self.source ) )
        output = ''.join( ( self.engine['xslt']['output-param'], self.output ) )
        call = ( ' '.join( ( self.language, self.path, script, source, output ) ) )
        #self._process(call)
        print call

    def xquery (self):
        self.language = self.engine['xquery']['language']
        self.path = os.path.abspath(self.engine['xquery']['path']) 
        script = ''.join( ( self.engine['xquery']['script-param'], self.script ) )
        source = ''.join( ( self.engine['xquery']['source-param'], self.source ) )
        call = ( ' '.join( ( self.language, self.path, script, source ) ) )



class Call (object):
    def __init__(self, language, script, source=convpy.tmpFile, output=convpy.tmpFile):
        #Converter.__init__(self, script, source, output)
        self.language = language
        self.script = os.path.abspath(script)
        self.source = os.path.abspath(source)
        self.output = os.path.abspath(output)

    def info (self):
        print ('I am a ' + self.language + ' Call!')

    def run (self, source=convpy.tmpFile, output=convpy.tmpFile):
        call =  ( ' '.join( (self.language, self.script, self.source) ) )
        #subprocess.check_output(call, shell=True)
        print call
