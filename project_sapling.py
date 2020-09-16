# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:22:07 2020

@author: pelie
"""

from colored import fg, bg, fore, attr, style
from nltk.tokenize import sent_tokenize
import os


VERSION = 0.1
FILE_MATCHES = 5
SENTENCE_MATCHES = 5
COLR_SYS = bg(9) # Color for displaying high level msg
COLR_FILE = fg(12) # Color for displaying compatible files
COLR_UI = fg(46) # Color for displaying user interactions
COLR_WARN = bg(11) + fg(1) + attr(1)
C_RESET = style.RESET
OPTION_test = {
    'opt': ['Y', 'N'],
    'Y': 'some text',
    'N': 'some text',
    'val': {
        'Y': True,
        'N': False}
    }

# TODO adjust control flows
# maybe with numbered options?

def main():
    # Display start up information - version, usage, link to instructions
    print('*' * 25)
    print(f'You are using Know v{VERSION}')
    print('*' * 25, '\n')

    while True:
        # May move this section to load_directory function, and make function call in load_data
        # Attempt to get and handle directory from user
        try:
            flag_d, file_list = get_directory()
        except TypeError:
            cont0 = input('\nOptions: \nY: Try again or \nN: quit program \nYour choice: ')
            if cont0.lower() == 'y':
                continue
            elif cont0.lower() == 'n':
                break
            else:
                print('Unrecognized option. Please provide a valid option!')
                continue
                #TODO - add location to loop to

        if flag_d:
            print(f'{sum(len(file_list[k]) for k in file_list)} compatible file(s) found.')
        else:
            print('Sorry, no compatible files found :(')
            break
            #TODO - add location to loop to

        # Load texts from supported file into memory
        files = load_data(file_list)

        # Compute idfs - each word carries a value to represent it's uniqueness
        file_words = {
            filename: tokenize(files[filename])
            for filename in files
            }
        file_idfs = compute_idfs(file_words)
        break

    while True:
            # Get user query
            query = set(tokenize(input("What do you want to search for: ")))
    
            # Determine top file matches according to TF-IDF
            filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)
        
            # Extract sentences from top files
            sentences = dict()
            for filename in filenames:
                for passage in files[filename].split("\n"):
                    for sentence in sent_tokenize(passage):
                        tokens = tokenize(sentence)
                        if tokens:
                            sentences[sentence] = tokens
        
            # Compute IDF values across sentences
            idfs = compute_idfs(sentences)
        
            # Determine top sentence matches
            matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
            for i, match in enumerate(matches):
                #TODO - display filename of the sentence, highlight query words
                print(f'{i+1}. {match}\n')
    
            # Check if user would like to continue searching
            cont = input('\nDo you want to continue? (y/n) ')
            if cont.lower() == 'y':
                continue
            elif cont.lower() == 'n':
                print('Thank you for using Know. For feedback or issues, please contact me at pelie_888888@hotmail.com')
                print('Goodbye!')
                break
            else:
                print('Unrecognized option. Please provide a valid option!')
                # TODO - add location to loop to

def subroutines(sel):
    return sel

def display_options(options):
    print('Options:')
    for option in options['opt']:
        print(options[option])

    sel = input('Your choice:').lower()

    if sel in options['val']:
        return options['val'][sel]
    else:
        print('Error message')


def get_directory():
    ''' 
    Get directory to load data from, and check if it contains valid files
    Return a flag and dict of valid files
    Limitations: will not go deeper than the given directory
    '''
    directory_found = False
    valid_extensions = ['.pdf', '.txt'] # '.docx' not implemented in this version

    directory = input(f'{COLR_UI}Which folder(directory) do you want to load files from?{C_RESET}\n[Please provide full path of your folder]\n')

    # Check if valid input is given
    if os.path.exists(directory):

        # Check if path contains valid file
        file_list = os.listdir(directory)
        valid_files = dict()

        print(f'\n{COLR_SYS}Checking {len(file_list)} file(s) in \'{os.path.basename(directory)}\'.....{C_RESET}')
        counter = 1
        for file in file_list:
            # get extension of each file in the directory
            ext = os.path.splitext(file)[1]
            if ext in valid_extensions:
                print(f'{COLR_FILE}{counter}. {file}{C_RESET}')
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

    else:
        print(f'\n{COLR_WARN}Oops!! Error: \'{directory}\' not found!{C_RESET}')
        return

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
        # TODO - .docx and .txt do nothing at the moment
        elif ext == '.doc':
            file_list[ext]
        elif ext == '.txt':
            file_list[ext]

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
                print(f'Found {COLR_FILE}\'{ef}\'{C_RESET} section')
                ind_ref = len(ending) - ending.find(ef)
                raw = parsed_file[tp[3]][:-ind_ref]
                break

        # Could not find keyword
        try:
            if len(raw) > 0:
                pass
        except UnboundLocalError:
            print('Could not find or No (COLR_WARN}reference{C_RESET} section')
            raw = parsed_file[tp[3]]

        ### Attempt to detect 'title page' by it's char count
        avg_word_count = sum(int(i) for i in char_counts) / n_pages

        # Char count of the first page
        n = int(char_counts[0])

        if n < avg_word_count:
            print(f'Found {COLR_FILE}title{C_RESET} page \n')
            files[file_name] = raw[n:].replace('-\n', '')
        else:
            print(f'Could not find or No {COLR_WARN}title{C_RESET} page \n')
            files[file_name] = raw.replace('-\n', ' ')

    if len(err_files) > 0:
        print('Sorry, texts in the following file(s) are not parsable: ')
        for i, file in enumerate(err_files):
            print(f'{i+1}. {file}')
        print('\n')

    return files


def load_docs(file_sublist):
    from docx import Document

    files = dict()

    print('Loading docx\'s.....')
    for file_path in file_sublist:
        file = Document(file_path)

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
    wordlist =[wnl.lemmatize(wd) for wd in wordlist]

    return wordlist


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    import math

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
        idf_word[wd] = math.log(n_docs / len(df_word[wd]))

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


if __name__ == "__main__":
    main()