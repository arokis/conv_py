import os
import json

class Config(object):
    
    def _readJSON (self, path):
        path = os.path.abspath(path)
        if os.path.isfile(path):
            with open(path, 'r') as data:
                return json.load(data)
    
    def __init__ (self, config='config/config.json', scenarios='config/scenarios.json', engines='config/engines.json'):
        self.config = self._readJSON(config)
        self.scenarios = self._readJSON(scenarios)
        self.engines = self._readJSON(engines)
        
        self.defaultFlow = self.config['default-convflow']
        self.conversions = self.config['conversions']
        self.tmpFile = self.config['tmp-file']

    def extensions (self):
        ext = dict()
        for conversion in self.conversions:
            for extension in self.conversions[conversion]['extensions']:
                ext[extension] = conversion
        return ext
    
    
"""
##################### Functions #############################

def configure (path):
    path = os.path.abspath(path)
    if os.path.isfile(path):
        return parse_JSON_file(path)

def parse_JSON_file (file):
    #file = file.encode('utf-8')
    with open(file, 'r') as data:
        return json.load(data)

def eval_extensions (conversions):
    obj = dict()
    for conv in conversions:
        for extension in conversions[conv]['extensions']:
            obj[extension] = conv
    return obj


###################### Global Variables ######################

# conv.py is living here
#home = os.path.dirname(os.path.abspath( __file__ ))

# load config JSON
config_path = 'config/config.json'
config = configure(config_path)

# load convPY's default scenarios JSON
scenarios = configure(config['default-scenarios'])

# load convPY's default convflow JSON
convflow = configure(config['default-convflow'])

# evaluate convPY's extensions supported by default
conversions = config['conversions']
extensions = eval_extensions(conversions)

engines = configure('config/engines.json')


# set temp-file from config
tmpXML = os.path.abspath(config["tmp-file"])
"""

