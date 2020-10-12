# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 01:26:38 2020

@author: pelie
"""

print('Loading query processing module...')
import os

from .DataProcessor import tokenize
from . import config, utils
from .utils import CLR_SYS, CLR_FILE, CLR_UI, CLR_WARN, CLR_SOFT_WARN, C_RESET

from collections import Counter
from nltk.tokenize import sent_tokenize
from torch import argmax, unsqueeze
from tqdm import tqdm
from transformers import AlbertTokenizer, AlbertForQuestionAnswering

Default_logic = utils.Default_logic

class QueryContainer(object):
    """  
    Handles query processes

    1. Preparing (init) for query:
        - download model if not found locally, save its file location
        # https://huggingface.co/transformers/main_classes/configuration.html#transformers.PretrainedConfig.save_pretrained

    2. Get query (on sapling.py)
         - Note: the max size of the input layer is 512 words

    3. find top files
    	- loop query over each file
        ? store top n results each time --> have to depend if the model works better with paragraphs or whole doc
        - finally compare score of all results and choose top n to display
    """
    def __init__(self):
        super(QueryContainer, self).__init__()
        self.get_query()

        self.query = []
        self.query_tokens = []
        self.topfiles = []
        self.directory = []

        self.matches = dict() # Store results
        self.num_matches = config.SENTENCE_MATCHES

    def __len__(self):
        return len(self.query)

    def add_query(self, query, query_tokens):
        self.query.append(query)
        self.query_tokens.append(query_tokens)

    def add_topfiles(self, filenames, directory):
        self.topfiles.append(filenames)
        self.directory.append(directory)

        if len(self) >= 20:
            self.query.pop(0)
            self.query_tokens.pop(0)
            self.topfiles.pop(0)
            self.directory.pop(0)

    def set_transformers_env(self):
        #TODO - allow user to change model
        model_options = {
            'default': 'twmkn9/albert-base-v2-squad2'
            }

        modelDir = os.path.join('cfg', 'nlp')
        tokPath = os.path.join(modelDir, 'tokenizer')
        modPath = os.path.join(modelDir, 'model')

        # Transformers auto create directory when saving, 
		# so when directory is not found, model is not downloaded yet
        # https://huggingface.co/transformers/main_classes/model.html#pretrainedmodel
        if not os.path.exists(modelDir):
            self.tokenizer = AlbertTokenizer.from_pretrained(model_options['default'])
            self.tokenizer.save_pretrained(tokPath)

            self.model = AlbertForQuestionAnswering.from_pretrained(model_options['default'], return_dict=True)
            self.model.save_pretrained(modPath)

        else:
            self.tokenizer = AlbertTokenizer.from_pretrained(tokPath)
            self.model = AlbertForQuestionAnswering.from_pretrained(modPath, return_dict=True)

        self.max_length = self.model.config.max_position_embeddings


    def get_query(self):

        while True:
            # Get user query
            query = input(f"{CLR_UI}Tell me, what is the question this human have?{C_RESET}\n")
            query_tokens = set(tokenize(query))

            if 1 < len(query_tokens) <= 50:
                print('Gotcha...')
                self.add_query(query, query_tokens)
                break

            elif len(query_tokens) > 50:
                print('(Warning) Your query is longer than 512 words, it may produce inaccurate result')
                self.add_query(query, query_tokens)
                break

            else:
                options = {
                    '1': '[1] Do you want to quit program,',
                    '2': '[2] or provide Sapling a query',
                    'logic': Default_logic
                    }

                print(f'{CLR_SOFT_WARN}Why don\'t you trust Sapling, you did not actually provide any query for me =< {C_RESET}\n')
                choice = utils.process_options(options)
                if choice:
                    utils.terminate()
                else:
                    continue


    def process_query(self, pdfobj, dirobj):

        while True:
            # Determine top file matches according to TF-IDF
            print('Sapling is going to speed read the texts...\n')
            filenames = top_files(self.query_tokens[-1], pdfobj.tokens, pdfobj.idfs, config.FILE_MATCHES)

            if len(filenames) > 0:
                self.add_topfiles(filenames, dirobj.directory)
                print('Okay~ Got something relevant in...\n')
            else:
                options = {
                    '1': '[1] Do you want to try another query,',
                    '2': '[2] or quit program?',
                    'logic': Default_logic
                    }
                print('Sorry, your query does not appear in the files you provided...\n')
                choice = utils.process_options(options)
                if choice:
                    continue
                else:
                    utils.terminate()

            for file in filenames:
                print(file)
            print()
            break

        ### Load transformers model for answer search ###
        print(f'{CLR_UI}Please bare with me for a few moments while I take a closer look...')
        self.set_transformers_env()

        query = self.query[-1]
        query_length = self.tokenizer(query, add_special_tokens=True, return_tensors="pt")
        query_length = len(query_length['input_ids'].tolist()[0])

        for filename in filenames:
            for passage in tqdm(pdfobj.passages[filename]):
                self.get_prediction(query, query_length, passage, filename)

        ### Display results ####
        if min(self.matches.keys()) > 15:
            print('Sapling found a few matches, but they are somewhat inaccurate...\n')
        else:
            print('Sapling thinks these are the closest answers to your question!\n')

        scores = []
        for i, loss_val in enumerate(sorted(self.matches.keys())):
            scores.append(loss_val)
            print(f'{i+1}. ', self.matches[loss_val]['file'])
            print('Match:\n', self.matches[loss_val]['answer'], '\n')
            print('In:\n', self.matches[loss_val]['context'], '\n\n')

        ### Get feedback ###
		# TODO - store this feedback
        options_0 = {
            '1': '[1] Did Sapling found the right answer for you?',
            '2': '[2] or not?',
            'logic': Default_logic
            }
        choice = utils.process_options(options_0)
        if choice:
            options_1 = {
                '1': f'Which one is the closest? (from results: 1 - {self.num_matches})',
                'logic': [1, 2, 3, 4, 5]
                }
            file_num = utils.process_options(options_1)
            print('Thank you for the feedback! 😉\n')
            self.results = {
                'question': query,
                'answer': self.matches[scores[file_num - 1]]['answer'],
                'context': self.matches[scores[file_num - 1]]['context']
                }
            config.Pause
            # TODO - For future implementation - saving data to user's system
            return os.path.join(dirobj.directory, self.matches[scores[file_num - 1]]['filename'])

        else:
            print("Sorry ☹ I'll try to do better next time...\n")
            config.Pause
            return False


    def get_prediction(self, query, query_length, passage, filename):
        # https://huggingface.co/transformers/model_doc/albert.html#albertforquestionanswering

        inputs = self.tokenizer(query, passage, add_special_tokens=True, return_tensors='pt')
        input_ids = inputs["input_ids"].tolist()[0]

        if len(input_ids) <= self.max_length:
            # Get labels of start and end of prediction
            output = self.model(**inputs)
            start_position = argmax(output['start_logits']).unsqueeze(0)
            end_position = argmax(output['end_logits']).unsqueeze(0)

            # Get loss value
            output = self.model(**inputs, start_positions=start_position, end_positions=end_position)
            loss = output.loss.item()

            ### Logic to save outputs ###
            if len(self.matches) <= self.num_matches: # Populate results var
                answer_start = argmax(output['start_logits'])
                answer_end = argmax(output['end_logits']) + 1

                self.matches[loss] = {
                    'file' : filename,
                    'answer': self.tokenizer.convert_tokens_to_string(
                        self.tokenizer.convert_ids_to_tokens(
                            input_ids[answer_start : answer_end])),
                    'context': passage
                    }

            elif loss < max(self.matches.keys()): # Replace with better result
                _ = self.matches.pop(max(self.matches.keys()))
                self.matches[loss] = {
                    'file' : filename,
                    'answer': self.tokenizer.convert_tokens_to_string(
                        self.tokenizer.convert_ids_to_tokens(
                            input_ids[answer_start : answer_end])),
                    'context': passage
                    }

        else:
            # Split paragraph returns a generator item
            for context in self.split_paragraph(query_length, passage):
                self.get_prediction(query, query_length, context, filename)


    def split_paragraph(self, query_length, passage):

        split_passage = ''

        for sentence in sent_tokenize(passage):
            tokens = self.tokenizer(sentence, add_special_tokens=True, return_tensors="pt")
            tokens = len(tokens['input_ids'].tolist()[0]) - 1

            if tokens + query_length <= self.max_length:
                split_passage += (sentence + ' ')
            else:
                yield split_passage
                split_passage = sentence

        yield split_passage


def top_files(query, files, idfs, n):
    """
	Given a `query` (a set of words), `files` (a dictionary mapping names of
	files to a list of their words), and `idfs` (a dictionary mapping words
	to their IDF values), return a list of the filenames of the the `n` top
	files that match the query, ranked according to tf-idf.
	"""
    # Initialize dict() using each file with value 0 as items
    tfidfs = dict(zip(files.keys(), [0]*len(files)))

    # Calculate tfidf for each search term for each file, then add the value
	# to the score of the file
    for word in tqdm(query):
        for filename in files:
            # Calculate tf
            c = Counter(files[filename])
            tfidfs[filename] += c[word] * idfs[word]

    # Sort tfidf.items according to its value, then loop the sorted list and
	# store the key according to the order
    ranked = [k for k,v in sorted(tfidfs.items(),
                                  key=lambda i: i[1], reverse=True)]

    # Slice n-elements from the ranked list and return it
    if n < len(ranked):
        return ranked[:n]
    else:
        return ranked