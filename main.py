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
    # Stop the folder checker
    fcheck.stop()
    fcheck.join()
    # Start Guelfo
    guelfo = guelfoset(output=logset())
    """GUElfo instance"""
    fcheck = checker_guelfoset()
    """Folder Checker"""
    # Start GUElfo
    guelfo.start()
    # Start the checker
    fcheck.start()
    # Wait for the GUElfo thread to finish
    guelfo.join()
    # Stop the checkers
    fcheck.stop()
    lcheck.stop()
    # End the program
    fcheck.join()
    lcheck.join()

if __name__ == "__main__":
    main()
