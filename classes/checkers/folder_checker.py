#!/bin/python3
'''
    EUgolino Folder Checker
    file name: folder_checker.py
    author: Lorenzo Radice
    license: European Union Public Licence v. 1.2.
'''

import os

from classes.checkers.checker import Checker

class FolderChecker(Checker):
    """
    A class that represents a checker for monitoring a directory.
    """

    directory:str = 'pdf/'
    """Directory to monitor."""
    previous_len:int = 0
    """Previous number of files in the directory."""    
    current_len:int = 0
    """Current number of files in the directory."""
    max_len:int = 0

    def __init__(self, directory:str, name:str = "Folder Checker", sleep_time:int = 10, url:str = None, send_check:bool = False, max_len:int = 0) -> None:
        """
        Costructor
        
        Initializes a new instace of the Folder Checker class.

        Args:
            directory (str): Directory to monitor.
            name (str, optional): Name of the checker. Defaults to "Folder Checker".
            sleep_time (int, optional): Time to wait before checking again. Defaults to 10.
            url (str, optional): URL to send the check. Defaults to None.
            send_check (bool, optional): Flag indicating if the check should be sent. Defaults to False.
            max_len (int, optional): Maximum number of files in the directory. Defaults
            
        """
        super().__init__(name=name, sleep_time=sleep_time, url=url, send_check=send_check)
        self.directory = directory
        self.max_len = max_len
    
    def __str__(self) -> str:
        """
        String representation of the Checker.

        Returns:
            str: String representation of the Checker.
        """
        return super().__str__() + "\nDirectory:\t" + self.directory + "\nMax Length:\t" + str(self.max_len)

    def send_done(self) -> bool:
        """
        Send a message indicating that the check is done.
        """
        # Update the current length
        self.update_current_len()
        # Send the message
        return super().send_done()

    def update_current_len(self) -> int:
        """
        Update the current length of the directory.

        Returns:
            int: The current length of the directory.
        """
        try:
            # Update the current length
            self.current_len = len(os.listdir(self.directory))
        except:
            self.current_len = 0
            self.previous_len = 0
        return self.current_len

    def get_progresses(self) -> str:
        """
        Returns the progress of the checker as a string.

        If the maximum length is not set, the progress is represented as the current length.
        If the maximum length is set, the progress is represented as a formatted string with the current length and the maximum length.

        Returns:
            str: The progress of the checker.
        """
        # If max length is not set
        if self.max_len == 0:
            # Make progress as current length
            return str(self.current_len)
        else:
            # Make progress
            return "[" + "{:{}}".format((self.current_len), len(str(self.max_len))) + '/' + str(self.max_len) + "]"
    
    def is_len_increased(self) -> bool:
        """
        Checks if the number of files in the directory has increased.

        Returns:
            bool: True if the length of the directory has increased, False otherwise.
        """
        # Assume that the check is not successful
        success = False
        # Check if the length of the directory has increased
        if self.current_len > self.previous_len:
            # Update the previous length
            self.previous_len = self.current_len
            # Success
            success = True
        # Send the check
        self.send(success)
        # Return the result of the check
        return success

    def check(self) -> bool:
        """
        Update the current lenght and check if it is increased.

        Returns:
            bool: True if the number is increased, False otherwise.
        """
        # Update current length
        self.update_current_len()
        # Return the result of the check
        return self.is_len_increased()
