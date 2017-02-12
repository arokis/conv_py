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


def getXml (url):
    response = urllib2.urlopen(url)
    data = response.read()
    return data

#************** global vars **************************

conv_py_home = os.path.dirname(os.path.abspath( __file__ ))

# load config
config_path = os.path.join(conv_py_home, 'config/config.json')
config = parseJSONFile(config_path)
#print(config)

# load engines from config
default_engines = config['conversion']

# load default-scenarios from config
def_scenarios_path = os.path.join(conv_py_home, config['default-scenarios'])
def_scenarios = parseJSONFile(def_scenarios_path)
#print (def_scenarios_path)

# load convflow from config
def_convflow_path = os.path.join(conv_py_home, config['default-convflow'])
def_convflow = parseJSONFile(def_convflow_path)
#print (convflow)
#print(def_convflow_path)

# set temp-file from config
xml_file_path = os.path.join(conv_py_home, config["tmp-file"])
#xml_file = config["tmp-file"]
#print(xml_file_path)

# set the saxon path from config.json
#saxon_path = config["engines"]["saxon"]["path"]



#~~~~~~~~~~~~~~~~ business logic ~~~~~~~~~~~~~~~~~~~~~

def mergeScenarios (convflow):
    result = []
    scenario_index = [i for i in def_scenarios]
    
    for step in convflow['steps']:
        scenario_name = step['scenario'] 
        if scenario_name in scenario_index:
            result.append(def_scenarios[scenario_name]) 
        else: 
            result.append(step)
    return result


def convert (xml_data, scenarios, data):
    scenario_index = []
    scenario_obj = {}
    steps = data['steps']
    
    for scenario in scenarios:
        scenario_index.append(scenario['scenario'])
        scenario_obj[scenario['scenario']] = scenario['script']
             
    print (scenario_index)
    print (scenario_obj)

    createTempFile(xml_file, xml_data)
    
    # run the convflow
    for i in steps:
        step = i['scenario']
        
        if step in scenario_index:
            print (step + " on " + xml_file + " via " + scenario_obj[step] + " with engine: " + saxon_path)
            #saxon(xml_file, scenario_obj[step])
        else:
            print (step + 'is undefined')

    # when conversion is finished read the last conversion output from file and remove it
    with open(xml_file, 'r') as out:
        output = out.read()
        os.remove(xml_file)
        #print output    
        


"""
# not functional yet
def readJson():
    steps = sys.stdin.readlines()
    return json.loads(steps[0])
"""


def saxon(xml, xsl) :
    script = "-xsl:" + xsl
    source = "-s:" + xml
    cmd_call = (config["engines"]["saxon"]["language"], config["engines"]["saxon"]["path"], source, script)
    
    output = subprocess.check_output(" ".join(cmd_call), shell=True)
    createTempFile(xml_file, output)


################# MAIN Flow #########################
def main ():
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw'

    

    xml_data = getXml(url)
    createTempFile(xml_file_path, xml_data)
    
    for scenario in mergeScenarios(def_convflow):
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
        
        #print conversion

        call = False

        if conversion != False:
            
            if conversion['engine'] != False:
                if conversion['name'] == 'saxon-xslt':
                    script = "-xsl:" + conversion['script']
                    source = "-s:" + xml_file_path
                    call = (conversion['language'], conversion['engine'], script, source)

                elif conversion['name'] == 'saxon-xquery':
                    script = "-xquery:" + conversion['script']
                    source = "-s:" + xml_file_path
                    call = (conversion['language'], conversion['engine'], script, source)
            else:
                call = (conversion['language'], conversion['script'], xml_file_path)
        
        #print(" ".join(call))
        output = subprocess.check_output(" ".join(call), shell=True)
        createTempFile(xml_file_path, output)

    with open(xml_file_path, 'r') as out:
        output = out.read()
        os.remove(xml_file_path)
        print output
    
    
    """
    xml_data = getXml(url)
    convert(xml_data, def_scenarios, convflow)
    """
   

if __name__ == '__main__':
    main()

