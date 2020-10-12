# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 16:52:02 2020

@author: pelie
"""
import os
from tqdm import tqdm
from tika import tika, parser
from sapling import utils, pdfProcessor
from sapling import sapling, DataProcessor

directory_data = sapling.get_directory()
sapling.process_directory(directory_data)
pdf_data = DataProcessor.PdfContainer()
pdf_data.load_pdf(directory_data.pdfs)

### Test XML parsing
# Generate test samples
directory_path = 'C:\\Users\\pelie\\OneDrive\\,Readings\\2021_BAP\\assigned'
file_list = os.listdir(directory_path)
file_list.pop(20)
file_list.pop(7)
file_list.pop(1)

all_files = {}
for fp in tqdm(file_list):
    path = os.path.join(directory_path, fp)
    all_files[fp] = parser.from_file(path,xmlContent=True)

    with open('.\\xml\\'+fp[:5]+'.xhtml', 'w', errors='xmlcharrefreplace') as f:
        f.write(all_files[fp]['content'])

# load individual file
idx = 0
file = file_list[idx]
txt_0 = files[os.listdir('xml')[idx]]
meta_0 = all_files[file]['metadata']

tp = ['metadata', 'pdf:charsPerPage', 'pdf:unmappedUnicodeCharsPerPage',
          'content', 'xmpTPg:NPages']
sum(int(i) for i in meta_0[tp[1]])

# test lxml functions
for i in file_list:
    p = parser.from_file(os.path.join(directory_path,i), xmlContent=True)
    tree = etree.parse(StringIO(p['content']), parser= etree.HTMLParser())
    title, cleaned = pdfProcessor.clean_xml(tree, int(p['metadata']['xmpTPg:NPages']))
    with open('txt\\' + i + '.txt', 'w', errors='xmlcharrefreplace') as f:
        f.write(f'{title}\n\n')
        for k in cleaned:
            f.write(f'{k}. {cleaned[k]}\n\n')

######
from lxml import etree
from io import StringIO

par= etree.XMLParser()
res = etree.parse(StringIO(txt_0), parser= par)
x,y = pdfProcessor.process_tree(res)

title, text, headers, footers = pdfProcessor.clean_xml(res, int(meta_0['xmpTPg:NPages']))
title, cleaned = pdfProcessor.clean_xml(res, int(meta_0['xmpTPg:NPages']))

texts = {2: text[2], 3: text[3]}
paragra = pdfProcessor.construct_paragraph(texts, title)

#####
dir(res)
test = []
test_tag = []
for i in res.iter():
    test.append(i)
    test_tag.append(i.tag)
c=Counter(test_tag)
c = dict(c)


# fix xhtml escaped chars
import html
import re
from collections import Counter
r = re.compile(r'&.{,10}?;')
esc_ch = []

for fil in tqdm(file_list):
    esc_ch.extend(re.findall(r, all_files[fil]['content']))

for fil in os.listdir('xml'):
    with open('xml\\'+fil) as f:
        esc_ch.extend(re.findall(r,f.read()))
c = Counter(esc_ch)
c = list(c)

c_0 = {}
for i in c:
    c_0[i] = html.unescape(i)

test = {}
for x in esc_ch:
    test[x]= html.unescape(x)

for fil in os.listdir('xml'):
    with open('xml\\'+fil) as f:
        if '&#61479' in f.read():
            print(fil)


html.unescape('&#8727;')
html.unescape('<body></body>')

xh = re.compile(r'&.{,10}?;')
s = '&#776;'
a = re.search(xh, 'asdas&#asd;')
a = re.findall(xh, txt_1)
a.group()

# Test load_pdf()
pdfs_path = [os.path.join(directory_path, f) for f in file_list]
pdfs = pdfProcessor.load_pdf(pdfs_path)


### fix tika's kill_server
# TODO test it on MacOS
file_path = os.path.join(directory_path, file_list[2])
test = parser.from_file(file_path)
tika.killServer()

# test new kill process logic
utils.check_mem() == True
utils.kill_java()

######
import pandas as pd
data = pd.DataFrame(columns=['title', 'paragraphs', 'tokens', 'num_pages', 'file_path'])
data = data.append({
    'title': 'a',
    'paragraphs': ['b'],
    'tokens': ['c'],
    'num_pages': '6',
    'file_path': 'c'
    }, ignore_index=True)

data[data.title == 'a'].index[0]

####
# Test tika
from tika import tika
import os
#from urllib.parse import urlparse

jarPath = os.path.join('cfg', 'tika-server.jar')
os.path.exists(jarPath)
#urlp = urlparse(jarPath)
#urlp.scheme

tika.TikaServerJar = jarPath
tika.TikaJarPath = 'cfg'

status = tika.startServer(jarPath)
if status:
    tika.killServer()

tika.TikaServerProcess
