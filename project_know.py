# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:22:07 2020

@author: pelie
"""

from colored import fg, bg, attr, fore, back, style
import os

#TODO adjust control flows
def main():
    while True:
        # May move this section to load_directory function, and make function call in load_data
        # Attempt to get and handle directory from user
        try:
            flag_d, file_list = get_directory()
        except TypeError:
            cont0 = input('Try again (y) or quit program (n). \nYour choice: ')
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

        # TODO - Load data and implement option to load different types of file (.pdf & .docx)
        files = load_data(file_list)
        print(files.keys())

        # Check if user would like to continue searching
        cont = input('\nDo you want to continue? (y/n) ')
        if cont.lower() == 'y':
            continue
        elif cont.lower() == 'n':
            break
        else:
            print('Unrecognized option. Please provide a valid option!')
            # TODO - add location to loop to


def get_directory():
    ''' 
    Get directory to load data from, and check if it contains valid files
    Return a flag and dict of valid files
    Limitations: will not go deeper than the given directory
    '''
    directory_found = False
    valid_extensions = ['.pdf', '.txt', '.docx']

    directory = input('Which folder(directory) do you want to load files from?\n[Please provide full path of your folder]\n')

    # Check if valid input is given
    if os.path.exists(directory):

        # Check if path contains valid file
        file_list = os.listdir(directory)
        valid_files = dict()

        print(f'\n{bg(1)}Checking {len(file_list)} file(s) in \'{os.path.basename(directory)}\'.....{style.RESET}')
        for file in file_list:
            # get extension of each file in the directory
            ext = os.path.splitext(file)[1]
            if ext in valid_extensions:
                #print(f'{fore.CYAN}{file}{style.RESET}')
                path = os.path.join(directory, file)
                if ext in valid_files:
                    valid_files[ext].append(path)
                else:
                    valid_files[ext] = [path]
            #else:
                #print(file)

        if len(valid_files) > 0:
            directory_found = True

    else:
        print(f'\n{fg(1)}{attr(1)}Oops!! Error: \'{directory}\' not found!{style.RESET}')
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
        DESCRIPTION.

    '''
    files = dict()

    for ext in file_list:
        if ext == '.pdf':
            files.update(load_pdf(file_list[ext]))
        elif ext == '.doc':
            file_list[ext]
        elif ext == '.txt':
            file_list[ext]

    return files


def load_pdf(file_sublist):
    from tika import parser

    files = dict()

    print('Loading pdfs....')
    for file_path in file_sublist:
        files[os.path.basename(file_path)] = parser.from_file(file_path)['content']

    return files


def load_docs(file_sublist):
    from docx import Document

    files = dict()

    print('Loading docx\'s.....')
    for file_path in file_sublist:
        file = Document(file_path)

    return files


if __name__ == "__main__":
    main()