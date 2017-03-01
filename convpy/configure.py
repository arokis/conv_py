#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
convpy/configure.py
*************
Defines configuration-functions and the Class "Config".
"""


import os
import sys

import iofd_handling as iofd


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-25"
__all__ = ['Config', 'configure']


class Config(object):
    """
    Config-Class:
    Representing a config file and content

    ARGS:
    * config: Path to JSON config-file
    """

    def __init__(self, config):
        self.path = os.path.dirname(config)
        self.config = Config.read_config(config)

    @staticmethod
    def read_config(file_path):
        """
        Config-Class static methode reading in a JSON config-file by its path

        ARGS:
        * file_path   : file path to JSON config

        RETURN:
            OK      > {DICT}: ...
            ERROR   > Exception & exits with error-code 1
        """
        try:
            return iofd.read_json_file(file_path)
        except:
            print('[convPY:Error] Could not read config-file "' + file_path +'". Exit!')
            sys.exit(1)