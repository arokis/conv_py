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

import iofd_handling as iofd
import conv as convpy


__author__ = "Uwe Sikora"
__email__ = "arokis.u@googlemail.com"
__date__ = "2017-02-12"


def configure(config_file):
    """
    configures ConvPY with homepath and reads engines and scipts configs

    ARGS:
    * config_file: path to config.json

    RETURN:
    {CONVPY OBJECT} that is configured with main-config, engines and scenario-scripts
    """
    config_path = iofd.pathify(True, config_file)
    main_config = convpy.Config(config_path)

    scripts_config = iofd.pathify(True, main_config.config['scripts']['path'], main_config.config['scripts']['config'])
    engines_config = iofd.pathify(True, main_config.config['engines']['path'], main_config.config['engines']['config'])

    scripts = convpy.Config(scripts_config)
    engines = convpy.Config(engines_config)
    return convpy.Confpy(main_config, engines, scripts)