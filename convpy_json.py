#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
convpy_json.py
*******

handles convpy with JSON std.in
"""

import json 
import sys

import convpy as convPY


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-12"


def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

################# MAIN #################
def main ():

    json_data = read_in()
    
    # loads the json-data
    url = json_data['url']
    scenario = json_data['steps']

    #print scenario
    
    # start convPY-Instance and configure session
    convpy = convPY.ConvPY('config/config.json')
    convpy.configure()
    # prepare !    
    convpy.prepare(url)
    # convert !
    convpy.convert(scenario)
    # ... and finish !
    convpy.finish(True)
    

if __name__ == '__main__':
    main()