#!/bin/python3
'''
    EUgolino Configuration
    file name: config.py
    author: Lorenzo Radice
    description:
        This is the configuration's file of the EUgolino project.
'''

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
