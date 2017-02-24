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

    #cmd_args = convPY.cmd_api(['-stdin'])
    #cmd_args = convPY.cmd_api(['-wf', 'scenarios/vmr2cs-nlp.json'])
    cmd_args = convPY.cmd_api()
    
    config = cmd_args.config
    source = cmd_args.input
    scenario = ''
    
    if cmd_args.stdin == True:
        json_data = convPY.stdin_api()
        source = json_data['source']
        scenario = json_data['steps']
    else:
        """
        print('NOPE')
        print cmd_args
        sys.exit(1)
        """
        # loads the json-data
        # open scenario from file
        try:
            with open(cmd_args.flow, 'r') as file:
                flow = file.read()
        except TypeError:
            print ('[convPY:ERROR] Could not identify workflow! Exit!')
            sys.exit(1)
        except IOError:
            print ('[convPY:ERROR] No such File "' + cmd_args.flow + '"! Exit!')
            sys.exit(1)
        
        # loads the json-data
        scenario = json.loads(flow)['steps']
    
    

    #print scenario
    
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