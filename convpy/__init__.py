#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
convpy/__init__.py
******************

initialises the main convPY-classes, APIs and functions
"""

from __future__ import absolute_import
from .apis import stdin_api, cmd_api
from .iofd_handling import read_json_file, request
from .conv import Convpy
from .converter import Converter, Saxon, Call