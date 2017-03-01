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
import conv as convpy


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
        self.config = self.read_config(config)

    def read_config(self, file_path):
        """
        Config-Class non-public methode reading in a JSON config-file by its path

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


def configure(config_file):
    """
    configures ConvPY with homepath and reads engines and scipts configs

    ARGS:
    * config_file: path to config.json

    RETURN:
    {CONVPY OBJECT} that is configured with main-config, engines and scenario-scripts
    """
    config_path = iofd.pathify(True, config_file)
    main_config = Config(config_path)

    scripts_config = iofd.pathify(True, main_config.config['scripts']['path'], main_config.config['scripts']['config'])
    engines_config = iofd.pathify(True, main_config.config['engines']['path'], main_config.config['engines']['config'])

    scripts = Config(scripts_config)
    engines = Config(engines_config)
    return convpy.Convpy(main_config, engines, scripts)
