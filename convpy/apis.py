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
    parser = argparse.ArgumentParser(prog='convPY', description='conversion tool to convert xml data with different scenarios.')
    parser.add_argument('-c', '--config', default='config/config.json', help="opens %(prog)s with custom config")
    parser.add_argument('-s', '--source', required=True, help='set %(prog)s source (directory, file, http-resource or python-list)')
    #parser.add_argument('-o', '--output', help='set %(prog)s output-directory')
    parser.add_argument('-scen', '--scenario', required=True, help='set %(prog)s scenario')
    parser.add_argument('-fileout', action='store_false', default='True', help='sets save-mode to save result to files.')
    parser.add_argument('-stdin', action='store_true', default='False', help='sets input-mode to JSON stdin.')
    parser.add_argument('-v','--version', action='version', version='%(prog)s 0.2')
    #args = parser.parse_args(['-wf', 'scenarios/vmr2cs-nlp2.json', '-i', 'http://coptot.manuscriptroom.com/community/vmr/api/transcript/get/?docID=690003&pageID=0-400&joinParts=true&format=teiraw'])
    
    if not args_list:
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