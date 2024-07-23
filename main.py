#!/bin/python3
'''
    EUgolino Main
    file name: main.py
    author: Lorenzo Radice
    license: European Union Public Licence v. 1.2.
    description:
        This is the main file of the EUgolino project.
        It downloads the pdfs and checks the status of itself.
'''

from classes.eugolino import EUgolino
from classes.checkers.checker import Checker
from config import *

def main():
    '''
        Main function of the EUgolino project.
    '''
    # Set up
    log_manager = setup()
    # Program
    eugolino = EUgolino(file, max_downloads=max, output=log_manager)
    checker = Checker(check_URL=URL, send_check=True, sleep_time=sleep_time, max_len=max, name=check_name)
    # Start the threads
    eugolino.start()
    checker.start()
    # Wait for the threads to finish
    eugolino.join()
    checker.stop()
    checker.join()

if __name__ == "__main__":
    main()
