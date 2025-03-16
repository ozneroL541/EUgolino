#!/bin/python3
'''
    LogManager  
    file name: log_manager.py  
    author: Lorenzo Radice  
    license: European Union Public Licence v. 1.2.  
'''

import sys
from io import TextIOWrapper
from typing import TextIO


class LogManager:
    """
    LogManager class.
    """
    OUT:TextIO = sys.stdout
    """Standard output"""
    ERR:TextIO = sys.stderr
    """Standard error"""
    out:TextIOWrapper = sys.stdout
    """Output log"""
    out_file:str = None
    """Path to the output log file"""
    err:TextIOWrapper = sys.stderr
    """Error log"""
    err_file:str = None
    """Path to the error log file"""
    duplicate:bool = False
    """Flag to duplicate the logs"""
    duplicate_out:bool = False
    """Flag to duplicate the output logs"""

    def __init__(self, out_file:str = "", out:TextIOWrapper = sys.stdout, err_file:str = "", err:TextIOWrapper = sys.stderr, duplicate_out:bool = False, duplicate:bool = False) -> None:
        """
        Initializes a LogManager object.

        Args:
            out_file (str): Path to the output log file (optional).
            err_file (str): Path to the error log file (optional).
            out (TextIOWrapper): Output log stream (default: sys.stdout).
            err (TextIOWrapper): Error log stream (default: sys.stderr).
            duplicate (bool): Flag to duplicate the logs (default: False).
        """
        if out_file != "":
            try:
                out = open(out_file, "a")
                self.out_file = out_file
                out.close()
            except:
                self.out_file = None
        self.out = out
        if err_file != "":
            try:
                err = open(err_file, "a")
                self.err_file = err_file
                err.close()
            except:
                self.err_file = None
        self.err = err
        self.duplicate = duplicate
        if self.duplicate:
            self.duplicate_out = True
        else:
            self.duplicate_out = duplicate_out
    
    def __str__(self) -> str:
        """
        Returns a string representation of the LogManager object.

        Returns:
            str: String representation of the object.
        """
        return f"out: {self.out}, err: {self.err}, duplicate: {self.duplicate}"

    def print_out(self, message:str, duplicate:bool = None, end:str = '\n') -> None:
        """
        Prints a message to the output log.

        Args:
            message (str): The message to be printed.
            duplicate (bool): Flag to duplicate the logs (optional).
        """
        if duplicate is None:
            duplicate = self.duplicate_out
        # Check if the output log file is set
        if self.is_outfile_set():
            # Open the output log file
            self.out = open(self.out_file, "a")
            # Print the message to the output log file
            print(message, file=self.out, end=end)
            # Close the output log file
            self.out.close()
        else:
            # Print the message to the output log
            print(message, file=self.out, end=end)
        # Check if the logs should be duplicated
        if duplicate and self.out != self.OUT:
            # Print the message to the standard output
            print(message, file=self.OUT, end=end)
    
    def print_err(self, message:str, duplicate:bool = None, end:str = '\n') -> None:
        """
        Prints a message to the error log.

        Args:
            message (str): The message to be printed.
            duplicate (bool): Flag to duplicate the logs (optional).
        """
        if duplicate is None:
            duplicate = self.duplicate
        # Check if the error log file is set
        if self.is_errfile_set():
            # Open the error log file
            self.err = open(self.err_file, "a")
            # Print the message to the error log file
            print(message, file=self.err, end=end)
            # Close the error log file
            self.err.close()
        else:
            # Print the message to the error log
            print(message, file=self.err, end=end)
        # Check if the logs should be duplicated
        if duplicate and self.err != self.ERR:
            # Print the message to the standard error
            print(message, file=self.ERR, end=end)

    def is_outfile_set(self) -> bool:
        """
        Checks if the output log file is set.

        Returns:
            bool: True if the output log file is set, False otherwise.
        """
        return self.out_file is not None
    
    def is_errfile_set(self) -> bool:
        """
        Checks if the error log file is set.

        Returns:
            bool: True if the error log file is set, False otherwise.
        """
        return self.err_file is not None
