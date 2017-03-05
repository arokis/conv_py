#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
convpy/iofd_handling.py
*************
Defines the functions for IO- , File- and Directoryhandling
"""

import json
import os
import sys
import urllib2


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-12"


def create_dir(path):
    """
    creates directories

    ARGS:
    * path: path of directory being created
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except IOError:
        print('[convPY:ERROR] Failed while creating Directory "' + path +'". Exit!')
        sys.exit(1)


def create_file(path, content, option='w+'):
    """
    creates files with params

    ARGS:
    * path: path of file being created
    * content: content being writen in file
    * options (optional): writing mode (no string-controll!), default: 'w+'
    """
    try:
        fo = open(path, option)
        fo.write(content)
        fo.close()
    except IOError:
        print ('[convPY:ERROR] Failed while creating File "' + path +'". Exit!')
        sys.exit(1)


def file_name_info(file_path):
    path = os.path.abspath(os.path.dirname(file_path)) 
    file_base = os.path.basename(file_path) 
    file_name = os.path.splitext(file_base)[0]
    file_extension = os.path.splitext(file_base)[1]
    
    return{
        'path' : path,
        'base' : file_base,
        'extension' : file_extension,
        'name' : file_name  
    }


def open_file(path):
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


def read_json_file(file_path):
    """
    reads JSON from a file

    ARGS:
    * file_path: JSON file which should be read in

    RETURNS:
    * {DICT}: JSON as Python Dictionary
    """
    content = open_file(file_path)
    return json.loads(content)


def retrieve(path):
    """
    input handler which loads the input data and decides if File or URL and returns the data

    ARGS:
    * path: file-path or url which should be read in
    """
    try:
        if os.path.exists(path) and os.path.isfile(path):
            return open_file(path)
        else:
            return request(path)
    except IOError:
        print ('[convPY:ERROR] Failed in reading input-data "' + path +'". Exit!')
        sys.exit(1)


def request(url):
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


def walk_dir(path):
    """
    walks given directory and filters files

    ARGS:
    * path: path of directory being walked

    TO-DO:
    * ignores should be configurable in config.json
    """
    ignore_starts_with = ('_', '.')
    ignore_ends_with = ('~', '.swp')
    
    dir_files = [os.path.join(root,f) 
    for root,dirs,files in os.walk(path) 
    for f in files 
    if not f.endswith(ignore_ends_with) and not f.startswith(ignore_starts_with)]
    
    return dir_files