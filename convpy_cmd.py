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

    args = convPY.cmd_api(['-wf', 'scenarios/vmr2cs-nlp.json'])

    config = args.config
    source = args.input
    
    # open scenario from file
    try:
        with open(args.flow, 'r') as file:
            flow = file.read()
    except TypeError:
        print ('[convPY:ERROR] Could not identify workflow! Exit!')
        sys.exit(1)
    except IOError:
        print ('[convPY:ERROR] No such File "' + args.flow + '"! Exit!')
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