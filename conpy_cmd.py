#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
convpy_cmd.py
*******

handles convpy with command-line arguments
"""

import json 
import sys
import argparse

import convpy as convPY


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-12"


################# MAIN #################
def main ():

    parser = argparse.ArgumentParser(prog='convpy_cmd')
    parser.add_argument('-c', '--config', default='config/config.json', help="opens convPY with custom config")
    parser.add_argument('-i', '--input', default='data/test_xml.xml', help='defines input directory or file')
    parser.add_argument('-wf', '--flow', help='runs convPY on defined workflow')
    parser.add_argument('-o', '--out', default='out/', help='defines output-directory')
    #parser.add_argument('-iter', action='store_true', default='False', help='iterate through directory')
    #args = parser.parse_args(['-wf', 'scenarios/vmr2cs-nlp2.json', '-i', 'http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw'])
    args = parser.parse_args()

    config = args.config
    source = args.input
    
    # open scenario from file
    try:
        with open(args.flow, 'r') as file:
            flow = file.read()
    except TypeError:
        print ('[convPY:ERROR] Could not identify workflow! Exit!')
        sys.exit(1)
    
    # loads the json-data
    scenario = json.loads(flow)

    # start convPY-Instance and configure session
    convpy = convPY.ConvPY(config)
    convpy.configure()
    # prepare !    
    convpy.prepare(source)
    # convert !
    convpy.convert(scenario['steps'])
    # ... and finish !
    convpy.finish(True)
    

if __name__ == '__main__':
    main()