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
    source = cmd_args.input
    scenario = ''

    if cmd_args.stdin is True:
        json_data = convPY.stdin_api()
        source = json_data['source']
        scenario = json_data['steps']
    else:
        # open scenario from file
        try:
            flow = convPY.open_file(cmd_args.flow)
        except TypeError:
            print('[convPY:ERROR] Could not identify workflow! Exit!')
            sys.exit(1)
        # loads the json-data
        scenario = json.loads(flow)['steps']

    #print scenario


    #########################
    # ConvPYs Main-Workflow #
    #########################

    # start convPY-Instance and configure session
    convpy = convPY.configure(config)

    # prepare !
    convpy.read_scenario(scenario)
    # convert !
    convpy.convert(source, False)
    # ... and finish !


if __name__ == '__main__':
    main()