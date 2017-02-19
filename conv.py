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

"""
print convpy.config
print convpy.home
print convpy.scenarios
print convpy.engines
print convpy.scripts
"""



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
                        "script": "convscripts/regex/cs_post.py",
                        "language"  : "python"
                    }
                ]}"""
    
    # loads the json-data 
    requested_scenario = json.loads(data)

      
    
    xml_data = functions.open_file('data/test_xml.xml')
    
    
    
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
    