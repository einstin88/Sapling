# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 03:41:47 2020

@author: pelie

Handles:

- storing a directory in python container
- processing and stroing PDFs into format usable by algorithm
"""

print('Loading data processing module...')
import os, re
#import prettytable
from io import StringIO
from lxml.etree import HTMLParser, parse
from string import punctuation
from tika import tika, parser
from tqdm import tqdm

from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import WordNetLemmatizer

# TODO - replace with spacy pipline
from . import utils, config
from .utils import CLR_SYS, CLR_FILE, CLR_UI, CLR_WARN, CLR_SOFT_WARN, C_RESET

Default_logic = utils.Default_logic
Valid_Extensions = ['.pdf', '.txt'] # '.docx' not implemented in this version


class DirContainer(object):
    """docstring for DirContainer"""
    def __init__(self):
        super(DirContainer, self).__init__()
        self.valid_directory = False
        self.pdfs = []
        self.docs = []
        self.txts = []
        self.get_directory()
 
    def __len__(self):
        return len(self.file_list)

    def get_directory(self):
        ''' 
        Get directory to load data from, and check if it contains valid files
        Return a flag and dict of valid files
        Limitations: will not go deeper than the given directory
        '''
        options_0 = {
            '1': '[1] Try with another directory instead,',
            '2': '[2] or quit program?',
            'logic': Default_logic
            }

        options_1 = {
            '1': '[1] Would you like to choose another directory instead,',
            '2': '[2] or proceed?',
            'logic': Default_logic
            }

        while True:
            
            directory = input(f'{CLR_UI}Where should Sapling look for the files?{C_RESET}\n[Please provide full path of your folder]\n')
            # Correct input format when path was given by user using drag and drop
            if directory[0] == '\'':
                directory = directory[1:-1]
            if not config.WINDOWS:
                directory = directory.replace('\,',',').replace('\ ', ' ').strip()
        
            # Check if valid path is given
            if os.path.exists(directory):
                if os.path.isdir(directory):
                    self.directory = directory
                    self.isFile = False
                    self.file_list = os.listdir(directory)

                elif os.path.isfile(directory):
                    self.directory = os.path.dirname(directory)
                    self.isFile = True
                    self.file_list = [os.path.basename(directory)]

            else:
                print(f'\n{CLR_WARN}Oops!! Error: \'{directory}\' not found!{C_RESET}')
                
                choice = utils.process_options(options_0)
                if choice:
                    continue
                else:
                    utils.terminate()
        
            # At least 2 files are required for TF-IDF algorithm to work properly
            if len(self) == 1:
                print(f'\n{CLR_SOFT_WARN}Seems like you\'ve only provided one file. Sapling works better with more given files, so I cannot guarantee accurate results here.{C_RESET}')
                
                choice = utils.process_options(options_1)    
                if choice:
                    continue
                else:
                    break
            else:
                break

    def process_directory(self):
        '''
        Check if path contains compatible file
        '''
        counter = 1

        print(f'\n{CLR_SYS}Checking {len(self)} file' +
              ('s in ' if len(self) > 1 else ' ') +
              f'\'{os.path.basename(self.directory)}\'.....{C_RESET}')

        for file in self.file_list:
            # Get extension of each file in the directory
            ext = os.path.splitext(file)[1]
            if ext in Valid_Extensions:
                print(f'{CLR_FILE}{counter}. {file}{C_RESET}')
                counter += 1

                if ext == '.pdf':
                    self.pdfs.append(file)
                elif ext == '.txt':
                    self.txts.append(file)
                else:
                    self.docs.append(file)
                
            else:
                print('- ', file)

        # Update file_list to include only valid files
        self.file_list = self.pdfs + self.docs + self.txts

        if len(self) > 0:
            self.valid_directory = True



class PdfContainer(object):
    """
    Handles PDF processes 
    1. Loading PDF for parsing
        - setup tika environment
            > check if tika-server jar already exist
            > if not, download tika Jar + md5 files
            > setup tika internal parameters
           so it can be used locally after the first start
        - parse with tika to xhtml

    2. preprocess xhtml with lxml
        - remove certain features from the text, eg. headers, footers
        ? convert in text citations to concat with sentence
        - construct paragraphs + tokenize them
        ? https://huggingface.co/transformers/preprocessing.html

    3. store passages & tokens 
        ? option to save cleaned txt in file in folder 'foldername_txt'

    4. compute idfs

    """

    def __init__(self, dirobj):
        super(PdfContainer, self).__init__()
        # Vars to store parsed texts & tokens
        self.passages = dict()
        self.tokens = dict()

        self.mapping = dict()
        self.err_files = [] 
        self.metadata = []

        # Load pdfs into memory
        self.load_pdf(dirobj)

    def __len__(self):
        return len(self.mapping)

    def get_idfs(self):
        self.idfs = compute_idfs(self.tokens)

    def set_tika_env(self):

        jarPath = os.path.join('cfg', 'tika', 'tika-server.jar')
        jarDir = os.path.join('cfg', 'tika')

        if not os.path.exists(jarPath) or not tika.checkJarSig(tika.TikaServerJar, jarPath):
            print('Need to download the parser, please ensure you are connected to the Internet')
            try:
                os.remove(jarPath)
            except:
                pass

            tika.getRemoteJar(tika.TikaServerJar, jarPath)

            if tika.checkJarSig(tika.TikaServerJar, jarPath):
                print('Sapling has downloaded PDF parser...\n')
            else:
                print('Error occured when downloading PDF parser...\n')

        # Set 'main' tika env vars to local path
        # Note: tika's log_path already modified to local path at source
        tika.TikaServerJar = jarPath
        tika.TikaJarPath = jarDir

        if not tika.TikaServerProcess:                
            try:
                #tika.startServer(jarPath)
                tika.checkTikaServer()
                utils.check_java_running()
                if utils.Java_pid:
                    print('PDF parser loaded...')
            
            except:
                if config.WINDOWS:
                    utils.open_file(jarPath)
                else:
                    print(f"{CLR_SOFT_WARN}Can't run Java automatically because your MacOS is 10.14 or older. To continue, please double-click on 'tika-server.jar'{C_RESET}")
                    utils.open_file(jarDir)
                    _ = input('Enter any key...')
            

    def load_pdf(self, dirobj):
        '''
        Handles the opening and preprocessing of pdf files
        Limitation: OCR not implemented in this version

        Parameters
        ----------
        file_sublist : list
            Full paths to pdfs found from the user-given directory.

        Returns
        -------
        files : dict()
            Keys --> file names
            Values --> cleaned string
        '''
        counter = 0
        #Tika parameters
        tp = ['metadata', 'pdf:charsPerPage', 'pdf:unmappedUnicodeCharsPerPage',
              'content', 'xmpTPg:NPages']
        file_list = dirobj.pdfs
        directory = dirobj.directory

        # Check set ups of the environment
        utils.check_java_running()
        if not utils.Java_pid:
            print('Sapling is setting up PDF parser...\n')
            self.set_tika_env()

        if config.UserXhtml:
            if not os.path.exists('xml'):
                os.mkdir('xml')

        #if config.UserTxt:
         #   if not os.path.exists('txt'):
          #      os.mkdir('txt')

        print('Loading those pdfs....\n')

        for file_name in tqdm(file_list):

            file_path = os.path.join(directory, file_name)

            parsed_file = parser.from_file(file_path, xmlContent=True)

            # Save the parsed pdf to xhtml 
            if config.UserXhtml:
                xhtml_filepath = os.path.join('xml', file_name[:-3] +'.xhtml')
                with open(xhtml_filepath, 'w', errors='xmlcharrefreplace') as f:
                    f.write(parsed_file[tp[3]])

            ### Check if texts in file are parsable - implemented through umc and nc
            # Determine number of pages with large amt of unmapped chars = file's texts mapping is corrupted
            umc = sum(True for i in parsed_file[tp[0]][tp[2]] if int(i) > 250)

            # Determine number of pages with 0 char = pages are images
            nc = sum(True for i in parsed_file[tp[0]][tp[1]] if int(i) == 0)

            n_pages = int(parsed_file[tp[0]][tp[4]])

            # TODO - implement OCR function for these files
            if umc > 2 or nc > 0.5 * n_pages:
                self.err_files.append(file_name)
                continue

            # Use lxml module to process the xhtml data
            html_parser = HTMLParser()
            tree = parse(StringIO(parsed_file[tp[3]]), parser= html_parser)

            # Process the tree of the given pdf
            title, raw, words, headers, footers = clean_xml(tree, n_pages)
            
            # Convert paragraphs into format that Sapling can process
            # and save a copy of that as txt file locally
            if config.UserTxt:
                txt_filepath = os.path.join(config.txtDir, file_name[:-3] +'.txt')
                with open(txt_filepath, 'w', errors='xmlcharrefreplace') as f:
                    #f.write(f'{title}\n\n')
                    for pr in raw:
                        f.write(f'{raw[pr]}\n')

            self.passages[file_name] = raw
            self.tokens[file_name] = words
            self.mapping[file_name] = counter
            self.metadata.append({ 
                'title': '-' if title == None else title,
                'num_pages': n_pages,
                #'path': file_path,
                'headers' : headers,
                'footers' : footers
                })
            counter += 1

        # TODO - set window size and truncate file name that are too long
        # Display result from loading pdfs
        #print(table)

        if len(self.err_files) > 0:
            print()
            print(f'{CLR_SOFT_WARN}Sorry, text' + ('s ' if len(self.err_files) > 1 else ' ') +
                   'in the following file' +
                   ('s are ' if len(self.err_files) > 1 else ' is ') +
                   f'not parsable:{C_RESET}')

            for i, file in enumerate(self.err_files):
                print(f'{i+1}. {file}')
            print()

        # Free up system memory if it is low
        utils.check_java_running()
        if utils.check_mem():
            #tika.killServer()
            utils.kill_java()

def clean_xml(tree, n_pages):

        title = None
        sus_headers, sus_footers = [], []
        # TODO - detect page numbers and try to keep track
        sus_page_nums = []
        headers, footers = set(), set()
        search_margin = min(8, n_pages)

        page = 1
        page_texts = dict()

        for node in tree.iter():

            if node.tag == 'title':
                title = node.text

            elif node.tag == 'div' and ('class', 'page') in node.items():
                page_texts[page], sus_header, sus_footer = extract_page(node, headers, footers)

                if page <= search_margin:
                    sus_headers.append(sus_header)
                    sus_footers.append(sus_footer)

                    headers, has_header = find_header(sus_headers, headers)
                    footers, has_footer = find_header(sus_footers, footers)

                    if has_header:
                        page_texts = remove_header(page_texts, headers)
                    elif has_footer:
                        page_texts = remove_header(page_texts, footers)
                page += 1

        cleaned, tokens = construct_paragraph(page_texts, title)

        return title, cleaned, tokens, headers, footers


def extract_page(node, headers, footers):

        nodes = list(node)
        page_txt = []

        page_nums_0 = re.compile(r'\d{1,4}')
        email_0 = re.compile(r'\w+[@]{1}\w+[.]{1}.{2,4} ')
        journals_0 = re.compile(r'Journal.{,60}?\d{2,4}')
        journals_1 = re.compile(r'American Political Science Review.{,30}?\d{2,4}')

        # Get all texts from <p> containers of the page
        for element in nodes:
            if element.tag == 'p':
                txt = element.text
            else:
                continue

            # TODO Check against rules/constraints
            if txt != None:
                margins = ((re.match(page_nums_0, txt) is not None and len(txt) < 10) or
                            (re.search(email_0, txt) is not None) or
                           (re.search(journals_0, txt) is not None) or
                           (re.search(journals_1, txt) is not None))
                if margins:
                    continue

                constraints = ((txt in headers) or (txt in footers) or
                               'http://' in txt)
                if constraints:
                    continue

                page_txt.append(txt)

        header_loc = (len(page_txt) // 4) + 1
        footer_loc = len(page_txt) - header_loc

        return page_txt, set(page_txt[:header_loc]), set(page_txt[footer_loc:])


def construct_paragraph(pages, title):

    tbc = ''
    paragraphs = []
    words = []

    citation_0 = r' ?\([A-Z].{2,}? \d{4}?\)'
    citation_1 = r' ?\([A-Z].{2,}? \d{4}?, \d+\)'

    reference = r'REFERENCES|References|Bibliography|BIBLIOGRAPHY'

    for page in pages:
        for i in range(len(pages[page])):
            # Standardize newlines to tidy up parsed text
            tmp = pages[page][i].replace(' \n', '\n').replace('-\n', '').replace('\n', ' ')
                
            if tmp.rstrip().endswith('.'):
                tmp = tmp.rstrip()

            # If title appears in the processed text, discard it
            if title != None and (title in tmp):
                continue

            # TODO - change to corect length
            if len(tmp) == 0:
                continue

            # Check if it is end of a paragraph
            try:
                next_line = pages[page][i + 1][0]
            except:
                try:
                    next_line = pages[page +1][0][0]
                except:
                    next_line = 'A'

            next_line_ch = next_line.isupper() or next_line.isnumeric()

            if ('.' in tmp[-1] and next_line_ch) or tmp.isupper():
                #TODO - check how to reformat citations
                tbc = re.sub(citation_0, '', f'{tbc} {tmp}')
                tbc = re.sub(citation_1, '', tbc)
                    
                tokens = tokenize(tbc)

                #if 6 < len(tokens) <= 512:
                if len(tokens) > 6:
                    paragraphs.append(tbc)
                #else: 
                 #   paragraphs.extend(process_paragraphs(tbc))
                    words.extend(tokens)
                    tbc = ''
                else:
                    continue

            # otherwise concat string
            else:
                if tmp.endswith(' '):
                    tbc += tmp
                else:
                    tbc += f' {tmp}'

            if re.match(reference, tmp) is not None:
                return paragraphs, words

    return paragraphs, words

'''
def process_paragraphs(passage):
 
    words = passage.split()
    split_passage = []
    prev_split_idx = 0
    
    for i in range(1, len(words)//512 + 1):
        search_idx = i * 512 - 1
        
        while True:    
            if words[search_idx][-1] == '.':
                split_idx = passage.rfind(words[search_idx], prev_split_idx, search_idx) + 1
                split_passage.append(passage[prev_split_idx : split_idx])
                prev_split_idx = split_idx
                break

            else:
                search_idx -= 1

    if split_idx < len(words):
        split_passage.append(passage[split_idx : ])

    return split_passage
'''

def find_header(susses, headers):

        list_length = len(susses)
        has_header = False

        if list_length == 1:
            return headers, has_header

        for i in range(list_length):
            j = i + 1

            for j in range(list_length):
                match = susses[i] & susses[j]
                if len(match) != 0:
                    has_header = True
                    headers = headers | match
                    break

        return headers, has_header


def remove_header(pages, headers):

        for page in pages:
            for p in pages[page]:
                if p in headers:
                    pages[page].remove(p)
                    if len(headers) == 1:
                        break

        return pages


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    stopwords_list = stopwords.words('english')
    wnl = WordNetLemmatizer()

    # Process: tokenize string --> filter punctuation --> convert to lowercase
    wordlist = [(word.lower() if word.isalpha() else word)
                    for word in wordpunct_tokenize(document)
                    if word not in punctuation]

    # Filter out stop words from the list
    wordlist = [token for token in wordlist
                    if token not in stopwords_list]

    # Lemmatize remaining words from the list
    wordlist = [wnl.lemmatize(wd) for wd in wordlist]

    return wordlist


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    from math import log

    # Constant -> number of files in 'documents'
    n_docs = len(documents)

    # Dictionary to keep track of number of documents a word appeared in
    df_word = dict()

    for filename in documents:
        for word in documents[filename]:

            # Add an entry for the word when encountered for the first time
            if word not in df_word:
                df_word[word] = [filename]

            # Add filename associated with the word for the first time
            elif word in df_word and filename not in df_word[word]:
                df_word[word].append(filename)

    idf_word = dict()
    for wd in df_word:
        idf_word[wd] = log(n_docs / len(df_word[wd]))

    return idf_word