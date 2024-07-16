#!/bin/python3
'''
    EUgolino Configuration
    file name: config.py
    author: Lorenzo Radice
    description:
        This is the configuration's file of the EUgolino project.
'''
import os
from contextlib import redirect_stdout, redirect_stderr

from classes.log_manager import LogManager


# Standard Configuration
log_dir="logs/"
"""Directory where the logs are saved"""
outlog="output.log"
"""File where the output logs are saved"""
errlog="error.log"
"""File where the error logs are saved"""
duplicate:bool = False

# EUgolino Configuration
file:str = "links.txt"
"""File from which the links are read"""
max:int = 1000
"""Max number of links to download"""

# Checker Configuration
check_name:str = "EUgolino"
"""Name of the checker"""
URL:str = "https://localhost"
"""URL of the checker"""
MINUTE:int = 60
"""Seconds in a minute"""
sleep_time:int = 5*MINUTE
"""Seconds to wait between each check"""

# Set up
def setup() -> LogManager:
    '''
        This function sets up the environment for the EUgolino project.
    '''
    # Make the log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    # Set up a Logging Manager
    log_manager = LogManager(out_file=log_dir+outlog, err_file=log_dir+errlog, duplicate=duplicate)
    return log_manager
