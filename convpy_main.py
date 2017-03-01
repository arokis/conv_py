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
def main():
    """
    main function running ConvPY out of the box
    """

    #########################
    # ConvPYs API Interface #
    #########################

    cmd_args = convPY.cmd_api()
    #cmd_args = convPY.cmd_api(['-stdin'])
    #cmd_args = convPY.cmd_api(['-wf', 'scenarios/vmr2cs-nlp.json'])

    config = cmd_args.config
    fileout = cmd_args.fileout
    source = ''
    scenario = ''


    if cmd_args.stdin is True:
        json_data = convPY.stdin_api()
        source = json_data['source']
        scenario = json_data['steps']
    else:
        # open scenario from file
        try:
            source = cmd_args.source
            #flow = convPY.open_file(cmd_args.scenario)
            scenario = convPY.read_json_file(cmd_args.scenario)
        except TypeError:
            print('[convPY:ERROR] Could not identify workflow! Exit!')
            sys.exit(1)
        
        

    #print scenario
    #print source

    #########################
    # ConvPYs Main-Workflow #
    #########################

    # start convPY-Instance and configure session
    convpy = convPY.configure(config)

    # convert !
    convpy.convert(source=source, scenario=scenario['steps'], write_output=fileout)
    # ... and finish !


if __name__ == '__main__':
    main()
