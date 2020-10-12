# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 20:01:42 2020

@author: pelie
"""

''' Configuration handler for Sapling '''
print('Loading configurations...')
import os #, json
from time import sleep

# Machine settings
#WINDOWS = True if 'nt' in os.name else False

# User settings
UserXhtml = False
UserTxt = False
FILE_MATCHES = 3
SENTENCE_MATCHES = 5

# Sapling settings
Delay = sleep(5)
Pause = sleep(3)


def setup_folders():
    #if not os.path.exists('cfg'):
     #   os.mkdir('cfg')

    jarDir = os.path.join('cfg', 'tika')
    if not os.path.exists(jarDir):
        os.makedirs(jarDir, exist_ok=True)

setup_folders()


'''
class SaplingConfig(object):
	"""
	docstring for SaplingConfig

	Stores user configurations, which can be loaded or preconfigured
	- Supports saving config in JSON

	"""
	def __init__(self):
		super(SaplingConfig, self).__init__()
		self.windows = True if 'nt' in os.name else False

		# Model type, query history, 
		
		if self.windows:
			self.user = os.environ['USERNAME']
			self.home = os.environ['HOMEPATH']
			self.processor = os.environ['PROCESSOR_IDENTIFIER']

		if os.path.exists('cfg'):
			self.load_cfg()
		else:
			os.mkdir('cfg')
			self.pre_config()

	def load_cfg(self):
		pass

	def pre_config(self):
		pass
		'''
