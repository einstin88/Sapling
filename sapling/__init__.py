# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 18:12:33 2020

@author: pelie
"""
import os

from . import config
from . import utils

if utils.check_java_vers():
    config.setup_folders('cfg', 'tika')
else:
    utils.terminate()

from . import DataProcessor
from . import QueryProcessor
from . import sapling



#config.config_save_data()
