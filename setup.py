#!/bin/python3
'''
    EUgolino Set-Up File  
    file name: config.py  
    author: Lorenzo Radice  
    license: European Union Public Licence v. 1.2.  
'''

import os
from typing import Tuple
from classes.cocito.eugolino import EUgolino
from classes.cocito.guelfo import GUElfo
from config import *

from classes.log_manager import LogManager
from classes.checkers.log_checker import LogChecker
from classes.checkers.folder_checker import FolderChecker

def logset() -> LogManager:
    '''
        This function sets up the environment for the EUgolino project.
        It initializes the log manager and returns it.
    '''
    # Make the log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    # Set up a Logging Manager
    log_manager = LogManager(out_file=outpath, err_file=errpath, duplicate=duplicate)
    return log_manager

def checkerset() -> Tuple[LogChecker, FolderChecker]:
    '''
        This function sets up the checkers for the EUgolino project.
        It initializes the log checker and the folder checker and returns them.

        Returns:
            LogChecker: The log checker
            FolderChecker: The folder checker
    '''
    # Set up the Folder Checker
    folder_checker = FolderChecker(directory=directory, max_len=max, name=fname, url=URL_FOL, sleep_time=sleep_time, send_check=send_check)
    # Set up the Log Checker
    log_checker = LogChecker(log_err=errpath, log_out=outpath, name=lname, url=URL_LOG, sleep_time=sleep_time, send_check=send_check)
    # Return the checkers
    return folder_checker, log_checker

def eugolinoset(output:LogManager) -> EUgolino:
    '''
        This function sets up the EUgolino project.
        It initializes the EUgolino class and returns it.

        Returns:
            EUgolino: The EUgolino
    '''
    # Set up the EUgolino
    e = EUgolino(file_in=file, max_downloads=max, starting_point=starting_point, output=output, name=eugolino_name, destination=directory)
    # Return the EUgolino
    return e

def guelfoset(output:LogManager) -> GUElfo:
    '''
        This function sets up the GUElfo project.
        It initializes the EUgolino class and returns
        it.

        Returns:
            EUgolino: The GUElfo
    '''
    # Set up the GUElfo
    g:GUElfo = GUElfo(file_in=file_guelfo, max_downloads=max_guelfo, starting_point=starting_point_guelfo, output=output, name=guelfo_name, destination=directory_guelfo)
    # Return the GUElfo
    return g

def checker_guelfoset() -> FolderChecker:
    '''
        This function sets up the checker for the GUElfo project.
        It initializes the folder checker and returns it.

        Returns:
            FolderChecker: The folder checker
    '''
    # Set up the Folder Checker
    folder_checker = FolderChecker(directory=directory_guelfo, max_len=max_guelfo, name=fname, url=URL_FOL, sleep_time=sleep_time, send_check=send_check)
    # Return the checkers
    return folder_checker

