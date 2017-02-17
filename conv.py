import json 
import os
import sys
import Config

from functions import clean_tmp, create_file, open_file, preset, request, finish  
from Converter import Converter, Call, Saxon

ConvPY = Config.Config('config/config.json')
# set default scenarios as given in scenarios.json and set temporary conversion file
default_scenarios = ConvPY.scenarios
tmpXML = ConvPY.tmpFile

#++++++++++++++ functions +++++++++++++

def convert (convflow):
    
    def scenarioise (scenario, defaults):
        try:
            obj = dict(defaults[scenario['scenario']])
            obj['name'] = scenario['scenario']
            return obj
        except KeyError:
            print ("[convPY:ERROR] Scenario does not match! Cleaning up and aborting conversion ...")
            dir = os.path.dirname(tmpXML)
            os.remove(tmpXML)
            os.rmdir(dir)
            sys.exit(1)
        
 
    result = []   
    #extensions = configuration.extensions
    #print extensions
    extensions = ConvPY.extensions()
    
    for step in convflow:
        if step.get('scenario'):
            scenario = scenarioise(step, default_scenarios)
                
            
            #print scenario
          
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
                eng = Saxon( script )
                eng.xslt()

            elif scenario['type'] == 'xquery':
                eng = Saxon()
                eng.xquery(script)
            
            else: 
                print ("[convPY:WARNING] Scenario-Type is unknown to convPY! It won't be converted")
        else :
            call = Call(step['language'],step['script'])
            call.run()
            #call.info()
            




################# MAIN #################
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
    
    # loads the json-data 
    requested_scenario = json.loads(data)

    
    #print (os.path.abspath(Config.tmpFile))
    # conv.py is living here
    #convpy_home = os.path.dirname(os.path.abspath( __file__ ))

    
    
    xml_data = open_file('data/test_xml.xml')
    
    # creates all the files needed
    preset(xml_data, tmpXML)
    
    # takes the conversion workflow from data
    defined_convflow = requested_scenario['steps']
    #print (defined_convflow)

    # runs the conversion for curren workflow
    wf = convert(defined_convflow)

    # puts out the result and clears temporary data
    finish(tmpXML)


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