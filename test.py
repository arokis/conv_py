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
convpy = convPY.configure('config/config.json')

#print convpy.engines.path


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
convpy.read_scenario(requested_scenario['steps'])
#print convpy.scenario

u = requested_scenario['source']
f = 'data/test_xml.xml'
l = [f, 'data/2_test_xml.xml']
d = 'data/'
convpy.convert(f, write_output=True)

