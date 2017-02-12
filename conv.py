import subprocess, json, os, tempfile, sys, urllib2

#++++++++++++++ functions (import-ready) +++++++++++++
def parseJSONFile (file):
    #file = file.encode('utf-8')
    with open(file, 'r') as data:
        return json.load(data)


def createTempFile (tmp_file, content):
    file = open(tmp_file,"w+") 
    file.write(content) 
    file.close()


def reguest (url):
    response = urllib2.urlopen(url)
    data = response.read()
    return data


#************** global vars **************************

# conv.py is living here
conv_py_home = os.path.dirname(os.path.abspath( __file__ ))

# load config
config_path = os.path.join(conv_py_home, 'config/config.json')
config = parseJSONFile(config_path)

# load engines from config
default_engines = config['conversion']

# load default-scenarios from config
def_scenarios_path = os.path.join(conv_py_home, config['default-scenarios'])
def_scenarios = parseJSONFile(def_scenarios_path)

# load convflow from config
def_convflow_path = os.path.join(conv_py_home, config['default-convflow'])
def_convflow = parseJSONFile(def_convflow_path)

# set temp-file from config
xml_file_path = os.path.join(conv_py_home, config["tmp-file"])



#~~~~~~~~~~~~~~~~ business logic ~~~~~~~~~~~~~~~~~~~~~

def scenarios (convflow):
    result = []
    scenario_index = [i for i in def_scenarios]
    
    for step in convflow['steps']:
        scenario_name = step['scenario'] 
        if scenario_name in scenario_index:
            result.append(def_scenarios[scenario_name]) 
        else: 
            result.append(step)
    #print result
    return result

def eval (scenario):
    scenario_type = scenario['conv-type']
    scenario_script = os.path.join(conv_py_home, scenario['script'])
    conversion = {}

    if scenario_type in default_engines:
        conversion = default_engines[scenario_type]
        conversion['engine'] = os.path.join(conv_py_home, default_engines[scenario_type]['engine'])
        conversion['script'] = scenario_script
    
    elif scenario.get('engine') and scenario.get('language'):
        conversion['engine'] = os.path.join(conv_py_home, scenario['engine'])
        conversion['language'] = scenario['language']
        conversion['script'] = scenario_script

    elif not scenario.get('engine') and scenario.get('language'):
        conversion['language'] = scenario['language']
        conversion['script'] = scenario_script
        conversion['name'] = scenario_type
        conversion['engine'] = False
        
    else:
        #print('[CONVPY:ERROR] No engine or language defined on ' + scenario_script)
        conversion = False
    
    return conversion
    

"""
# not functional yet
def readJson():
    steps = sys.stdin.readlines()
    return json.loads(steps[0])
"""

def open_xml (f):
    with open(f, 'r') as out:
        output = out.read()
    return output

class Conversion (object):
    def __init__(self, obj, source):
        self.script = obj['script']
        self.language = obj['language']
        self.engine = obj['engine']
        self.name = obj['name']
        self.source = source
    
    def speak (self):
        print ('Conversion "' + self.name + '" via ' + self.language + ':' + str(self.engine) + ' using ' + self.script + ' on ' + self.source)

    def createXML (self, content):
        file = open(self.source,"w+") 
        file.write(content) 
        file.close()

    def run (self):
        call = ''
        if self.engine != False:
            if self.name == 'saxon-xslt':
                script = "-xsl:" + self.script
                source = "-s:" + self.source
                call = (self.language, self.engine, script, source)

            elif self.name == 'saxon-xquery':
                script = "-xquery:" + self.script
                source = "-s:" + xml_file_path
                call = (self.language, self.engine, script, source)
        else:
            call = (self.language, self.script, self.source)
        
        output = subprocess.check_output(" ".join(call), shell=True)
        self.createXML(output)
        

################# MAIN Flow #########################
def main ():
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw'


    #xml_data = request(url)
    xml_data = open_xml('data/test_xml.xml')
    createTempFile(xml_file_path, xml_data)
    

    conversion_steps = scenarios(def_convflow)

    for scenario in conversion_steps:
        conv = eval(scenario) 
        conversion = Conversion(conv, xml_file_path)
        conversion.run()

    
    with open(xml_file_path, 'r') as out:
        output = out.read()
        os.remove(xml_file_path)
        print output
 
   

if __name__ == '__main__':
    main()

