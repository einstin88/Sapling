# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:22:07 2020

@author: pelie
"""

from colored import fg, bg, attr, style
from nltk.tokenize import sent_tokenize
import os

### Global vars
VERSION = 0.1
FILE_MATCHES = 5
SENTENCE_MATCHES = 5

### Color schemes
CLR_SYS = bg(9) # Color for displaying high level msg
CLR_FILE = fg(12) # Color for displaying compatible files
CLR_UI = fg(46) # Color for displaying user interactions
CLR_WARN = bg(11) + fg(1) + attr(1)
CLR_SOFT_WARN = fg(1)
C_RESET = style.RESET


# TODO adjust control flows with numbered options in subroutine function
def main():

    print_title()

    # Get a directory from user
    file_list = subroutines(1)
    # Pre-process files from directory
    files, file_words, file_idfs = subroutines(2, f_list=file_list)

    sent_tokens = dict()
    while True:
        # Get query
        query = subroutines(3)
        # Process query
        sent_tokens.update(subroutines(4, q=query, f=files, f_words=file_words, f_idfs=file_idfs))

        # Handle repeat query
        choice = process_options('main_0')
        if choice:
            continue
        else:
            terminate()


def subroutines(sel, q=None, f=None, f_words=None, f_idfs=None, f_list=None):

    # Get and handle directory from user
    if sel == 1:
        while True:
            try:
                flag_d, file_list = get_directory()
            except TypeError:
                choice = process_options('sub1_0')
                if choice:
                    continue
                else:
                    terminate()

            if flag_d:
                print(f'{sum(len(file_list[k]) for k in file_list)} compatible file(s) found.\n')
                return file_list
            else:
                print('Sorry, no compatible files found :(\n')
                choice = process_options('sub1_0')
                if choice:
                    continue
                else:
                    terminate()

    # Texts preprocessing
    if sel == 2:
        # Load texts from compatible file into memory
        files = load_data(f_list)

        # Tokenize the cleaned texts
        file_words = {
            filename: tokenize(files[filename])
            for filename in files
            }

        file_idfs = compute_idfs(file_words)

        return files, file_words, file_idfs

    # Get and handle query
    if sel == 3:
        while True:
            # Get user query
            query = set(tokenize(input("What do you want to search for: ")))
            if len(query) > 0:
                print('Processing your query...')
                return query
            else:
                print(f'{CLR_SOFT_WARN}You did not enter any query{C_RESET}')
                choice = process_options('sub3_0')
                if choice:
                    terminate()
                else:
                    continue

    # Process query and print results
    if sel == 4:
        # Determine top file matches according to TF-IDF
        filenames = top_files(q, f_words, f_idfs, n=FILE_MATCHES)
        
        # Extract sentences from top files
        sentences = dict()
        sent_tkn_files = dict()

        for filename in filenames:
            #for passage in files[filename].split("\n"):
            sent_tkn_files[filename] = set()
            for sentence in sent_tokenize(f[filename]):
                    tokens = tokenize(sentence)
                    if len(tokens) > 6:
                        sentences[sentence] = tokens
                        sent_tkn_files[filename].add(sentence)
        
        # Compute IDF values across sentences
        idfs = compute_idfs(sentences)
        
        # Determine top sentence matches
        matches = top_sentences(q, sentences, idfs, n=SENTENCE_MATCHES)
        for i, match in enumerate(matches):
            #TODO - display filename of the sentence, highlight query words
            for file in filenames:
                if match in sent_tkn_files[file]:
                    text = f''
                    for word in sentences[match]:
                        if word in q:
                            text += f'{CLR_FILE}{word}{C_RESET} '
                        else:
                            text += f'{word} '
                    print(f'{i+1}. {file}')
                    print(f'{text:<5}\n')
                    break

        return sent_tkn_files


def print_title():
    '''
    Display start up information - version, usage, link to instructions
    '''
    import random

    path = os.path.abspath('ascii_title')
    file = random.choice(os.listdir(path))
    default = f'You are using v{VERSION} of'
    end_quote = ['For instructions, tutorials or latest updates, please visit',
                 'https://github.com/einstin88/Sapling/blob/master/README.md']
    min_length = max(len(i) for i in end_quote)

    with open(os.path.join(path, file), encoding='utf-8') as f:
        logo = f.read().splitlines()
        length = len(logo[0])

        if length > min_length:
            min_length = length
            logo_offset = 0
        else:
            logo_offset = (min_length - length)//2 - 1

        ## Output Section
        print()
        print('*' * min_length)
        print(' '* ((min_length - len(default))//2 -1), default)
        for line in logo:
            print(' ' * logo_offset, line)
        print()
        for txt in end_quote:
            print(txt)
        print('*' * min_length, '\n')


def process_options(caller):
    optns = ['1', '2']

    OPTIONS = {
        'get_directory_0': {
            '1': '[1] Would you like to choose another directory,',
            '2': '[2] or proceed?'
            },
        'main_0': {
            '1': '[1] Do you want to make another query,',
            '2': '[2] or quit program'
            },
        'sub1_0': {
            '1': '[1] Try with another directory,',
            '2': '[2] or quit program'
            },
        'sub3_0': {
            '1': '[1] Do you want to quit program,',
            '2': '[2] or provide a query'
            }
    }

    for option in optns:
        print(OPTIONS[caller][option])

    while True:
        sel = input('Your choice: ')

        if sel == '1':
            return True
        elif sel == '2':
            return False
        elif sel == 'quit':
            terminate()
        else:
            print(f'{CLR_WARN}Invalid option. Please provide a valid option!{C_RESET}\n')


def get_directory():
    ''' 
    Get directory to load data from, and check if it contains valid files
    Return a flag and dict of valid files
    Limitations: will not go deeper than the given directory
    '''
    directory_found = False
    valid_extensions = ['.pdf', '.txt'] # '.docx' not implemented in this version

    while True:
        directory = input(f'{CLR_UI}Which folder do you want to load files from?{C_RESET}\n[Please provide full path of your folder].\n')
        # Correct input format when path was given by user using drag and drop
        if directory[0] == '\'':
            directory = directory[1:-1]
    
        # Check if valid input is given
        if os.path.exists(directory):
            if os.path.isdir(directory):
                file_list = os.listdir(directory)
            elif os.path.isfile(directory):
                file_list = [os.path.basename(directory)]

        else:
            print(f'\n{CLR_WARN}Oops!! Error: \'{directory}\' not found!{C_RESET}')
            return
    
        if len(file_list) == 1:
            print(f'\n{CLR_SOFT_WARN}Warning: you have only provided one file. Query results may be inaccurate.{C_RESET}')
            choice = process_options('get_directory_0')
    
            if choice:
                continue
            else:
                break
        else:
            break

    # Check if path contains valid file
    valid_files = dict()
    counter = 1

    print(f'\n{CLR_SYS}Checking {len(file_list)} file' +
          ('s in' if len(file_list)>1 else '') +
          f' \'{os.path.basename(directory)}\'.....{C_RESET}')
    for file in file_list:
            # Get extension of each file in the directory
            ext = os.path.splitext(file)[1]
            if ext in valid_extensions:
                print(f'{CLR_FILE}{counter}. {file}{C_RESET}')
                counter += 1

                path = os.path.join(directory, file)
                if ext in valid_files:
                    valid_files[ext].append(path)
                else:
                    valid_files[ext] = [path]

            else:
                print('- ', file)

    if len(valid_files) > 0:
            directory_found = True

    return (directory_found, valid_files)


def load_data(file_list):
    '''
    Parameters
    ----------
    file_list : dict()
        Keys    --> File type
        Values  --> list of files to load into memory

    Returns
    -------
    files : dict()
        Keys --> base file names
        Values --> cleaned texts

    '''
    files = dict()

    for ext in file_list:
        if ext == '.pdf':
            files.update(load_pdf(file_list[ext]))
        # TODO - .docx do nothing at the moment
        elif ext == '.doc':
            files.update(load_docs(file_list[ext]))
        elif ext == '.txt':
            files.update(load_texts(file_list[ext]))

    return files


def load_pdf(file_sublist):
    '''
    Parameters
    ----------
    file_sublist : list
        Full paths to pdfs found from the given directory.

    Returns
    -------
    files : dict()
        Keys --> file names
        Values --> cleaned string

    '''
    from tika import unpack

    files = dict()
    err_files = []
    tp = ['metadata', 'pdf:charsPerPage', 'pdf:unmappedUnicodeCharsPerPage',
          'content', 'xmpTPg:NPages']
    end_filters = ['References', 'REFERENCES', 'Bibliography', 'BIBLIOGRAPHY']

    print('Loading pdfs....')
    counter = 1
    for file_path in file_sublist:
        #TODO Implement XML parsing and regex processing
        try:
            parsed_file = unpack.from_file(file_path)

        except UnicodeDecodeError:
            from tika import parser
            parsed_file = parser.from_file(file_path)

        file_name = os.path.basename(file_path)

        ### Check if texts in file are parsable
        # Determine number of pages with large amt of unmapped chars
        umc = sum(True for i in parsed_file[tp[0]][tp[2]] if int(i) > 250)

        # Determine number of pages with 0 char = pages are images
        nc = sum(True for i in parsed_file[tp[0]][tp[1]] if int(i) == 0)

        n_pages = int(parsed_file[tp[0]][tp[4]])

        # TODO - implement OCR function for these files
        if umc > 2 or nc > 0.5 * n_pages:
            err_files.append(file_name)
            continue
        else:
            print(f'{counter}: Successfully loaded \'{file_name}\'')
            counter +=1

        ### Attempt to filter out references
        # A list of number of chars for each page
        char_counts = parsed_file[tp[0]][tp[1]]

        # Look for keywords at the ends of file
        ends = int(0.75* n_pages) -1
        ends = sum(int(char_counts[j]) for j in range(ends, n_pages))
        ending = parsed_file[tp[3]][-ends:]
        for ef in end_filters:
            if ef in ending:
                print(f'Found {CLR_FILE}\'{ef}\'{C_RESET} section')
                ind_ref = len(ending) - ending.find(ef)
                raw = parsed_file[tp[3]][:-ind_ref]
                break

        # Could not find keyword
        try:
            if len(raw) > 0:
                pass
        except UnboundLocalError:
            print('Could not find or No (CLR_SOFT_WARN}reference{C_RESET} section')
            raw = parsed_file[tp[3]]

        ### Attempt to detect 'title page' by it's char count
        avg_word_count = sum(int(i) for i in char_counts) / n_pages

        # Char count of the first page
        n = int(char_counts[0])

        if n < avg_word_count:
            print(f'Found {CLR_FILE}title{C_RESET} page \n')
            raw = raw[n:].replace('-\n', '')
            files[file_name] = raw.replace('\n', ' ')
        else:
            print(f'Could not find or No {CLR_SOFT_WARN}title{C_RESET} page \n')
            raw = raw.replace('-\n', '')
            files[file_name] = raw.replace('\n', ' ')

    if len(err_files) > 0:
        print('Sorry, texts in the following file(s) are not parsable: ')
        for i, file in enumerate(err_files):
            print(f'{i+1}. {file}')
        print()

    return files


def load_docs(file_sublist):
    #from docx import Document

    files = dict()

    print('Loading docx\'s.....')
    #for file_path in file_sublist:
     #   file = Document(file_path)

    return files

def load_texts(file_sublist):
    files = dict()

    print('Loading texts.....')
    for file_path in file_sublist:
        with open(file_path, encoding='utf-8') as f:
            files[os.path.basename(file_path)] = f.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    import string
    from nltk.corpus import stopwords
    from nltk.tokenize import wordpunct_tokenize
    from nltk.stem import WordNetLemmatizer

    stopwords_list = stopwords.words('english')
    wnl = WordNetLemmatizer()

    # Process: tokenize string --> filter punctuation --> convert to lowercase
    wordlist = [(word.lower() if word.isalpha() else word)
                for word in wordpunct_tokenize(document)
                if word not in string.punctuation]

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


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    from collections import Counter

    # Initialize dict() using each file with value 0 as items
    tfidfs = dict(zip(files.keys(), [0]*len(files)))

    # Calculate tfidf for each search term for each file, then add the value
    # to the score of the file
    for word in query:
        for filename in files:

            # Calculate tf
            c = Counter(files[filename])
            tfidfs[filename] += c[word] * idfs[word]

    # Sort tfidf.items according to its value, then loop the sorted list and
    # store the key according to the order
    ranked = [k for k,v in sorted(tfidfs.items(),
                                  key=lambda i: i[1], reverse=True)]

    # Slice n-elements from the ranked list and return it
    return ranked[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sent_score = dict()

    for word in query:
        for sentence in sentences:

            # Update sentence score if word is in the sentence
            if word in sentences[sentence]:
                if sentence not in sent_score:
                    sent_score[sentence] = idfs[word]
                else:
                    sent_score[sentence] += idfs[word]


    ranked = [k for k,v in sorted(sent_score.items(),
                                  key=lambda i: i[1], reverse=True)]

    if len(ranked) < n:
        return ranked

    # Check if there is a tie btwn the n'th sentence and (n+1)'th sentence
    if sent_score[ranked[n-1]] == sent_score[ranked[n]]:
        from collections import Counter
        c0 = Counter(sentences[ranked[n-1]])
        c1 = Counter(sentences[ranked[n]])
        sent_0, sent_1 = [0,0]

        # Calculate query term density
        for word in query:
            sent_0 += (c0[word] if word in c0 else 0)
            sent_1 += (c1[word] if word in c1 else 0)

        sent_0 /= len(sentences[ranked[n-1]])
        sent_1 /= len(sentences[ranked[n]])

        if sent_0 > sent_1:
            return ranked[:n]
        elif n == 1:
            return [ranked[1]]
        else:
            return ranked[:n-1] + [ranked[n]]

    else:
        return ranked[:n]


def terminate():
    import sys

    print(f'{CLR_SYS}Thank you for using Sapling. For feedbacks or issues, please contact me at pelie_888888@hotmail.com{C_RESET}')
    print('Goodbye!')
    sys.exit()


if __name__ == "__main__":
    main()