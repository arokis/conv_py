import json, os, sys, urllib2
import convpy


#++++++++++++++ functions (import-ready) +++++++++++++


def createTempFile (tmp_file, content):
    file = open(tmp_file,"w+") 
    file.write(content) 
    file.close()


def request (url):
    response = urllib2.urlopen(url)
    data = response.read()
    return data





#************** configure convpy instance **************************

# conv.py is living here
conv_py_home = convpy.home
#print(conv_py_home)

# load configuration
config = convpy.config

# set default scenarios as given in scenarios.json
def_scenarios = convpy.scenarios

# set default conversion flow as given in config.json (default: vmr2nlp)
def_convflow = convpy.convflow

# set default engines as given in config.json (default: xslt, xquery, other)
default_engines = convpy.engines

# set the temporary xml-file-path to store the data as given in config.json (default: tmp/tmp.xml)
xml_file_path = convpy.tmpXML



#~~~~~~~~~~~~~~~~ business logic ~~~~~~~~~~~~~~~~~~~~~

def eval (scenario):
    scenario_type = scenario['type']
    scenario['script'] = os.path.join(conv_py_home, scenario['script'])
    conversion = {}
    #print scenario
    
    if scenario_type in default_engines:
        #conversion = default_engines[scenario_type]
        scenario['engine'] = os.path.join(conv_py_home, default_engines[scenario_type]['engine'])
        scenario['language'] = default_engines[scenario_type]['language']
    elif scenario.get('engine') and scenario.get('language'):
        scenario['engine'] = os.path.join(conv_py_home, scenario['engine'])
    elif not scenario.get('engine') and scenario.get('language'):
        scenario['engine'] = False
    else:
        #print('[CONVPY:ERROR] No engine or language defined on ' + scenario_script)
        scenario = False
    return scenario
    

def open_xml (f):
    with open(f, 'r') as out:
        output = out.read()
    return output

def inform(xml, clean):
    with open(xml, 'r') as out:
        output = out.read()
    if clean == True:
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
    #xml_data = request(url)
    xml_data = open_xml('data/test_xml.xml')
    createTempFile(xml_file_path, xml_data)
    
    # sort the conversion steps
    conversion_steps = convpy.workflow(def_convflow, def_scenarios)
    #print (def_scenarios)
    #print (def_convflow)
    #print (conversion_steps)

    
    for scenario in conversion_steps:
        step = eval(scenario)     
        #print step
        
        if step['engine'] != False:
            if step['type'] == 'xslt':
                saxon = convpy.Xslt(step, xml_file_path)
                saxon.run()
                del saxon
                #print(saxon.call())
        else:
            conversion = convpy.Conversion(step, xml_file_path)
            conversion.run()
            del conversion
            #print(conversion.call())   
    
    # well ... fire output and remove tmp-data
    inform(xml_file_path, False)


if __name__ == '__main__':
    main()

