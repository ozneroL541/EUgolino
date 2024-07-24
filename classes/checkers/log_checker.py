#!/bin/python3
'''
    EUgolino Log Checker
    file name: log_checker.py
    author: Lorenzo Radice
    license: European Union Public Licence v. 1.2.
'''

from classes.checkers.checker import Checker

class LogChecker(Checker):
    """
    A class that represents a checker for monitoring the logs.
    """

    log_err:str = 'log/error.log'
    """Log file for errors."""
    log_out:str = 'log/output.log'
    """Log file for output."""
    last_err_line:int = 0
    """Last line read from the error log."""
    progresses:str = ""
    """Progresses of the checker."""
    new_error:bool = False
    """Flag indicating if there are new errors."""

    def __init__(self, log_err:str, log_out:str = None, name: str = "Log Checker", sleep_time: int = 10, url: str = None, send_check: bool = False) -> None:
        """
        Costructor

        Initializes a new instace of the Log Checker class.

        Args:
            log_err (str): Log file for errors.
            log_out (str, optional): Log file for output. Defaults to None.
            name (str, optional): Name of the checker. Defaults to "Log Checker".
            sleep_time (int, optional): Time to wait before checking again. Defaults to 10.
            url (str, optional): URL to send the check. Defaults to None.
            send_check (bool, optional): Flag indicating if the check should be sent. Defaults to False
        """
        super().__init__(name, sleep_time, url, send_check)
        self.log_err = log_err
        self.log_out = log_out

    def __str__(self) -> str:
        """
        String representation of the Checker.

        Returns:
            str: String representation of the Checker.
        """
        s = super().__str__() + "\nError Log:\t" + self.log_err
        if self.log_out is not None:
            s += "\nOutput Log:\t" + self.log_out
        return s

    def get_progresses(self) -> str:
        """
        Get the progresses of the checker.
        
        Returns:
            str: Progresses of the checker.
        """
        # Check if there is a new error
        if self.new_error:
            # Reset the flag
            self.new_error = False
            # Return the progresses
            return self.progresses
        # Check if log_out is None
        if self.log_out is None:
            return "OK"
        # Get the last line of the output log
        with open(self.log_out, 'r') as file:
            lines = file.readlines()
            last_line = lines[-1].strip() if lines else ""
            file.close()
        # Update the progresses
        self.progresses = last_line
        # Return the last line
        return self.progresses
    
    def check(self) -> bool:
        """
        Check the log files for new errors.

        Returns:
            bool: True if there are no errors, False otherwise        
        """
        self.new_error = False
        # Open error file
        with open(self.log_err, 'r') as file:
            # Read the lines
            lines = file.readlines()
            # Check if there are new errors
            if len(lines) > self.last_err_line:
                # Set the flag 
                self.new_error = True
                # Get the new errors
                self.progresses = "".join(lines[self.last_err_line:])
                # Update the last line read
                self.last_err_line = len(lines)
            # Close the file
            file.close()
        # Return the result
        return not self.new_error
