import json 
import os
import sys

import functions

import Converter 
import Conversion
import Config



convpy = Config.ConvPY('config/config.json')
convpy.configure()

# set default scenarios as given in scenarios.json and set temporary conversion file
#default_scenarios = ConvPY.scenarios
#tmpXML = ConvPY.tmpFile


#print convpy.config
#print convpy.home
#print convpy.scenarios
#print convpy.engines_path
#print convpy.engines_config
#print os.path.join(convpy.home, convpy.engines['Saxon']['xslt']['path'])
#print convpy.scripts



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
                        "script": "scripts/regex/cs_post.py",
                        "language"  : "python"
                    }
                ]}"""
    
    #print (' '.join(sys.argv[1:]))

    # loads the json-data 
    requested_scenario = json.loads(data)
    
    f = 'data/test_xml.xml'
    url = requested_scenario['url']

    #xml_data = functions.open_file('data/test_xml.xml')
    xml_data = functions.retrieve(url)
    
    
    # creates all the files needed
    convpy.prepare(xml_data)
   
    
    

    # takes the conversion workflow from data
    defined_convflow = requested_scenario['steps']
    #print (defined_convflow)



    functions.convert(defined_convflow, convpy)


    # puts out the result and clears temporary data
    functions.finish(convpy.tmpFile, convpy.tmpFile, True)
    

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
    