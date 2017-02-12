import json, os, sys, urllib2
from conv import Conversion, Xslt

#++++++++++++++ functions (import-ready) +++++++++++++

def parseJSONFile (file):
    #file = file.encode('utf-8')
    with open(file, 'r') as data:
        return json.load(data)


def createTempFile (tmp_file, content):
    file = open(tmp_file,"w+") 
    file.write(content) 
    file.close()


def request (url):
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


def open_xml (f):
    with open(f, 'r') as out:
        output = out.read()
    return output

def return_and_cleanup (xml):
    with open(xml, 'r') as out:
        output = out.read()
        os.remove(xml)
        print output
"""
# not functional yet
def readJson():
    steps = sys.stdin.readlines()
    return json.loads(steps[0])
"""

################# MAIN Flow #########################
def main ():
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw'

    
    # Get the data 
    xml_data = request(url)
    #xml_data = open_xml('data/test_xml.xml')
    createTempFile(xml_file_path, xml_data)
    
    # sort the conversion steps
    conversion_steps = scenarios(def_convflow)

    # process the steps
    for scenario in conversion_steps:
        step = eval(scenario)         
        if step['engine'] != False:
            if step['name'] == 'saxon-xslt':
                saxon = Xslt(step, xml_file_path)
                saxon.run()
                #print(saxon.call())
        else:
            conversion = Conversion(step, xml_file_path)
            conversion.run()
            #print(conversion.call())   
            
    # well ... fire output and remove tmp-data
    return_and_cleanup(xml_file_path)
   

if __name__ == '__main__':
    main()

