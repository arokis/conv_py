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

# load config
config = parseJSONFile('config/config.json')
#print(config)

# load default-scenarios from config
def_scenarios = parseJSONFile(config['default-scenarios'])
#print (def_scenarios)

# load convflow from config
convflow = parseJSONFile(config['default-convflow'])
#print (convflow)

# set temp-file from config
xml_file = config["tmp-file"]
    
# set the saxon path from config.json
saxon_path = config["engines"]["saxon"]["path"]



#~~~~~~~~~~~~~~~~ business logic ~~~~~~~~~~~~~~~~~~~~~

def convert (xml_data, scenarios, data):
    scenario_index = []
    scenario_obj = {}
    steps = data['steps']
    
    for scenario in scenarios:
        scenario_index.append(scenario['scenario'])
        scenario_obj[scenario['scenario']] = scenario['script']
             
    #print (scenario_index)
    #print (scenario_obj)

    createTempFile(xml_file, xml_data)
    
    # run the convflow
    for i in steps:
        step = i['scenario']
        
        if step in scenario_index:
            #print (step + " on " + xml_file + " via " + scenario_obj[step] + " with engine: " + saxon_path)
            saxon(xml_file, scenario_obj[step])

    # when conversion is finished read the last conversion output from file and remove it
    with open(xml_file, 'r') as out:
        output = out.read()
        os.remove(xml_file)
        print output    
        


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

def buildURL (provider, request):
    return 0


################# MAIN Flow #########################
def main ():
    #print(sys.argv[1])
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw'


    #print ('conv.py: ' + url)
        
    #print ('internal: ' + url)

    xml_data = getXml(url)
    convert(xml_data, def_scenarios, convflow)
   
   

if __name__ == '__main__':
    main()

