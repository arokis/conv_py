#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
test.py
*******

A testing script
"""

import json 
import sys

import convpy.conv as convPY


__date__ = "2017-02-23"


# start convPY-Instance and configure session
convpy = convPY.ConvPY('config/config.json')
print convpy.home
print convpy.tmpFile
print convpy.config
