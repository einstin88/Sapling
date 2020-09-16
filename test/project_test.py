# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 15:55:03 2020

@author: pelie
"""
from project_know import *

# how to filter out title and reference page
# C:\Users\pelie\OneDrive\,Readings\2021_BAP\assigned
flag_d, file_list = get_directory()

sublist = file_list['.pdf']
pdfs = load_pdf(sublist)

for file in pdfs:
    print(len(pdfs[file]))

files = load_data(file_list)
###################
import os
from tika import parser
from tika import unpack

directory_path = 'C:\\Users\\pelie\\OneDrive\\,Readings\\2021_BAP\\assigned'
file_list = os.listdir(directory_path)

file_path = os.path.join(directory_path, file_list[4])
test = parser.from_file(file_path, xmlContent=True)
test1 = unpack.from_file(file_path)
txt = test["content"][-16321:]
txt = test1["content"]

len(txt)
txt.replace('\n', '')

test = dict()
test1 = dict()
for i in file_list:
    file_path = os.path.join(directory_path, i)
    test[os.path.basename(i)] = parser.from_file(file_path)
    test1[os.path.basename(i)] = unpack.from_file(file_path)


