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

import convpy.conv as convPY


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-12"


# start convPY-Instance and configure session
convpy = convPY.ConvPY('config/config.json')
convpy.configure()





################# MAIN #################
def main ():

    parser = argparse.ArgumentParser(prog='convpy_cmd')
    parser.add_argument('-c', '--config', nargs=1, default='config/config.json', help="opens convPY with custom config")
    parser.add_argument('-i', '--input', nargs=1, default='data/test_xml.xml', help='defines input directory or file')
    parser.add_argument('-f', '--flow', nargs=1, help='runs convPY on defined workflow')
    parser.add_argument('-o', '--out', nargs=1, default='out/', help='defines output-directory')
    parser.add_argument('iterate', nargs="?", help='iterate through directory')
    args = parser.parse_args()
    
    print (args)

    """
    # loads the json-data 
    requested_scenario = json.loads(data)
    
    f = 'data/test_xml.xml'
    url = requested_scenario['url']
    
    
    # creates all the files needed
    convpy.prepare(f)
     

    # takes the conversion workflow from data
    defined_convflow = requested_scenario['steps']
    #print (defined_convflow)


    convpy.convert(defined_convflow)


    # puts out the result and clears temporary data
    convpy.finish(True)
    """

if __name__ == '__main__':
    main()