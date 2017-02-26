#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
convpy/functions.py
*************
Defines the base-functions like open or reading files etc.
"""

import json 
import os
import sys
import urllib2
from shutil import rmtree


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-12"


def clean_tmp (file_path):
    """
    cleans all temporary files and folders being created during convPY working 
    
    ARGS:
    * path: path of tmp-file to be deleted inkl. it's parent directory 
    """
    try:
        rmtree(os.path.dirname(file_path))
    except:
        print ('[convPY:WARNING] Could not clean up tmp-file "' + file_path +'". Maybe you should clean it manually!')
        sys.exit(0)


def create_file (path, content, option='w+'):
    """
    creates files with params 
    
    ARGS:
    * path: path of file being created
    * content: content being writen in file
    * options (optional): writing mode (no string-controll!), default: 'w+' 
    """
    try:
        fo = open( path, option ) 
        fo.write( content ) 
        fo.close()
    except:
        print ('[convPY:ERROR] Failed while creating File "' + path +'". Exit!')
        sys.exit(1)


def open_file (path):
    """
    opens files and reads it in with params 

    ARGS:
    * path: path of file being opened 

    RETURN:
    * content of a file or sys.exit(1)
    """
    try:
        with open(path, 'r') as out:
            output = out.read()
        return output
    except IOError:
        print ('[convPY:ERROR] No such File "' + path + '"! Exit!')
        sys.exit(1)


def read_JSON_file (file_path):
    content = open_file(file_path)
    return json.loads(content)


def retrieve (path):
    """
    input handler which loads the input data and decides if File or URL and returns the data
    
    ARGS:
    * path: file-path or url which should be read in
    """
    try:
        if path.startswith('http'):
            return request(path)
        elif os.path.exists(path) and os.path.isfile(path):
            return open_file(path)
    except:
        print ('[convPY:ERROR] Failed in reading input-data "' + path +'". Exit!')    
        sys.exit(1)


def request (url):
    """
    requests data from url 
    
    ARGS:
    * url: url whose data is going do be responded (well ... when server resonds)
    """
    try:
        response = urllib2.urlopen(url)
        data = response.read()
        return data
    except:
        print ('[convPY:ERROR] Failed retrieving data from url "' + url +'" Exit!')
        sys.exit(1)