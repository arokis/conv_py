#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
convpy/apis.py
*************
Defines different APIs to communicate with convPY
"""

import json 
import sys
import argparse


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-24"
__all__ = ['stdin_api', 'cmd_api']


def cmd_api(args_list=False):
    """
    defines convPY's command-line API

    RETURN:
    {ARGPARSE-OBJECT: Namespace}
    """
    parser = argparse.ArgumentParser(prog='convpy_cmd')
    parser.add_argument('-c', '--config', default='config/config.json', help="opens convPY with custom config")
    parser.add_argument('-i', '--input', default='data/test_xml.xml', help='defines input directory or file')
    parser.add_argument('-wf', '--flow', default='scenarios/testing.json', help='runs convPY on defined workflow')
    parser.add_argument('-o', '--out', default='out/', help='defines output-directory')
    parser.add_argument('-stdin', action='store_true', default='False', help='sets input-mode to JSON stdin.')
    #args = parser.parse_args(['-wf', 'scenarios/vmr2cs-nlp2.json', '-i', 'http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw'])
    
    if args_list == False:
        return parser.parse_args()
    else: 
        return parser.parse_args(args_list)


def stdin_api():
    """
    reads in JSON stdin

    RETURN:
    {DICT} from JSON stdin
    """
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])