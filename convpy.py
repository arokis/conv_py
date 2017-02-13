import subprocess, os, json
from modules import Xslt, Conversion, Xquery


##################### Functions #############################

def configure (path):
    path = os.path.abspath(path)
    if os.path.isfile(path):
        return parseJSONFile(path)

def parseJSONFile (file):
    #file = file.encode('utf-8')
    with open(file, 'r') as data:
        return json.load(data)

def outputFile (content, file):
    file = open(file,"w+") 
    file.write(content) 
    file.close()


def workflow (convflow, scenarios):
    result = []
    scenario_index = [i for i in scenarios]
    
    for step in convflow['steps']:
        scenario_name = step['scenario'] 
        if scenario_name in scenario_index:
            result.append(scenarios[scenario_name]) 
        else: 
            result.append(step)
    #print result
    return result

###################### Global Variables ######################

# conv.py is living here
home = os.path.dirname(os.path.abspath( __file__ ))

# load config JSON
config_path = 'config/config.json'
config = configure(config_path)

# load convPY's default scenarios JSON
scenarios = configure(config['default-scenarios'])

# load convPY's default convflow JSON
convflow = configure(config['default-convflow'])

# set convPY's default engines
engines = config['conversion']

# set temp-file from config
tmpXML = os.path.abspath(config["tmp-file"])
