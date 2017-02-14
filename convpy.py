import json, os, sys, urllib2
import modules

# conv.py is living here
convpy_home = os.path.dirname(os.path.abspath( __file__ ))

# set default scenarios as given in scenarios.json
default_scenarios = modules.scenarios

# set default engines as given in config.json (default: xslt, xquery, other)
default_engines = modules.engines

tmpXML = modules.tmpXML

#++++++++++++++ functions (import-ready) +++++++++++++



def workflow (convflow):
    result = []    
    for step in convflow['steps']:
        if step.get('scenario'):
            default_scenarios[step['scenario']]['name'] = step['scenario']
            result.append(default_scenarios[step['scenario']])
        else:
            result.append(step)
    return result

def eval (scenario):
    scenario_type = scenario['type']
    scenario['script'] = os.path.abspath(scenario['script'])
    conversion = {}
    #print scenario
    
    if scenario['type'] in [key for key in default_engines] and not scenario.get('engine'):
        #conversion = default_engines[scenario_type]
        scenario['engine'] = os.path.abspath(default_engines[scenario_type]['engine'])
        scenario['language'] = default_engines[scenario_type]['language']
    elif scenario.get('engine') and scenario.get('language'):
        scenario['engine'] = os.path.abspath(scenario['engine'])
    elif not scenario.get('engine') and scenario.get('language'):
        scenario['engine'] = False
    else:
        #print('[CONVPY:ERROR] No engine or language defined on ' + scenario_script)
        scenario = False
    return scenario

def convert (step, source):
    if step['engine'] != False:
        if step['type'] == 'xslt':
            saxon = modules.Xslt(step, source)
            saxon.run()
            #print(saxon.call())
            del saxon
            
    else:
        conversion = modules.Conversion(step, source)
        conversion.run()
        #print(conversion.call())
        del conversion
        
def outputFile (content, file):
    file = open(file,"w+") 
    file.write(content) 
    file.close()
    

def request (url):
    response = urllib2.urlopen(url)
    data = response.read()
    return data

def open_xml (f):
    with open(f, 'r') as out:
        output = out.read()
    return output

def inform(xml, clean):
    #print(os.path.dirname(xml))
    #
    with open(xml, 'r') as out:
        output = out.read()
    if clean == True:
        dir = os.path.dirname(xml)
        os.remove(xml)
        os.rmdir(dir)
    print output
    #

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
    #xml_data = request(url)
    xml_data = open_xml('data/test_xml.xml')

    if not os.path.exists(os.path.dirname(tmpXML)):
        os.makedirs(os.path.dirname(tmpXML))
        modules.createTempFile(tmpXML, xml_data)

    
    
    # sort the conversion steps
    defined_convflow = modules.convflow
    conversion = workflow(defined_convflow)
   
    
    for scenario in conversion:
        step = eval(scenario)     
        #print step
        convert(step, tmpXML)   
    
    # well ... fire output and remove tmp-data
    inform(tmpXML, True)
    

if __name__ == '__main__':
    main()

