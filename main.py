#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
main.py
*******

One possiblem main.py. There may be more to serve specific puposes like CMD-focused or std.in-focused or whatever

TO-DO:
* make the data input straight -> make it a function!
"""

import json 
import sys

import convpy as convPY


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-12"


# start convPY-Instance and configure session
convpy = convPY.ConvPY('config/config.json')
convpy.configure()


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
                "source" : "http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw",
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
    
    #print (data)

    # loads the json-data 
    requested_scenario = json.loads(data)
    
    f = 'data/test_xml.xml'
    source = requested_scenario['source']
    
    
    # creates all the files needed
    convpy.prepare(f)
     

    # takes the conversion workflow from data
    defined_convflow = requested_scenario['steps']
    #print (defined_convflow)


    convpy.convert(defined_convflow)


    # puts out the result and clears temporary data
    convpy.finish(True)
    

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
    