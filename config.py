#!/bin/python3
'''
    EUgolino Configuration File
    file name: config.py
    author: Lorenzo Radice
    license: European Union Public Licence v. 1.2.
    description:
        This is the configuration's file of the EUgolino project.
'''

# Standard Configuration
from classes.eugolino import DownloadCandidate


log_dir="logs/"
"""Directory where the logs are saved"""
outlog="output.log"
"""File where the output logs are saved"""
errlog="error.log"
"""File where the error logs are saved"""
duplicate:bool = False
"""If True, the logs are duplicated on the console"""
# Make paths
outpath:str = log_dir+outlog
"""Path to the output log"""
errpath:str = log_dir+errlog
"""Path to the error log"""

# EUgolino Configuration
eugolino_name:str = "EUgolino"
"""Name of the EUgolino"""
file:str = "links.txt"
"""File from which the links are read"""
max:int = 0
"""Max number of links to download"""
directory:str = "pdf/"
"""Directory where the files are saved"""
starting_point:int = 1000
"""Starting link"""

# Checker Configuration
checker_name:str = "EUgolino"
"""Name of the checker"""
MINUTE:int = 60
"""Seconds in a minute"""
sleep_time:int = 5*MINUTE
"""Seconds to wait between each check"""
send_check:bool = True
"""If True, the checker sends a check to the URL"""
delay:int = sleep_time // 2
"""Seconds to wait before start the next thread"""

# Folder Checker Configuration
fname:str = checker_name+" Folder Checker"
"""Name of the Folder Checker"""
URL_FOL:str = "https://hc-ping.com/1"
"""URL of the folder checker"""

# Log Checker Configuration
lname:str = checker_name+" Log Checker"
"""Name of the Log Checker"""
URL_LOG:str = "https://hc-ping.com/2"
"""URL of the log checker"""
