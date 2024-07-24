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

import time
from classes.eugolino import EUgolino
from classes.checkers.folder_checker import FolderChecker
from setup import *

def main():
    '''
        Main function of the EUgolino project.
    '''
    # Program
    eugolino = eugolinoset(output=logset())
    """EUgolino instance"""
    fcheck, lcheck = checkerset()
    """Checkers"""
    # Start EUgolino
    eugolino.start()
    # Start the checkers
    fcheck.start()
    # Delay the next checker
    time.sleep(delay)
    lcheck.start()
    # Wait for the EUgolino thread to finish
    eugolino.join()
    # Stop the checkers
    lcheck.stop()
    fcheck.stop()
    # End the program
    lcheck.join()
    fcheck.join()

if __name__ == "__main__":
    main()
