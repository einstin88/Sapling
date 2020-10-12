# Stores functions no longer used

'''
XML_to_STR = {
    '&amp;': '&',
     '&gt;': '>',
     '&#8727;': '∗',
     '&#776;': '̈',
     '&#780;': '̌',
     '&#65533;': '�',
     '&quot;': '"',
     '&#769;': '́',
     '&#61594;': '\uf09a',
     '&#61593;': '\uf099',
     '&#61665;': '\uf0e1',
     '&#61857;': '\uf1a1',
     '&#61664;': '\uf0e0',
     '&#61582;': '\uf08e',
     '&#8629;': '↵',
     '&#61465;': '\uf019',
     '&#61945;': '\uf1f9',
     '&#61601;': '\uf0a1',
     '&#61612;': '\uf0ac',
     '&#61540;': '\uf064',
     '&#61717;': '\uf115',
     '&#9654;': '▶',
     '&#10003;': '✓',
     '&#61802;': '\uf16a',
     '&#61598;': '\uf09e',
     '&#9679;': '●',
     '&#8722;': '−',
     '&#807;': '̧',
     '&#771;': '̃',
     '&#61479;': '\uf027',
     '&#61495;': '\uf037',
     '&#61485;': '\uf02d',
     '&#61520;': '\uf050',
     '&#61472;': '\uf020',
     '&#61623;': '\uf0b7',
     '&lt;': '<',
     '&#770;': '̂',
     '&#345;': 'ř',
     '&#8208;': '‐',
     '&#61745;': '\uf131',
     '&#61753;': '\uf139',
     '&#8486;': 'Ω',
     '&#730;': '˚',
     '&#945;': 'α',
     '&#946;': 'β',
     '&#8712;': '∈',
     '&#8721;': '∑',
     '&#955;': 'λ',
     '&#963;': 'σ',
     '&#63723;': '\uf8eb',
     '&#63725;': '\uf8ed',
     '&#63724;': '\uf8ec',
     '&#63734;': '\uf8f6',
     '&#63736;': '\uf8f8',
     '&#63735;': '\uf8f7',
     '&#968;': 'ψ',
     '&#931;': 'Σ',
     '&#961;': 'ρ',
     '&#8704;': '∀',
     '&#8805;': '≥',
     '&#8710;': '∆',
     '&#960;': 'π',
     '&#8800;': '≠',
     '&#63726;': '\uf8ee',
     '&#63728;': '\uf8f0',
     '&#63727;': '\uf8ef',
     '&#63737;': '\uf8f9',
     '&#63739;': '\uf8fb',
     '&#63738;': '\uf8fa',
     '&#948;': 'δ',
     '&#8804;': '≤',
     '&#8594;': '→'
    }
'''

def get_tags(element):
	# formerly in pdfprocessor.py
    ele_dict = {
        element.tag: {
            'items': element.items(),
            'text': [(0 if element.text == None else len(element.text))]
            }
        }

    if not has_children(element):
        return ele_dict

    for child in element:
        if has_children(child):
            ele_dict.update(get_tags(child))
        else:
            if child.tag in ele_dict:
                if child.items() != [] and child.items()[0] not in ele_dict[child.tag]['items']:
                    ele_dict[child.tag]['items'].extend(child.items())
                ele_dict[child.tag]['text'].append((0 if child.text == None else len(child.text)))
            else:
                ele_dict[child.tag] = {
                    'items': child.items(),
                    'text': [(0 if child.text == None else len(child.text))]
                    }

    return ele_dict

def has_children(element):
	# formerly in pdfprocessor.py
    if len(list(element)) > 0:
        return True
    else:
        return False


def process_tree(tree):
	# formerly in pdfprocessor.py
    # Used for testing purposes
    data = dict()
    raw = []

    for node in tree.iter():
        tag = node.tag
        items = node.items()
        texts = (0 if node.text == None else len(node.text))

        raw.append((tag, items, texts))
        if tag in data:
            for it in items:
                if it not in data[tag]['items']:
                    data[tag]['items'].append(it)
            data[tag]['text'].append(texts)

        else:
            data[tag] = {
                'items': items or [],
                'text': [texts]
                }

    return data, raw


def load_pdf(file_sublist):
	# formerlly in sapling.py
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
    from tika import tika, unpack

    files = dict()
    err_files = []
    #Tika parameters
    tp = ['metadata', 'pdf:charsPerPage', 'pdf:unmappedUnicodeCharsPerPage',
          'content', 'xmpTPg:NPages']
    end_filters = ['References', 'REFERENCES', 'Bibliography', 'BIBLIOGRAPHY']
    table = prettytable.PrettyTable(['n', 'File Name', 'Loaded',
                                     'Found Cover Page', 'Found References'])

    print('Loading those pdfs....')
    counter = 1
    for file_path in tqdm(file_sublist):
        #TODO Implement XML parsing and regex processing
        fl_load = 'No'
        fl_cover = 'No'
        fl_ref = 'No'

        try:
            parsed_file = unpack.from_file(file_path)

        except UnicodeDecodeError:
            from tika import parser
            parsed_file = parser.from_file(file_path)

        file_name = os.path.basename(file_path)

        ### Check if texts in file are parsable - implemented through umc and nc
        # Determine number of pages with large amt of unmapped chars = file's texts mapping is corrupted
        umc = sum(True for i in parsed_file[tp[0]][tp[2]] if int(i) > 250)

        # Determine number of pages with 0 char = pages are images
        nc = sum(True for i in parsed_file[tp[0]][tp[1]] if int(i) == 0)

        n_pages = int(parsed_file[tp[0]][tp[4]])

        # TODO - implement OCR function for these files
        if umc > 2 or nc > 0.5 * n_pages:
            err_files.append(file_name)
            continue
        else:
            #print(f'{counter}: Successfully loaded \'{file_name}\'')
            fl_load = 'Yes'
            c = counter
            counter +=1

        ### Attempt to filter out references section
        # A list of number of chars for each page
        char_counts = parsed_file[tp[0]][tp[1]]

        # Look for keywords at the ends of file
        ends = int(0.75* n_pages) -1
        ends = sum(int(char_counts[j]) for j in range(ends, n_pages))
        ending = parsed_file[tp[3]][-ends:]
        raw = ''
        for ef in end_filters:
            if ef in ending:
                #print(f'{W_SP}Found {CLR_FILE}\'{ef}\'{C_RESET} section')
                fl_ref = 'Yes'
                ind_ref = len(ending) - ending.find(ef)
                raw = parsed_file[tp[3]][:-ind_ref]
                break

        # Could not find keyword
        if raw != '':
                pass
        else:
            #print(f'{W_SP}Could not find or No {CLR_SOFT_WARN}reference{C_RESET} section')
            raw = parsed_file[tp[3]]

        ### Attempt to detect 'title page' by comparing char count on the first
        ### page with the rest of the document
        avg_word_count = sum(int(i) for i in char_counts) / n_pages

        # Char count of the first page
        n = int(char_counts[0])

        if n < avg_word_count:
            #print(f'{W_SP}Found {CLR_FILE}title{C_RESET} page \n')
            fl_cover = 'Yes'
            raw = raw[n:].replace('-\n', '')
            files[file_name] = raw.replace('\n', ' ')
        else:
            #print(f'{W_SP}Could not find or No {CLR_SOFT_WARN}title{C_RESET} page \n')
            raw = raw.replace('-\n', '')
            files[file_name] = raw.replace('\n', ' ')
        table.add_row([c, file_name, fl_load, fl_cover, fl_ref])

    # TODO - set window size and truncate file name that are too long
    # Display result from loading pdfs
    print(table)

    if len(err_files) > 0:
        print('Sorry, text' + ('s ' if len(err_files) > 1 else ' ') +
               'in the following file' +
               ('s are ' if len(err_files) > 1 else ' is ') + 'not parsable: ')
        for i, file in enumerate(err_files):
            print(f'{i+1}. {file}')
        print()

    # Free up system memory if it is low
    if utils.check_mem():
        tika.killServer()
        utils.kill_java()

    return files

def find_newline(text):
    # Formely in pdfprocessor
    if '\n' in text:
        return True
    else:
        return False

def subroutines(sel, q=None, f=None, f_words=None, f_idfs=None, f_list=None):
    '''
    Handle the flow of the program in a neat way
    Current version contains 4 blocks of code (sub-routines)

    Parameters
    ----------
    sel : int()
        A number representing the execution sequence.

    q : set(), optional
        Query words from user.

    f : dict(), optional
        keys    --> filename
        values  --> text-strings loaded from directory

    f_words : dict(), optional
        keys    --> filenames
        values  --> word tokens from the loaded text-strings

    f_idfs : dict(), optional
        keys    --> word tokens
        values  --> idf score of each word based on given corpus

    f_list : dict(), optional
        keys    --> the type of file extension
        values  --> paths to all located files with the same extension

    Returns
    -------
    Depends on which block of code (sub-routine) is executed

    '''

    # Get and handle directory from user
    if sel == 1:
        while True:
            #try:
             #   flag_d, file_list = get_directory()
            #except TypeError:
                choice = process_options('sub1_0')
                if choice:
                    continue
                else:
                    terminate()

            print()
            if flag_d:
                tot = sum(len(file_list[k]) for k in file_list)
                print(f'{CLR_SYS}Aha! Sapling\'s stolen {tot} compatible file' +
                    ('s ' if tot > 1 else ' ') + f'from the folder. Just kidding, its still there! I swear!{C_RESET}\n')
                if tot > 10:
                    print(f'{CLR_UI}OH Sweet Jesus, that\'s a lot of readings you have to do.\nYou know I\'ve been through a lot too. On a positive note though, knowledge is power!{C_RESET}\n')
                return file_list
            else:
                print(f'{CLR_SOFT_WARN}Sorry human, no compatible files found in that folder :({C_RESET}\n')
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
            query = set(tokenize(input(f"{CLR_UI}Tell me, what does this erudite human want to search for:{C_RESET} ")))
            if len(query) > 0:
                print('Gotcha, time for Sapling to do some intellectual magic behind the scenes...')
                return query
            else:
                print(f'{CLR_SOFT_WARN}Why don\'t you trust Sapling, you did not actually provide any query for me =< {C_RESET}')
                choice = process_options('sub3_0')
                if choice:
                    terminate()
                else:
                    continue

    # Process query and print results
    if sel == 4:
        from nltk.tokenize import sent_tokenize

        print(f'{CLR_UI}Please bare with me for a few moments while I speed read through all the documents you fed me with...')
        # Determine top file matches according to TF-IDF
        filenames = top_files(q, f_words, f_idfs, n=FILE_MATCHES)
        
        if len(filenames) > 0:
            #print(f'Okay~ Think I\'ve got something... Hmm, just need to figure out...')
            print()

        # Extract sentences from top files
        sentences = dict()
        sent_tkn_files = dict()

        for filename in filenames:
            sent_tkn_files[filename] = set()
            for passage in f[filename].split("\n"):
                for sentence in sent_tokenize(passage):
                        tokens = tokenize(sentence)
                        if len(tokens) > 6:
                            sentences[sentence] = tokens
                            sent_tkn_files[filename].add(sentence)
        
        # Compute IDF values across sentences
        idfs = compute_idfs(sentences)
        
        # Determine top sentence matches
        matches = top_sentences(q, sentences, idfs, n=SENTENCE_MATCHES)
        if len(matches) > 0:
            print(f'{CLR_SYS}Sapling thinks these are the most relevant to what you told me to look for.{C_RESET}\n')
            #table = prettytable.PrettyTable(
             #   ['Rank','Doc','Sentence'])

        matched_files = []
        for i, match in enumerate(matches):
            for file in filenames:
                if match in sent_tkn_files[file]:
                    matched_files.append(file)
                    text = f''
                    for word in sentences[match]:
                        if word in q:
                            text += f'{CLR_FILE}{word}{C_RESET} '
                        else:
                            text += f'{word} '
                    #table.add_row([i+1, f'{CLR_FILE}{file}{C_RESET}', text])
                    print(f'{CLR_FILE}{i+1}. {file}{C_RESET}')
                    print(f'{text}\n')
                    break # Stop looping other files if matching sentence is found

        #print(table)

        # TODO - For future implementation - saving data to user's system
        return matched_files #sent_tkn_files


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


def load_data(file_list):
    '''
    Load and process files into program's memory space by calling load_pdf() or load_texts()

    Parameters
    ----------
    file_list : dict()
        Keys    --> File type
        Values  --> list of filepaths to load into memory

    Returns
    -------
    files : dict()
        Keys --> base file names
        Values --> cleaned texts

    '''
    files = dict()

    for ext in file_list:
        if ext == '.pdf':
            files.update(DataProcessor.load_pdf(file_list[ext]))
        # TODO - .docx do nothing at the moment
        elif ext == '.doc':
            files.update(load_docs(file_list[ext]))
        elif ext == '.txt':
            files.update(load_texts(file_list[ext]))

    return files


def load_docs(file_sublist):
    #from docx import Document
    # docx file not implemented in this version
    files = dict()

    print('Loading docx\'s.....')
    #for file_path in file_sublist:
     #   file = Document(file_path)

    return files


def load_texts(file_sublist):
    '''
    Load .txt files

    Parameters
    ----------
    file_sublist : TYPE
        DESCRIPTION.

    Returns
    -------
    files : TYPE
        DESCRIPTION.

    '''
    files = dict()

    print('Loading them texts.....')
    for file_path in file_sublist:
        with open(file_path, encoding='utf-8') as f:
            files[os.path.basename(file_path)] = f.read()

    return files
