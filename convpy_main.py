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


################# MAIN #################
def main ():
    
    #########################
    # ConvPYs API Interface #
    #########################

    cmd_args = convPY.cmd_api()
    #cmd_args = convPY.cmd_api(['-stdin'])
    #cmd_args = convPY.cmd_api(['-wf', 'scenarios/vmr2cs-nlp.json'])
    
    config = cmd_args.config
    source = cmd_args.input
    scenario = ''
    
    if cmd_args.stdin == True:
        json_data = convPY.stdin_api()
        source = json_data['source']
        scenario = json_data['steps']
    else:
        
        # open scenario from file
        try:
            flow = convPY.open_file(cmd_args.flow)    
        except TypeError:
            print ('[convPY:ERROR] Could not identify workflow! Exit!')
            sys.exit(1)
        
        # loads the json-data
        scenario = json.loads(flow)['steps']
    
    #print scenario
    

    #########################
    # ConvPYs Main-Workflow #
    #########################

    # start convPY-Instance and configure session
    convpy = convPY.ConvPY(config)
    convpy.configure()
    
    # prepare !    
    convpy.prepare(source)
    # convert !
    convpy.convert(scenario)
    # ... and finish !
    convpy.finish(True)
    

if __name__ == '__main__':
    main()