# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 14:03:07 2020

@author: pelie
"""

print('Loading utility functions...')
import os, psutil, signal, sys #, logging

from subprocess import run
from colored import fg, bg, attr, style
from random import choice

from . import config

### Color schemes
CLR_SYS = bg(22) # Color for displaying high level msg
CLR_FILE = fg(12) # Color for displaying compatible files
CLR_UI = fg(46) # Color for displaying user interactions
CLR_WARN = bg(11) + fg(1) + attr(1) # Color for displaying serious errors
CLR_SOFT_WARN = fg(1) # Color for displaying warnings
C_RESET = style.RESET

##
Default_logic = [True, False]
Java_pid = False


def disp_banner(version):
    '''
    Display start up information 
    - version, program logo, link to instructions
    - program logo is randomly selected during each start up
    '''
    # Logo folder has to be in the same folder as this code file. Otherwise there will be error.
    # Ref: https://stackoverflow.com/questions/51060894/adding-a-data-file-in-pyinstaller-using-the-onefile-option
    try:
        path = sys._MEIPASS + os.sep + 'logo'
    except:
        if os.path.exists('logo'):
            path = os.path.abspath('logo')
        else:
            path = os.path.abspath('..'+os.sep+'logo')

    file = choice(os.listdir(path))
    top = [f'Hey there! This is Sapling v.{version}.',
           'It\'s so nice to meet you!\n']
    end_quote = ['For instructions and latest updates, please visit',
                 'https://github.com/einstin88/sapling-release']
    min_length = max(len(i) for i in end_quote)

    with open(os.path.join(path, file), encoding='utf-8') as f:
        logo = f.read().splitlines()
        lg_length = len(logo[0])

        # Formatting for displaying program title
        if lg_length > min_length:
            min_length = lg_length
            logo_offset = 0
        else:
            logo_offset = (min_length - lg_length)//2 - 1

        ## Display logo and message
        print()
        print('*' * min_length)
        for ln in top:
            print(' ' *((min_length - len(ln))//2 -1), ln)
        for line in logo:
            print(' ' * logo_offset, line)
        print()
        for txt in end_quote:
            print(txt)
        print('*' * min_length, '\n')


def process_options(selection):
    '''
    Handle the display and validation of options given by user

    Parameters
    ----------
    caller : string
        Caller is a 'code'.that is assigned based on which function calls for options to be processed
        The code is to match a 'key' in the OPTIONS dict() below.

    Returns
    -------
    bool
        Return appropriate value to caller.

    '''
    err_msg = f'{CLR_WARN}Wait a minute, that\'s not a valid option! @#$%& !! {C_RESET}\n'

    for option in selection:
        if option != 'logic':
            print(selection[option])

    print("(typing 'quit' will shutdown Sapling)")
    # Get and validate user input
    while True:
        sel = input(f'{CLR_UI}Please enter your numeric choice:{C_RESET} ')
        print()
        sel = sel.strip()

        if sel == 'quit':
            terminate()
        else:
            try:
                sel = int(sel)
            except:
                print(err_msg)
                continue

        if 0 < sel <= len(selection['logic']):
            return selection['logic'][sel - 1]

        else:
            print(err_msg)


def check_mem(limit_percent=85, limit_kb= 1_000_000):
    mem = psutil.virtual_memory()

    if mem.percent > limit_percent or mem.free < limit_kb:
        print('Memory usage is High...')
        return True
    else:
        return False


def check_java_vers():

    j_cmd = 'java -version'
    print('Checking Java version...')
    try:
        j = run(j_cmd, capture_output=True, shell=True)
    except FileNotFoundError:
        print('Could not find Java in system path...')
        terminate()

    version = j.stderr.decode(encoding='utf-8')

    if '1.8' in version or '1.7' in version:
        print('PASS :))')
        return True
    else:
        print('Java did not meet minimum requirement')
        return False

def check_java_running():

    global Java_pid

    # https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
    process_found = False
    for ps in psutil.process_iter(['pid', 'name']):
        if 'java' in ps.name():
            Java_pid = ps.pid
            process_found = True
            break

    if not process_found:
        Java_pid = False


def kill_java():

    global Java_pid
    
    if Java_pid:
        print('Attempting to terminate Java runtime...')
        os.kill(Java_pid, signal.SIGTERM)
        Java_pid = False
        print('Successfully terminated Java runtime\n')
    else:
        print("Info: Java runtime not found to be running\n")


def open_file(file_path):

    if config.WINDOWS:
        os.startfile(file_path)
    else:
        cmd_file = f'open {file_path}'
        run(cmd_file, shell=True)


def terminate():
    '''
    Exit point for the program
    '''

    # TODO - Message to be replaced with link to Google Form 
    print('Shutting down...')
    if Java_pid:
        kill_java()
    print(f'{CLR_SYS}Thank you for using Sapling. For feedbacks or issues, please contact me at pelie_888888@hotmail.com{C_RESET}')
    print('Goodbye!')

    sys.exit()



if check_java_vers():
    config.setup_folders()
else:
    terminate()
