#!/bin/python3
'''
    EUgolino Main
    file name: main.py
    author: Lorenzo Radice
    description:
        This is the main file of the EUgolino project.
        It downloads the pdfs and checks the status of itself.
'''

import sys
from classes.eugolino import EUgolino
from classes.checker import Checker
from config import *

# Set up
log_manager = setup()

# Program
eugolino = EUgolino(file, max_downloads=max, output=log_manager)
checker = Checker(URL=URL, sleep_time=sleep_time, max_len=max, name=check_name)
# Start the threads
eugolino.start()
checker.start()
# Wait for the threads to finish
eugolino.join()
checker.stop()
checker.join()
