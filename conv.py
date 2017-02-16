import json, os, sys, urllib2
#import modules
from classes import Conversion, Call, Saxon
import configuration

# conv.py is living here
#convpy_home = os.path.dirname(os.path.abspath( __file__ ))

# set default scenarios as given in scenarios.json
default_scenarios = configuration.scenarios

tmpXML = configuration.tmpXML

#++++++++++++++ functions +++++++++++++
def create_file (file, content):
    file = open(file,"w+") 
    file.write(content) 
    file.close()

def convert (convflow):
    
    def scenarioise (scenario, defaults):
        obj = dict(defaults[scenario['scenario']])
        obj['name'] = scenario['scenario']
        #obj[scenario['scenario']] = defaults[scenario['scenario']] 
        return obj
 
    result = []   
    extensions = configuration.extensions
    #print extensions
    
    for step in convflow:
        if step.get('scenario'):
            #print 'Default SCENARIO'   
            scenario = scenarioise(step, default_scenarios)
            #print scenario
            #print scenario['type']

            """
            scenario_type = None
            for key in scenario:
                #print key
                file_extension = os.path.splitext(scenario['script'])[1]
                if file_extension in [key for key in extensions]:
                    scenario_type = configuration.conversions[extensions[file_extension]]
            """  
        
            script = scenario['script']

            if scenario['type'] == 'xslt':
                #print script
                eng = Saxon( script )
                eng.xslt()
                #eng.info()
            elif scenario['type'] == 'xquery':
                eng = Saxon()
                eng.xquery(script)
        else :
            #print 'Normal STEP'
            call = Call(step['language'],step['script'])
            call.run()
            #call.info()
            
            #print step
            #result.append(step)
    #print(result)
    #return result

def get_extensions (engines):
    obj = dict()
    for engine in engines:
        for extension in engine['on-extensions']:
            obj[extension] = engine
    return obj

def inform(clean, xml=configuration.tmpXML):
    #print(os.path.dirname(xml))
    #
    with open(xml, 'r') as out:
        output = out.read()
    if clean == True:
        dir = os.path.dirname(xml)
        os.remove(xml)
        os.rmdir(dir)
    print output

def open_xml (f):
    with open(f, 'r') as out:
        output = out.read()
    return output

def presets(data, tmpXML=configuration.tmpXML):
    if not os.path.exists(os.path.dirname(tmpXML)):
        os.makedirs(os.path.dirname(tmpXML))
        create_file(tmpXML, open_xml(data))

def request (url):
    response = urllib2.urlopen(url)
    data = response.read()
    return data

################# MAIN Flow #########################
def main ():
    if len(sys.argv) > 1:
        data = ' '.join(sys.argv[1:])
        #{"url" : "http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw","steps" : [{"scenario"  : "cs:nlp"},{"name"  : "cs:post-processing","desc"  : "RegEx","type"  : "regex","script"    : "regex/cs_post.py","conversion": {"language"  : "python"}}]}
    else:
        data = """{
                "url" : "http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw",
                "steps" : [
                    {"scenario" : "cs_nlp"},
                    {"scenario" :   "strip-space"},
                    {
                        "name"  : "cs_post-processing",
                        "desc"  : "RegEx Postprocessing to clean up the data",
                        "type"  : "regex",
                        "script": "regex/cs_post.py",
                        "language"  : "python"
                    }
                ]}"""
    

    
    

    data = json.loads(data)

    presets('data/test_xml.xml', tmpXML)
    
    #print (modules.routine())
    #print ('CONVFLOW: ')
    defined_convflow = data['steps']
    #print (defined_convflow)

    
    #print ('WORKFLOW: ')
    wf = convert(defined_convflow)

    
    inform(True)


if __name__ == '__main__':
    main()



"""
class Test(object):
    def __init__(self, t):
        self.test = t
    
    def hello(self):
        print self.test


a = {"Testing" : "Test"}
print(type(a['Testing']))

print(type(a['Testing']).__name__)

b = vars()[a['Testing']]('s')
b.hello()
"""