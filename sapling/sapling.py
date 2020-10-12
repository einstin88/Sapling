# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:22:07 2020

@author: pelie
"""
''' Core module '''

print('Loading main module...')

from . import DataProcessor
from .QueryProcessor import QueryContainer
from . import utils
from .utils import CLR_SYS, CLR_FILE, CLR_UI, CLR_WARN, CLR_SOFT_WARN, C_RESET

# Note: some imports are delayed to reduce load on active memory

### Global vars
VERSION = 0.1
#W_SP = f'{chr(32):<3}' # white space formatting for displaying results


def main():

    utils.disp_banner(VERSION)

    # Get a directory from user
    while True:
        directory_data = DataProcessor.DirContainer()
        directory_data.process_directory()

        if directory_data.valid_directory:
            print(f'{CLR_SYS}Aha! Sapling\'s stolen {len(directory_data)} compatible file' +
                    ('s ' if len(directory_data) > 1 else ' ')
                    + f'from the folder. Just kidding, its still there! I swear!{C_RESET}\n')
                #if tot > 10:
                 #   print(f'{CLR_UI}OH Sweet Jesus, that\'s a lot of readings you have to do.\nYou know I\'ve been through a lot too. On a positive note though, knowledge is power!{C_RESET}\n')

            # Pre-process files from directory
            if len(directory_data.pdfs) > 0:
                pdf_data = DataProcessor.PdfContainer()
                pdf_data.load_pdf(directory_data)
                pdf_data.get_idfs()
            break

        else:
            print(f'{CLR_SOFT_WARN}Sorry human, no compatible files found in that folder :({C_RESET}\n')
            options_0 = {
                '1': '[1] Try with another directory instead,',
                '2': '[2] or quit program?',
                'logic': utils.Default_logic
                }

            choice = utils.process_options(options_0)
            if choice:
                continue
            else:
                utils.terminate()

    while True:
        # Get and handle query
        query_data = QueryContainer()

        ### Process query - this is the bones (or main cognitive ability) of the program!
        result = query_data.process_query(pdf_data, directory_data)

        # TODO - For future implementation - saving data to user's system

        if result:
        # Handle repeat query
            options_1 = {
                '1': '[1] Would you like Sapling to open it?',
                '2': '[2] or would you like to ask something else,',
                '3': '[3] or quit program',
                'logic': [1, 2, 3]
                }

            choice = utils.process_options(options_1)

            if choice == 1:
                utils.open_file(result)

            elif choice == 2:
                continue

            else:
                utils.terminate()  
    
