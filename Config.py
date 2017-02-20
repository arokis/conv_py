import os
import json

import functions
import Converter 

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
        

    def prepare (self, data):
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
