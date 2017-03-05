#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
test.py
*******

A testing script
"""

import json 
import sys

import convpy as convPY


__date__ = "2017-02-23"


# start convPY-Instance and configure session
"""
convpy = convPY.ConvPY('config/config.json')
print convpy.home
print convpy.tmpFile
print convpy.config
"""

#print convpy.engines.path

data1 = """{
            "source" : "http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw",
            "steps" : [
                {"scenario" : "cs_nlp"},
                {
                    "name"  : "cs_post-processing",
                    "desc"  : "RegEx Postprocessing to clean up the data",
                    "type"  : "regex",
                    "script": "scripts/regex/cs_post.py",
                    "language"  : "python",
                    "output" : ".xml"
                },
                {
                    "name"  : "cs_post-processing",
                    "desc"  : "RegEx Postprocessing to clean up the data",
                    "type"  : "regex",
                    "script": "scripts/xslt/test.xquery",
                    "language"  : "python",
                    "output" : ".xml"
                }
            ]}"""
data = """{
            "source" : "http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw",
            "steps" : [
                {"scenario" : "cs_nlp"},
                {
                    "name"  : "cs_post-processing",
                    "desc"  : "RegEx Postprocessing to clean up the data",
                    "type"  : "regex",
                    "script": "scripts/regex/cs_post.py",
                    "language"  : "python",
                    "output" : ".xml"
                }
            ]}"""

#print (data)



# loads the json-data 
requested_scenario = json.loads(data)
scenario = requested_scenario['steps']
#convpy.read_scenario(requested_scenario['steps'])
#print convpy.scenario
fu = 'http://bnjhbasdhb.de/bka'
u = requested_scenario['source']
f = 'data/test_xml.xml'
l = [f, 'data/2_test_xml.xml']
d = 'data/'
convpy = convPY.Convpy('config/config.json')
#print convPY.Convpy.__dict__

#print convpy.main_config
#print convpy.scripts
#print convpy.engines
#print convpy.__dict__
#print convpy.scripts
convpy.convert(source=f,scenario=scenario)

