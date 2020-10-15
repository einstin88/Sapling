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
WINDOWS = True if 'nt' in os.name else False

# User settings
UserXhtml = False
UserTxt = False
FILE_MATCHES = 3
SENTENCE_MATCHES = 5

# Sapling settings
Delay = sleep(5)
Pause = sleep(3)


def setup_folders():

    jarDir = os.path.join('cfg', 'tika')
    if not os.path.exists(jarDir):
        os.makedirs(jarDir, exist_ok=True)


def config_save_txt():

	print('To speed up your future queries if you are using the same directory, Sapling can save the parsed PDFs as texts on your computer.')
	print(' Would you like to do that? [Y/N]')

	while True:
		sel = input("Please enter 'Y' or 'N': ")

		try:
			sel = sel.lower()
			break
		except :
			print(f'{sel} is not a recognized option')
			continue

	global UserTxt, txtDir
	if sel == 'y':
		UserTxt = True
		txtDir = 'SavedTexts'

		if not os.path.exists(txtDir):
			os.mkdir(txtDir)

	elif sel == 'n':
		UserTxt = False


'''

### Goal: save parsed pdfs into texts for future retrieval
Req: mapping (directory & file list) --> folder name created for storage
- mappings saved with JSON as history records, can be easily used to retrieve data in future

Req: option to save data during boot up


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
